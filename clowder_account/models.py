from shortuuidfield import ShortUUIDField

from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from clowder_server.models import Ping

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Company(models.Model):

    public_key = ShortUUIDField(auto=True, db_index=True, unique=True)
    secret_key = ShortUUIDField(auto=True)

    def __unicode__(self):
        return self.public_key

class ClowderUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    language = models.CharField(max_length=1024, blank=True)
    company = models.ForeignKey('clowder_account.Company', null=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

class ClowderUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'public_key', 'get_full_name', 'language', 'number_of_pings')

    def public_key(self, obj):
        return obj.company.public_key
    public_key.allow_tags = True

    def number_of_pings(self, obj):
        return '%s' % (Ping.objects.filter(company=obj.company).count())
    number_of_pings.allow_tags = True
