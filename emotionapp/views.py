from django.shortcuts import render,redirect
from pandas.core.indexes.base import Index
from .forms import ImageForm,LoginForm,SignUpForm
from .models import ModelFile
from fer import FER
import matplotlib.pyplot as plt
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
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
class Login(LoginView):
    form_class = LoginForm
    template_name = 'emotionapp/login.html'

class Logout(LogoutView):
    template_name = 'emotionapp/base.html'

def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      #フォームから'username'を読み取る
      username = form.cleaned_data.get('username')
      #フォームから'password1'を読み取る
      password = form.cleaned_data.get('password1')
      # 読み取った情報をログインに使用する情報として new_user に格納
      new_user = authenticate(username=username, password=password)
      if new_user is not None:
         # new_user の情報からログイン処理を行う
        login(request, new_user)
        # ログイン後のリダイレクト処理
        return redirect('emotionapp/index.html')
  # POST で送信がなかった場合の処理
  else:
    form = SignUpForm()
    return render(request, 'emotionapp/signup.html', {'form': form})
