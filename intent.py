from typing import Literal, Optional
from pydantic import BaseModel

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