from .models import Müraciət, Əlaqə, Qeydiyyat, Bootcamps, BootcampTipi, Təlimlər, Mətinlər, Sessiyalar, Nümayişlər, Sillabuslar, Təlimçilər, Müəllimlər, Məzunlar, FAQ
from .serializers import MüraciətSerializer, ƏlaqəSerializer, QeydiyyatSerializer, BootcampsSerializer, BootcampTipiSerializer, TəlimlərSerializer, MətinlərSerializer, SessiyalarSerializer, NümayişlərSerializer, SillabuslarSerializer, TəlimçilərSerializer, MüəllimlərSerializer, MəzunlarSerializer, FAQSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from storages.backends.s3boto3 import S3Boto3Storage

def clean_filename(filename):
    import os
    from django.utils.text import slugify
    name, ext = os.path.splitext(filename)
    return f"{slugify(name)}{ext}"

class MüraciətViewSet(viewsets.ModelViewSet):
    queryset = Müraciət.objects.all()
    serializer_class = MüraciətSerializer

class ƏlaqəViewSet(viewsets.ModelViewSet):
    queryset = Əlaqə.objects.all()
    serializer_class = ƏlaqəSerializer

class QeydiyyatViewSet(viewsets.ModelViewSet):
    queryset = Qeydiyyat.objects.all()
    serializer_class = QeydiyyatSerializer

class BootcampsViewSet(viewsets.ModelViewSet):
    queryset = Bootcamps.objects.all().prefetch_related('bootcamp_tipi__telimler')
    serializer_class = BootcampsSerializer

class BootcampTipiViewSet(viewsets.ModelViewSet):
    queryset = BootcampTipi.objects.all()
    serializer_class = BootcampTipiSerializer

class TəlimlərViewSet(viewsets.ModelViewSet):
    queryset = Təlimlər.objects.all()
    serializer_class = TəlimlərSerializer

class MətinlərViewSet(viewsets.ModelViewSet):
    queryset = Mətinlər.objects.all().select_related('nümayislər').prefetch_related('trainers', 'syllabus', 'sessiyalar')
    serializer_class = MətinlərSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        storage = S3Boto3Storage()
        if 'image' in request.FILES:
            image_file = request.FILES.getlist('image')[0]
            file_name = clean_filename(image_file.name)
            saved_path = storage.save(f"metinler/{file_name}", image_file)
            instance.image = saved_path

        if 'certificate_image' in request.FILES:
            cert_file = request.FILES.getlist('certificate_image')[0]
            file_name = clean_filename(cert_file.name)
            saved_path = storage.save(f"certificates/{file_name}", cert_file)
            instance.certificate_image = saved_path

        serializer.save()
        return Response(serializer.data)

class SessiyalarViewSet(viewsets.ModelViewSet):
    queryset = Sessiyalar.objects.all()
    serializer_class = SessiyalarSerializer

class NümayişlərViewSet(viewsets.ModelViewSet):
    queryset = Nümayişlər.objects.all()
    serializer_class = NümayişlərSerializer

class SillabuslarViewSet(viewsets.ModelViewSet):
    queryset = Sillabuslar.objects.all()
    serializer_class = SillabuslarSerializer

class TəlimçilərViewSet(viewsets.ModelViewSet):
    queryset = Təlimçilər.objects.all()
    serializer_class = TəlimçilərSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'image' in request.FILES:
            image_file = request.FILES.getlist('image')[0]
            storage = S3Boto3Storage()
            file_name = clean_filename(image_file.name)
            saved_path = storage.save(f"trainers/{file_name}", image_file)
            instance.image = saved_path

        serializer.save()
        return Response(serializer.data)

class MüəllimlərViewSet(viewsets.ModelViewSet):
    queryset = Müəllimlər.objects.all()
    serializer_class = MüəllimlərSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'image' in request.FILES:
            image_file = request.FILES.getlist('image')[0]
            storage = S3Boto3Storage()
            file_name = clean_filename(image_file.name)
            saved_path = storage.save(f"trainers/{file_name}", image_file)
            instance.image = saved_path

        serializer.save()
        return Response(serializer.data)

class MəzunlarViewSet(viewsets.ModelViewSet):
    queryset = Məzunlar.objects.all()
    serializer_class = MəzunlarSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'image' in request.FILES:
            image_file = request.FILES.getlist('image')[0]
            storage = S3Boto3Storage()
            file_name = clean_filename(image_file.name)
            saved_path = storage.save(f"graduates/{file_name}", image_file)
            instance.image = saved_path

        serializer.save()
        return Response(serializer.data)

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
