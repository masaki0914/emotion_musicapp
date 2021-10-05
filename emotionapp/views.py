from django.shortcuts import render
from pandas.core.indexes.base import Index
from .forms import ImageForm
from .models import ModelFile
from fer import FER
import matplotlib.pyplot as plt
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Create your views here.
def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            img_name = request.FILES['image']
            img_url = 'media/documents/{}'.format(img_name)
            img = img_url
            image = plt.imread(img)
            emo_detector = FER(mtcnn=True)
            captured_emotions = emo_detector.detect_emotions(image)
            dominant_emotion, emotion_score = emo_detector.top_emotion(image)
            songs = pd.read_csv("music/song.csv")
            if dominant_emotion == 'angry':
                dominant_emotion = '怒り'
                ser_abs_diff = songs.sort_values('loudness',ascending=False).head(10)
                df_top = ser_abs_diff.loc[:,['曲名','アーティスト名']]
                result = df_top.to_html(index=False)
            elif dominant_emotion == 'disgust':
                dominant_emotion = '嫌悪'
                ser_abs_diff = songs.sort_values('energy',ascending=False).head(10)
                df_top = ser_abs_diff.loc[:,['曲名','アーティスト名']]
                result = df_top.to_html(index=False)
            elif dominant_emotion == 'happy':
                dominant_emotion = '幸せ'
                ser_abs_diff = songs.sort_values('valence',ascending=False).head(10)
                df_top = ser_abs_diff.loc[:,['曲名','アーティスト名']]
                result = df_top.to_html(index=False)
            elif dominant_emotion == 'sad':
                dominant_emotion = '悲しみ'
                ser_abs_diff = songs.sort_values('acousticness',ascending=False).head(10)
                df_top = ser_abs_diff.loc[:,['曲名','アーティスト名']]
                result = df_top.to_html(index=False)
            elif dominant_emotion == 'surprise':
                dominant_emotion = '驚き'
                ser_abs_diff = songs.sort_values('danceability',ascending=False).head(10)
                df_top = ser_abs_diff.loc[:,['曲名','アーティスト名']]
                result = df_top.to_html(index=False)
            else: dominant_emotion = '自然'
            emotion_score = emotion_score*100
            return render(request, 'emotionapp/classify.html', {'img_url':img_url,'t':dominant_emotion,'y':emotion_score,'music':result})
    else:
        form = ImageForm()
        return render(request,'emotionapp/index.html',{'form':form})   
