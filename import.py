import os
import csv
import django
from django.utils.dateparse import parse_datetime
from django.utils import timezone

# ==== Django konfiqurasiyası ====
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dsa.settings")
django.setup()

from main.models import Certificate  # noqa: E402


# ---- Tarixi timezone ilə parse etmək ----
def parse_with_tz(value):
    """
    CSV-dəki datetime dəyərini parse edib,
    naive-dirsə timezone.make_aware ilə UTC-yə çevir.
    """
    if not value:
        return None
    dt = parse_datetime(value)
    if dt and timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    return dt


# ==== CSV faylını oxu və DB-yə yaz ====
csv_file = "certificates.csv"  # Faylın yolu

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        Certificate.objects.update_or_create(
            certificate_id=row["certificate_id"],
            defaults={
                "name": row["name"],
                "name_en": row["name_en"],
                "image": row["image"],
                "image_en": row["image_en"],
                "file": row["file"],
                "file_en": row["file_en"],
                "date": row["date"],
                "date_en": row["date_en"],
                "created_at": parse_with_tz(row["created_at"]),
                "updated_at": parse_with_tz(row["updated_at"]),
            },
        )

print("Import tamamlandı ✅")
