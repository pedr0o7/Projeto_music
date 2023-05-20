from flask import Flask, render_template, jsonify
from pytube import YouTube
import os
import moviepy.editor as mp
import re
import sys
import urllib.request
from googleapiclient.discovery import build
from datetime import datetime

app = Flask(__name__,template_folder='Template')

@app.route('/index')
def ini():
    return 'Ola mundo'

def download_video(link, link_img, nome, nome_artista, nome_musica):
    with app.app_context():
        try:
            urllib.request.urlretrieve(link_img, nome)
            print("Imagem salva! =)")
        except:
            erro = sys.exc_info()
            print("Ocorreu um erro:", erro)
        path = '\Projeto_music\musicas'

        yt = YouTube(link)
        # Fazer o download
        ys = yt.streams.filter(only_audio=True).first().download(path)
        # Converter o video(mp4) para mp3
        for file in os.listdir(path):
            if re.search('mp4', file):
                mp4_path = os.path.join(path, file)
                mp3_path = os.path.join(path, os.path.splitext(file)[0] + '.mp3')
                new_file = mp.AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                os.remove(mp4_path)
        print("Download Completo")

        lista = {}
        lista['titulo'] = nome_musica
        lista['artista'] = nome_artista
        lista['src'] = mp3_path
        lista['img'] = nome

        return lista


def get_musicas():
        musicas = []
        youTubeApiKey='AIzaSyCH8bkP6xRQDn0f24XkAwbZtW8FOMXp8Lw'

        youtube=build('youtube','v3',developerKey=youTubeApiKey)

        #extraindo musicas de uma playlist
        #https://music.youtube.com/playlist?list=LpWNlrG9ev8
        playlistId= 'PLxyqXg5XfqVYt9npPl4do2UkPSB6k6fX1'
        playlistName = 'Boiadera'
        nextPage_token = None

        playliste_musicas=[]
        while True :
            res = youtube.playlistItems().list(part='snippet', playlistId = playlistId, maxResults=50, pageToken=nextPage_token).execute()
            playliste_musicas += res['items']
            nextPage_token = res.get('nestPageToken')
            
            if nextPage_token is None :
                break

        #print('Numero total de musicas: ', len(playliste_musicas))
        musicas_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], playliste_musicas))
        #print(musicas_ids)
        stats = []

        for musica_id in musicas_ids:
            res = youtube.videos().list(part='statistics', id=musica_id).execute()
            stats += res['items']
            #print('-'*1000)
            #print(stats)
            titulo = list(map(lambda x: x['snippet']['title'],playliste_musicas))

            artista = list(map(lambda x: x['snippet']['videoOwnerChannelTitle'],playliste_musicas))
            videos_title = list(map(lambda x: x['snippet']['title'], playliste_musicas))
            url_thumbnails = list(map(lambda x: x['snippet']['thumbnails']['high']['url'], playliste_musicas))
            published_date = list(map(lambda x: str(x['snippet']['publishedAt']), playliste_musicas)) #conversion from ISO8601 date format
            video_description = list(map(lambda x: x['snippet']['description'], playliste_musicas))
            videoid = list(map(lambda x: x['snippet']['resourceId']['videoId'], playliste_musicas))

            extraction_date = [str(datetime.now())]*len(musicas_ids)

        #for i in range(len(playliste_musicas)):
        for i in range(1):
            #print (stats)
            #for i in len(videoid):
            #print('https://music.youtube.com/watch?v='+videoid[i]+'&&list='+playlistId)
            #print (videos_title) #NOMES
            #print (url_thumbnails) #imagens das musicas
            #print(titulo[i])
            nome_artista = artista[i].translate(str.maketrans('', '', ' - Topic'))
            #print(nome_artista)
            caminho_img = '\Projeto_music\imagens/'+ videos_title[i]+'.jpg'
            img = url_thumbnails[i]
            
            playlistlink = 'https://music.youtube.com/watch?v='+videoid[i]+'&&list='+playlistId
            musica_info=download_video(playlistlink,img,caminho_img,nome_artista,titulo[i])
            print(img,'-',caminho_img)
            musicas.append(musica_info)
        print(musicas)
        return 0


@app.route('/')
def index():
    get_musicas()
    return render_template('index.html')

    #return render_template('index.html')


app.run()