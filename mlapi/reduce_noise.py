from scipy.io import wavfile
import noisereduce as nr

def reduce_noise(file_name):
    # load data
    rate, data = wavfile.read(file_name)
    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(file_name, rate, reduced_noise)

'''
# load data
rate, data = wavfile.read("examples/yasan.wav")
# perform noise reduction
reduced_noise = nr.reduce_noise(y=data, sr=rate)
wavfile.write("mywav_reduced_noise.wav", rate, reduced_noise)
'''