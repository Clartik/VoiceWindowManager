from RealtimeSTT import AudioToTextRecorder

def on_update(text):
    print("Live:", text)

if __name__ == "__main__":
    recorder = AudioToTextRecorder()
    
    print("\nPress Esc to exit.\n")

    while True:
        print("Final:", recorder.text())

