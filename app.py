from flask import Flask, render_template, jsonify
from pytube import YouTube
import os
import moviepy.editor as mp
import re
import sys
import urllib.request
from googleapiclient.discovery import build
from datetime import datetime

app = Flask(__name__,template_folder='template')

@app.route('/')
def ini():
    return 'Ola mundo'

def download_video(link, link_img, nome, nome_artista, nome_musica):
    with app.app_context():
        try:
            urllib.request.urlretrieve(link_img, nome)
            # print("Imagem salva! =)")
        except:
            erro = sys.exc_info()
            # print("Ocorreu um erro:", erro)
        path = '\PROJETO_SPOTIFY_PARTE_2\musicas'

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
        # print("Download Completo")

        lista = {}
        lista['titulo'] = nome_musica
        lista['artista'] = nome_artista
        lista['src'] = mp3_path
        lista['img'] = nome

        return lista


def get_musicas():
    musicas = []
    youTubeApiKey = 'YOUR_YOUTUBE_API_KEY'

    youtube = build('youtube', 'v3', developerKey=youTubeApiKey)

    # Extraindo músicas de uma playlist
    playlistId = 'YOUR_PLAYLIST_ID'
    nextPage_token = None

    playlist_musicas = []
    while True:
        res = youtube.playlistItems().list(part='snippet', playlistId=playlistId, maxResults=50,
                                           pageToken=nextPage_token).execute()
        playlist_musicas += res['items']
        nextPage_token = res.get('nextPageToken')

        if nextPage_token is None:
            break

    for musica in playlist_musicas:
        musica_id = musica['snippet']['resourceId']['videoId']
        res = youtube.videos().list(part='statistics', id=musica_id).execute()
        stats = res['items']
        titulo = musica['snippet']['title']
        artista = musica['snippet']['videoOwnerChannelTitle']
        videos_title = musica['snippet']['title']
        url_thumbnails = musica['snippet']['thumbnails']['high']['url']
        published_date = str(musica['snippet']['publishedAt'])
        video_description = musica['snippet']['description']
        videoid = musica['snippet']['resourceId']['videoId']

        nome_artista = artista.translate(str.maketrans('', '', ' - Topic'))
        caminho_img = '\PROJETO_SPOTIFY_PARTE_2\imagens/' + videos_title + '.jpg'
        img = url_thumbnails
        playlistlink = 'https://music.youtube.com/watch?v='+videoid+'&&list='+playlistId
        musica_info = download_video(playlistlink, img, caminho_img, nome_artista, titulo)
        musicas.append(musica_info)
        return jsonify(musicas)


@app.route('/index')
def index():
    return get_musicas()

    #return render_template('index.html')


app.run()