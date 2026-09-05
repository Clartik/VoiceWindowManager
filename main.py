from RealtimeSTT import AudioToTextRecorder
from intent import parse_intent, WindowIntent

import pywinctl as pwc

import sys

def execute_intent(intent: WindowIntent):    
    if intent.action == 'exit':
        print("Exiting program...")
        sys.exit(0)

if __name__ == "__main__":
    recorder = AudioToTextRecorder()

    print("\nSay 'Exit' to stop.\n")

    user_input = ''

    while True:
        user_input = recorder.text()
        print("[User]:", user_input)
        
        intent = parse_intent(user_input)
        execute_intent(intent)
    