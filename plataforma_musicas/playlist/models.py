from django.db import models
from usuarios.models import Usuario
from datetime import datetime

class Playlist(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    thumb = models.ImageField(upload_to = "thumb_musicas")

    def __str__(self) -> str:
        return self.nome

class Musicas(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    musica = models.FileField(upload_to = "musica")
    playlist = models.ForeignKey(Playlist, on_delete = models.DO_NOTHING, null=True, blank=True)


    def __str__(self) -> str:
        return self.nome


class Comentarios(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete = models.DO_NOTHING)
    comentario = models.TextField()
    data = models.DateTimeField(default = datetime.now)
    musicas = models.ForeignKey(Musicas, on_delete = models.DO_NOTHING)
 

    def __str__(self) -> str:
        return self.usuario.nome        


class NotasMusicas(models.Model):
    choices = (
        ('p', 'Péssimo'),
        ('r', 'Ruim'),
        ('re', 'Regular'),
        ('b', 'bom'),
        ('o', 'Ótimo')
    )

    musica = models.ForeignKey(Musicas, on_delete=models.DO_NOTHING)
    nota = models.CharField(max_length=50, choices=choices)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)        