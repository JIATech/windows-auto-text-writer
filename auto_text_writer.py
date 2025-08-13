import time
import pyautogui
import pygetwindow as gw
from datetime import datetime, timedelta
import threading
import sys

class WindowTextWriter:
    def __init__(self):
        self.window_title = ""
        self.text_configs = []
        self.running = False
        self.typing_speed = 0.5
        
        # PyAutoGUI Configuration
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
    
    def configure(self, window_title, text_configs, typing_speed=0.5):
        """Configures the script with necessary parameters"""
        self.window_title = window_title
        self.text_configs = text_configs
        self.typing_speed = typing_speed
    
    def find_window(self):
        """Finds and returns the window by title"""
        try:
            windows = gw.getWindowsWithTitle(self.window_title)
            if windows:
                return windows[0]
            return None
        except Exception as e:
            print(f"Error searching for window: {e}")
            return None
    
    def focus_window(self, window):
        """Focuses the specified window"""
        try:
            if window.isMinimized:
                window.restore()
            window.activate()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error focusing window: {e}")
            return False
    
    def write_text(self, text):
        """Writes text in the active window character by character"""
        try:
            # Press Enter to open the console
            pyautogui.press('enter')
            time.sleep(0.5)  # Pause for console to open
            
            # Write text character by character with configurable delay
            for char in text:
                pyautogui.write(char)
                time.sleep(self.typing_speed)  # Configurable pause between each character
            
            # Press Enter to send the command
            pyautogui.press('enter')
            
            return True
        except Exception as e:
            print(f"Error writing text: {e}")
            return False
    
    def execute_text_write(self, text_config):
        """Executes the writing of a specific text"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Executing: {text_config['text']}")
        
        window = self.find_window()
        if not window:
            print(f"Window '{self.window_title}' not found")
            return False
        
        if not self.focus_window(window):
            print("Could not focus the window")
            return False
        
        if self.write_text(text_config['text']):
            print(f"Text written successfully: {text_config['text']}")
            return True
        else:
            print(f"Error writing: {text_config['text']}")
            return False
    
    def start(self):
        """Starts the continuous process with multiple threads for different intervals"""
        self.running = True
        print("=" * 50)
        print("    WINDOWS AUTO TEXT WRITER v0.1 - STARTING")
        print("=" * 50)
        print(f"Target window: {self.window_title}")
        print(f"Configured texts: {len(self.text_configs)}")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        print()
        
        # Execute all enabled texts immediately at startup
        print("=== INITIAL EXECUTION ===")
        for config in self.text_configs:
            if config.get('enabled', True):
                self.execute_text_write(config)
                time.sleep(2)  # Pause between texts
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Skipping disabled command: {config['text']}")
        print("=== INITIAL EXECUTION COMPLETED ===")
        print()
        
        # Initialize next executions after initial execution
        now = datetime.now()
        for config in self.text_configs:
            config['next_execution'] = now + timedelta(minutes=config['interval_minutes'])
        
        try:
            while self.running:
                now = datetime.now()
                
                # Check which texts should be executed (only enabled ones)
                for config in self.text_configs:
                    if config.get('enabled', True) and now >= config['next_execution']:
                        self.execute_text_write(config)
                        config['next_execution'] = now + timedelta(minutes=config['interval_minutes'])
                
                # Show next executions (only enabled commands)
                print(f"[{now.strftime('%H:%M:%S')}] Next executions:")
                for config in self.text_configs:
                    if config.get('enabled', True):
                        remaining = config['next_execution'] - now
                        minutes_left = int(remaining.total_seconds() / 60)
                        print(f"  '{config['text']}' in {minutes_left} minutes")
                    else:
                        print(f"  '{config['text']}' [DISABLED]")
                
                # Wait 1 minute before next check
                print("Waiting 1 minute...")
                for _ in range(60):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n" + "=" * 50)
            print("    SCRIPT STOPPED BY USER")
            print("=" * 50)
            print("  Developed by JIATech - johndev@jiacode.dev")
            print("=" * 50)
            self.running = False
        except Exception as e:
            print(f"\nError in main loop: {e}")
            print("=" * 50)
            print("  Developed by JIATech - johndev@jiacode.dev")
            print("=" * 50)
            self.running = False
    
    def stop(self):
        """Stops the process"""
        self.running = False


def get_user_configuration():
    """Requests complete configuration from user with default values"""
    print("=" * 60)
    print("    COMPLETE CONFIGURATION - WINDOWS AUTO TEXT WRITER v0.1")
    print("=" * 60)
    print("    Developed by JIATech - johndev@jiacode.dev")
    print("=" * 60)
    print()
    print("Press ENTER to use default values or enter custom values")
    print()
    
    # Default configuration
    default_window = "Notepad"
    default_speed = 0.5
    default_commands = [
        {"text": "Text 1", "interval_minutes": 91, "enabled": True},
        {"text": "Text 2", "interval_minutes": 31, "enabled": True}, 
        {"text": "Text 3", "interval_minutes": 32, "enabled": True}
    ]
    
    try:
        # Request window title
        print(f"1. Window title (default: '{default_window}'):")
        window_input = input("   Title: ").strip()
        window_title = window_input if window_input else default_window
        print(f"   ✓ Window: {window_title}")
        print()
        
        # Request typing speed
        print("2. Typing speed - seconds between characters (default: 0.5):")
        print("   • 0.1 = Very fast  • 0.5 = Normal  • 1.0 = Slow  • 2.0 = Very slow")
        while True:
            speed_input = input("   Speed: ").strip()
            
            if not speed_input:
                typing_speed = default_speed
                break
            
            try:
                typing_speed = float(speed_input)
                if 0.01 <= typing_speed <= 10.0:
                    break
                else:
                    print("   ⚠️  Valid range: 0.01 - 10.0 seconds")
            except ValueError:
                print("   ❌ Enter a valid number (e.g.: 0.5)")
        
        print(f"   ✓ Speed: {typing_speed} seconds/character")
        print()
        
        # Request commands
        print("3. Commands to execute:")
        print("   Do you want to configure commands? (y/N - default: use all predefined commands)")
        configure_commands = input("   Configure commands: ").strip().lower()
        
        if configure_commands in ['y', 'yes', 'si', 'sí', 's']:
            print("\n   Use custom commands or select from predefined ones?")
            print("   1. Custom commands (create new ones)")
            print("   2. Select predefined commands (enable/disable)")
            
            while True:
                option = input("   Option (1/2): ").strip()
                if option in ['1', '2']:
                    break
                print("   ❌ Enter 1 or 2")
            
            if option == '1':
                # Custom commands
                commands = []
                print("\n   Enter custom commands (press ENTER without text to finish):")
                
                command_num = 1
                while True:
                    print(f"\n   Command {command_num}:")
                    text_input = input("     Command text: ").strip()
                    
                    if not text_input:
                        if not commands:
                            print("   ⚠️  Using default commands (no commands entered)")
                            commands = default_commands
                        break
                    
                    while True:
                        interval_input = input("     Interval in minutes: ").strip()
                        try:
                            interval = int(interval_input)
                            if interval > 0:
                                break
                            else:
                                print("     ❌ Interval must be greater than 0")
                        except ValueError:
                            print("     ❌ Enter a valid integer number")
                    
                    commands.append({"text": text_input, "interval_minutes": interval, "enabled": True})
                    print(f"     ✓ Added: '{text_input}' every {interval} minutes")
                    command_num += 1
            
            else:
                # Select predefined commands
                print("\n   Predefined commands - choose which ones to enable:")
                commands = []
                
                for i, cmd in enumerate(default_commands, 1):
                    print(f"\n   {i}. '{cmd['text']}' every {cmd['interval_minutes']} minutes")
                    while True:
                        enable = input(f"     Enable this command? (Y/n): ").strip().lower()
                        if enable in ['', 'y', 'yes', 'si', 'sí', 's']:
                            cmd_copy = cmd.copy()
                            cmd_copy['enabled'] = True
                            commands.append(cmd_copy)
                            print(f"     ✓ Enabled: '{cmd['text']}'")
                            break
                        elif enable in ['n', 'no']:
                            cmd_copy = cmd.copy()
                            cmd_copy['enabled'] = False
                            commands.append(cmd_copy)
                            print(f"     ✗ Disabled: '{cmd['text']}'")
                            break
                        else:
                            print("     ❌ Answer Y (yes) or N (no)")
        else:
            commands = default_commands
            print("   ✓ Using all default commands enabled")
        
        print()
        print("=" * 60)
        print("    CONFIGURATION COMPLETED")
        print("=" * 60)
        print("    Developed by JIATech - johndev@jiacode.dev")
        print("=" * 60)
        
        return window_title, typing_speed, commands
        
    except KeyboardInterrupt:
        print("\n\nScript cancelled by user")
        sys.exit(0)

def main():
    # Request complete configuration from user
    window_title, typing_speed, text_configs = get_user_configuration()
    
    writer = WindowTextWriter()
    
    # Configure the writer with specified values
    writer.configure(window_title, text_configs, typing_speed)
    
    # Show final configuration
    print()
    print("=" * 50)
    print("    FINAL CONFIGURATION - v0.1")
    print("=" * 50)
    print(f"Target window: {window_title}")
    print(f"Typing speed: {typing_speed} seconds/character")
    print(f"Configured commands:")
    for i, config in enumerate(text_configs, 1):
        status = "✓ ACTIVE" if config.get('enabled', True) else "✗ DISABLED"
        print(f"  {i}. '{config['text']}' every {config['interval_minutes']} minutes [{status}]")
    print("=" * 50)
    print("  Developed by JIATech - johndev@jiacode.dev")
    print("=" * 50)
    print()
    
    # Start the process
    writer.start()


if __name__ == "__main__":
    main()