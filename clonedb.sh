heroku pg:backups capture
curl -o latest.dump `heroku pg:backups public-url`
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d clowder latest.dump
rm latest.dump
