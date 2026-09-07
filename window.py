from typing import Optional

from pywinctl._pywinctl_win import Win32Window

import pywinctl as pwc
import pymonctl as pmc

from intents import WindowIntent
from primitives import Action

class WindowsManager:
    @staticmethod
    def _get_window(target: Optional[str]):
        if target is not None:
            windows = pwc.getWindowsWithTitle(target, condition=pwc.Re.CONTAINS, flags=pwc.Re.IGNORECASE)
            
            if len(windows) > 0:
                window = windows[0]
            else:
                window = None
        else:
            window = pwc.getActiveWindow()
            
        return window

    @staticmethod
    def close(intent: WindowIntent) -> Optional[Win32Window]:
        if intent.action != 'close':
            return None
        
        window = WindowsManager._get_window(intent.target)
        
        if not window:
            print('[WindowManager]: No window found!')
            return None
        
        return window
        
    @staticmethod
    def confirm_close(window: Win32Window) -> None:
        if not window.isAlive:
            return
        
        window.close()
        
        print(f'[WindowManager]: Closed `{window.title}` window!')
        
    @staticmethod
    def restore(intent: WindowIntent, last_action: Optional[Action]) -> None:
        if intent.action != 'restore':
            return

        if not intent.target and last_action and last_action.intent.action == 'dock':
            window = last_action.window
        else:
            window = WindowsManager._get_window(intent.target)

        if not window:
            print('[WindowManager]: No window found!')
            return
        
        window.restore()
        print(f'[WindowManager]: Restored "{window.title}" window!')
            
    @staticmethod
    def minimize(intent: WindowIntent, last_action: Optional[Action]) -> Optional[Win32Window]:
        if intent.action != 'dock':
            return None

        if intent.position != 'empty':
            return None
        
        if intent.target != 'all':
            if intent.target is None and last_action and last_action.intent.action == 'dock' and last_action.intent.position == 'full':
                window = last_action.window
            else:
                window = WindowsManager._get_window(intent.target)
            
            if not window:
                print("[WindowManager]: Failed to find window!")
                return None
            
            window.minimize()
            print(f"[WindowManager]: Minimized `{window.title}` window!")       
            
            return window
        else:
            windows = pwc.getAllWindows()
            
            for window in windows:
                if window.isMinimized:
                    continue
                
                try:
                    window.minimize()
                except Exception:
                    pass
                
            print("[WindowManager]: Minimized all windows!")
            return None

    @staticmethod
    def maximize(intent: WindowIntent, last_action: Optional[Action]) -> Optional[Win32Window]:
        if intent.action != 'dock':
            return None
        
        if intent.position != 'full':
            return None

        if intent.target != 'all':
            if intent.target is None and last_action and last_action.intent.action == 'dock' and last_action.intent.position == 'empty':
                window = last_action.window
            else:
                window = WindowsManager._get_window(intent.target)

            if not window:
                print("[WindowManager]: Failed to find window!")
                return None

            window.maximize()
            print(f"[WindowManager]: Maximized `{window.title}` window!")

            return window
        else:
            for window in pwc.getAllWindows():
                if window.isMaximized:
                    continue

                try:
                    window.maximize()
                except Exception:
                    pass

            print("[WindowManager]: Maximized all windows!")
            return None

    @staticmethod
    def dock(intent: WindowIntent) -> None:
        if intent.action != 'dock':
            return

        if intent.position == 'empty' or intent.position == 'full' or intent.position == 'none':
            return

        window = WindowsManager._get_window(intent.target)

        if not window:
            print('[WindowManager]: No window found!')
            return

        window.restore()

        # Get monitor returns a list but usually contains only one
        monitor_name_with_window: str = window.getMonitor()[0]

        monitor: Optional[pmc.Monitor] = None
        for mon in pmc.getAllMonitors():
            if mon.name != monitor_name_with_window:
                continue

            monitor = mon

        if not monitor:
            monitor = pmc.getPrimary()

        mw, mh = monitor.size
        mx, my = monitor.position

        half_width = mw // 2
        half_height = mh // 2

        # Box = Left, Top, Right, Bottom
        hidden_frame_x = window.getExtraFrameSize()[0]        # Targeting Left Value
        hidden_frame_y = window.getExtraFrameSize()[1]        # Targeting Top Value

        if intent.position == "left_half":
            # When docking to only half of screen, windows makes this offset 3 pixels smaller
            hidden_frame_x = hidden_frame_x - 3

            window.moveTo(mx - hidden_frame_x, my)
            window.resizeTo(half_width + (hidden_frame_x * 2), mh)

            print(f"[WindowManager]: Moved '{window.title}' to left half of screen!")
        elif intent.position == "right_half":
            # When docking to only half of screen, windows makes this offset 3 pixels smaller
            hidden_frame_x = hidden_frame_x - 3

            window.moveTo(half_width - hidden_frame_x, 0)
            window.resizeTo(half_width + (hidden_frame_x * 2), mh)

            print(f"[WindowManager]: Moved '{window.title}' to right half of screen!")
        # Revisit implementation. Currently encountering too many issues!
        # elif intent.position == "top_half":
        #     window.moveTo(-hidden_frame_x, 0)
        #     window.resizeTo(mw + hidden_frame_x, half_height + hidden_frame_x)
        #
        #     print(f"[WindowManager]: Moved '{window.title}' to top half of screen!")
        # elif intent.position == "bottom_half":
        #     window.moveTo(-hidden_frame_x, half_height)
        #     window.resizeTo(mw + hidden_frame_x, half_height + hidden_frame_y)
        #
        #     print(f"[WindowManager]: Moved '{window.title}' to bottom half of screen!")
        elif intent.position == "top_left":
            window.moveTo(mx, my)
            window.resizeTo(mw // 2, mh // 2)

            print(f"[WindowManager]: Moved '{window.title}' to top left of screen!")
        elif intent.position == "top_right":
            half_width = mw // 2

            window.moveTo(mx + half_width, my)
            window.resizeTo(half_width, mh // 2)

            print(f"[WindowManager]: Moved '{window.title}' to top right of screen!")
        elif intent.position == "bottom_left":
            pass
        elif intent.position == "bottom_right":
            pass