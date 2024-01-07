from transformers import pipeline

import sys

pipe = pipeline("automatic-speech-recognition", model="Ransaka/whisper-tiny-sinhala-20k-8k-steps-v2")

def whisper_sinhala(file):
    res = pipe(file)
    return res["text"]


def process_file(file_name):
    try:
        res = whisper_sinhala(file_name)
        return res
    except FileNotFoundError:
        return "File not found or could not be opened"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python whisper_sinhala.py <file_name>")
    else:
        file_name = sys.argv[1]
        processed_text = process_file(file_name)
        #print(processed_text)
        res = processed_text.encode('utf-8')
        sys.stdout.buffer.write(res)
        sys.stdout.flush() 


'''
res = whisper_sinhala("doctor/segment1.wav")
print(res)
'''