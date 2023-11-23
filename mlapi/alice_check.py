from english_transcribe import eng_transcribe
from document_query import document_query
from text_to_speech import text_to_speech

def alice_check(file):
    # get english transcription
    eng_trans = eng_transcribe(file)
    print("English translation : ", eng_trans)

    # check if "alice" utterance is there
    # sometimes "alice" is detected as "at least or At least"
    if "alice" in eng_trans or "Alice" in eng_trans or "Adis" in eng_trans or "Addis" in eng_trans or "At least" in eng_trans or "at least" in eng_trans or "patient number" in eng_trans:
        # Remove "Alice" or "alice" from the text
        eng_trans = eng_trans.replace("Alice", "").replace("alice", "").replace("At least", "").replace("at least", "")
        print("Question for alice: ", eng_trans)
        alice_res = document_query(eng_trans)
        text_to_speech(alice_res)