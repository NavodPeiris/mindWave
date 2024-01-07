import subprocess
import sys

# Path to the Python script to execute
script_path = "whisper_sinhala.py"

file_path = "doctor/segment1.wav"

try:
    # Run the test.py script in a subprocess and pass voice.wav as an argument
    result = subprocess.Popen([sys.executable, script_path, file_path], stdout=subprocess.PIPE)
    processed_text = result.stdout.read() 
    res = processed_text.decode('utf-8')
    print("Received processed text:", res)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
