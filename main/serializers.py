from rest_framework import serializers
from .models import (
    Müraciət,
    Əlaqə,
    Qeydiyyat,
    Bootcamps,
    BootcampTipi,
    Təlimlər,
    Mətinlər,
    Sessiyalar,
    Nümayişlər,
    Sillabuslar,
    Təlimçilər,
    Müəllimlər,
    Məzunlar,
    FAQ
)

class TəlimlərSerializer(serializers.ModelSerializer):
    money = serializers.SerializerMethodField()

    class Meta:
        model = Təlimlər
        fields = '__all__'  

    def get_money(self, obj):
        metinler = Mətinlər.objects.filter(trainings=obj)

        if metinler.exists():
            return min(metinler.values_list('money', flat=True)) 
        return None


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
    class Meta:
        model = Təlimçilər
        fields = '__all__'

class MüəllimlərSerializer(serializers.ModelSerializer):
    class Meta:
        model = Müəllimlər
        fields = '__all__'

class MəzunlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Məzunlar
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class MətinlərSerializer(serializers.ModelSerializer):
    sessiyalar = SessiyalarSerializer(many=True, read_only=True)  
    nümayislər = NümayişlərSerializer( read_only=True)
    syllabus = SillabuslarSerializer(many=True, read_only=True)
    trainers = TəlimçilərSerializer(many=True, read_only=True)

    class Meta:
        model = Mətinlər
        fields = '__all__'
