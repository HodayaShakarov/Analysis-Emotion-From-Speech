from __future__ import print_function
import os
from urllib.request import Request

from django.shortcuts import render, redirect
from news.models import User, Headline, Record
import bcrypt
import os.path
import json
import pathlib
import requests
from django.conf import settings
from bs4 import BeautifulSoup as BSoup
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, QueryDict
import speech_recognition as sr
import news.emotionRecognition as er
requests.packages.urllib3.disable_warnings()

reco = []
file_name_model = er.train_model(reco)
user_records_size = 0


def news_list(request):
    context = {
    }
    return render(request, "news/main.html", context)


def login(request):
    context = {
    }
    return render(request, "news/login.html", context)


def register(request):
    context = {
    }
    return render(request, "news/register.html", context)


@csrf_protect
def password(request):
    context = {
    }
    return render(request, "news/password.html", None)


def news_list2(request):
    context = {
    }
    return render(request, "news/textToSign.html", context)


def news_list3(request):
    print({settings.BASE_DIR})
    os.system(f"streamlit run {settings.BASE_DIR}/prog/app.py")
    context = {
    }
    return render(request, "news/signToText2.html", context)


def news_list4(request):
    context = {
    }
    return render(request, "news/voiceToSign.html", context)


def back_to_record(request):
    return redirect("voiceToSign")


def news_list5(request):
    context = {
    }
    return render(request, "news/register.html", context)


def listWords(request):
    context = {
    }
    return render(request, "news/wordsList.html", context)


def records_table(request):
    context = {
    }
    return render(request, "news/recordsTable.html", context)


def upload_file(request):
    response = translateToText(request)
    context = json.loads(response.content.decode())
    ordinary_dict = dict(request.POST)
    query_dict = QueryDict('', mutable=True)
    query_dict.update(context)
    query_dict.update(ordinary_dict)
    request.POST = query_dict
    return translateToSign(request)


def translateToSign(request):
    print("i whats up?")

    path = pathlib.Path(__file__).parent.resolve()
    f = open(str(path) + '\\sign-videos.json')
    dictionary = json.load(f)
    text_box_value = request.POST['text'].split(" ")
    if text_box_value == '':
        text_box_value.pop()
    print(text_box_value);
    arraysrc = [];
    counter = 0
    for i in text_box_value:
        counter = counter + 1
        if i not in dictionary:
            if i != " ":
                context = {
                    'arraysrc': i,
                }
                print("error")
                return render(request, "news/oops.html", context)
        if counter == 1:
            arraysrc = [(dictionary[text_box_value[0]])]
        if counter == 2:
            arraysrc = [(dictionary[text_box_value[0]]), (dictionary[text_box_value[1]])]
        if counter == 3:
            arraysrc = [(dictionary[text_box_value[0]]), (dictionary[text_box_value[1]]),
                        (dictionary[text_box_value[2]])]
        if counter == 4:
            arraysrc = [(dictionary[text_box_value[0]]), (dictionary[text_box_value[1]]),
                        (dictionary[text_box_value[2]]), (dictionary[text_box_value[3]])]
        if counter == 5:
            arraysrc = [(dictionary[text_box_value[0]]), (dictionary[text_box_value[1]]),
                        (dictionary[text_box_value[2]]), (dictionary[text_box_value[3]]),
                        (dictionary[text_box_value[4]])]
        if counter == 6:
            arraysrc = [(dictionary[text_box_value[0]]), (dictionary[text_box_value[1]]),
                        (dictionary[text_box_value[2]]), (dictionary[text_box_value[3]]),
                        (dictionary[text_box_value[4]]), (dictionary[text_box_value[5]])]

    arraysrc.reverse();
    text = ""
    emotion = ""
    if 'text' in request.POST:
        text = request.POST["text"]
    if 'emotion' in request.POST:
        emotion = request.POST["emotion"]

    context = {
        'arraysrc': arraysrc,
        'translation': text,
        'emotion': emotion,
    }
    return render(request, "news/foo.html", context)


