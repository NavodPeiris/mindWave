import os
from pyannote.audio import Pipeline
from datetime import datetime, timedelta

from hf_access import ACCESS_TOKEN
from bandpass_filter import bandpass_filter
from wav_segmenter import wav_file_segmentation_doc, wav_file_segmentation_patient
from unintelligent_speech import unintelligent_speech
from speaker_recognition import speaker_recognition
from voice_activity import voice_activity
from re_encode import re_encode
from convert_to_mono import convert_to_mono
from write_log_file import write_log_file
from write_summary_file import write_summary_file

from sound_classifier import sound_classifier
from scream_detection import scream_detection

'''
recorded_samples/buwaneka_scream.wav
recorded_samples/alice_quest.wav
examples/kawada_kawa_beheth_biwwada_kawe_na.wav
examples/repeat/sorry_repeated.wav
'''

file_name = "examples/kawada_kawa_beheth_biwwada_kawe_na.wav"

voice_detected = voice_activity(file_name)

is_screaming = scream_detection(file_name)

date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
record_start = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
print("date time obj : ", record_start)

if voice_detected:

    # <-------------------Processing file-------------------------->

    # apply bandpass filter
    #file_name = bandpass_filter(file_name)  

    # check if file has more than 1 channels and convert it to mono
    convert_to_mono(file_name)

    # normally wav files has Linear PCM encoding
    # if wav file is not having 16-bit PCM encoding, make it 16 bit
    # because if it is 8-bit then it will not work with google speech-to-text
    re_encode(file_name)


    speaker_tags = []

    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token=ACCESS_TOKEN)

    diarization = pipeline(file_name, min_speakers=0, max_speakers=10)

    doctors = []
    patients = []
    speakers = {}

    common = []

    # create a dictionary of SPEAKER_XX to real name mappings
    speaker_map = {}

    for turn, _, speaker in diarization.itertracks(yield_label=True):

        start = round(turn.start, 1)
        end = round(turn.end, 1)
        common.append([start, end, speaker])

        # find different speakers
        if speaker not in speaker_tags:
            speaker_tags.append(speaker)
            speakers[speaker] = []

        print(f"start={start}s stop={end}s speaker_{speaker}")

        speakers[speaker].append([start, end, speaker])

        
            
    '''
    print("commons : \n\n")
    for item in common:
        start = item[0]
        end = item[1]
        speaker = item[2]
        print(f"start={start}s stop={end}s speaker_{speaker}")

    print("docs : \n\n")
    for doc in doctor:
        start = doc[0]
        end = doc[1]
        print(f"start={start}s stop={end}s speaker_SPEAKER_00")

    print("patients : \n\n")
    for pat in patient:
        start = pat[0]
        end = pat[1]
        print(f"start={start}s stop={end}s speaker_SPEAKER_01")
    '''

    identified = []
    prev_spk = ""

    for spk_tag, spk_segments in speakers.items():
        spk_details = speaker_recognition(file_name, spk_segments, identified, prev_spk)
        spk = spk_details["name"]
        identified.append(spk)
        speaker_map[spk_tag] = spk
        print(f"{spk_tag} is {spk}")
        if spk_details["type"] == "doctor":
            print(f"speaker {spk} is a doctor")
            if spk not in doctors:
                doctors.append(spk)
        else:
            print(f"speaker {spk} is a patient")
            if spk not in patients:
                patients.append(spk)

        if spk in patients:
            prev_spk = spk

    print(f"before : {speaker_map}")

    keys_to_remove = []
    merged = []

    # merging same speakers
    for spk_tag1, spk_segments1 in speakers.items():
        for spk_tag2, spk_segments2 in speakers.items():
            if spk_tag1 not in merged and spk_tag2 not in merged and spk_tag1 != spk_tag2 and speaker_map[spk_tag1] == speaker_map[spk_tag2]:
                for segment in spk_segments2:
                    speakers[spk_tag1].append(segment)

                merged.append(spk_tag1)
                merged.append(spk_tag2)
                keys_to_remove.append(spk_tag2)
    
    # fixing the speaker names in common
    for segment in common:
        speaker = segment[2]
        segment[2] = speaker_map[speaker]

    for key in keys_to_remove:
        print(f"removing {key}")
        del speakers[key]
        del speaker_map[key]

    print(f"after : {speaker_map}")

    patient_metrics = {}        # contain counts of screams and repeats

    # transcribing the texts differently according to speaker
    for spk_tag, spk_segments in speakers.items():
        spk = speaker_map[spk_tag]
        if spk in doctors:
            doctor_segment = wav_file_segmentation_doc(file_name, spk_segments)
            speakers[spk_tag] = doctor_segment
        else:
            details = wav_file_segmentation_patient(file_name, spk_segments)
            patient_segment = details[0]
            speakers[spk_tag] = patient_segment
            distress_count = details[1]
            repeats = details[2]
            metric = [distress_count, repeats]
            patient_metrics[spk] = metric
            

    # detect unintelligent speech 
    speakers = unintelligent_speech(speakers, speaker_map, doctors, patients)

    common_segments = []

    for item in common:
        speaker = item[2]
        start = item[0]
        end = item[1]

        for spk_tag, spk_segments in speakers.items():
            if speaker == speaker_map[spk_tag]:
                for segment in spk_segments:
                    if start == segment[0] and end == segment[1]:
                        newStart = record_start + timedelta(seconds=int(segment[0]))  # adding start time  
                        newEnd = record_start + timedelta(seconds=int(segment[1]))    # adding end time
                        newStart = newStart.strftime("%Y-%m-%d_%H-%M-%S")            # start object
                        newEnd = newEnd.strftime("%Y-%m-%d_%H-%M-%S")                # end object
                        start_time = newStart.split("_")[1].split(".")[0]            # start time
                        end_time = newEnd.split("_")[1].split(".")[0]                # end time
                        common_segments.append([start_time, end_time, segment[2], segment[3], segment[4], segment[5], segment[6], segment[7], segment[8], segment[9], segment[10], speaker])

        
    for item in common_segments:
        start = item[0]
        end = item[1]
        text = item[2]
        print(f"start={start}s stop={end}s text={text}")

    # writing log file
    write_log_file(common_segments, patient_metrics)  

    # write summary file
    write_summary_file(common_segments, patient_metrics, speaker_tags, is_screaming)   

else:
    print("no speech detected")
    