import librosa
import librosa.display
import soundfile as sf

# Define the input and output file paths
input_file = 'mama_navod.wav'
output_file = 'output_16k.wav'

def resampler(file):
    # Load the audio file
    y, sr = librosa.load(file, sr=16000)

    # Save the resampled audio
    sf.write(file, y, sr)