def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.theonion.com/"
    content = session.get(url, verify=False).content
    soup = BSoup(content, "html.parser")
    News = soup.find_all('div', {"class": "curation-module__item"})
    for artcile in News:
        main = artcile.find_all('a')[0]
        link = main['href']
        image_src = str(main.find('img')['srcset']).split(" ")[-4]
        title = main['title']
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = image_src
        new_headline.save()
    return redirect("../")


def translateToText(request):
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(request.FILES["audio_data"]) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)

    myfile = request.FILES['audio_data']
    fs = FileSystemStorage()
    filename = fs.save(str(myfile.name).replace(':', ''), myfile)
    uploaded_file_url = fs.url(filename)
    records_user = record_user_list(request)

    if 'user_id' in request.session:
        emotion = er.emotion_reco_user(uploaded_file_url, file_name_model, records_user)
        user = User.objects.get(id=request.session['user_id'])

        record = Record.objects.create(record=request.FILES["audio_data"], user_email=user.email,
                                       translation=text, emotion=emotion)
    else:
        emotion = er.emotion_reco(uploaded_file_url, file_name_model)
    context = {
        'text': text,
        'emotion': emotion,
    }
    return JsonResponse(context)


def record_user_list(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        records = []
        user_records = Record.objects.filter(user_email=user.email)
        user_records_size = len(user_records)
        for rec in user_records:
            temp = {"recordId": rec.id, "record": rec.record.url, "createdDate": rec.created_at,
                    "translation": rec.translation,
                    "emotion": rec.emotion}
            records.append(temp)
        return records


def records_list(request):
    if 'user_id' in request.session:
        records = record_user_list(request)

        return JsonResponse({
            'context': records
        })
    else:
        return render('/news/main.html')


def update_emotion(request):
    if 'user_id' in request.session:
        try:
            Record.objects.filter(id=request.POST["recordId"]).update(emotion=request.POST["emotion"])
            print("update_emotion: ok")
            return JsonResponse({
                'context': "ok"
            })
        except:
            print("update_emotion: error")
            return JsonResponse({
                'context': "error"
            })
    else:
        return render(request, '')


# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect('/news/main')
    else:
        return render(request, 'login.html')


def registerSubmit(request):
    if request.method == "POST":
        error = User.objects.register_validator(request.POST)
        url = "/register"
        if error["type"] != "":
            context = {"error": error}
        else:
            context = {
                "user": {"firstName": request.POST['firstName'],
                         "lastName": request.POST['lastName'],
                         "email": request.POST['email']}
            }
            url = '/register/password'
        return JsonResponse({
            'context': context,
            'url': url,
        })
    else:
        return redirect("/")


def passwordSubmit(request):
    if request.method == "POST":
        url = "/password"
        error = User.objects.register_validator(request.POST)
        if error["type"] != "":
            return JsonResponse({
                'context': {},
                'url': url,
            })
        error1 = User.objects.password_validator(request.POST)
        if error1["type"] != "":
            context = {"error": error1}
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(firstName=request.POST['firstName'], lastName=request.POST['lastName'],
                                       email=request.POST['email'], password=pw_hash.decode())
            request.session.set_expiry(1200)
            request.session['user_id'] = user.id
            context = {"user": request.POST['firstName'] + " " + request.POST['lastName']}
            url = "/login"
        return JsonResponse({
            'context': context,
            'url': url,
        })
    else:
        return redirect("/")


def loginSubmit(request):
    if request.method == "POST":
        error = User.objects.login_validator(request.POST)
        url = "/login"
        if error["type"] != "":
            context = {"error": error}
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session.set_expiry(1200)
            request.session['user_id'] = user.id

            context = {
                "userName": user.firstName + " " + user.lastName
            }
            url = '/'
        return JsonResponse({
            'context': context,
            'url': url,
        })
    else:
        return redirect("/")


def logout(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        request.session.clear()
        print("session has been cleared")
        return redirect("/")
