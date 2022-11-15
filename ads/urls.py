from django.urls import path

from ads import views
from ads.models import Category, Ad
from users.models import Location

urlpatterns = [
    path('', views.index_ads),
    path("upload_csv/", views.csv_in_bd),
    # списковые
    path('cat/', views.Ads_Cat_List_View.as_view(model=Category)),
    path('ad/', views.Ads_Ad_List_View.as_view(model=Ad)),
    path('loc/', views.Ads_Loc_List_View.as_view(model=Location)),
    # детальные
    path('cat/<int:pk>/', views.Ads_Detail_View.as_view(model=Category)),
    path('ad/<int:pk>/', views.Ads_Detail_View.as_view(model=Ad)),
    path('loc/<int:pk>/', views.Ads_Detail_View.as_view(model=Location)),
    # создание
    path('cat/create/', views.Ads_Create_View.as_view(model=Category)),
    path('ad/create/', views.Ads_Ad_Create_View.as_view()),
    path('loc/create/', views.Ads_Create_View.as_view(model=Location)),
    # изменение
    path('cat/<int:pk>/update/', views.Ads_Update_View.as_view(model=Category)),
    path('ad/<int:pk>/update/', views.Ads_Update_View.as_view(model=Ad)),
    path('loc/<int:pk>/update/', views.Ads_Update_View.as_view(model=Location)),
    # удаление
    path('cat/<int:pk>/delete/', views.Ads_Delete_View.as_view(model=Category)),
    path('ad/<int:pk>/delete/', views.Ads_Delete_View.as_view(model=Ad)),
    path('loc/<int:pk>/delete/', views.Ads_Delete_View.as_view(model=Location)),
    # работа с картинками
    path('ad/<int:pk>/image/', views.Ads_Image_View.as_view(model=Ad)),

]
