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

from test import core_analysis

from scream_detection import scream_detection

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
        shutil.move(file, new_file_path)   # copy to work folder for analyzing     

#analyze recorded audio files
def analyze():

    work_folder = "work"

    # Check if folder exists, if not create it
    if not os.path.exists(work_folder):
        os.makedirs(work_folder)
    
    file_list = os.listdir(work_folder)

    for file in file_list:

        date = file.split("_")[0]
        time = file.split("_")[1].split(".")[0]
        print("date : ", date)
        print("time : ", time)

        file_name = work_folder + "/" + file

        print(file_name)

        # reducing noise in the file
        reduce_noise(file_name)

        core_analysis(file_name)

        # Delete the processed file
        os.remove(file_name)


# for testing with streaming device
record()
analyze()
    