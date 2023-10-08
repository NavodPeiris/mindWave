import socket
import time
from hf_access import ACCESS_TOKEN
import os

from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import soundfile as sf
import librosa

models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
    "facebook/fastspeech2-en-ljspeech",
    arg_overrides={"vocoder": "hifigan", "fp16": False}
)
model = models[0]
TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
generator = task.build_generator([model], cfg)

def text_to_speech(text):

    alice_folder = "alice"

    # Check if folder exists, if not create it
    if not os.path.exists(alice_folder):
        os.makedirs(alice_folder)

    sample = TTSHubInterface.get_model_input(task, text)
    wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)

    # Save the audio as a WAV file
    sf.write("alice/response.mp3", wav, rate)

    # Load the audio file
    y, sr = librosa.load("alice/response.mp3")

    # Get the duration in seconds
    duration = librosa.get_duration(y=y, sr=sr)

    print(f"The duration of the audio file is {duration:.2f} seconds.")

    # send the text to esp32
    send_to_ESP32(text, duration)


def send_to_ESP32(message, duration):
    # connect to the esp32 socket
    sock = socket.socket()

    try:
        sock.connect(("microphone.local", 5002))
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        # Send the message
        sock.sendall(message.encode('utf-8'))

        # response from ESP32
        response = sock.recv(1024)
        print("Received from ESP32:", response.decode('utf-8'))
        
    except Exception as e:
        print(f"Failed to connect or send message: {e}")
    
    time.sleep(duration)

    sock.close()

text_to_speech("On October 4th, 2023, patient Buwaneka's mood was neutral. They did not scream or repeat any words during the day. Their average response time was 2.70 seconds, and they did not respond at all 0 times. They gave one related answer and zero unrelated answers.")
