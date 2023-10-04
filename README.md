# MindWave 

this is a project that focus on detecting symptoms of mental health patients through analyzing voice data.

We use an ESP32 as the audio streaming device.

clone this repo and make sure **path of project folder contain no spaces!!**

**if spaces are in path. errors will occur**

run this project in vscode

open vscode as Administrator

**vscode may need to be run as Administartor for tasks to be done uninterrupted manner** 

1. running Firmware part

- first install drivers for communication between PC and ESP32. without these drivers you will not be able to upload the firmware to ESP32.

 - driver link - https://www.silabs.com/documents/public/software/CP210x_Universal_Windows_Driver.zip

 - extract and save to a folder

 - connect ESp32 and select the relevent COM port on device Manager and click "Update driver"

 - next select "browse my computer for drivers"

 - give path to folder that you extracted your driver.

 - now driver will be installed

- install PlatformIO extension in vscode

- cd firmware

- upload to an ESP32 device via USB

- wait until upload finishes

- press reset button on ESP32

- on PC search wifi Access point called **"MindWave_testing"**. click on it and choose wifi router you want ESP32 to connect to. enter the password for router.

- now ESP32 will connect to that wifi router

- make sure both PC and ESP32 is connected to same Wifi router

2. Python app part

- cd mlapi

- create a virtual environment
 - python -m venv venv

- activate virtual environment
 - venv/Scripts/activate
 - if activated it shows -> (venv) alongside path in terminal

- install requirements by running following commands:
 - pip install -r requirements.txt

- pip install googletrans==4.0.0-rc1

- pip install https://github.com/marianne-m/brouhaha-vad/archive/main.zip

- clone speechbrain repo and prepare speechbrain:
 - git clone https://github.com/speechbrain/speechbrain.git
 - cd speechbrain
 - pip install -r requirements.txt
 - pip install --editable .

download required llama2 model from:
- https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q4_0.bin
- store downloaded llama2 model into a folder named "llama2" inside mlapi

3. before running python app make sure PC user account have write permissions to "C:" and "D:" drives.

4. run main.py
 - python main.py

