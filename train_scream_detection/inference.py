import numpy as np
import librosa
import tensorflow as tf

# Load the saved model
loaded_model = tf.keras.models.load_model("scream_detection_model.h5")

# Define function to extract features from audio signal
def extract_features(file_path, max_pad_len=500):
    X, sample_rate = librosa.load(file_path)
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
    spectrogram = librosa.amplitude_to_db(np.abs(librosa.stft(X)), ref=np.max)
    pad_width = max_pad_len - mfccs.shape[1]
    pad_width1 = max_pad_len - spectrogram.shape[1] 
    if pad_width < 0:
        mfccs = mfccs[:, :max_pad_len]
        spectrogram = spectrogram[:, :max_pad_len]
    else:
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        spectrogram = np.pad(spectrogram, pad_width=((0, 0), (0, pad_width)), mode='constant')
    combined_features = np.concatenate((mfccs.flatten(), spectrogram.flatten()))
    return combined_features


# use the loaded model for inference
new_file_path = "test/girl_scream.wav"
features = extract_features(new_file_path)
prediction = loaded_model.predict(np.expand_dims(features, axis=0))

if prediction > 0.5:
    print("Scream detected")
else:
    print("No scream detected")
