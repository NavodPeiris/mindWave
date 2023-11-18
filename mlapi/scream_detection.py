import torch
from ModelEval import process_file

model = torch.load('scream_detection_models/Resnet34_Model_2023-10-13--17-11-18.pt', map_location=torch.device('cpu'))

def scream_detection(filename):
    evaluation_result = process_file(filename, model)

    # Convert NumPy boolean to Python boolean
    evaluation_result = bool(evaluation_result)

    print(f"scream detected = {evaluation_result}")

    return evaluation_result

'''
scream_detection("recorded_samples/buwaneka_2760YmUD.wav")
'''