import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import pyautogui
import pygetwindow as gw
from datetime import datetime, timedelta
import threading
import sys
import json
import os
from pynput import keyboard

class AutoTextWriterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows Auto Text Writer v0.3")
        self.root.geometry("1050x900")
        self.root.resizable(True, True)
        
        # State variables
        self.running = False
        self.text_configs = []
        self.typing_speed = 0.2
        self.window_title = "Notepad"
        
        # About dialog dimensions configuration
        self.about_dialog_width = 600
        self.about_dialog_height = 850
        
        # Dark mode configuration
        self.dark_mode = False
        
        # Pyautogui configuration
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Variable for key listener
        self.key_listener = None
        
        self.setup_ui()
        self.load_default_commands()
        self.setup_key_listener()
        
    def setup_ui(self):
        """Sets up the user interface"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Windows Auto Text Writer v0.3", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Window title
        ttk.Label(config_frame, text="Window title (partial):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.window_title_var = tk.StringVar(value=self.window_title)
        window_entry = ttk.Entry(config_frame, textvariable=self.window_title_var, width=40)
        window_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Typing speed
        ttk.Label(config_frame, text="Speed (sec/char):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.typing_speed_var = tk.DoubleVar(value=self.typing_speed)
        speed_spinbox = ttk.Spinbox(config_frame, from_=0.01, to=10.0, increment=0.1, 
                                   textvariable=self.typing_speed_var, width=10)
        speed_spinbox.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Commands frame
        commands_frame = ttk.LabelFrame(main_frame, text="Commands", padding="10")
        commands_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        commands_frame.columnconfigure(0, weight=1)
        commands_frame.rowconfigure(1, weight=1)
        
        # Command buttons
        buttons_frame = ttk.Frame(commands_frame)
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Add Command", 
                  command=self.add_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Edit Command", 
                  command=self.edit_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Delete Command", 
                  command=self.delete_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Load Defaults", 
                  command=self.load_default_commands).pack(side=tk.LEFT)
        
        # Commands list
        columns = ("Text", "Interval", "Status")
        self.commands_tree = ttk.Treeview(commands_frame, columns=columns, show='headings', height=8)
        self.commands_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure columns
        self.commands_tree.heading("Text", text="Command")
        self.commands_tree.heading("Interval", text="Interval (min)")
        self.commands_tree.heading("Status", text="Status")
        
        self.commands_tree.column("Text", width=300)
        self.commands_tree.column("Interval", width=100)
        self.commands_tree.column("Status", width=100)
        
        # Scrollbar for the list
        commands_scrollbar = ttk.Scrollbar(commands_frame, orient=tk.VERTICAL, command=self.commands_tree.yview)
        commands_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.commands_tree.configure(yscrollcommand=commands_scrollbar.set)
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Control", padding="10")
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Control buttons
        self.start_button = ttk.Button(control_frame, text="Start (¡)", 
                                      command=self.toggle_execution, style='Green.TButton')
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Stopped - Press '¡' to start")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                                font=('Arial', 10, 'bold'))
        status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Information/credits button
        info_button = ttk.Button(control_frame, text="About", 
                                command=self.show_about_dialog)
        info_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Dark mode button
        self.theme_button = ttk.Button(control_frame, text="🌙", 
                                      command=self.toggle_theme, width=3)
        self.theme_button.pack(side=tk.RIGHT)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Text area for logs
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Credits in the bottom right corner
        credits_label = ttk.Label(main_frame, text="JIATech - johndev@jiacode.dev", 
                                 font=('Arial', 8), foreground='gray')
        credits_label.grid(row=5, column=1, sticky=tk.E, pady=(10, 0))
        
        # Configure row weights
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Configure styles
        self.setup_themes()
        self.apply_theme()
        
    def setup_key_listener(self):
        """Sets up the listener for the ¡ key"""
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char == '¡':
                    # Execute in main thread
                    self.root.after(0, self.toggle_execution)
            except AttributeError:
                pass
        
        self.key_listener = keyboard.Listener(on_press=on_press)
        self.key_listener.start()
        
    def load_default_commands(self):
        """Loads default commands"""
        self.text_configs = [
            {"text": "Hello, this is a test message.", "interval_minutes": 5, "enabled": True},
            {"text": "Reminder: check email.", "interval_minutes": 10, "enabled": True},
            {"text": "Important note for later.", "interval_minutes": 15, "enabled": True}
        ]
        self.refresh_commands_tree()
        self.log("Default commands loaded")
        
    def refresh_commands_tree(self):
        """Updates the commands view"""
        for item in self.commands_tree.get_children():
            self.commands_tree.delete(item)
            
        for i, config in enumerate(self.text_configs):
            status = "✓ Active" if config.get('enabled', True) else "✗ Inactive"
            self.commands_tree.insert('', 'end', iid=i, values=(
                config['text'], 
                config['interval_minutes'], 
                status
            ))
            
    def add_command(self):
        """Opens dialog to add command"""
        self.show_command_dialog()
        
    def edit_command(self):
        """Edits the selected command"""
        selection = self.commands_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a command to edit")
            return
            
        index = int(selection[0])
        config = self.text_configs[index]
        self.show_command_dialog(config, index)
        
    def delete_command(self):
        """Deletes the selected command"""
        selection = self.commands_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a command to delete")
            return
            
        if messagebox.askyesno("Confirm", "Delete the selected command?"):
            index = int(selection[0])
            del self.text_configs[index]
            self.refresh_commands_tree()
            self.log(f"Command deleted")
            
    def show_command_dialog(self, config=None, index=None):
        """Shows dialog to add/edit command"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Command" if config is None else "Edit Command")
        dialog.geometry("600x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Center the dialog
        dialog.transient(self.root)
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Command text
        ttk.Label(frame, text="Command text:").grid(row=0, column=0, sticky=tk.W, pady=5)
        text_var = tk.StringVar(value=config['text'] if config else "")
        text_entry = ttk.Entry(frame, textvariable=text_var, width=40)
        text_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        text_entry.focus()
        
        # Interval
        ttk.Label(frame, text="Interval (minutes):").grid(row=1, column=0, sticky=tk.W, pady=5)
        interval_var = tk.IntVar(value=config['interval_minutes'] if config else 30)
        interval_spinbox = ttk.Spinbox(frame, from_=1, to=9999, textvariable=interval_var, width=10)
        interval_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Status
        ttk.Label(frame, text="Status:").grid(row=2, column=0, sticky=tk.W, pady=5)
        enabled_var = tk.BooleanVar(value=config.get('enabled', True) if config else True)
        enabled_check = ttk.Checkbutton(frame, text="Enabled", variable=enabled_var)
        enabled_check.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save_command():
            text = text_var.get().strip()
            interval = interval_var.get()
            enabled = enabled_var.get()
            
            if not text:
                messagebox.showerror("Error", "Command text cannot be empty")
                return
                
            if interval <= 0:
                messagebox.showerror("Error", "Interval must be greater than 0")
                return
                
            new_config = {
                "text": text,
                "interval_minutes": interval,
                "enabled": enabled
            }
            
            if config is None:
                # Add new
                self.text_configs.append(new_config)
                self.log(f"Command added: '{text}'")
            else:
                # Edit existing
                self.text_configs[index] = new_config
                self.log(f"Command edited: '{text}'")
                
            self.refresh_commands_tree()
            dialog.destroy()
            
        ttk.Button(buttons_frame, text="Save", command=save_command).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        
    def show_about_dialog(self):
        """Shows dialog with author information - configurable dimensions"""
        dialog = tk.Toplevel(self.root)
        dialog.title("About Windows Auto Text Writer")
        
        # Usar variables configurables para las dimensiones
        dialog.geometry(f"{self.about_dialog_width}x{self.about_dialog_height}")
        dialog.resizable(True, True)
        dialog.grab_set()
        dialog.transient(self.root)
        
        # Center the dialog
        x_offset = (self.root.winfo_width() - self.about_dialog_width) // 2
        y_offset = (self.root.winfo_height() - self.about_dialog_height) // 2
        dialog.geometry(f"+{self.root.winfo_rootx() + x_offset}+{self.root.winfo_rooty() + y_offset}")
        
        # Simple main frame without scroll (to avoid issues)
        main_frame = ttk.Frame(dialog, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Title
        title_label = ttk.Label(main_frame, text="Windows Auto Text Writer", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 5))
        
        version_label = ttk.Label(main_frame, text="Version 0.3", 
                                 font=('Arial', 12), foreground='gray')
        version_label.pack(pady=(0, 25))
        
        # Author information
        author_frame = ttk.LabelFrame(main_frame, text="Developer", padding="20")
        author_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(author_frame, text="Author:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        ttk.Label(author_frame, text="JIATech", font=('Arial', 11)).pack(anchor=tk.W, padx=(20, 0), pady=(2, 0))
        
        ttk.Label(author_frame, text="Email:", font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(15, 0))
        email_label = ttk.Label(author_frame, text="johndev@jiacode.dev", font=('Arial', 11), 
                               foreground='blue', cursor='hand2')
        email_label.pack(anchor=tk.W, padx=(20, 0), pady=(2, 0))
        
        # Application information
        info_frame = ttk.LabelFrame(main_frame, text="Application Information", padding="20")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        info_text = """Text automator for Windows applications.

Main features:

• Global control with '¡' key (from any application)
• Complete command management (add, edit, delete)
• Individual command activation/deactivation
• Configurable typing speed
• Real-time log with timestamps
• Immediate execution on startup + independent timers
• Persistent configuration during session"""
        
        # Calculate wraplength based on window width
        wrap_width = self.about_dialog_width - 100
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, 
                              font=('Arial', 10), wraplength=wrap_width)
        info_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        
        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=dialog.destroy)
        close_button.pack(pady=(20, 0))
        
        # Apply theme to dialog
        self.apply_theme_to_dialog(dialog)
        
        # Show current dimensions in log for debugging
        self.log(f"'About' window opened: {self.about_dialog_width}x{self.about_dialog_height}")
        self.log("To adjust: modify about_dialog_width and about_dialog_height in code")
    
    def setup_themes(self):
        """Configures light and dark themes"""
        self.style = ttk.Style()
        
        # Light theme (default)
        self.light_theme = {
            'bg': '#f0f0f0',
            'fg': '#000000',
            'select_bg': '#0078d7',
            'select_fg': '#ffffff',
            'field_bg': '#ffffff',
            'field_fg': '#000000',
            'button_bg': '#e1e1e1',
            'button_fg': '#000000',
            'frame_bg': '#f0f0f0',
            'log_bg': '#ffffff',
            'log_fg': '#000000',
            'labelframe_bg': '#f0f0f0',
            'inner_bg': '#ffffff'
        }
        
        # Dark theme
        self.dark_theme = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'select_bg': '#404040',
            'select_fg': '#ffffff',
            'field_bg': '#3d3d3d',        # Darker for fields
            'field_fg': '#ffffff',
            'button_bg': '#404040',
            'button_fg': '#ffffff',
            'frame_bg': '#2b2b2b',
            'log_bg': '#1e1e1e',
            'log_fg': '#ffffff',
            'labelframe_bg': '#353535',    # Specific background for LabelFrames
            'inner_bg': '#333333'          # Background for inner content
        }
    
    def apply_theme(self):
        """Applies current theme to all widgets"""
        theme = self.dark_theme if self.dark_mode else self.light_theme
        
        # Configure base styles
        green_color = '#00ff00' if self.dark_mode else 'green'
        red_color = '#ff4444' if self.dark_mode else 'red'
        
        self.style.configure('Green.TButton', foreground=green_color)
        self.style.configure('Red.TButton', foreground=red_color)
        
        # Disable hover effects for special buttons
        self.style.map('Green.TButton',
                      background=[('active', theme['button_bg']),
                                 ('pressed', theme['button_bg'])],
                      foreground=[('active', green_color),
                                 ('pressed', green_color)])
        
        self.style.map('Red.TButton',
                      background=[('active', theme['button_bg']),
                                 ('pressed', theme['button_bg'])],
                      foreground=[('active', red_color),
                                 ('pressed', red_color)])
        
        # Configure main window background colors
        self.root.configure(bg=theme['bg'])
        
        # Configure frame styles
        self.style.configure('TFrame', background=theme['frame_bg'])
        self.style.configure('TLabelFrame', 
                           background=theme.get('labelframe_bg', theme['frame_bg']), 
                           foreground=theme['fg'],
                           borderwidth=0 if self.dark_mode else 1,
                           relief='flat' if self.dark_mode else 'solid')
        self.style.configure('TLabelFrame.Label', 
                           background=theme.get('labelframe_bg', theme['frame_bg']), 
                           foreground=theme['fg'])
        
        # Configure internal theme for LabelFrames
        self.style.configure('TLabelFrame.Border', background=theme.get('labelframe_bg', theme['frame_bg']))
        
        # Configure label styles
        self.style.configure('TLabel', background=theme['frame_bg'], foreground=theme['fg'])
        
        # Configure button styles
        self.style.configure('TButton', 
                           background=theme['button_bg'], 
                           foreground=theme['button_fg'],
                           borderwidth=1,
                           focuscolor='none')
        
        # Disable hover effects
        self.style.map('TButton',
                      background=[('active', theme['button_bg']),
                                 ('pressed', theme['button_bg'])],
                      foreground=[('active', theme['button_fg']),
                                 ('pressed', theme['button_fg'])])
        
        # Configure entry styles
        self.style.configure('TEntry', 
                           fieldbackground=theme['field_bg'],
                           foreground=theme['field_fg'],
                           borderwidth=1)
        
        # Configure spinbox styles
        self.style.configure('TSpinbox', 
                           fieldbackground=theme['field_bg'],
                           foreground=theme['field_fg'],
                           borderwidth=0 if self.dark_mode else 1,
                           arrowcolor=theme['field_fg'],
                           buttonbackground=theme['field_bg'])
        
        # Configure treeview styles
        self.style.configure('Treeview', 
                           background=theme['field_bg'],
                           foreground=theme['field_fg'],
                           fieldbackground=theme['field_bg'],
                           borderwidth=0,
                           highlightthickness=0)
        self.style.configure('Treeview.Heading', 
                           background=theme['field_bg'],
                           foreground=theme['field_fg'],
                           borderwidth=0,
                           relief='flat')
        
        # Disable hover effects in treeview
        self.style.map('Treeview',
                      background=[('selected', theme['select_bg'])],
                      foreground=[('selected', theme['select_fg'])])
        
        # Disable hover effects in treeview headers
        self.style.map('Treeview.Heading',
                      background=[('active', theme['field_bg']),
                                 ('pressed', theme['field_bg'])],
                      foreground=[('active', theme['field_fg']),
                                 ('pressed', theme['field_fg'])])
        
        # Configure checkbutton styles
        self.style.configure('TCheckbutton', 
                           background=theme['frame_bg'],
                           foreground=theme['fg'],
                           focuscolor='none')
        
        # Disable hover effects on checkbuttons
        self.style.map('TCheckbutton',
                      background=[('active', theme['frame_bg']),
                                 ('pressed', theme['frame_bg'])],
                      foreground=[('active', theme['fg']),
                                 ('pressed', theme['fg'])],
                      focuscolor=[('active', 'none'),
                                 ('pressed', 'none')])
        
        # Configure log area
        if hasattr(self, 'log_text'):
            self.log_text.configure(
                bg=theme['log_bg'],
                fg=theme['log_fg'],
                insertbackground=theme['fg'],
                selectbackground=theme['select_bg'],
                selectforeground=theme['select_fg']
            )
    
    def apply_theme_to_dialog(self, dialog):
        """Applies current theme to a dialog"""
        theme = self.dark_theme if self.dark_mode else self.light_theme
        dialog.configure(bg=theme['bg'])
        
        # Configure TTK styles for the dialog
        self.style.configure('Dialog.TFrame', background=theme['frame_bg'])
        self.style.configure('Dialog.TLabelFrame', 
                           background=theme['frame_bg'], 
                           foreground=theme['fg'])
        self.style.configure('Dialog.TLabelFrame.Label', 
                           background=theme['frame_bg'], 
                           foreground=theme['fg'])
        
        # Apply theme to all dialog widgets
        def apply_to_children(widget):
            widget_class = widget.winfo_class()
            if widget_class == 'Frame':
                widget.configure(bg=theme['frame_bg'])
            elif widget_class == 'Label':
                widget.configure(bg=theme['frame_bg'], fg=theme['fg'])
            elif widget_class == 'Button':
                widget.configure(bg=theme['button_bg'], fg=theme['button_fg'])
            
            for child in widget.winfo_children():
                apply_to_children(child)
        
        apply_to_children(dialog)
    
    def toggle_theme(self):
        """Switches between light and dark mode"""
        self.dark_mode = not self.dark_mode
        
        # Update button emoji
        if self.dark_mode:
            self.theme_button.configure(text="☀️")
            self.log("Dark mode activated")
        else:
            self.theme_button.configure(text="🌙")
            self.log("Light mode activated")
        
        # Apply new theme
        self.apply_theme()
        
        # Force update of all widgets
        self.root.update_idletasks()
        
    def toggle_execution(self):
        """Starts or stops execution"""
        if self.running:
            self.stop_execution()
        else:
            self.start_execution()
            
    def start_execution(self):
        """Starts command execution"""
        if not self.text_configs:
            messagebox.showwarning("Warning", "No commands configured")
            return
            
        # Update configuration
        self.window_title = self.window_title_var.get().strip()
        self.typing_speed = self.typing_speed_var.get()
        
        if not self.window_title:
            messagebox.showerror("Error", "Window title cannot be empty")
            return
            
        self.running = True
        self.start_button.configure(text="Stop (¡)", style='Red.TButton')
        self.status_var.set("Running - Press '¡' to stop")
        
        # Start execution thread
        self.execution_thread = threading.Thread(target=self.execution_loop, daemon=True)
        self.execution_thread.start()
        
        self.log(f"Started - Window: '{self.window_title}', Speed: {self.typing_speed}s")
        
    def stop_execution(self):
        """Stops command execution"""
        self.running = False
        self.start_button.configure(text="Start (¡)", style='Green.TButton')
        self.status_var.set("Stopped - Press '¡' to start")
        self.log("Execution stopped")
        
    def execution_loop(self):
        """Main execution loop"""
        # Execute enabled commands immediately
        self.log("=== INITIAL EXECUTION ===")
        for config in self.text_configs:
            if not self.running:
                break
            if config.get('enabled', True):
                self.execute_text_write(config)
                time.sleep(2)
            else:
                self.log(f"Skipping disabled command: {config['text']}")
        
        if self.running:
            self.log("=== INITIAL EXECUTION COMPLETED ===")
        
        # Initialize next executions
        now = datetime.now()
        for config in self.text_configs:
            config['next_execution'] = now + timedelta(minutes=config['interval_minutes'])
            
        # Main loop
        while self.running:
            now = datetime.now()
            
            # Check commands to execute
            for config in self.text_configs:
                if not self.running:
                    break
                if config.get('enabled', True) and now >= config['next_execution']:
                    self.execute_text_write(config)
                    config['next_execution'] = now + timedelta(minutes=config['interval_minutes'])
            
            # Update status every minute
            if self.running:
                self.update_status_display()
                
            # Wait 1 minute
            for _ in range(60):
                if not self.running:
                    break
                time.sleep(1)
                
    def execute_text_write(self, config):
        """Executes text writing for a command"""
        self.log(f"Executing: {config['text']}")
        
        window = self.find_window()
        if not window:
            self.log(f"ERROR: Window '{self.window_title}' not found")
            return False
            
        if not self.focus_window(window):
            self.log("ERROR: Could not focus window")
            return False
            
        if self.write_text(config['text']):
            self.log(f"✓ Command executed: {config['text']}")
            return True
        else:
            self.log(f"✗ Error executing: {config['text']}")
            return False
            
    def find_window(self):
        """Searches for window by partial title match"""
        try:
            # First try exact search (faster)
            windows = gw.getWindowsWithTitle(self.window_title)
            if windows:
                return windows[0]
            
            # If not found by exact title, search by partial match
            all_windows = gw.getAllWindows()
            matching_windows = []
            
            for window in all_windows:
                if window.title and self.window_title.lower() in window.title.lower():
                    matching_windows.append(window)
            
            if matching_windows:
                # If multiple matches, prioritize visible window
                visible_windows = [w for w in matching_windows if w.visible]
                if visible_windows:
                    if len(visible_windows) > 1:
                        self.log(f"WARNING: {len(visible_windows)} windows found with '{self.window_title}':")
                        for i, w in enumerate(visible_windows):
                            self.log(f"  {i+1}. '{w.title}'")
                        self.log(f"Using first: '{visible_windows[0].title}'")
                    else:
                        self.log(f"Window found by partial match: '{visible_windows[0].title}'")
                    return visible_windows[0]
                else:
                    if len(matching_windows) > 1:
                        self.log(f"WARNING: {len(matching_windows)} windows found with '{self.window_title}' (not visible):")
                        for i, w in enumerate(matching_windows):
                            self.log(f"  {i+1}. '{w.title}'")
                        self.log(f"Using first: '{matching_windows[0].title}'")
                    else:
                        self.log(f"Window found by partial match: '{matching_windows[0].title}'")
                    return matching_windows[0]
            
            return None
        except Exception as e:
            self.log(f"Error searching for window: {e}")
            return None
            
    def focus_window(self, window):
        """Focuses the window"""
        try:
            if window.isMinimized:
                window.restore()
            window.activate()
            time.sleep(1)
            return True
        except Exception as e:
            self.log(f"Error focusing window: {e}")
            return False
            
    def write_text(self, text):
        """Writes text character by character"""
        try:
            # Enter to open console
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Write character by character
            for char in text:
                if not self.running:
                    return False
                pyautogui.write(char)
                time.sleep(self.typing_speed)
                
            # Enter to send
            pyautogui.press('enter')
            return True
        except Exception as e:
            self.log(f"Error writing text: {e}")
            return False
            
    def update_status_display(self):
        """Updates status information"""
        if not self.running:
            return
            
        now = datetime.now()
        status_info = []
        
        for config in self.text_configs:
            if config.get('enabled', True):
                remaining = config['next_execution'] - now
                minutes_left = int(remaining.total_seconds() / 60)
                status_info.append(f"'{config['text']}' en {minutes_left}min")
                
        if status_info:
            self.log(f"Next executions: {' | '.join(status_info)}")
            
    def log(self, message):
        """Adds message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Execute in main thread
        self.root.after(0, lambda: self._append_log(log_message))
        
    def _append_log(self, message):
        """Adds message to log widget (main thread)"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        
        # Limit log lines
        lines = self.log_text.get("1.0", tk.END).split("\n")
        if len(lines) > 100:
            self.log_text.delete("1.0", f"{len(lines) - 100}.0")
            
    def on_closing(self):
        """Handles application closure"""
        if self.running:
            self.stop_execution()
            
        if self.key_listener:
            self.key_listener.stop()
            
        self.root.destroy()
        
    def run(self):
        """Runs the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    try:
        app = AutoTextWriterGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Error starting application:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()