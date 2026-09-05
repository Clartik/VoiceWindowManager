from RealtimeSTT import AudioToTextRecorder

import pywinctl as pwc

def execute_command(command: str):
    command = command.lower()
    
    if 'exit' in command:
        print("Exiting program...")
        exit()
        
    if 'find' in command:
        window = pwc.getWindowsWithTitle()

if __name__ == "__main__":
    recorder = AudioToTextRecorder()

    print("\nSay 'Exit' to stop.\n")

    last_command = ''

    while True:
        last_command = recorder.text()
        print("[User]:", last_command)
        
        if 'exit' in last_command.lower():
            break
    