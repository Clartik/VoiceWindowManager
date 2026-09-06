from dataclasses import dataclass
from typing import Optional
from pywinctl._pywinctl_win import Win32Window

from intents import WindowIntent

YES_WORD_CASES = ['yes', 'yep', 'yeah', 'sure', 'confirm', 'okay']
NO_WORD_CASES =  ['no', 'nah', 'nope', 'cancel', 'nevermind']

@dataclass
class Confirmation:
    is_waiting: bool = False
    is_confirmed: bool = False

@dataclass
class Action:
    input: str
    intent: WindowIntent
    
    window: Optional[Win32Window] = None
    confirmation: Optional[Confirmation] = None