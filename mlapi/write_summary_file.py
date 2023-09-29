import os
from datetime import datetime

def write_summary_file(common_segments, patient_metrics, speaker_tags):

    current_datetime = datetime.now().strftime("%Y-%m-%d")

    # -------------------------summary file part-----------------------

    summary_folder = "summaries"

    for spk, metric in patient_metrics.items():
        moods = []
        delays = []
        no_reponses = 0
        related_responses = 0
        unrelated_responses = 0
        average_response_delay = 0

        for segment in common_segments:
            emotion = segment[3]
            question = segment[6]
            response = segment[7]
            timing = segment[8]
            related = segment[9]
            askedFrom = segment[10]
            speaker = segment[11]

            if speaker == spk:
                if emotion != "":
                    if emotion not in moods:
                        moods.append(emotion)

            if askedFrom == spk:
                if question != "":
                    if response != "":
                        delays.append(timing)
                        if related:
                            related_responses += 1
                        else:
                            unrelated_responses += 1
                    else:
                        no_reponses += 1
            
        if len(delays) > 0:
            average_response_delay = sum(delays) / len(delays)

        screams = metric[0]
        repeats = metric[1]

        summary_file = spk + "_" + current_datetime + ".txt"

        sf=open(os.path.join(summary_folder, summary_file),"wb")
        
        s_entry = f"patient: {spk}\ndate: {current_datetime}\n\n"
        s_entry += "summary:\n"
        # conversation or a monologue
        if len(speaker_tags) > 1:
            s_entry += "conversation\n"
        elif len(speaker_tags) == 1:
            s_entry += "monologue\n"
        else:
            s_entry += "no speech\n"
        s_entry += "list of moods patient had during day: "

        for mood in moods:
            s_entry += f"{mood}, "
        s_entry += "\n"
        s_entry += f"number of times patient screamed during day: {screams}\n"
        s_entry += f"number of times patient repeated same word during day: {repeats}\n"
        s_entry += f"average response time: {average_response_delay} seconds\n"
        s_entry += f"number of times where patient did not respond: {no_reponses}\n"
        s_entry += f"number of times where patient give a related answer: {related_responses}\n"
        s_entry += f"number of times where patient give an unrelated answer: {unrelated_responses}\n"

        sf.write(bytes(s_entry.encode('utf-8')))
        sf.close()
        print("summary file written")

    #-------------------------summary file end-------------------------