from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

app_name = 'lesson'
class MyHacKostyl(auth_views.PasswordResetView):
    success_url = reverse_lazy("lesson:password_reset_done")
urlpatterns = [
    # path('', views.all_materials, name='all_materials'),
    path('', views.MaterialListView.as_view(), name='all_materials'),
    path('<int:yy>/<int:mm>/<int:dd>/<slug:slug>/',
         views.detailed_material, name='detailed_material'),
    path('<int:material_id>/share/', views.share_material,
         name='share_material'),
    path('create/', views.create_material,
         name='create_form'),
    # path('login/', views.custom_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("password_reset/", MyHacKostyl.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("lesson:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]