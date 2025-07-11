from django import forms
from .models import Cat, SellerProfile  # Import SellerProfile!

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['breed', 'age', 'gender', 'price', 'description', 'image', 'location']
        labels = {
            'breed': 'Порода',
            'age': 'Возраст',
            'gender': 'Пол',
            'price': 'Цена',
            'description': 'Описание',
            'image': 'Изображение',
            'location': 'Местоположение',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        cat = super().save(commit=commit)
        return cat

class SellerProfileForm(forms.ModelForm):  # SellerProfileForm все равно пригодится
    class Meta:
        model = SellerProfile
        fields = ['phone_number', 'location', 'about']
        labels = {
            'phone_number': 'Номер телефона',
            'location': 'Местоположение',
            'about': 'О себе',
        }
