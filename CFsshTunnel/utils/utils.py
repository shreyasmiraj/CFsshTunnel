import time

def keep_alive(state: bool = True):
    # keeps the server alive?
    while state:
        time.sleep(60)
        continue