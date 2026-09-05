from typing import Literal, Optional
from pydantic import BaseModel

import ollama

class WindowIntent(BaseModel):
    action: Literal[
        "open",
        "close",
        "minimize",
        "move",
        "dock",
        "assign_desktop",
        "switch_desktop",
        "exit",
        "unknown"
    ]
    
    # Remains free text as app/window names tend to be open-ended. This does need to accept "all" for minimizing
    target: Optional[str] = None
    
    # This is used by move, assign_desktop, and switch_desktop actions.
    destination: Optional[str] = None
    
    position: Optional[Literal[
        "left_half",
        "right_half",
        "top_half",
        "bottom_half",
        "top_left",
        "top_right",
        "bottom_left",
        "bottom_right",
        "full",
    ]] = None
    
SYSTEM_PROMPT_PATH = './prompts/system_prompt.md'
    
def parse_system_prompt() -> str:
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as file:
        content = file.read()
        
        # Section 1 = Before Splitter, Section 2 = Metadata, Section 3 = System Prompt
        sections = content.split('---')
        
        system_prompt = sections[2]
        return system_prompt.strip()        # Remove empty whitespace for cleaner text
    
SYSTEM_PROMPT = parse_system_prompt()
    
def parse_intent(intent: str) -> WindowIntent:
    response = ollama.chat(
        model='llama3.2:3b',
        format=WindowIntent.model_json_schema(),
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': "user",
                "content": intent
            }
        ]
    )
    
    return WindowIntent.model_validate_json(response.message.content)