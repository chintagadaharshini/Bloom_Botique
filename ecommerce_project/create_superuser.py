import os
import sys
import django

# Add project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth.models import User

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            password='Admin@1234',
            email='admin@bloom.com'
        )
        print('✅ Superuser created successfully!')
    else:
        print('✅ Superuser already exists!')
except Exception as e:
    print(f'❌ Error: {e}')