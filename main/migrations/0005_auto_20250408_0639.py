# migrations/000X_auto_...py
from django.db import migrations

def forwards_func(apps, schema_editor):
    # Eski modeli al
    Təlimçilər = apps.get_model('main', 'Təlimçilər')
    # Tüm təlimçileri döngüye al
    for təlimçi in Təlimçilər.objects.all():
        if təlimçi.metinler:  # Eğer ForeignKey doluysa
            # Eski ForeignKey verisini ManyToManyField'a ekle
            təlimçi.metinler_temp.add(təlimçi.metinler)

def reverse_func(apps, schema_editor):
    # Geri dönüş için bir şey yapmamıza gerek yok, ama boş bir fonksiyon tanımlıyoruz
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0004_təlimçilər_metinler_temp_alter_təlimçilər_metinler'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]