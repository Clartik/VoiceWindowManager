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
    def minimize(intent: WindowIntent):
        if intent.action != 'minimize':
            return
        
        if intent.target != 'all':
            window = WindowsManager._get_window(intent.target)
            
            if not window:
                return
            
            window.minimize()
            
            print(f"[WindowManager]: Minimized first `{intent.target}` window!")       
        else:
            windows = pwc.getAllWindows()
            
            for window in windows:
                if window.isMinimized:
                    continue
                
                window.minimize()
                
            print("[WindowManager]: Minimized all windows!")       

    @staticmethod
    def maximize(intent: WindowIntent):
        if intent.action != 'dock':
            return
        
        if intent.position != 'full':
            return
        
        if intent.target != 'all':
            window = WindowsManager._get_window(intent.target)
            
            if not window:
                return
            
            window.maximize()
            
            print(f"[WindowManager]: Maximized first `{intent.target}` window!")       
        else:
            windows = pwc.getAllWindows()
            
            for window in windows:
                if window.isMaximized:
                    continue
                
                window.maximize()
                
            print("[WindowManager]: Maximized all windows!")     