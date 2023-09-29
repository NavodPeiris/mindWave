from analyze import record, analyze
import threading

threading.Thread(target=record).start()  # record sound independently
threading.Thread(target=analyze).start() # process recorded files independently
