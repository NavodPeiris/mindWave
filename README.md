# MindWave 

this is a project that focus on detecting symptoms of mental health patients through analyzing voice data.

clone speechbrain repo and prepare speechbrain:
 - git clone https://github.com/speechbrain/speechbrain.git
 - cd speechbrain
 - pip install -r requirements.txt
 - pip install --editable .

install requirements by running following commands:
 - cd mlapi
 - pip install -r requirements.txt

download required llama2 model from:
- https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q4_0.bin
- store downloaded llama2 model into a folder named "llama2"