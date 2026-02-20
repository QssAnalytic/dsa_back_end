from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MüraciətViewSet, ƏlaqəViewSet, QeydiyyatViewSet, BootcampsViewSet, BootcampTipiViewSet,
    TəlimlərViewSet, EmailSubscriptionViewSet,
    SessiyaQeydiyyatiViewSet, MətinlərViewSet, SessiyalarViewSet, NümayişlərViewSet,
    SillabuslarViewSet, TəlimçilərViewSet, MüəllimlərViewSet, MəzunlarViewSet,
    FAQViewSet, check_certificate, ProgramPDFViewSet, CertificateViewSet
)

router = DefaultRouter()
router.register(r"muraciet", MüraciətViewSet)
router.register(r"elaqe", ƏlaqəViewSet)
router.register(r"program", ProgramPDFViewSet, basename="program")
router.register(r"qeydiyyat", QeydiyyatViewSet)
router.register(r"bootcamps", BootcampsViewSet)
router.register(r"bootcamptipi", BootcampTipiViewSet)
router.register(r"telimler", TəlimlərViewSet)
router.register(r"emailsubscription", EmailSubscriptionViewSet)
router.register(r"sessiyaqeydiyyati", SessiyaQeydiyyatiViewSet)
router.register(r"metinler", MətinlərViewSet)
router.register(r"sessiyalar", SessiyalarViewSet)
router.register(r"numayisler", NümayişlərViewSet)
router.register(r"sillabuslar", SillabuslarViewSet)
router.register(r"telimciler", TəlimçilərViewSet)
router.register(r"muellimler", MüəllimlərViewSet)
router.register(r"mezunlar", MəzunlarViewSet)
router.register(r"faq", FAQViewSet)
router.register(r"certificates", CertificateViewSet, basename="certificates")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/check-certificate/", check_certificate, name="check-certificate"),
]
