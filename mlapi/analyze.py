import os
from pyannote.audio import Pipeline
import wave
from transformers import pipeline
import pyaudio
import socket
import threading
from time import sleep
import struct
from datetime import datetime, timedelta
import shutil

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
from reduce_noise import reduce_noise
from sound_classifier import sound_classifier

# this will run in a thread reading audio from the tcp socket and buffering it
buffer = []
buffering = False
record_duration = 20  # Duration in seconds

success = False

def read_audio_from_socket():
    global buffering, buffer, success

    buffer = []
    # connect to the esp32 socket
    sock = socket.socket()

    try:
        sock.connect(("microphone.local", 5001))
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        # Get the start time for the 20-second buffer
        start_time = datetime.now()

        while True:
            
            data = sock.recv(4096)
            if data == b"":
                raise RuntimeError("Lost connection")
            buffer.append(data)

            # Check if 20 seconds have elapsed, and if so, stop buffering
            if (datetime.now() - start_time).total_seconds() >= record_duration:
                break

        success = True
        print("finished recording successfully")
    except:
        print("failed to connect")
        success = False
    finally:
        buffering = False
  

# recording audio from streaming ESP32 device
def record():

    global buffer, buffering, success
    # initiaslise pyaudio
    p = pyaudio.PyAudio()
    # kick off the audio buffering thread

    while True:

        success = False
        
        # Create a thread
        thread = threading.Thread(target=read_audio_from_socket)

        # Save file with the current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        print("started recording")

        # Start the thread
        thread.start()

        # Wait for the thread to finish 
        thread.join()

        if success:
            file_name = f"{current_datetime}.wav"

            process_folder = "process"
            output_folder = "work"  
            
            # Check if folder exists, if not create it
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Check if folder exists, if not create it
            if not os.path.exists(process_folder):
                os.makedirs(process_folder)
        
            file = process_folder + "/" + file_name  # write to wav file in process folder

            # write the buffered audio to a wave file
            with wave.open(file, "wb") as wave_file:
                print("writing file")
                wave_file.setnchannels(1)
                wave_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wave_file.setframerate(44100)
                wave_file.writeframes(b"".join(buffer))
            
            new_file_path = output_folder + "/" + file_name
            shutil.move(file, new_file_path)   # move to work folder for analyzing


#analyze recorded audio files
def analyze():

    while True:
        work_folder = "work"
        file_list = os.listdir(work_folder)

        # Check if folder exists, if not create it
        if not os.path.exists(work_folder):
            os.makedirs(work_folder)

        for file in file_list:

            date = file.split("_")[0]
            time = file.split("_")[1].split(".")[0]
            print("date : ", date)
            print("time : ", time)

            file_name = work_folder + "/" + file

            print(file_name)

            # reducing noise in the file
            reduce_noise(file_name)

            sound = sound_classifier(file_name)

            date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            record_start = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
            print("date time obj : ", record_start)

            if sound == "Speech":

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

                pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0",
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
                write_summary_file(common_segments, patient_metrics, speaker_tags)   

            else:
                print("no speech detected")
                print(f"Sound detected: {sound}")

            # Delete the processed file
            os.remove(file_name)


    