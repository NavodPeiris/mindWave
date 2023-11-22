import os
from pydub import AudioSegment
from google_transcription import sinhala_transcription, english_transcription

from emotion_recognition import emotion_recognition
from scream_detection import scream_detection
from repeat_detection import is_repeating
from document_query import document_query
from text_to_speech import text_to_speech
from english_transcribe import eng_transcribe
from scream_detection import scream_detection

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

        emotion = ""

        start = segment[0] * 1000   # start time in miliseconds
        end = segment[1] * 1000     # end time in miliseconds
        clip = audio[start:end]
        i = i + 1
        file = folder_name + "/" + "segment"+ str(i) + ".wav"
        clip.export(file, format="wav")
        trans = sinhala_transcription(file)  # get sinhala transcription

        print(trans)

        # get english transcription
        eng_trans = eng_transcribe(file)
        print("English translation : ", eng_trans)

        texts.append([segment[0], segment[1], trans, emotion, 0, 0])
        
        # check if "alice" utterance is there
        # sometimes "alice" is detected as "at least or At least"
        if "alice" in eng_trans or "Alice" in eng_trans or "Adis" in eng_trans or "Addis" in eng_trans or "At least" in eng_trans or "at least" in eng_trans or "patient number" in eng_trans:
            # Remove "Alice" or "alice" from the text
            eng_trans = eng_trans.replace("Alice", "").replace("alice", "").replace("At least", "").replace("at least", "")
            print("Question for alice: ", eng_trans)
            alice_res = document_query(eng_trans)
            text_to_speech(alice_res)

        # return -> [[start time, end time, transcript, emotion, distress, repeating], [start time, end time, transcript,..], ..],

        # Delete the WAV file after processing
        os.remove(file)

    return texts



# segment according to speaker
def wav_file_segmentation_patient(file_name, segments):

    # Load the WAV file
    audio = AudioSegment.from_file(file_name, format="wav")

    texts = []
    
    distress_count = 0
    repetitions = 0

    folder_name = "patient"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    i = 0

    for segment in segments:

        emotion = ""

        start = segment[0] * 1000   # start time in miliseconds
        end = segment[1] * 1000     # end time in miliseconds
        clip = audio[start:end]
        i = i + 1
        file = folder_name + "/" + "segment"+ str(i) + ".wav"
        clip.export(file, format="wav")
        trans = sinhala_transcription(file)  # get sinhala transcription

        is_screaming = scream_detection(file)
        reps = is_repeating(trans)
        
        # emotion recognition only works is there is speech
        if not is_screaming: 
            emotion = emotion_recognition(file)
        
        distress = 0   # if distressed or not
        repeating = 0

        if is_screaming:
            distress = 1
            distress_count += 1
    
        if reps > 0:
            repeating = 1
            repetitions += reps
        
        texts.append([segment[0], segment[1], trans, emotion, distress, repeating])

        # return -> [[start time, end time, transcript, emotion, distress, repeating], [start time, end time, transcript,..], ..],
        #            scream count
        #            repeat count

        # Delete the WAV file after processing
        os.remove(file)

    return texts, distress_count, repetitions