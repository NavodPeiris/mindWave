from analyze import record, analyze
from alice_stream import run_alice_stream
import threading

threading.Thread(target=record).start()  # record sound independently
threading.Thread(target=analyze).start() # process recorded files independently
threading.Thread(target=run_alice_stream).start()   # running alice server
