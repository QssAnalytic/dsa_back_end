from django.db import models




class Müraciət(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Əlaqə(models.Model):
    CATEGORY_CHOICES = [
        ('Data Science Bootcamp', 'Data Science Bootcamp'),
        ('SPSS Modeler Bootcamp', 'SPSS Modeler Bootcamp'),
        ('Kredit-Risk Analitikası', 'Kredit-Risk Analitikası'),
        ('Korporativ Təlimlər', 'Korporativ Təlimlər'),
        ('Data ilə əlaqəli işçi axtarırsınız', 'Data ilə əlaqəli işçi axtarırsınız'),
        ('Ödənişli proyekt köməyi', 'Ödənişli proyekt köməyi'),
        ('Ödənişsiz proyekt köməyi', 'Ödənişsiz proyekt köməyi')
    ]
    
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Data Science Bootcamp')

    def __str__(self):
        return f'{self.name} {self.surname} - {self.category}'

    
    
class Qeydiyyat(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    event_date = models.DateField(help_text="Etkinlik tarihini seçin", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

## Models for Data Science Bootcamp--------------------------------------------------------------------------------------------------
 
 
 
 
class Bootcamps(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'main_bootcamps'

    def __str__(self):
        return self.name


class BootcampTipi(models.Model):
    bootcamp = models.ForeignKey(Bootcamps, on_delete=models.CASCADE, related_name='bootcamp_tipi')
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
    
    
class Təlimlər(models.Model):
    id = models.AutoField(primary_key=True)
    bootcamp_tipi = models.ForeignKey(BootcampTipi, on_delete=models.CASCADE, related_name='telimler')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField()
    title = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metinler = models.ForeignKey('Mətinlər', on_delete=models.CASCADE, related_name='telimler_metinler', blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def metinler_ids(self):
        return [self.metinler.id] if self.metinler else []

    
    
    
   
    
class Mətinlər(models.Model):
    id = models.AutoField(primary_key=True)
    trainings = models.ForeignKey(Təlimlər, on_delete=models.CASCADE, related_name='metinler_trainings')
    title = models.TextField(max_length=100)
    description = models.TextField()
    information = models.TextField()
    money = models.IntegerField()
    image = models.ImageField(upload_to='mətinlər/')
    for_who = models.TextField()
    certificates = models.TextField()
    certificate_image = models.ImageField(upload_to='certificates/')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

class Sessiyalar(models.Model):
    metinler = models.ForeignKey(Mətinlər, on_delete=models.CASCADE, related_name='sessiyalar',default=1)
    session_number = models.IntegerField()
    date = models.DateField()
    hour = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.session_number} - {self.date} - {self.hour}'
    

class Nümayişlər(models.Model):
    metinler = models.OneToOneField(Mətinlər, on_delete=models.CASCADE, related_name='nümayislər')
    title = models.CharField(max_length=100)
    info = models.TextField()
    link = models.TextField()
    trainer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Sillabuslar(models.Model):
    metinler = models.ForeignKey(Mətinlər, on_delete=models.CASCADE, related_name='syllabus', default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    label = models.CharField(max_length=100,null=True)
    information = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class Təlimçilər(models.Model):
    metinler = models.ForeignKey(Mətinlər, on_delete=models.CASCADE, related_name='trainers', default=1)
    info = models.TextField()
    name = models.CharField(max_length=100)
    work_location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='trainers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


    
class Müəllimlər(models.Model):
    info = models.TextField()
    name = models.CharField(max_length=100)
    work_position = models.CharField(max_length=100)
    work_location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='trainers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    
class Məzunlar(models.Model):
    name = models.CharField(max_length=100)
    work_position = models.CharField(max_length=100)
    work_location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='trainers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    
    
class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    question_en = models.TextField()
    answer_en = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
