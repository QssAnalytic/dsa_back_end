from django.contrib import admin
from .models import Müraciət, Əlaqə, Qeydiyyat, Bootcamps, BootcampTipi, Təlimlər, Mətinlər, Sessiyalar, Nümayişlər, Sillabuslar, Təlimçilər, Müəllimlər, Məzunlar, FAQ
import unicodedata
import re

# Dosya adlarını temizlemek için yardımcı fonksiyon
def clean_filename(filename):
    # Özel karakterleri kaldır ve boşlukları _ ile değiştir
    filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return filename

# Müəllimlər için Admin sınıfı
@admin.register(Müəllimlər)
class MüəllimlərAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print("Admin panelinden save_model çağrıldı (Müəllimlər)")
        if 'image' in form.changed_data:
            print(f"Yüklenen dosya: {obj.image.name}")
            from storages.backends.s3boto3 import S3Boto3Storage
            storage = S3Boto3Storage()
            file = form.cleaned_data['image']
            file_name = clean_filename(file.name)  # Dosya adını temizle
            saved_path = storage.save(f"trainers/{file_name}", file)
            obj.image.name = f"trainers/{file_name}"  # Çift önek oluşmasını engelliyoruz
            print(f"Manuel olarak S3'e kaydedildi: {obj.image.name}")
            if storage.exists(saved_path):
                print(f"Dosya S3'te başarıyla doğrulandı: {saved_path}")
            else:
                print(f"Hata: Dosya S3'te bulunamadı: {saved_path}")
        super().save_model(request, obj, form, change)

# Mətinlər için Admin sınıfı
@admin.register(Mətinlər)
class MətinlərAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print("Admin panelinden save_model çağrıldı (Mətinlər)")
        for field in ['image', 'certificate_image']:
            if field in form.changed_data:
                print(f"Yüklenen dosya ({field}): {getattr(obj, field).name}")
                from storages.backends.s3boto3 import S3Boto3Storage
                storage = S3Boto3Storage()
                file = form.cleaned_data[field]
                file_name = clean_filename(file.name)  # Dosya adını temizle
                if field == 'image':
                    file_name = f"metinler/{file_name}"  # mətinlər yerine metinler kullandım, çünkü S3'te özel karakterler sorun çıkarabilir
                else:
                    file_name = f"certificates/{file_name}"
                saved_path = storage.save(file_name, file)
                setattr(obj, field, file_name)  # Çift önek olmamasına dikkat ediyoruz
                print(f"Manuel olarak S3'e kaydedildi ({field}): {saved_path}")
                if storage.exists(saved_path):
                    print(f"Dosya S3'te başarıyla doğrulandı ({field}): {saved_path}")
                else:
                    print(f"Hata: Dosya S3'te bulunamadı ({field}): {saved_path}")
        super().save_model(request, obj, form, change)

# Təlimçilər için Admin sınıfı
@admin.register(Təlimçilər)
class TəlimçilərAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print("Admin panelinden save_model çağrıldı (Təlimçilər)")
        if 'image' in form.changed_data:  # Təlimçilər modelinde image alanı olduğunu varsayıyorum
            print(f"Yüklenen dosya: {obj.image.name}")
            from storages.backends.s3boto3 import S3Boto3Storage
            storage = S3Boto3Storage()
            file = form.cleaned_data['image']
            file_name = clean_filename(file.name)  # Dosya adını temizle
            saved_path = storage.save(f"trainers/{file_name}", file)
            obj.image.name = f"trainers/{file_name}"  # Çift önek oluşmasını engelliyoruz
            print(f"Manuel olarak S3'e kaydedildi: {obj.image.name}")
            if storage.exists(saved_path):
                print(f"Dosya S3'te başarıyla doğrulandı: {saved_path}")
            else:
                print(f"Hata: Dosya S3'te bulunamadı: {saved_path}")
        super().save_model(request, obj, form, change)

# Məzunlar için Admin sınıfı
@admin.register(Məzunlar)
class MəzunlarAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print("Admin panelinden save_model çağrıldı (Məzunlar)")
        if 'image' in form.changed_data:  # Məzunlar modelinde image alanı olduğunu varsayıyorum
            print(f"Yüklenen dosya: {obj.image.name}")
            from storages.backends.s3boto3 import S3Boto3Storage
            storage = S3Boto3Storage()
            file = form.cleaned_data['image']
            file_name = clean_filename(file.name)  # Dosya adını temizle
            saved_path = storage.save(f"graduates/{file_name}", file)  # Mezunlar için ayrı bir klasör
            obj.image.name = f"graduates/{file_name}"  # Çift önek oluşmasını engelliyoruz
            print(f"Manuel olarak S3'e kaydedildi: {obj.image.name}")
            if storage.exists(saved_path):
                print(f"Dosya S3'te başarıyla doğrulandı: {saved_path}")
            else:
                print(f"Hata: Dosya S3'te bulunamadı: {saved_path}")
        super().save_model(request, obj, form, change)

# Diğer modeller için basit kayıt (dosya yükleme alanı yoksa)
admin.site.register(Müraciət)
admin.site.register(Əlaqə)
admin.site.register(Qeydiyyat)
admin.site.register(Bootcamps)
admin.site.register(BootcampTipi)
admin.site.register(Təlimlər)
admin.site.register(Sessiyalar)
admin.site.register(Nümayişlər)
admin.site.register(Sillabuslar)
admin.site.register(FAQ)
