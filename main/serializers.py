from rest_framework import serializers
from .models import (
    Müraciət, Əlaqə, Qeydiyyat, Bootcamps, BootcampTipi, Təlimlər, Mətinlər,
    Sessiyalar, Nümayişlər, Sillabuslar, Təlimçilər, Müəllimlər, Məzunlar, FAQ, EmailSubscription
)

class TəlimlərSerializer(serializers.ModelSerializer):
    money = serializers.SerializerMethodField()
    metinler_ids = serializers.SerializerMethodField()

    class Meta:
        model = Təlimlər
        fields = ['id', 'bootcamp_tipi', 'is_active', 'order', 'title', 'created_at', 'updated_at', 'money', 'metinler_ids']

    def get_metinler_ids(self, obj):
        return list(obj.metinler_trainings.values_list('id', flat=True))

    def get_money(self, obj):
        metinler = Mətinlər.objects.filter(trainings=obj)
        return min(metinler.values_list('money', flat=True)) if metinler.exists() else None

class BootcampTipiSerializer(serializers.ModelSerializer):
    telimler = TəlimlərSerializer(many=True, read_only=True)

    class Meta:
        model = BootcampTipi
        fields = '__all__'

class BootcampsSerializer(serializers.ModelSerializer):
    bootcamp_tipi = BootcampTipiSerializer(many=True, read_only=True)

    class Meta:
        model = Bootcamps
        fields = '__all__'

class MüraciətSerializer(serializers.ModelSerializer):
    class Meta:
        model = Müraciət
        fields = '__all__'

class ƏlaqəSerializer(serializers.ModelSerializer):
    class Meta:
        model = Əlaqə
        fields = '__all__'
        
class EmailSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ['id', 'email', 'created_at', 'updated_at']

class QeydiyyatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qeydiyyat
        fields = '__all__'

class SessiyalarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessiyalar
        fields = '__all__'

class NümayişlərSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nümayişlər
        fields = '__all__'

class SillabuslarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sillabuslar
        fields = '__all__'

class TəlimçilərSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    telimler = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Təlimlər.objects.all()
    )

    class Meta:
        model = Təlimçilər
        fields = '__all__'


class MüəllimlərSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Müəllimlər
        fields = '__all__'

class MəzunlarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Məzunlar
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class MətinlərSerializer(serializers.ModelSerializer):
    sessiyalar = SessiyalarSerializer(many=True, read_only=True)
    nümayislər = NümayişlərSerializer(read_only=True)
    syllabus = SillabuslarSerializer(many=True, read_only=True)
    trainers = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True)
    certificate_image = serializers.ImageField(use_url=True)

    class Meta:
        model = Mətinlər
        fields = '__all__'

    def get_trainers(self, obj):
        trainers = Təlimçilər.objects.filter(telimler=obj.trainings).distinct()
        unique_trainers = {trainer.name: trainer for trainer in trainers}
        return TəlimçilərSerializer(unique_trainers.values(), many=True).data