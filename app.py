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

app = Flask(__name__)

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
       
        ys = yt.streams.filter(only_audio=True).first().download(path)
        
        
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
        youTubeApiKey='AIzaSyCH8bkP6xRQDn0f24XkAwbZtW8FOMXp8Lw'

        youtube=build('youtube','v3',developerKey=youTubeApiKey)

        
        playlistId= yt_id
        
        nextPage_token = None

        playliste_musicas=[]
        while True :
            res = youtube.playlistItems().list(part='snippet', playlistId = playlistId, maxResults=50, pageToken=nextPage_token).execute()
            playliste_musicas += res['items']
            nextPage_token = res.get('nestPageToken')
            
            if nextPage_token is None :
                break

       
        musicas_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], playliste_musicas))
      
        stats = []

        for musica_id in musicas_ids:
            res = youtube.videos().list(part='statistics', id=musica_id).execute()
            stats += res['items']
    
            titulo = list(map(lambda x: x['snippet']['title'],playliste_musicas))

            artista = list(map(lambda x: x['snippet']['videoOwnerChannelTitle'],playliste_musicas))
            videos_title = list(map(lambda x: x['snippet']['title'], playliste_musicas))
            url_thumbnails = list(map(lambda x: x['snippet']['thumbnails']['high']['url'], playliste_musicas))
            videoid = list(map(lambda x: x['snippet']['resourceId']['videoId'], playliste_musicas))

     
        for i in range(3):
          
            nome_artista = artista[i].translate(str.maketrans('', '', ' - Topic'))
       
            caminho_img = '.\static\imagens\\'+ videos_title[i]+'.jpg'
            img = url_thumbnails[i]
            
            playlistlink = 'https://music.youtube.com/watch?v='+videoid[i]+'&&list='+playlistId
            musica_info=download_video(playlistlink,img,caminho_img,nome_artista,titulo[i])
            print(img,'-',caminho_img)
            music.append(musica_info)
    
        return jsonify(music)

@app.route('/home')
def get_new():
    return render_template('new.html')

@app.route('/loading', methods=['POST'])
def get_loading():
    name = request.form['dados']
    print(name)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
   
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://music.youtube.com/')
    search_button = driver.find_element("xpath",'//*[@id="layout"]/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/tp-yt-paper-icon-button[1]')
    search_button.click()
    search_box = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/input'))
    )
  
    search_box.send_keys(name)
    search_box.send_keys(Keys.ENTER)
  
    time.sleep(5)
    search_playlist = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[1]/ytmusic-chip-cloud-renderer/iron-selector/ytmusic-chip-cloud-chip-renderer[4]/div/a'))
    )
   
    search_playlist.click()
    time.sleep(5)
    search_first_playlist = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer/div[3]/ytmusic-responsive-list-item-renderer/a'))
    )
 
    
    search_first_playlist.click()
    time.sleep(5)
    get_url = driver.current_url
    print(get_url)
  
    url_id = get_url.split('list=')
    print(url_id[1])
    driver.quit()
    return render_template('new.html', dados=url_id[1])

@app.route('/')
def index():
    return render_template('teste.html')


if __name__ == '__main__':
    app.run()
