from speechbrain.speechbrain.pretrained import SpeakerRecognition
import os
from pydub import AudioSegment
from collections import defaultdict
from name_ID_mapping import ID_details
from sound_classifier import sound_classifier
from scream_detection import scream_detection

verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

voice_folder = "voices"    # this folder act as a voice database

# Check if source_folder exists, if not create it
if not os.path.exists(voice_folder):
    os.makedirs(voice_folder)

voices = os.listdir(voice_folder)

# recognize speaker name
def speaker_recognition(file_name, segments, wildcards, prev_spk):

    Id_count = defaultdict(int)
    # Load the WAV file
    audio = AudioSegment.from_file(file_name, format="wav")

    folder_name = "temp"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    i = 0
    distress_count = 0

    for segment in segments:
        start = segment[0] * 1000   # start time in miliseconds
        end = segment[1] * 1000     # end time in miliseconds
        clip = audio[start:end]
        i = i + 1
        file = folder_name + "/" + file_name.split("/")[-1].split(".")[0] + "_segment"+ str(i) + ".wav"
        clip.export(file, format="wav")

        max_score = 0
        person = "unknown"      # if no match to any voice, then return unknown

        is_screaming = scream_detection(file)
        if is_screaming:
            distress_count += 1

        for voice in voices:
            voice_file = voice_folder + "/" + voice

            print(voice_file)

            # compare voice file with audio file
            score, prediction = verification.verify_files(voice_file, file)
            prediction = prediction[0].item()
            score = score[0].item()

            if prediction == True:
                if score >= max_score:
                    max_score = score
                    speakerId = voice.split(".")[0]  
                    if speakerId not in wildcards:        # speaker_00 cannot be speaker_01
                        person = speakerId

        Id_count[person] += 1

        # Delete the WAV file after processing
        os.remove(file)
    
    most_common_Id = max(Id_count, key=Id_count.get)
    if most_common_Id == "unknown" and distress_count > 0 and prev_spk != "" and prev_spk != "unknown":
        for id, details in ID_details.items():
            if details["name"] == prev_spk:
                most_common_Id = id
        person_details = ID_details[most_common_Id]
    elif most_common_Id == "unknown":
        person_details = {"name": "unknown", "type": "patient"}
    else:
        person_details = ID_details[most_common_Id]
        
    return person_details

