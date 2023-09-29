import os
from datetime import datetime

def write_log_file(common_segments, patient_metrics):

    patient_ids = []
    file_name = ""

    for spk, metric in patient_metrics.items():
        patient_ids.append(spk)
        file_name += spk + "_"

    current_datetime = datetime.now().strftime("%Y-%m-%d")

    #---------------------log file part-------------------------

    log_folder = "logs"
    log_file = file_name + "_" + current_datetime + ".txt"

    lf=open(os.path.join(log_folder, log_file),"wb")

    entry = ""
    
    for segment in common_segments:
        start = segment[0]
        end = segment[1]
        text = segment[2]
        emotion = segment[3]
        screaming = segment[4]
        repeating = segment[5]
        question = segment[6]
        response = segment[7]
        timing = segment[8]
        related = segment[9]
        speaker = segment[11]

        entry += f"{speaker} ({start} : {end}) : {text}\n"
        if emotion != "":
            entry += f"\temotion : {emotion}\n"
        if screaming:
            entry += f"\tscreaming\n"
        if repeating:
            entry += f"\trepeating same word\n"
        if question != "":
            entry += f"\tquestion : {question}\n"
            if response != "":
                entry += f"\tresponse received : {response}\n"
                entry += f"\tresponse delay : {timing}\n"
                
                if related:
                    entry += f"\tresponse is related\n"
                   
                else:
                    entry += f"\tresponse is unrelated\n"
                    
            else:
                entry += f"\tpatient not responding\n"
                

    entry += "\n\n"

    lf.write(bytes(entry.encode('utf-8')))      
    lf.close()
    print("log file written")

    # -------------------------log file end-------------------------
