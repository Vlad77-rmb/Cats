from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('cat/<int:pk>/', views.cat_detail, name='cat_detail'),
    path('cat/new/', views.create_cat, name='create_cat'),  # Для создания объявления
    path('cat/<int:pk>/update/', views.create_cat, name='update_cat'),  # Для редактирования объявления
    path('cat/<int:pk>/delete/', views.delete_cat, name='delete_cat'),
    path('breed/<str:breed_name>/', views.breed_list, name='breed_list'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]

