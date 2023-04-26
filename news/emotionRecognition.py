import glob
import os
import soundfile as sf
import numpy as np
import librosa as lb
import pickle
from warnings import simplefilter
from sklearn.ensemble import RandomForestClassifier

# from views import user_records_size

emotion_labels = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

focused_emotion_labels = ['angry', 'happy', 'sad']


def audio_features(file_title, mfcc, chroma, mel):
    with sf.SoundFile(file_title) as audio_recording:
        audio = audio_recording.read(dtype="float32")
        sample_rate = audio_recording.samplerate
        if chroma:
            stft = np.abs(lb.stft(audio))
            result = np.array([])
        if mfcc:
            mfccs = np.mean(lb.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(lb.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(lb.feature.melspectrogram(audio, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
        return result


def audio_features_my(file_title, mfcc, chroma, mel):
    with sf.SoundFile(file_title) as audio_recording:
        audio = audio_recording.read(dtype="float32")
        audio = audio.ravel()
        sample_rate = audio_recording.samplerate
        if chroma:
            stft = np.abs(lb.stft(audio))
            result = np.array([])
        if mfcc:
            mfccs = np.mean(lb.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(lb.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(lb.feature.melspectrogram(audio, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
        return result


def emotion_reco_user(userRecord, file_name_model, records_user):
    if len(records_user) > 160:
        train_model(records_user)

    X_test = loading_audio_data(userRecord)
    loaded_model = pickle.load(open(file_name_model, 'rb'))
    y_pred = loaded_model.predict(X_test)
    return y_pred[0]


def emotion_reco(userRecord, file_name_model):
    X_test = loading_audio_data(userRecord)
    loaded_model = pickle.load(open(file_name_model, 'rb'))
    y_pred = loaded_model.predict(X_test)
    return y_pred[0]


def train_model(records_user):
    if len(records_user) > 160:
        X_train, y_train = loading_audio_train_data_my(records_user)
    else:
        X_train, y_train = loading_audio_train_data()
    random = RandomForestClassifier()
    random.fit(X_train, y_train)
    filename = 'finalized_model.sav'
    pickle.dump(random, open(filename, 'wb'))
    return filename


# test from user
def loading_audio_data(userRecord):
    z = []
    # user
    src = "./news_listtranslateToSign" + userRecord
    feature = audio_features_my(src, mfcc=True, chroma=True, mel=True)
    z.append(feature)
    final_dataset = np.array(z)
    return final_dataset


# actors train
def loading_audio_train_data():
    sf.available_formats()
    x = []
    y = []
    # dataset
    for file in glob.glob("data//Actor_*//*.wav"):
        file_path = os.path.basename(file)
        emotion = emotion_labels[file_path.split("-")[0]]
        if emotion not in focused_emotion_labels:
            continue
        # print(file_path)
        feature = audio_features(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    final_dataset = np.array(x), y
    return final_dataset


simplefilter(action='ignore', category=FutureWarning)


def loading_audio_train_data_my(records_user):
    sf.available_formats()
    x = []
    y = []
    # dataset
    for record in records_user:
        file_path = "./news_listtranslateToSign" + record["record"]
        emotion = record["emotion"]
        feature = audio_features_my(file_path, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    final_dataset = np.array(x), y
    return final_dataset
