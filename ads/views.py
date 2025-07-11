from django.shortcuts import render, get_object_or_404, redirect
from .models import Cat, Breed, SellerProfile
from .forms import CatForm, SellerProfileForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    cats = Cat.objects.all().order_by('-date_posted')
    paginator = Paginator(cats, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'home.html', context)

def cat_detail(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    return render(request, 'cat_detail.html', {'cat': cat})

@login_required
def create_cat(request, pk=None):  # Добавили pk=None для создания и редактирования
    print("request.user:", request.user)  # Добавили print statement

    if pk:
        cat = get_object_or_404(Cat, pk=pk, seller=request.user) # Убедитесь, что продавец совпадает
    else:
        cat = None

    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            print("Form is valid!")
            cat = form.save(commit=False)  # Создаем объект Cat, но ПОКА НЕ сохраняем
            cat.seller = request.user  # Присваиваем текущего пользователя как продавца!
            cat.save()  # Теперь сохраняем объект Cat с назначенным продавцом

            # Создаем или получаем SellerProfile ПОСЛЕ успешного сохранения Cat
            seller_profile, created = SellerProfile.objects.get_or_create(user=cat.seller)

            return redirect('cat_detail', pk=cat.pk)
        else:
            print("Form is NOT valid:")
            print(form.errors)
            return render(request, 'cat_form.html', {'form': form})
    else:
        form = CatForm(instance=cat)

    return render(request, 'cat_form.html', {'form': form})

@login_required
def delete_cat(request, pk):
    cat = get_object_or_404(Cat, pk=pk, seller=request.user)
    if request.method == 'POST':
        cat.delete()
        return redirect('home')
    return render(request, 'cat_confirm_delete.html', {'cat': cat})

def breed_list(request, breed_name):
    breed = get_object_or_404(Breed, name=breed_name)
    cats = Cat.objects.filter(breed=breed).order_by('-date_posted')
    context = {'breed': breed, 'cats': cats}
    return render(request, 'breed_list.html', context)

def search(request):
    query = request.GET.get('q')
    results = Cat.objects.filter(description__icontains=query) | Cat.objects.filter(breed__name__icontains=query) | Cat.objects.filter(location__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = SellerProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        user_form = UserCreationForm()
        profile_form = SellerProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile(request):
    profile = get_object_or_404(SellerProfile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(SellerProfile, user=request.user)
    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = SellerProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})