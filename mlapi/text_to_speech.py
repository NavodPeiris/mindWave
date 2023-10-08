import socket
from hf_access import ACCESS_TOKEN
import os

from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import soundfile as sf

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
    sf.write("alice/buwa.wav", wav, rate)

text_to_speech("On October 4th, 2023, patient Buwaneka's mood was neutral. They did not scream or repeat any words during the day. Their average response time was 2.70 seconds, and they did not respond at all 0 times. They gave one related answer and zero unrelated answers.")
