from RealtimeSTT import AudioToTextRecorder

from intents import parse_intent, WindowIntent
from window import WindowsManager

import sys

YES_WORD_CASES = ['yes', 'yep', 'yeah', 'sure', 'confirm', 'okay']
NO_WORD_CASES =  ['no', 'nah', 'nope', 'cancel', 'nevermind']

class VoiceAgent:
    def __init__(self):
        self.recorder = AudioToTextRecorder()
        self.is_running: bool = True
        
        self.intent: WindowIntent | None = None
        
        self.current_window = None
        
        self.is_awaiting_confirmation: bool = False
        self.is_confirmed: bool = False
        
    def get_user_input(self) -> str:
            input = self.recorder.text()
            print('[User]:', input)
            
            return input
        
    @staticmethod
    def check_input_for_confirmation(input: str) -> bool | None:
        for case in YES_WORD_CASES:
            if case not in input.lower():
                continue
            
            return True
            
        for case in NO_WORD_CASES:
            if case not in input.lower():
                continue
            
            return False
        
        return None
    
    def cleanup_confirmation(self):
        self.current_window = None
        self.is_confirmed = False
        self.is_awaiting_confirmation = False
        
    def start(self):
        print("\nSay 'Exit' to stop.\n")
        
        while self.is_running:
            input = self.get_user_input()
            
            if self.is_awaiting_confirmation:
                ret = self.check_input_for_confirmation(input)
                
                if ret is not None:
                    self.is_confirmed = ret
                    self.execute_intent()
                    continue
                else:
                    self.cleanup_confirmation()
                
            self.intent = parse_intent(input)
            print(self.intent)          
            
            self.execute_intent()
    
    def execute_intent(self):    
        if self.intent.action == 'exit':
            print("Exiting program...")
            sys.exit(0)
            
        if self.intent.action == 'close':
            if self.is_awaiting_confirmation:
                if self.is_confirmed:
                    WindowsManager.confirm_close(self.current_window)
                    
                self.cleanup_confirmation()
                return
            
            ret = WindowsManager.close(self.intent)
            
            if ret is not None:
                print(f'[WindowManager]: Are you sure you want to close "{ret.title}" window?')
                self.current_window = ret
                self.is_awaiting_confirmation = True
                
            return
        
        if self.intent.action == 'minimize':
            WindowsManager.minimize(self.intent)
            return
        
        if self.intent.action == 'dock':
            if self.intent.position == 'full':
                WindowsManager.maximize(self.intent)
                return

        
if __name__ == "__main__":    
    agent = VoiceAgent()
    agent.start()