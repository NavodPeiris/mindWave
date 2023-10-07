import os
from pydub import AudioSegment
from google_transcription import sinhala_transcription, english_transcription

from emotion_recognition import emotion_recognition
from scream_detection import scream_detection
from repeat_detection import is_repeating
from document_query import document_query
from text_to_speech import text_to_speech

# segment according to speaker
def wav_file_segmentation_doc(file_name, segments):
    # Load the WAV file
    audio = AudioSegment.from_file(file_name, format="wav")

    texts = []

    folder_name = "doctor"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    i = 0

    for segment in segments:
        start = segment[0] * 1000   # start time in miliseconds
        end = segment[1] * 1000     # end time in miliseconds
        clip = audio[start:end]
        i = i + 1
        file = folder_name + "/" + "segment"+ str(i) + ".wav"
        clip.export(file, format="wav")
        trans = sinhala_transcription(file)

        texts.append([segment[0], segment[1], trans, "", 0, 0])

        # get english translation
        eng_trans = english_transcription(file)
        print(eng_trans)
        
        # check if "alice" utterance is there
        if "alice" in eng_trans or "Alice" in eng_trans:
            # get response from model
            print("a question for alice")
            alice_res = document_query(eng_trans)
            text_to_speech(alice_res)

        # if screaming -> 1
        # if reapeating -> 1
        # return -> [[start time, end time, transcript, emotion, screaming, repeating], [start time, end time, transcript,..], ..],

        # Delete the WAV file after processing
        os.remove(file)

    return texts


# segment according to speaker
def wav_file_segmentation_patient(file_name, segments):
    # Load the WAV file
    audio = AudioSegment.from_file(file_name, format="wav")

    texts = []
    screams = 0
    repeats = 0

    folder_name = "patient"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    i = 0

    for segment in segments:
        start = segment[0] * 1000   # start time in miliseconds
        end = segment[1] * 1000     # end time in miliseconds
        clip = audio[start:end]
        i = i + 1
        file = folder_name + "/" + "segment"+ str(i) + ".wav"
        clip.export(file, format="wav")
        trans = sinhala_transcription(file)

        # get english translation
        eng_trans = english_transcription(file)
        print(eng_trans)

        # check if "alice" utterance is there
        if "alice" in eng_trans or "Alice" in eng_trans:
            # get response from model
            print("a question for alice")
            alice_res = document_query(eng_trans)
            text_to_speech(alice_res)

        emotion = emotion_recognition(file)
        screaming = scream_detection(file)
        repeating = is_repeating(trans)

        if screaming:
            screams += 1
        if repeating:
            repeats += 1
        
        screaming = int(screaming)   # true -> 1
        repeating = int(repeating)   # true -> 1 

        texts.append([segment[0], segment[1], trans, emotion, screaming, repeating])

        # if screaming -> 1
        # if reapeating -> 1
        # return -> [[start time, end time, transcript, emotion, screaming, repeating], [start time, end time, transcript,..], ..],
        #            scream count
        #            repeat count

        # Delete the WAV file after processing
        os.remove(file)

    return texts, screams, repeats