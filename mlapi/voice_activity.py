from pyannote.audio import Model
from hf_access import ACCESS_TOKEN
from pyannote.audio import Inference

model = Model.from_pretrained("pyannote/brouhaha", 
                              use_auth_token=ACCESS_TOKEN)


def voice_activity(file):
    inference = Inference(model)
    output = inference(file)

    # iterate over each frame
    for frame, (vad, snr, c50) in output:
        t = frame.middle
        print(f"{t:8.3f} vad={100*vad:.0f}% snr={snr:.0f} c50={c50:.0f}")
        if vad >= 0.3:
            return True
    return True
