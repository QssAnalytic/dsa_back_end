from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from .models import (
    Müraciət, Əlaqə, Qeydiyyat, Bootcamps, BootcampTipi, Təlimlər, Mətinlər,
    Sessiyalar, Nümayişlər, Sillabuslar, Təlimçilər, Müəllimlər, Məzunlar, FAQ, EmailSubscription,
    SessiyaQeydiyyati, Certificate, ProgramPDF
)
from .serializers import (
    MüraciətSerializer, ƏlaqəSerializer, QeydiyyatSerializer, BootcampsSerializer,
    BootcampTipiSerializer, TəlimlərSerializer, MətinlərSerializer, SessiyalarSerializer,
    NümayişlərSerializer, SillabuslarSerializer, TəlimçilərSerializer, MüəllimlərSerializer,
    MəzunlarSerializer, FAQSerializer, EmailSubscriptionSerializer, SessiyaQeydiyyatiSerializer,
    CertificateSerializer, ProgramPDFSerializer
)
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView


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


class EmailSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = EmailSubscription.objects.all()
    serializer_class = EmailSubscriptionSerializer

class ProgramPDFView(APIView):
    def get(self, request, slug):
        try:
            program = ProgramPDF.objects.get(slug=slug)
            serializer = ProgramPDFSerializer(program)
            return Response(serializer.data)
        except ProgramPDF.DoesNotExist:
            return Response({"error": "Program not found"}, status=status.HTTP_404_NOT_FOUND)


class ProgramPDFListCreateView(ListCreateAPIView):
    queryset = ProgramPDF.objects.all()
    serializer_class = ProgramPDFSerializer
    parser_classes = [MultiPartParser, FormParser]

class ProgramPDFViewSet(viewsets.ModelViewSet):
    queryset = ProgramPDF.objects.all()
    serializer_class = ProgramPDFSerializer
    parser_classes = [MultiPartParser, FormParser]

class SessiyaQeydiyyatiViewSet(viewsets.ModelViewSet):
    queryset = SessiyaQeydiyyati.objects.all()
    serializer_class = SessiyaQeydiyyatiSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            training_id = request.data.get('training')
            session_id = request.data.get('session')
            if training_id:
                Təlimlər.objects.get(id=training_id)
            if session_id:
                Sessiyalar.objects.get(id=session_id)
            serializer.save()
            return Response(serializer.data, status=201)
        except Təlimlər.DoesNotExist:
            raise ValidationError("Belirtilen təlim tapılmadı.")
        except Sessiyalar.DoesNotExist:
            raise ValidationError("Belirtilen sessiya tapılmadı.")
        except Exception as e:
            raise ValidationError(f"Qeydiyyat xətası: {str(e)}")


class MətinlərViewSet(viewsets.ModelViewSet):
    queryset = Mətinlər.objects.all().select_related('nümayislər').prefetch_related('syllabus', 'sessiyalar')
    serializer_class = MətinlərSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            if 'image' in request.FILES:
                instance.image = request.FILES['image']
            if 'certificate_image' in request.FILES:
                instance.certificate_image = request.FILES['certificate_image']
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

    @method_decorator(cache_control(no_cache=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            instance = serializer.save()
            if 'telimler' in request.data:
                telimler_ids = request.data.getlist('telimler')
                instance.telimler.set(telimler_ids)
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
            if 'telimler' in request.data:
                telimler_ids = request.data.getlist('telimler')
                instance.telimler.set(telimler_ids)
            else:
                instance.telimler.clear()
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
                instance.image = request.FILES['image']
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
                instance.image = request.FILES['image']
        except Exception as e:
            raise ValidationError(f"Dosya yükleme hatası: {str(e)}")

        serializer.save()
        return Response(serializer.data)


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


@api_view(['POST'])
def check_certificate(request):
    certificate_id = request.data.get('certificate_id')
    if not certificate_id:
        return Response({"error": "certificate_id göndərilməyib"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cert = Certificate.objects.get(certificate_id=certificate_id)
        serializer = CertificateSerializer(cert)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Certificate.DoesNotExist:
        return Response({"error": "Certificate tapılmadı"}, status=status.HTTP_404_NOT_FOUND)
