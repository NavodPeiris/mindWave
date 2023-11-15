from speechbrain.speechbrain.pretrained.interfaces import foreign_class

emotions = {"neu": "neutral", "ang": "angry", "hap": "happy", "sad": "sad"}

def emotion_recognition(file):

    classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")
    out_prob, score, index, text_lab = classifier.classify_file(file)
    key = text_lab[0]
    emotion = emotions[key]
    return emotion

