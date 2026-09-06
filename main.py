from RealtimeSTT import AudioToTextRecorder
from typing import Optional

from intents import parse_intent
from window import WindowsManager
from primitives import *

import sys
    
def check_input_for_confirmation(input: str) -> Optional[bool]:
    """
    Checks if the input can confirm/deny the confirmation
    
    :param input: The user input
    :type input: str
    
    :returns: True if confirmation is confirmed, False if confirmation is denied, None if input ignores confirmation/moves to new command
    :rtype: Optional[bool]
    """
    
    for case in YES_WORD_CASES:
        if case not in input.lower():
            continue
        
        return True
        
    for case in NO_WORD_CASES:
        if case not in input.lower():
            continue
        
        return False
    
    # When input ignores confirmation and goes to a new command or such
    return None

class VoiceAgent:
    def __init__(self):
        self.recorder = AudioToTextRecorder(language='en', model='small', device='cuda', beam_size=5)
        
        self.is_running: bool = True
        
        self.current_action: Optional[Action] = None
        self.last_action: Optional[Action] = None
        
    def get_user_input(self) -> str:
        input = self.recorder.text()
        print('[User]:', input)
            
        return input
        
    def cleanup_action(self):        
        self.last_action = self.current_action
        self.current_action = None
        
    def start(self):
        print("\nSay 'Exit' to stop.\n")
        
        while self.is_running:
            input = self.get_user_input()
            
            if self.current_action and self.current_action.confirmation and self.current_action.confirmation.is_waiting:
                # If none, new command is being awaited so cleanup
                ret = check_input_for_confirmation(input)
                
                if ret is not None:
                    self.current_action.confirmation.is_confirmed = ret
                    
                    self.execute_action()
                    self.cleanup_action()
                    continue
                else:
                    self.cleanup_action()
                
            intent = parse_intent(input)
            print(intent)
            
            self.current_action = Action(input, intent)

            self.execute_action()
            self.cleanup_action()
    
    def execute_action(self): 
        if not self.current_action:
            return
        
        intent = self.current_action.intent
        
        if intent.action == 'exit':
            print("Exiting program...")
            self.cleanup_action()
            
            sys.exit(0)
            
        elif intent.action == 'close':
            if self.current_action.confirmation and self.current_action.confirmation.is_waiting:
                if self.current_action.confirmation.is_confirmed:
                    assert self.current_action.window is not None
                    WindowsManager.confirm_close(self.current_action.window)
                    
                    return
            else:
                window = WindowsManager.close(intent)
                
                if window is not None:
                    print(f'[WindowManager]: Are you sure you want to close "{window.title}" window?')
                    
                    self.current_action.window = window
                    self.current_action.is_awaiting_confirmation = True
        
        elif intent.action == 'restore':
            WindowsManager.restore(intent, self.last_action)
        
        elif intent.action == 'dock':
            if intent.position == 'empty':
                self.current_action.window = WindowsManager.minimize(intent, self.last_action)

            elif intent.position == 'full':
                self.current_action.window = WindowsManager.maximize(intent, self.last_action)

            elif intent.position == 'none':
                return

            WindowsManager.dock(intent)


        
if __name__ == "__main__":    
    agent = VoiceAgent()
    agent.start()