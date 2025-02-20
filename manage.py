import os
import sys
from django.core.management import call_command
from django.contrib.auth.models import User

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dsa.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def create_superuser():
    username = os.getenv('SUPERUSER_USERNAME', 'admin')
    email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('SUPERUSER_PASSWORD', 'adminadmin')
    
    if not User.objects.filter(username=username).exists():
        call_command('createsuperuser', interactive=False, username=username, email=email, password=password)

if __name__ == '__main__':
    main()
