from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from config.settings import get_env_variable


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--username')
        parser.add_argument('--email')
        parser.add_argument('--password')
        parser.add_argument('--no-input', action='store_true')

    def handle(self, *args, **options):
        User = get_user_model()

        if options['no_input']:
            options['username'] = get_env_variable('APP_SUPERUSER_USERNAME')
            options['email'] = get_env_variable('APP_SUPERUSER_EMAIL')
            options['password'] = get_env_variable('APP_SUPERUSER_PASSWORD')

        if options['username'] and options['password']:
            if not User.objects.filter(username=options['username']).exists():
                User.objects.create_superuser(
                    username=options['username'],
                    email=options['email'],
                    password=options['password'],
                )
                self.stdout.write(self.style.SUCCESS('Superuser {} created'.format(options['username'])))
            else:
                self.stdout.write(self.style.SUCCESS('Superuser {} already exists'.format(options['username'])))
        else:
            self.stdout.write(self.style.SUCCESS('No username or password provided'))
