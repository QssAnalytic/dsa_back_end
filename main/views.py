from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from .models import (
    Müraciət, Əlaqə, Qeydiyyat, Bootcamps, BootcampTipi, Təlimlər, Mətinlər,
    Sessiyalar, Nümayişlər, Sillabuslar, Təlimçilər, Müəllimlər, Məzunlar, FAQ
)
from .serializers import (
    MüraciətSerializer, ƏlaqəSerializer, QeydiyyatSerializer, BootcampsSerializer,
    BootcampTipiSerializer, TəlimlərSerializer, MətinlərSerializer, SessiyalarSerializer,
    NümayişlərSerializer, SillabuslarSerializer, TəlimçilərSerializer, MüəllimlərSerializer,
    MəzunlarSerializer, FAQSerializer
)
from rest_framework import viewsets
from rest_framework.response import Response
from storages.backends.s3boto3 import S3Boto3Storage
from rest_framework.exceptions import ValidationError

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

        try:
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                instance.image = image_file
            if 'certificate_image' in request.FILES:
                cert_file = request.FILES['certificate_image']
                instance.certificate_image = cert_file
        except Exception as e:
            raise ValidationError(f"Dosya yükleme hatası: {str(e)}")

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

    @method_decorator(cache_control(no_cache=True))  # Use method_decorator for class-based view
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            instance = serializer.save()
            if 'metinler' in request.data:
                metinler_ids = request.data.getlist('metinler')
                instance.metinler.set(metinler_ids)
            if 'image' in request.FILES:
                instance.image = request.FILES['image']
                instance.save()
        except Exception as e:
            raise ValidationError(f"Oluşturma hatası: {str(e)}")
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            if 'image' in request.FILES:
                instance.image = request.FILES['image']
            serializer.save()
            if 'metinler' in request.data:
                metinler_ids = request.data.getlist('metinler')
                instance.metinler.set(metinler_ids)
            else:
                instance.metinler.clear()
        except Exception as e:
            raise ValidationError(f"Güncelleme hatası: {str(e)}")
        return Response(serializer.data)

class MüəllimlərViewSet(viewsets.ModelViewSet):
    queryset = Müəllimlər.objects.all()
    serializer_class = MüəllimlərSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                instance.image = image_file
        except Exception as e:
            raise ValidationError(f"Dosya yükleme hatası: {str(e)}")

        serializer.save()
        return Response(serializer.data)

class MəzunlarViewSet(viewsets.ModelViewSet):
    queryset = Məzunlar.objects.all()
    serializer_class = MəzunlarSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                instance.image = image_file
        except Exception as e:
            raise ValidationError(f"Dosya yükleme hatası: {str(e)}")

        serializer.save()
        return Response(serializer.data)

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
