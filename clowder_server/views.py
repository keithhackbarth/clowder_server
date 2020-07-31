#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# pylint: disable=no-member,line-too-long

import datetime
import pytz

from braces.views import CsrfExemptMixin, LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import decorators
from django.views.generic import TemplateView, View
from ipware.ip import get_client_ip

from clowder_account.models import Company
from clowder_server.emailer import send_alert
from clowder_server.models import Alert, Ping

class APIView(CsrfExemptMixin, View):

    def post(self, request):

        name = request.POST.get('name')
        frequency = request.POST.get('frequency')
        value = request.POST.get('value', 1)
        api_key = request.POST.get('api_key')
        status = int(request.POST.get('status', 1))
        public = bool(request.POST.get('public'))
        send_email = bool(request.POST.get('send_email'))
        expire = request.POST.get('expire')

        # Cache most common
        # TODO: Eventually rename company so that this is primary key
        if api_key == 'GVMN3bNgw54baRyjFjjB7C':
            company_id = 86
        else:
            company_id = Company.objects.get(public_key=api_key).id
        ip = get_client_ip(request) or '127.0.0.1'

        if not name:
            return HttpResponse('name needed')

        alert, created = Alert.objects.get_or_create(
            company_id=company_id,
            name=name,
            defaults={'ip_address': ip, 'send_email': send_email},
        )

        if expire:
            alert.expire_at = datetime.datetime.strptime(expire, "%Y%m%dT%H%M%SZ")

        if status == -1:
            if created or alert.notify_at is not None:
                send_alert(alert)
            alert.notify_at = None

        elif frequency:
            expiration_date = (
                datetime.datetime.now(pytz.utc) +
                datetime.timedelta(seconds=int(frequency))
            )
            alert.notify_at = expiration_date

        # save alert updates
        alert.ip_address = ip
        alert.save()

        ping = Ping.objects.create(
            name=name,
            company_id=company_id,
            value=value,
            ip_address=ip,
            status_passing=(status == 1),
            public=public,
        )
        return HttpResponse(ping)

    def get(self, request):

        name = request.GET.get('name')
        api_key = request.GET.get('api_key')

        if not all((api_key, name)):
            return HttpResponseBadRequest('Both name and api_key are required')

        company = Company.objects.get(public_key=api_key)
        pings = Ping.objects.filter(company=company, name=name) \
            .order_by('name', '-create')

        table = []
        for ping in pings:
            table.append([ping.create.isoformat(), ping.value])

        return JsonResponse(table, safe=False)


class DashboardView(TemplateView):

    template_name = "dashboard.html"
    public = False

    @staticmethod
    def _pings(request, *args, **kwargs):
        return list(
            Ping.objects.filter(company=request.user.company) \
                .order_by('name', '-create') \
                .distinct('name')
        )

    def get(self, request, *args, **kwargs):
        pings = self._pings(request, *args, **kwargs)

        context = {
            'pings': pings,
            'total_num_pings': len(pings),
            'public': self.public,
        }

        if pings:
            context['num_passing'] = len([ping for ping in pings if ping.status_passing])
            context['num_failing'] = context['total_num_pings'] - context['num_passing']
            context['percent_passing'] = round(
                context['num_passing'] / context['total_num_pings'] * 100
            )

        return self.render_to_response(context)


class PrivateView(LoginRequiredMixin, DashboardView):
    pass

class PublicView(DashboardView):

    template_name = "dashboard.html"
    public = True

    @staticmethod
    def _pings(request, *args, **kwargs):
        return list(
            Ping.objects.filter(company__secret_key=kwargs['secret_key'], public=True) \
                .order_by('name', '-create') \
                .distinct('name')
        )


class DeleteView(CsrfExemptMixin, View):

    @decorators.login_required
    def get(self, request, *args, **kwargs):
        Ping.objects.filter(company=request.user.company).delete()
        Alert.objects.filter(company=request.user.company).delete()
        return HttpResponse('ok')

    def post(self, request, *args, **kwargs):
        api_key = request.POST.get('api_key')
        name = request.POST.get('name')

        company = Company.objects.get(public_key=api_key)

        if name:
            Ping.objects.filter(company=company, name=name).delete()
            Alert.objects.filter(company=company, name=name).delete()
            return HttpResponse('deleted')

        return HttpResponse('ok')
