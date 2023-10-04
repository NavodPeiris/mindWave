import librosa
import librosa.display
import soundfile as sf

# Define the input and output file paths
input_file = 'noise.wav'
output_file = 'output_16k.wav'

# Load the audio file
y, sr = librosa.load(input_file, sr=16000)

# Save the resampled audio
sf.write(output_file, y, sr)
