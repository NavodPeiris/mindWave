import librosa
import pickle
import numpy as np

def testing_unit(filename):
    tester = []
    test, ans = librosa.load(filename)  # provide path of  wave file
    mfccs = np.mean(librosa.feature.mfcc(y=test, sr=ans, n_mfcc=40).T, axis=0)
    tester.append(mfccs)
    tester = np.array(tester)
    return tester #return Mfcss extracted arrray


def scream_detection(filename):

    load_model2 = pickle.load(open('scream_detection_models/phase2_model.sav', 'rb'))  # loading phase2 model

    ok = load_model2.predict(testing_unit(filename))  # using second phase_model
    if ok[0] == 1:
        # scream
        return True
    else:
        # speech
        return False