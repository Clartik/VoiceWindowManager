from typing import Optional

import pywinctl as pwc

from intents import WindowIntent

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
    def close(intent: WindowIntent):
        if intent.action != 'close':
            return
        
        window = WindowsManager._get_window(intent.target)
        
        if not window:
            print('[WindowManager]: No window found!')
            return None
        
        return window
        
    @staticmethod
    def confirm_close(window):
        if not window.isAlive:
            return
        
        window.close()
        
        print(f'[WindowManager]: Closed `{window.title}` window!')
        
    @staticmethod
    def restore(intent: WindowIntent):
        if intent.action != 'restore':
            return
        
        window = WindowsManager._get_window(intent.target)
        
        if not window:
            return
        
        window.restore()
        
        print(f'[WindowManager]: Restored "{window.title}" window!')
            
    @staticmethod
    def minimize(intent: WindowIntent):
        if intent.action != 'dock' or intent.position != 'empty':
            return
        
        if intent.target != 'all':
            window = WindowsManager._get_window(intent.target)
            
            if not window:
                return
            
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
    def maximize(intent: WindowIntent, last_intent: WindowIntent, last_window):
        if intent.action != 'dock':
            return
        
        if intent.position != 'full':
            return
        
        if intent.target != 'all':
            window = WindowsManager._get_window(intent.target)

            if not window:
                was_last_minimize = (
                    last_intent is not None
                    and last_intent.action == 'dock'
                    and last_intent.position == 'empty'
                )

                if not was_last_minimize:
                    print('[WindowManager]: No window found!')
                    return None

                if not last_window:
                    print('[WindowManager]: No last window!')
                    return None

                last_window.maximize()
                print(f'[WindowManager]: Restoring minimized "{last_window.title}" window!')

                return last_window

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