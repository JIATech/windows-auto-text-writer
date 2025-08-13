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

# Import internationalization and configuration modules
from i18n import t, set_language, get_language, get_available_languages, get_i18n
from config import get_config

class AutoTextWriterGUI:
    def __init__(self):
        # Initialize configuration and i18n
        self.config = get_config()
        
        # Load language from config and set up i18n
        saved_language = self.config.get_language()
        set_language(saved_language)
        
        self.root = tk.Tk()
        self.root.title(t("app.title"))
        self.root.geometry("1050x900")
        self.root.resizable(True, True)
        
        # State variables
        self.running = False
        self.text_configs = []
        self.typing_speed = self.config.get('typing_speed', 0.2)
        self.window_title = t("defaults.window_title")
        
        # About dialog dimensions configuration
        self.about_dialog_width = 600
        self.about_dialog_height = 850
        
        # Dark mode configuration
        saved_theme = self.config.get_theme()
        self.dark_mode = (saved_theme == 'dark')
        
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
        self.title_label = ttk.Label(main_frame, text=t("app.title"), 
                                    font=('Arial', 16, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Configuration frame
        self.config_frame = ttk.LabelFrame(main_frame, text=t("ui.configuration"), padding="10")
        self.config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.config_frame.columnconfigure(1, weight=1)
        
        # Window title
        self.window_title_label = ttk.Label(self.config_frame, text=t("ui.window_title"))
        self.window_title_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.window_title_var = tk.StringVar(value=self.window_title)
        self.window_entry = ttk.Entry(self.config_frame, textvariable=self.window_title_var, width=40)
        self.window_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Typing speed
        self.typing_speed_label = ttk.Label(self.config_frame, text=t("ui.typing_speed"))
        self.typing_speed_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        self.typing_speed_var = tk.DoubleVar(value=self.typing_speed)
        self.speed_spinbox = ttk.Spinbox(self.config_frame, from_=0.01, to=10.0, increment=0.1, 
                                        textvariable=self.typing_speed_var, width=10)
        self.speed_spinbox.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Language selector
        self.language_label = ttk.Label(self.config_frame, text=t("ui.language"))
        self.language_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        self.language_var = tk.StringVar()
        available_langs = get_available_languages()
        self.language_combo = ttk.Combobox(self.config_frame, textvariable=self.language_var,
                                          values=list(available_langs.values()), state="readonly", width=15)
        self.language_combo.grid(row=2, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Set current language in combobox
        current_lang = get_language()
        current_lang_name = available_langs.get(current_lang, available_langs['en'])
        self.language_var.set(current_lang_name)
        
        # Bind language change event
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_changed)
        
        # Commands frame
        self.commands_frame = ttk.LabelFrame(main_frame, text=t("ui.commands"), padding="10")
        self.commands_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.commands_frame.columnconfigure(0, weight=1)
        self.commands_frame.rowconfigure(1, weight=1)
        
        # Command buttons
        buttons_frame = ttk.Frame(self.commands_frame)
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.add_button = ttk.Button(buttons_frame, text=t("buttons.add_command"), 
                                    command=self.add_command)
        self.add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.edit_button = ttk.Button(buttons_frame, text=t("buttons.edit_command"), 
                                     command=self.edit_command)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.delete_button = ttk.Button(buttons_frame, text=t("buttons.delete_command"), 
                                       command=self.delete_command)
        self.delete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.defaults_button = ttk.Button(buttons_frame, text=t("buttons.load_defaults"), 
                                         command=self.load_default_commands)
        self.defaults_button.pack(side=tk.LEFT)
        
        # Commands list
        columns = ("Text", "Interval", "Status")
        self.commands_tree = ttk.Treeview(self.commands_frame, columns=columns, show='headings', height=8)
        self.commands_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure columns - will be updated in refresh_ui()
        self.commands_tree.heading("Text", text=t("table.command"))
        self.commands_tree.heading("Interval", text=t("table.interval"))
        self.commands_tree.heading("Status", text=t("table.status"))
        
        self.commands_tree.column("Text", width=300)
        self.commands_tree.column("Interval", width=100)
        self.commands_tree.column("Status", width=100)
        
        # Scrollbar for the list
        commands_scrollbar = ttk.Scrollbar(self.commands_frame, orient=tk.VERTICAL, command=self.commands_tree.yview)
        commands_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.commands_tree.configure(yscrollcommand=commands_scrollbar.set)
        
        # Control frame
        self.control_frame = ttk.LabelFrame(main_frame, text=t("ui.control"), padding="10")
        self.control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Control buttons
        self.start_button = ttk.Button(self.control_frame, text=t("buttons.start"), 
                                      command=self.toggle_execution, style='Green.TButton')
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value=t("messages.status_stopped"))
        self.status_label = ttk.Label(self.control_frame, textvariable=self.status_var, 
                                     font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Information/credits button
        self.info_button = ttk.Button(self.control_frame, text=t("ui.about"), 
                                     command=self.show_about_dialog)
        self.info_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Dark mode button
        self.theme_button = ttk.Button(self.control_frame, text="🌙" if not self.dark_mode else "☀️", 
                                      command=self.toggle_theme, width=3)
        self.theme_button.pack(side=tk.RIGHT)
        
        # Log frame
        self.log_frame = ttk.LabelFrame(main_frame, text=t("ui.activity_log"), padding="10")
        self.log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
        
        # Text area for logs
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=8, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Credits in the bottom right corner
        self.credits_label = ttk.Label(main_frame, text="JIATech - johndev@jiacode.dev", 
                                      font=('Arial', 8), foreground='gray')
        self.credits_label.grid(row=5, column=1, sticky=tk.E, pady=(10, 0))
        
        # Configure row weights
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Configure styles
        self.setup_themes()
        self.apply_theme()
        
    def on_language_changed(self, event):
        """Handle language selection change"""
        selected_name = self.language_var.get()
        
        # Find language code by name
        available_langs = get_available_languages()
        selected_code = None
        for code, name in available_langs.items():
            if name == selected_name:
                selected_code = code
                break
        
        if selected_code and selected_code != get_language():
            # Set the new language
            set_language(selected_code)
            
            # Save language preference
            self.config.set_language(selected_code)
            
            # Update the default window title ONLY if it matches known default values
            # This preserves custom user window titles when switching languages
            current_title = self.window_title_var.get().strip()
            
            # Known default values for both languages
            english_default = "Notepad"
            spanish_default = "Bloc de notas"
            
            # Only update if current title exactly matches a known default
            # Custom titles entered by the user will be preserved
            if current_title == english_default or current_title == spanish_default:
                # Set language first, then get the new default
                set_language(selected_code)
                new_default_title = t("defaults.window_title")
                self.window_title_var.set(new_default_title)
                self.window_title = new_default_title
            else:
                # Just set the language without changing window title
                set_language(selected_code)
            
            # Refresh the entire UI
            self.refresh_ui()
            
            # Log the change
            self.log(t("log.language_changed"))
    
    def refresh_ui(self):
        """Refresh all UI text after language change"""
        # Update main window title
        self.root.title(t("app.title"))
        
        # Update all labels and frames
        self.title_label.configure(text=t("app.title"))
        self.config_frame.configure(text=t("ui.configuration"))
        self.window_title_label.configure(text=t("ui.window_title"))
        self.typing_speed_label.configure(text=t("ui.typing_speed"))
        self.language_label.configure(text=t("ui.language"))
        
        # Update commands frame and buttons
        self.commands_frame.configure(text=t("ui.commands"))
        self.add_button.configure(text=t("buttons.add_command"))
        self.edit_button.configure(text=t("buttons.edit_command"))
        self.delete_button.configure(text=t("buttons.delete_command"))
        self.defaults_button.configure(text=t("buttons.load_defaults"))
        
        # Update treeview headers
        self.commands_tree.heading("Text", text=t("table.command"))
        self.commands_tree.heading("Interval", text=t("table.interval"))
        self.commands_tree.heading("Status", text=t("table.status"))
        
        # Update control frame and buttons
        self.control_frame.configure(text=t("ui.control"))
        self.start_button.configure(text=t("buttons.start") if not self.running else t("buttons.stop"))
        self.info_button.configure(text=t("ui.about"))
        
        # Update log frame
        self.log_frame.configure(text=t("ui.activity_log"))
        
        # Update status message
        if self.running:
            self.status_var.set(t("messages.status_running"))
        else:
            self.status_var.set(t("messages.status_stopped"))
        
        # Refresh commands tree to update status text
        self.refresh_commands_tree()
        
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
        """Loads default commands using translations"""
        self.text_configs = [
            {"text": t("defaults.test_message"), "interval_minutes": 5, "enabled": True},
            {"text": t("defaults.reminder_message"), "interval_minutes": 10, "enabled": True},
            {"text": t("defaults.note_message"), "interval_minutes": 15, "enabled": True}
        ]
        self.refresh_commands_tree()
        self.log(t("log.default_commands_loaded"))
        
    def refresh_commands_tree(self):
        """Updates the commands view"""
        for item in self.commands_tree.get_children():
            self.commands_tree.delete(item)
            
        for i, config in enumerate(self.text_configs):
            status = t("table.active") if config.get('enabled', True) else t("table.inactive")
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
            messagebox.showwarning(t("messages.warning"), t("messages.select_command_edit"))
            return
            
        index = int(selection[0])
        config = self.text_configs[index]
        self.show_command_dialog(config, index)
        
    def delete_command(self):
        """Deletes the selected command"""
        selection = self.commands_tree.selection()
        if not selection:
            messagebox.showwarning(t("messages.warning"), t("messages.select_command_delete"))
            return
            
        if messagebox.askyesno(t("messages.confirm"), t("messages.confirm_delete")):
            index = int(selection[0])
            del self.text_configs[index]
            self.refresh_commands_tree()
            self.log(t("log.command_deleted"))
            
    def show_command_dialog(self, config=None, index=None):
        """Shows dialog to add/edit command"""
        dialog = tk.Toplevel(self.root)
        dialog.title(t("dialogs.add_command_title") if config is None else t("dialogs.edit_command_title"))
        dialog.geometry("600x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Center the dialog
        dialog.transient(self.root)
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Command text
        ttk.Label(frame, text=t("dialogs.command_text")).grid(row=0, column=0, sticky=tk.W, pady=5)
        text_var = tk.StringVar(value=config['text'] if config else "")
        text_entry = ttk.Entry(frame, textvariable=text_var, width=40)
        text_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        text_entry.focus()
        
        # Interval
        ttk.Label(frame, text=t("dialogs.interval_minutes")).grid(row=1, column=0, sticky=tk.W, pady=5)
        interval_var = tk.IntVar(value=config['interval_minutes'] if config else 30)
        interval_spinbox = ttk.Spinbox(frame, from_=1, to=9999, textvariable=interval_var, width=10)
        interval_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Status
        ttk.Label(frame, text=t("dialogs.status_label")).grid(row=2, column=0, sticky=tk.W, pady=5)
        enabled_var = tk.BooleanVar(value=config.get('enabled', True) if config else True)
        enabled_check = ttk.Checkbutton(frame, text=t("dialogs.enabled"), variable=enabled_var)
        enabled_check.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save_command():
            text = text_var.get().strip()
            interval = interval_var.get()
            enabled = enabled_var.get()
            
            if not text:
                messagebox.showerror(t("messages.error"), t("messages.empty_command_text"))
                return
                
            if interval <= 0:
                messagebox.showerror(t("messages.error"), t("messages.invalid_interval"))
                return
                
            new_config = {
                "text": text,
                "interval_minutes": interval,
                "enabled": enabled
            }
            
            if config is None:
                # Add new
                self.text_configs.append(new_config)
                self.log(f"{t('log.command_added')}: '{text}'")
            else:
                # Edit existing
                self.text_configs[index] = new_config
                self.log(f"{t('log.command_edited')}: '{text}'")
                
            self.refresh_commands_tree()
            dialog.destroy()
            
        ttk.Button(buttons_frame, text=t("buttons.save"), command=save_command).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text=t("buttons.cancel"), command=dialog.destroy).pack(side=tk.LEFT)
        
        # Apply theme to dialog
        self.apply_theme_to_dialog(dialog)
        
    def show_about_dialog(self):
        """Shows dialog with author information - configurable dimensions"""
        dialog = tk.Toplevel(self.root)
        dialog.title(t("dialogs.about_title"))
        
        # Use configurable variables for dimensions
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
        title_label = ttk.Label(main_frame, text=t("app.title"), 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 5))
        
        version_label = ttk.Label(main_frame, text=t("app.version"), 
                                 font=('Arial', 12), foreground='gray')
        version_label.pack(pady=(0, 25))
        
        # Author information
        author_frame = ttk.LabelFrame(main_frame, text=t("dialogs.developer"), padding="20")
        author_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(author_frame, text=t("dialogs.author"), font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        ttk.Label(author_frame, text="JIATech", font=('Arial', 11)).pack(anchor=tk.W, padx=(20, 0), pady=(2, 0))
        
        ttk.Label(author_frame, text=t("dialogs.email"), font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(15, 0))
        email_label = ttk.Label(author_frame, text="johndev@jiacode.dev", font=('Arial', 11), 
                               foreground='blue', cursor='hand2')
        email_label.pack(anchor=tk.W, padx=(20, 0), pady=(2, 0))
        
        # Application information
        info_frame = ttk.LabelFrame(main_frame, text=t("dialogs.app_info"), padding="20")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Calculate wraplength based on window width
        wrap_width = self.about_dialog_width - 100
        
        info_label = ttk.Label(info_frame, text=t("dialogs.app_description"), justify=tk.LEFT, 
                              font=('Arial', 10), wraplength=wrap_width)
        info_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        
        # Close button
        close_button = ttk.Button(main_frame, text=t("buttons.close"), command=dialog.destroy)
        close_button.pack(pady=(20, 0))
        
        # Apply theme to dialog
        self.apply_theme_to_dialog(dialog)
        
    
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
        
        # Configure combobox styles
        self.style.configure('TCombobox', 
                           fieldbackground=theme['field_bg'],
                           foreground=theme['field_fg'],
                           borderwidth=1,
                           arrowcolor=theme['field_fg'],
                           buttonbackground=theme['field_bg'])
        
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
        
        # Save theme preference
        theme_name = 'dark' if self.dark_mode else 'light'
        self.config.set_theme(theme_name)
        
        # Update button emoji
        if self.dark_mode:
            self.theme_button.configure(text="☀️")
            self.log(t("log.dark_mode_activated"))
        else:
            self.theme_button.configure(text="🌙")
            self.log(t("log.light_mode_activated"))
        
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
            messagebox.showwarning(t("messages.warning"), t("messages.no_commands"))
            return
            
        # Update configuration
        self.window_title = self.window_title_var.get().strip()
        self.typing_speed = self.typing_speed_var.get()
        
        if not self.window_title:
            messagebox.showerror(t("messages.error"), t("messages.empty_window_title"))
            return
            
        self.running = True
        self.start_button.configure(text=t("buttons.stop"), style='Red.TButton')
        self.status_var.set(t("messages.status_running"))
        
        # Start execution thread
        self.execution_thread = threading.Thread(target=self.execution_loop, daemon=True)
        self.execution_thread.start()
        
        self.log(f"{t('log.started')}: '{self.window_title}', {t('ui.typing_speed')} {self.typing_speed}s")
        
    def stop_execution(self):
        """Stops command execution"""
        self.running = False
        self.start_button.configure(text=t("buttons.start"), style='Green.TButton')
        self.status_var.set(t("messages.status_stopped"))
        self.log(t("log.execution_stopped"))
        
    def execution_loop(self):
        """Main execution loop"""
        # Execute enabled commands immediately
        self.log(t("log.initial_execution"))
        for config in self.text_configs:
            if not self.running:
                break
            if config.get('enabled', True):
                self.execute_text_write(config)
                time.sleep(2)
            else:
                self.log(f"{t('log.skipping_disabled')}: {config['text']}")
        
        if self.running:
            self.log(t("log.initial_completed"))
        
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
        self.log(f"{t('log.executing')}: {config['text']}")
        
        window = self.find_window()
        if not window:
            self.log(t("log.window_not_found", self.window_title))
            return False
            
        if not self.focus_window(window):
            self.log(t("log.error_focus_window"))
            return False
            
        if self.write_text(config['text']):
            self.log(f"{t('log.command_executed')}: {config['text']}")
            return True
        else:
            self.log(f"{t('log.error_executing')}: {config['text']}")
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
                        self.log(t("log.multiple_windows_warning", len(visible_windows), self.window_title))
                        for i, w in enumerate(visible_windows):
                            self.log(f"  {i+1}. '{w.title}'")
                        self.log(t("log.using_first", visible_windows[0].title))
                    else:
                        self.log(t("log.window_found_partial", visible_windows[0].title))
                    return visible_windows[0]
                else:
                    if len(matching_windows) > 1:
                        self.log(t("log.multiple_windows_warning", len(matching_windows), self.window_title) + " (not visible):")
                        for i, w in enumerate(matching_windows):
                            self.log(f"  {i+1}. '{w.title}'")
                        self.log(t("log.using_first", matching_windows[0].title))
                    else:
                        self.log(t("log.window_found_partial", matching_windows[0].title))
                    return matching_windows[0]
            
            return None
        except Exception as e:
            self.log(t("log.error_searching_window", str(e)))
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
            self.log(t("log.error_focusing_window", str(e)))
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
            self.log(t("log.error_writing_text", str(e)))
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
            self.log(f"{t('log.next_executions')}: {' | '.join(status_info)}")
            
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
        # Use fallback text since i18n might not be available during startup errors
        messagebox.showerror("Fatal Error", f"Error starting application:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()