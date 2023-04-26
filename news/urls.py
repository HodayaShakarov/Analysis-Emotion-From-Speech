from django.urls import path
import news.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('scrape/', news.views.scrape, name="scrape"),
    path('', news.views.news_list, name="home"),
    path('login/', news.views.login, name="login"),
    path('register/', news.views.register, name="register"),
    path('register/password/', news.views.password, name="password"),
    path('textToSign/', news.views.news_list2, name="textToSign"),
    path('signToText2/', news.views.news_list3, name="signToText2"),
    path('voiceToSign/', news.views.news_list4, name="voiceToSign"),
    path('wordsList/', news.views.listWords, name="wordsList"),
    path('translateToSign/', news.views.translateToSign, name="translateToSign"),
    path('translateToText/', news.views.translateToText, name="translateToText"),
    path('retMain', news.views.news_list, name="retMain"),
    path('login/loginSubmit/', news.views.loginSubmit, name="loginSubmit"),
    path('register/registerSubmit/', news.views.registerSubmit, name="registerSubmit"),
    path('register/password/passwordSubmit/', news.views.passwordSubmit, name="passwordSubmit"),
    path('logout/', news.views.logout, name="logout"),
    path('/', news.views.news_list, name="main"),
    path('myRecords/', news.views.records_table, name="recordsTable"),
    path('myRecordsList/', news.views.records_list, name="recordsList"),
    path('updateEmotion/', news.views.update_emotion, name="updateEmotion"),
    path('backToRecord/', news.views.back_to_record, name="backToRecord"),
    path('uploadFile/', news.views.upload_file, name="uploadFile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
