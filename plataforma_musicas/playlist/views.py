from django.http.response import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from.models import Playlist, Musicas, Comentarios, NotasMusicas
import json

def home(request):
    if request.session.get('usuario'):
        playlists = Playlist.objects.all()
        request_usuario = request.session.get('usuario')
        return render(request, 'home.html', {'playlists': playlists, 'request_usuario': request_usuario})
    else:
        return redirect('/auth/login/?status=2')


def playlist(request, id):
    if request.session.get('usuario'):
        musicas = Musicas.objects.filter(playlist = id)
        request_usuario = request.session.get('usuario')
        return render(request, 'playlist.html', {'musicas': musicas, 'request_usuario': request_usuario})
    else:
        return redirect('/auth/login/?status=2')     


def musica(request, id):
    if request.session.get('usuario'):
        musicas = Musicas.objects.get(id = id)
        usuario_id = request.session['usuario']
        comentarios = Comentarios.objects.filter(musicas = musicas).order_by('-data')

        request_usuario = request.session.get('usuario')
        usuario_avaliou = NotasMusicas.objects.filter(musica_id = id).filter(usuario_id = request_usuario)
        avaliacoes = NotasMusicas.objects.filter(musica_id = id)



        return render(request, 'musica.html', {'musicas': musicas,
                                            'usuario_id': usuario_id,
                                            'comentarios': comentarios,
                                            'request_usuario': request_usuario,
                                            'usuario_avaliou': usuario_avaliou,
                                            'avaliacoes': avaliacoes})
    else:
        return redirect('/auth/login/?status=2')


def comentarios(request):
    usuario_id = int(request.POST.get('usuario_id'))
    comentario = request.POST.get('comentario')
   
    musica_id = int(request.POST.get('musica_id'))
   
    comentario_instancia = Comentarios(usuario_id = usuario_id,
                                       comentario = comentario,
                                       musicas_id = musica_id)
    comentario_instancia.save()

    comentarios = Comentarios.objects.filter(musica = musica_id).order_by('-data')
    somente_nomes = [i.usuario.nome for i in comentarios]
    somente_comentarios = [i.comentario for i in comentarios]
    comentarios = list(zip(somente_nomes, somente_comentarios))

    return HttpResponse(json.dumps({'status': '1', 'comentarios': comentarios }))                   

def processa_avaliacao(request):
    if request.session.get('usuario'):

        avaliacao = request.POST.get('avaliacao')
        musica_id = request.POST.get('musica_id')
        
        usuario_id = request.session.get('usuario')

        usuario_avaliou = NotasMusicas.objects.filter(musica_id = musica_id).filter(usuario_id = usuario_id)

        if not usuario_avaliou:
            nota_musicas = NotasMusicas(musica_id = musica_id,
                                    nota = avaliacao,
                                    usuario_id = usuario_id,
                                    )
            nota_musicas.save()
            return redirect(f'/home/musica/{musica_id}')
        else:
            return redirect('/auth/login/')

    else:
        return redirect('/auth/login/')