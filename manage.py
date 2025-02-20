import os
import sys
import django
from django.core.management import call_command
from django.contrib.auth.models import User

# Ayarları başlatmak için
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dsa.settings')
django.setup()

def create_superuser():
    username = os.getenv('SUPERUSER_USERNAME', 'admin')
    email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('SUPERUSER_PASSWORD', 'adminpassword')

    # User modelini kontrol et ve superuser oluştur
    if not User.objects.filter(username=username).exists():
        call_command('createsuperuser', interactive=False, username=username, email=email, password=password)

def main():
    try: # Superuser'ı oluştur
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
    create_superuser() 
