from google.cloud import speech

# google cloud speech-to-text API V1 client
speechClientV1 = speech.SpeechClient.from_service_account_file("key.json")

# accurate 
def sinhala_transcription(file_name):
    # google cloud speech to text

    # Reads a file as bytes
    with open(file_name, "rb") as f:
        content = f.read()

    audio_file = speech.RecognitionAudio(content=content)

    # sinhala = si-LK
    # english = en-US

    config = speech.RecognitionConfig(
        #sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code='si-LK',
        audio_channel_count=1
    )

    # Transcribes the audio into text
    response = speechClientV1.recognize(
        config=config,
        audio=audio_file
    )

    transcript=""

    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript

def english_transcription(file_name):
    # google cloud speech to text

    # Reads a file as bytes
    with open(file_name, "rb") as f:
        content = f.read()

    audio_file = speech.RecognitionAudio(content=content)

    # sinhala = si-LK
    # english = en-US

    config = speech.RecognitionConfig(
        #sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code='en-US',
        audio_channel_count=1
    )

    # Transcribes the audio into text
    response = speechClientV1.recognize(
        config=config,
        audio=audio_file
    )

    transcript=""

    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript