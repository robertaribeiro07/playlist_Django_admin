from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('playlist/<int:id>', views.playlist, name = 'playlist'),
    path('musica/<int:id>', views.musica, name = 'musica'),
    path('comentarios/', views.comentarios, name = 'comentarios'),
    path('processa_avaliacao/', views.processa_avaliacao, name = 'processa_avaliacao'),
]