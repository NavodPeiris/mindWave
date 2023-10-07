import socket
from hf_access import ACCESS_TOKEN
import os
import scipy

from transformers import AutoProcessor, AutoModel

processor = AutoProcessor.from_pretrained("suno/bark")
model = AutoModel.from_pretrained("suno/bark")

def text_to_speech(text):

    alice_folder = "alice"

    # Check if folder exists, if not create it
    if not os.path.exists(alice_folder):
        os.makedirs(alice_folder)

    inputs = processor(
        text=[text],
        return_tensors="pt",
    )

    speech_values = model.generate(**inputs, do_sample=True)

    sampling_rate = model.config.sample_rate
    scipy.io.wavfile.write("alice/bark_out.wav", rate=sampling_rate, data=speech_values.cpu().numpy().squeeze())
