from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Breed(models.Model):  # задаем параметры классу Breed
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional

    def __str__(self):
        return self.name


class Cat(models.Model):  # задаем параметру классу Cat
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    age = models.IntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='cat_images/')  # Укажите папку для изображений
    location = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем

    def __str__(self):
        return f"{self.breed.name} - {self.age} years - {self.price}"

    def save(self, *args, **kwargs):
        #  изменяем размер только если есть изображение
        if self.image:
            # Открываем изображение с помощью Pillow
            img = Image.open(self.image)

            # Определяем желаемый размер
            output_size = (600, 400)  # Замените на желаемый размер

            # Изменяем размер изображения
            img = img.resize(output_size)

            # Создаем буфер в памяти для сохранения измененного изображения
            output = BytesIO()

            # Определяем формат изображения (например, JPEG)
            img_format = self.image.name.split('.')[-1].upper()  # Получаем расширение файла

            # Преобразуем формат если не jpeg
            if img_format == 'JPG':
                img_format = 'JPEG'

            # Сохраняем измененное изображение в буфер
            img.save(output, format=img_format, quality=70)  # Установите нужное качество

            # Получаем содержимое буфера
            output.seek(0)

            # Создаем новый файл Django на основе буфера
            self.image = InMemoryUploadedFile(
                output,
                'ImageField',
                self.image.name,  # Имя файла сохраняем прежним
                'image/' + img_format.lower(),  # Content type
                sys.getsizeof(output),
                None
            )

        super().save(*args, **kwargs)


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"