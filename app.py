from flask import Flask, render_template, jsonify, request
from pytube import YouTube
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import moviepy.editor as mp
import re
import sys
import urllib.request
from googleapiclient.discovery import build
from datetime import datetime

app = Flask(__name__)

@app.route('/dados', methods=['GET'])
def obter_dados():
    dados = {
        'nome': 'João',
        'idade': 30,
        'cidade': 'Exemploville'
    }
    return jsonify(dados)


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
        path = '.\static\musicas'

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

@app.route('/music/<yt_id>', methods=['GET'])
def get_musicas(yt_id):
        print('tamo on',yt_id)
        music = []
        youTubeApiKey='SUA API KEY'

        youtube=build('youtube','v3',developerKey=youTubeApiKey)

        #extraindo musicas de uma playlist
        #https://music.youtube.com/playlist?list=LpWNlrG9ev8
        #playlistId= 'RDCLAK5uy_lW5Ba7hNPuQjGabDvy4cUZgj-FeONdfsM'
        playlistId= yt_id
        #playlistName = 'Boiadera'
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
        for i in range(3):
            #print (stats)
            #for i in len(videoid):
            #print('https://music.youtube.com/watch?v='+videoid[i]+'&&list='+playlistId)
            #print (videos_title) #NOMES
            #print (url_thumbnails) #imagens das musicas
            #print(titulo[i])
            nome_artista = artista[i].translate(str.maketrans('', '', ' - Topic'))
            #print(nome_artista)
            caminho_img = '.\static\imagens\\'+ videos_title[i]+'.jpg'
            img = url_thumbnails[i]
            
            playlistlink = 'https://music.youtube.com/watch?v='+videoid[i]+'&&list='+playlistId
            musica_info=download_video(playlistlink,img,caminho_img,nome_artista,titulo[i])
            print(img,'-',caminho_img)
            music.append(musica_info)
        #print(music)
        return music

@app.route('/home')
def get_new():
    return render_template('new.html')


@app.route('/loading', methods=['POST'])
def get_loading():
    name = request.form['dados']
    print(name)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Executa em modo headless
    #chrome_options.add_argument("--no-sandbox")  
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://music.youtube.com/')
    search_button = driver.find_element("xpath",'//*[@id="layout"]/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/tp-yt-paper-icon-button[1]')
    search_button.click()
    search_box = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input'))
    )
    #search_box = driver.find_element("xpath",'//*[@id="input"]')
    #driver.implicitly_wait(10)
    search_box.send_keys(name)
    search_box.send_keys(Keys.ENTER)
    #driver.implicitly_wait(30)
    time.sleep(5)
    search_playlist = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[1]/ytmusic-chip-cloud-renderer/iron-selector/ytmusic-chip-cloud-chip-renderer[4]/div/a'))
    )
    #search_playlist = driver.find_element("xpath",'')
    search_playlist.click()
    time.sleep(5)
    search_first_playlist = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer/div[3]/ytmusic-responsive-list-item-renderer/a'))
    )
    #search_first_playlist = driver.find_element("xpath",'')
    
    search_first_playlist.click()
    time.sleep(5)
    get_url = driver.current_url
    print(get_url)
    #https://music.youtube.com/playlist?list=RDCLAK5uy_lW5Ba7hNPuQjGabDvy4cUZgj-FeONdfsM
    url_id = get_url.split('list=')
    print(url_id[1])
    driver.quit()
    return render_template('new.html', dados=url_id[1])


def get_search_yt(name):
    print(name)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Executa em modo headless
    #chrome_options.add_argument("--no-sandbox")  
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://music.youtube.com/')
    search_button = driver.find_element("xpath",'//*[@id="layout"]/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/tp-yt-paper-icon-button[1]')
    search_button.click()
    search_box = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input'))
    )
    #search_box = driver.find_element("xpath",'//*[@id="input"]')
    #driver.implicitly_wait(10)
    search_box.send_keys(name)
    search_box.send_keys(Keys.ENTER)
    #driver.implicitly_wait(30)
    time.sleep(5)
    search_playlist = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[1]/ytmusic-chip-cloud-renderer/iron-selector/ytmusic-chip-cloud-chip-renderer[4]/div/a'))
    )
    #search_playlist = driver.find_element("xpath",'')
    search_playlist.click()
    time.sleep(5)
    search_first_playlist = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer/div[3]/ytmusic-responsive-list-item-renderer/a'))
    )
    #search_first_playlist = driver.find_element("xpath",'')
    
    search_first_playlist.click()
    time.sleep(5)
    get_url = driver.current_url
    print(get_url)
    #https://music.youtube.com/playlist?list=RDCLAK5uy_lW5Ba7hNPuQjGabDvy4cUZgj-FeONdfsM
    url_id = get_url.split('list=')
    print(url_id[1])
    driver.quit()
    #get_musicas()
    return jsonify(get_musicas(url_id[1]))

@app.route('/')
def index():
    #print(get_musicas())
    #response = get_musicas()
    return render_template('teste.html')


if __name__ == '__main__':
    #get_search_yt('hungria')
    app.run()
