import os
import sys
import django

# Ayarları başlatmak için
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dsa.settings')
django.setup()

def main():
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
