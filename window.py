from typing import Optional
from pywinctl._pywinctl_win import Win32Window

import pywinctl as pwc

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
            return
        
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

        if not intent.target and last_action:
            if last_action.intent.action == 'dock':
                window = last_action.window
            else:
                window = WindowsManager._get_window(intent.target)
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
            if intent.target is None and last_action:
                if last_action.intent.action == 'dock' and last_action.intent.position == 'empty':
                    window = last_action.window
                else:
                    window = WindowsManager._get_window(intent.target)
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
            if intent.target is None and last_action:
                if last_action.intent.action == 'dock' and last_action.intent.position == 'empty':
                    window = last_action.window
                else:
                    window = WindowsManager._get_window(intent.target)
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