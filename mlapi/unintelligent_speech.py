from is_question import is_question
from is_related import is_related
from google_trans import translate_sinhala_to_english

# additional flags segment[6] -> question, segment[7] -> response, segment[8] -> timing, segment[9] -> related (1/0)
def unintelligent_speech(speakers, speaker_map, doctors, patients):

    edited_speakers = speakers

    for spk_tag, spk_segments in edited_speakers.items():
        spk = speaker_map[spk_tag]
        if spk in doctors:    
            for doc_segment in spk_segments:
                doc_segment.append("")                  # segment[6] -> question
                doc_segment.append("")                  # segment[7] -> response default empty
                doc_segment.append("")                  # segment[8] -> timing default empty
                doc_segment.append("")                  # segment[9] -> related default empty
                doc_segment.append("")                  # segment[10] -> question asked from who    
        else:
            for pat_segment in spk_segments:
                pat_segment.append("")                  # not used
                pat_segment.append("")                  # not used
                pat_segment.append("")                  # not used
                pat_segment.append("")                  # not used
                pat_segment.append("")                  # not used
    
    for spk_tag, spk_segments in edited_speakers.items():
        print(f"{spk_tag} : {spk_segments}")

    if len(patients) > 0:         # if no patients in audio can't look for answers

        for spk_tag, spk_segments in edited_speakers.items():
            answering = {}      # answering patient and answer time value
            spk = speaker_map[spk_tag]
            if spk in doctors:
                for doc_segment in spk_segments:
                    text = doc_segment[2]
                    if ("බෙහෙත්" in text) and ("බිව්වද" in text or "ගත්තද" in text or "බිව්වා ද" in text or "බිව්වාද" in text) :
                        english_text = "Have you taken medicine?"
                    elif ("කෑම" in text) and ("කෑවද" in text or "කාලාද" in text or "කාලද" in text or "ගත්තද" in text) :
                        english_text = "did you eat?"
                    elif ("නිදාගත්තද" in text or "නිදගත්තාද" in text or "නිදාගත්තාද" in text or "නින්ද ගියාද" in text):
                        english_text = "did you sleep?"
                    elif ("කොහොමද" in text):
                        english_text = "how do you feel now?"
                    elif ("සනීපද" in text):
                        english_text = "are you well now?"
                    else:
                        english_text = translate_sinhala_to_english(text)

                    q = is_question(english_text)
                    print(q)
                    if 'True' in q:
                        question = english_text
                        q_end = doc_segment[1]   # question ending time
                        answer = ""
                        time_to_answer = 0
                        doc_segment[6] = question

                        for spk_tag, spk_segments in edited_speakers.items():
                            spk = speaker_map[spk_tag]
                            if spk in patients:
                                for pat_segment in spk_segments:
                                    a_start = pat_segment[0]   # answer start time (should be after question)
                                    if a_start >= q_end:
                                        answering[spk_tag] = a_start
                                        break
                        
                        if len(answering) > 0:
                            # patient who answer first is actually answering the question
                            answering_patient = min(answering, key=answering.get)
                            ans_time = answering[answering_patient]
                            pat_name = speaker_map[answering_patient]

                            doc_segment[10] = pat_name

                            pat_segments = edited_speakers[answering_patient]

                            for pat_segment in pat_segments:
                                if pat_segment[0] == ans_time:
                                    si_answer = pat_segment[2]     # sinhala answer
                                    answer = translate_sinhala_to_english(si_answer)   # english answer
                                    time_to_answer = ans_time - q_end
                                    doc_segment[7] = answer
                                    doc_segment[8] = time_to_answer

                                    r = is_related(question, answer)
                                    print(r)

                                    if 'True' in r:
                                        # patient give a related answer
                                        doc_segment[9] = 1
                                        break
                                    else:
                                        # patient give unrelated answer
                                        doc_segment[9] = 0
                                        break
                        
                        # if no answer was found then answer flag will be empty

    return edited_speakers
