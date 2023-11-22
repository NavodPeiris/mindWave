# MindWave Project Setup Guide

The MindWave project focuses on detecting symptoms of mental health patients through the analysis of voice data. To get started with this project, follow these step-by-step instructions for setting up and running it in Visual Studio Code (VSCode).

**Note: Ensure that the path to the project folder contains no spaces, as spaces in the path can lead to errors. Also, run VSCode as an Administrator for uninterrupted task execution.**

## 1. Running Firmware Part

### 1.1 Install Communication Drivers

- Download the communication drivers for ESP32:
  - Driver Link: [CP210x Universal Windows Driver](https://www.silabs.com/documents/public/software/CP210x_Universal_Windows_Driver.zip)
  - Extract and save the drivers to a folder.

- Connect the ESP32 device to your PC and open the Device Manager.
- Select the relevant COM port for the ESP32 and click "Update driver."
- Choose "Browse my computer for drivers" and provide the path to the folder where you extracted the drivers.
- The driver installation will be completed.

### 1.2 Install PlatformIO Extension in VSCode

- Install the PlatformIO extension in Visual Studio Code.

### 1.3 Upload Firmware to ESP32

- Open VSCode.
- Navigate to the `firmware` directory.
- Upload the firmware to the ESP32 device via USB.
- Wait until the upload finishes.
- Press the reset button on the ESP32.

### 1.4 Connect ESP32 to Wi-Fi

- On your PC, search for a Wi-Fi Access Point named **"MindWave_testing."**
- Click on it and choose the Wi-Fi router you want the ESP32 to connect to.
- Enter the router's password.
- The ESP32 will now connect to the selected Wi-Fi router.

### 1.5 Verify Connectivity

- Make sure both your PC and the ESP32 are connected to the same Wi-Fi router.

## 2. Python App Part

### use python 3.9.0 
### use latest pip version (or upgrade pip)

### install Microsoft visual studio with C++ development. Ensure you install this as it is a dependency of a package called 'fairseq'.

### 2.1 Set Up Python Environment

- Navigate to the `mlapi` directory.

- Create a virtual environment:
    - python -m venv venv


- Activate the virtual environment:
    - venv/Scripts/activate


- If activated successfully, you will see `(venv)` alongside the path in the terminal.

### 2.2 Install Required Dependencies

- Install the project's Python dependencies by running the following commands:
    - pip install -r requirements.txt
    - pip install googletrans==4.0.0-rc1
    - pip install https://github.com/marianne-m/brouhaha-vad/archive/main.zip

- Clone the SpeechBrain repository and prepare SpeechBrain:

    - git clone https://github.com/speechbrain/speechbrain.git
    - cd speechbrain
    - pip install -r requirements.txt
    - pip install --editable .

- Download the required Llama2 model from:
[Llama-2-7B-Chat-GGML Model](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q4_0.bin)
- Store the downloaded Llama2 model into a folder named "llama2" inside the `mlapi` directory.

- Download scream detection model from following URL: 
- place the scream_detection_model.h5 in a folder called "scream_detection_models" inside the mlapi directory

### 2.3 Permissions Setup

- Before running the Python app, ensure that your PC user account has write permissions to the "C:" and "D:" drives.

## 3. Running the Python App in Production (if streaming device available)
- Run the `alice_stream.py` for running server for `alice`

    - python alice_stream.py

- in a different terminal, Run the `main.py` script to run recording and analyzing:

    - python main.py

## 4. Running the Python App in test mode (using recorded files)
- Run the `test.py` with any audio file as input

Now, you have successfully set up and run the MindWave project for detecting symptoms of mental health patients through voice data analysis.

**Note:** Always run VSCode as an Administrator to avoid any interruptions during the execution of tasks.

Enjoy using MindWave to make a positive impact on mental health!
