from flask import Flask, Response
import os

app = Flask(__name__)

@app.route('/audio.mp3')
def audio():
    alice_folder = "alice"

    # Check if folder exists, if not create it
    if not os.path.exists(alice_folder):
        os.makedirs(alice_folder)
    
    file_list = os.listdir(alice_folder)

    def generate():
        #for file in file_list:
        #    file = alice_folder + "/" + file
        file = "about_buwa.mp3"
        with open(file, 'rb') as audio_file:
            data = audio_file.read(4096)
            while data:
                yield data
                data = audio_file.read(4096)

    return Response(generate(), mimetype='audio/mp3')

app.run(debug=True, host='0.0.0.0', port=5001)