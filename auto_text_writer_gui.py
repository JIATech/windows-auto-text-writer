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

class MUAutoTextWriterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows Auto Text Writer v0.2.1")
        self.root.geometry("1050x900")
        self.root.resizable(True, True)
        
        # Variables de estado
        self.running = False
        self.text_configs = []
        self.typing_speed = 0.2
        self.window_title = "Bloc de notas"
        
        # Configuración de dimensiones del diálogo "Acerca de"
        self.about_dialog_width = 600
        self.about_dialog_height = 850
        
        # Configuración de modo oscuro
        self.dark_mode = False
        
        # Configuración de pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Variable para el listener de teclas
        self.key_listener = None
        
        self.setup_ui()
        self.load_default_commands()
        self.setup_key_listener()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Windows Auto Text Writer v0.2.1", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Título de ventana
        ttk.Label(config_frame, text="Título de ventana (parcial):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.window_title_var = tk.StringVar(value=self.window_title)
        window_entry = ttk.Entry(config_frame, textvariable=self.window_title_var, width=40)
        window_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Velocidad de escritura
        ttk.Label(config_frame, text="Velocidad (seg/char):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.typing_speed_var = tk.DoubleVar(value=self.typing_speed)
        speed_spinbox = ttk.Spinbox(config_frame, from_=0.01, to=10.0, increment=0.1, 
                                   textvariable=self.typing_speed_var, width=10)
        speed_spinbox.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Frame de comandos
        commands_frame = ttk.LabelFrame(main_frame, text="Comandos", padding="10")
        commands_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        commands_frame.columnconfigure(0, weight=1)
        commands_frame.rowconfigure(1, weight=1)
        
        # Botones de comandos
        buttons_frame = ttk.Frame(commands_frame)
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Agregar Comando", 
                  command=self.add_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Editar Comando", 
                  command=self.edit_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Eliminar Comando", 
                  command=self.delete_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Cargar Defaults", 
                  command=self.load_default_commands).pack(side=tk.LEFT)
        
        # Lista de comandos
        columns = ("Texto", "Intervalo", "Estado")
        self.commands_tree = ttk.Treeview(commands_frame, columns=columns, show='headings', height=8)
        self.commands_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar columnas
        self.commands_tree.heading("Texto", text="Comando")
        self.commands_tree.heading("Intervalo", text="Intervalo (min)")
        self.commands_tree.heading("Estado", text="Estado")
        
        self.commands_tree.column("Texto", width=300)
        self.commands_tree.column("Intervalo", width=100)
        self.commands_tree.column("Estado", width=100)
        
        # Scrollbar para la lista
        commands_scrollbar = ttk.Scrollbar(commands_frame, orient=tk.VERTICAL, command=self.commands_tree.yview)
        commands_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.commands_tree.configure(yscrollcommand=commands_scrollbar.set)
        
        # Frame de control
        control_frame = ttk.LabelFrame(main_frame, text="Control", padding="10")
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botones de control
        self.start_button = ttk.Button(control_frame, text="Iniciar (¡)", 
                                      command=self.toggle_execution, style='Green.TButton')
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Label de estado
        self.status_var = tk.StringVar(value="Detenido - Presiona '¡' para iniciar")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                                font=('Arial', 10, 'bold'))
        status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Botón de información/créditos
        info_button = ttk.Button(control_frame, text="Acerca de", 
                                command=self.show_about_dialog)
        info_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Botón de modo oscuro
        self.theme_button = ttk.Button(control_frame, text="🌙", 
                                      command=self.toggle_theme, width=3)
        self.theme_button.pack(side=tk.RIGHT)
        
        # Frame de log
        log_frame = ttk.LabelFrame(main_frame, text="Registro de Actividad", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Área de texto para logs
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Créditos en la esquina inferior derecha
        credits_label = ttk.Label(main_frame, text="JIATech - johndev@jiacode.dev", 
                                 font=('Arial', 8), foreground='gray')
        credits_label.grid(row=5, column=1, sticky=tk.E, pady=(10, 0))
        
        # Configurar peso de las filas
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Configurar estilos
        self.setup_themes()
        self.apply_theme()
        
    def setup_key_listener(self):
        """Configura el listener para la tecla ¡"""
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char == '¡':
                    # Ejecutar en el hilo principal
                    self.root.after(0, self.toggle_execution)
            except AttributeError:
                pass
        
        self.key_listener = keyboard.Listener(on_press=on_press)
        self.key_listener.start()
        
    def load_default_commands(self):
        """Carga los comandos por defecto"""
        self.text_configs = [
            {"text": "Hola, este es un texto de prueba.", "interval_minutes": 5, "enabled": True},
            {"text": "Recordatorio: revisar el correo electrónico.", "interval_minutes": 10, "enabled": True},
            {"text": "Nota importante para más tarde.", "interval_minutes": 15, "enabled": True}
        ]
        self.refresh_commands_tree()
        self.log("Comandos por defecto cargados")
        
    def refresh_commands_tree(self):
        """Actualiza la vista de comandos"""
        for item in self.commands_tree.get_children():
            self.commands_tree.delete(item)
            
        for i, config in enumerate(self.text_configs):
            status = "✓ Activo" if config.get('enabled', True) else "✗ Desactivado"
            self.commands_tree.insert('', 'end', iid=i, values=(
                config['text'], 
                config['interval_minutes'], 
                status
            ))
            
    def add_command(self):
        """Abre diálogo para agregar comando"""
        self.show_command_dialog()
        
    def edit_command(self):
        """Edita el comando seleccionado"""
        selection = self.commands_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un comando para editar")
            return
            
        index = int(selection[0])
        config = self.text_configs[index]
        self.show_command_dialog(config, index)
        
    def delete_command(self):
        """Elimina el comando seleccionado"""
        selection = self.commands_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un comando para eliminar")
            return
            
        if messagebox.askyesno("Confirmar", "¿Eliminar el comando seleccionado?"):
            index = int(selection[0])
            del self.text_configs[index]
            self.refresh_commands_tree()
            self.log(f"Comando eliminado")
            
    def show_command_dialog(self, config=None, index=None):
        """Muestra diálogo para agregar/editar comando"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Comando" if config is None else "Editar Comando")
        dialog.geometry("600x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Centrar el diálogo
        dialog.transient(self.root)
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Texto del comando
        ttk.Label(frame, text="Texto del comando:").grid(row=0, column=0, sticky=tk.W, pady=5)
        text_var = tk.StringVar(value=config['text'] if config else "")
        text_entry = ttk.Entry(frame, textvariable=text_var, width=40)
        text_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        text_entry.focus()
        
        # Intervalo
        ttk.Label(frame, text="Intervalo (minutos):").grid(row=1, column=0, sticky=tk.W, pady=5)
        interval_var = tk.IntVar(value=config['interval_minutes'] if config else 30)
        interval_spinbox = ttk.Spinbox(frame, from_=1, to=9999, textvariable=interval_var, width=10)
        interval_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Estado
        ttk.Label(frame, text="Estado:").grid(row=2, column=0, sticky=tk.W, pady=5)
        enabled_var = tk.BooleanVar(value=config.get('enabled', True) if config else True)
        enabled_check = ttk.Checkbutton(frame, text="Activado", variable=enabled_var)
        enabled_check.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Botones
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save_command():
            text = text_var.get().strip()
            interval = interval_var.get()
            enabled = enabled_var.get()
            
            if not text:
                messagebox.showerror("Error", "El texto del comando no puede estar vacío")
                return
                
            if interval <= 0:
                messagebox.showerror("Error", "El intervalo debe ser mayor a 0")
                return
                
            new_config = {
                "text": text,
                "interval_minutes": interval,
                "enabled": enabled
            }
            
            if config is None:
                # Agregar nuevo
                self.text_configs.append(new_config)
                self.log(f"Comando agregado: '{text}'")
            else:
                # Editar existente
                self.text_configs[index] = new_config
                self.log(f"Comando editado: '{text}'")
                
            self.refresh_commands_tree()
            dialog.destroy()
            
        ttk.Button(buttons_frame, text="Guardar", command=save_command).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT)
        
    def show_about_dialog(self):
        """Muestra diálogo con información del autor - dimensiones configurables"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Acerca de Windows Auto Text Writer")
        
        # Usar variables configurables para las dimensiones
        dialog.geometry(f"{self.about_dialog_width}x{self.about_dialog_height}")
        dialog.resizable(True, True)
        dialog.grab_set()
        dialog.transient(self.root)
        
        # Centrar el diálogo
        x_offset = (self.root.winfo_width() - self.about_dialog_width) // 2
        y_offset = (self.root.winfo_height() - self.about_dialog_height) // 2
        dialog.geometry(f"+{self.root.winfo_rootx() + x_offset}+{self.root.winfo_rooty() + y_offset}")
        
        # Frame principal simple sin scroll (para evitar problemas)
        main_frame = ttk.Frame(dialog, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Título
        title_label = ttk.Label(main_frame, text="Windows Auto Text Writer", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 5))
        
        version_label = ttk.Label(main_frame, text="Versión 0.2.1", 
                                 font=('Arial', 12), foreground='gray')
        version_label.pack(pady=(0, 25))
        
        # Información del autor
        author_frame = ttk.LabelFrame(main_frame, text="Desarrollador", padding="20")
        author_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(author_frame, text="Autor:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        ttk.Label(author_frame, text="JIATech", font=('Arial', 11)).pack(anchor=tk.W, padx=(20, 0), pady=(2, 0))
        
        ttk.Label(author_frame, text="Email:", font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(15, 0))
        email_label = ttk.Label(author_frame, text="johndev@jiacode.dev", font=('Arial', 11), 
                               foreground='blue', cursor='hand2')
        email_label.pack(anchor=tk.W, padx=(20, 0), pady=(2, 0))
        
        # Información de la aplicación
        info_frame = ttk.LabelFrame(main_frame, text="Información de la Aplicación", padding="20")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        info_text = """Automatizador de texto para aplicaciones Windows.

Funcionalidades principales:

• Control global con tecla '¡' (desde cualquier aplicación)
• Gestión completa de comandos (agregar, editar, eliminar)
• Activación/desactivación individual de comandos
• Velocidad de escritura configurable
• Log en tiempo real con timestamps
• Ejecución inmediata al inicio + temporizadores independientes
• Configuración persistente durante la sesión"""
        
        # Calculamos el wraplength basado en el ancho de la ventana
        wrap_width = self.about_dialog_width - 100
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, 
                              font=('Arial', 10), wraplength=wrap_width)
        info_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        
        # Botón cerrar
        close_button = ttk.Button(main_frame, text="Cerrar", command=dialog.destroy)
        close_button.pack(pady=(20, 0))
        
        # Aplicar tema al diálogo
        self.apply_theme_to_dialog(dialog)
        
        # Mostrar las dimensiones actuales en el log para debugging
        self.log(f"Ventana 'Acerca de' abierta: {self.about_dialog_width}x{self.about_dialog_height}")
        self.log("Para ajustar: modificar about_dialog_width y about_dialog_height en el código")
    
    def setup_themes(self):
        """Configura los temas claro y oscuro"""
        self.style = ttk.Style()
        
        # Tema claro (por defecto)
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
        
        # Tema oscuro
        self.dark_theme = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'select_bg': '#404040',
            'select_fg': '#ffffff',
            'field_bg': '#3d3d3d',        # Más oscuro para campos
            'field_fg': '#ffffff',
            'button_bg': '#404040',
            'button_fg': '#ffffff',
            'frame_bg': '#2b2b2b',
            'log_bg': '#1e1e1e',
            'log_fg': '#ffffff',
            'labelframe_bg': '#353535',    # Fondo específico para LabelFrames
            'inner_bg': '#333333'          # Fondo para contenido interno
        }
    
    def apply_theme(self):
        """Aplica el tema actual a todos los widgets"""
        theme = self.dark_theme if self.dark_mode else self.light_theme
        
        # Configurar estilos base
        green_color = '#00ff00' if self.dark_mode else 'green'
        red_color = '#ff4444' if self.dark_mode else 'red'
        
        self.style.configure('Green.TButton', foreground=green_color)
        self.style.configure('Red.TButton', foreground=red_color)
        
        # Desactivar efectos hover para botones especiales
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
        
        # Configurar colores de fondo de la ventana principal
        self.root.configure(bg=theme['bg'])
        
        # Configurar estilo de frames
        self.style.configure('TFrame', background=theme['frame_bg'])
        self.style.configure('TLabelFrame', 
                           background=theme.get('labelframe_bg', theme['frame_bg']), 
                           foreground=theme['fg'],
                           borderwidth=0 if self.dark_mode else 1,
                           relief='flat' if self.dark_mode else 'solid')
        self.style.configure('TLabelFrame.Label', 
                           background=theme.get('labelframe_bg', theme['frame_bg']), 
                           foreground=theme['fg'])
        
        # Configurar el tema interno de los LabelFrames
        self.style.configure('TLabelFrame.Border', background=theme.get('labelframe_bg', theme['frame_bg']))
        
        # Configurar estilo de labels
        self.style.configure('TLabel', background=theme['frame_bg'], foreground=theme['fg'])
        
        # Configurar estilo de botones
        self.style.configure('TButton', 
                           background=theme['button_bg'], 
                           foreground=theme['button_fg'],
                           borderwidth=1,
                           focuscolor='none')
        
        # Desactivar efectos hover
        self.style.map('TButton',
                      background=[('active', theme['button_bg']),
                                 ('pressed', theme['button_bg'])],
                      foreground=[('active', theme['button_fg']),
                                 ('pressed', theme['button_fg'])])
        
        # Configurar estilo de entries
        self.style.configure('TEntry', 
                           fieldbackground=theme['field_bg'],
                           foreground=theme['field_fg'],
                           borderwidth=1)
        
        # Configurar estilo de spinbox
        self.style.configure('TSpinbox', 
                           fieldbackground=theme['field_bg'],
                           foreground=theme['field_fg'],
                           borderwidth=0 if self.dark_mode else 1,
                           arrowcolor=theme['field_fg'],
                           buttonbackground=theme['field_bg'])
        
        # Configurar estilo de treeview
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
        
        # Desactivar efectos hover en treeview
        self.style.map('Treeview',
                      background=[('selected', theme['select_bg'])],
                      foreground=[('selected', theme['select_fg'])])
        
        # Desactivar efectos hover en headers de treeview
        self.style.map('Treeview.Heading',
                      background=[('active', theme['field_bg']),
                                 ('pressed', theme['field_bg'])],
                      foreground=[('active', theme['field_fg']),
                                 ('pressed', theme['field_fg'])])
        
        # Configurar estilo de checkbutton
        self.style.configure('TCheckbutton', 
                           background=theme['frame_bg'],
                           foreground=theme['fg'],
                           focuscolor='none')
        
        # Desactivar efectos hover en checkbuttons
        self.style.map('TCheckbutton',
                      background=[('active', theme['frame_bg']),
                                 ('pressed', theme['frame_bg'])],
                      foreground=[('active', theme['fg']),
                                 ('pressed', theme['fg'])],
                      focuscolor=[('active', 'none'),
                                 ('pressed', 'none')])
        
        # Configurar área de log
        if hasattr(self, 'log_text'):
            self.log_text.configure(
                bg=theme['log_bg'],
                fg=theme['log_fg'],
                insertbackground=theme['fg'],
                selectbackground=theme['select_bg'],
                selectforeground=theme['select_fg']
            )
    
    def apply_theme_to_dialog(self, dialog):
        """Aplica el tema actual a un diálogo"""
        theme = self.dark_theme if self.dark_mode else self.light_theme
        dialog.configure(bg=theme['bg'])
        
        # Configurar estilos TTK para el diálogo
        self.style.configure('Dialog.TFrame', background=theme['frame_bg'])
        self.style.configure('Dialog.TLabelFrame', 
                           background=theme['frame_bg'], 
                           foreground=theme['fg'])
        self.style.configure('Dialog.TLabelFrame.Label', 
                           background=theme['frame_bg'], 
                           foreground=theme['fg'])
        
        # Aplicar tema a todos los widgets del diálogo
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
        """Cambia entre modo claro y oscuro"""
        self.dark_mode = not self.dark_mode
        
        # Actualizar emoji del botón
        if self.dark_mode:
            self.theme_button.configure(text="☀️")
            self.log("Modo oscuro activado")
        else:
            self.theme_button.configure(text="🌙")
            self.log("Modo claro activado")
        
        # Aplicar nuevo tema
        self.apply_theme()
        
        # Forzar actualización de todos los widgets
        self.root.update_idletasks()
        
    def toggle_execution(self):
        """Inicia o detiene la ejecución"""
        if self.running:
            self.stop_execution()
        else:
            self.start_execution()
            
    def start_execution(self):
        """Inicia la ejecución de comandos"""
        if not self.text_configs:
            messagebox.showwarning("Advertencia", "No hay comandos configurados")
            return
            
        # Actualizar configuración
        self.window_title = self.window_title_var.get().strip()
        self.typing_speed = self.typing_speed_var.get()
        
        if not self.window_title:
            messagebox.showerror("Error", "El título de ventana no puede estar vacío")
            return
            
        self.running = True
        self.start_button.configure(text="Detener (¡)", style='Red.TButton')
        self.status_var.set("Ejecutándose - Presiona '¡' para detener")
        
        # Iniciar hilo de ejecución
        self.execution_thread = threading.Thread(target=self.execution_loop, daemon=True)
        self.execution_thread.start()
        
        self.log(f"Iniciado - Ventana: '{self.window_title}', Velocidad: {self.typing_speed}s")
        
    def stop_execution(self):
        """Detiene la ejecución de comandos"""
        self.running = False
        self.start_button.configure(text="Iniciar (¡)", style='Green.TButton')
        self.status_var.set("Detenido - Presiona '¡' para iniciar")
        self.log("Ejecución detenida")
        
    def execution_loop(self):
        """Bucle principal de ejecución"""
        # Ejecutar comandos habilitados inmediatamente
        self.log("=== EJECUCIÓN INICIAL ===")
        for config in self.text_configs:
            if not self.running:
                break
            if config.get('enabled', True):
                self.execute_text_write(config)
                time.sleep(2)
            else:
                self.log(f"Saltando comando desactivado: {config['text']}")
        
        if self.running:
            self.log("=== EJECUCIÓN INICIAL COMPLETADA ===")
        
        # Inicializar próximas ejecuciones
        now = datetime.now()
        for config in self.text_configs:
            config['next_execution'] = now + timedelta(minutes=config['interval_minutes'])
            
        # Bucle principal
        while self.running:
            now = datetime.now()
            
            # Verificar comandos a ejecutar
            for config in self.text_configs:
                if not self.running:
                    break
                if config.get('enabled', True) and now >= config['next_execution']:
                    self.execute_text_write(config)
                    config['next_execution'] = now + timedelta(minutes=config['interval_minutes'])
            
            # Actualizar estado cada minuto
            if self.running:
                self.update_status_display()
                
            # Esperar 1 minuto
            for _ in range(60):
                if not self.running:
                    break
                time.sleep(1)
                
    def execute_text_write(self, config):
        """Ejecuta la escritura de un comando"""
        self.log(f"Ejecutando: {config['text']}")
        
        window = self.find_window()
        if not window:
            self.log(f"ERROR: Ventana '{self.window_title}' no encontrada")
            return False
            
        if not self.focus_window(window):
            self.log("ERROR: No se pudo enfocar la ventana")
            return False
            
        if self.write_text(config['text']):
            self.log(f"✓ Comando ejecutado: {config['text']}")
            return True
        else:
            self.log(f"✗ Error ejecutando: {config['text']}")
            return False
            
    def find_window(self):
        """Busca la ventana por coincidencia parcial en el título"""
        try:
            # Primero intentar búsqueda exacta (más rápida)
            windows = gw.getWindowsWithTitle(self.window_title)
            if windows:
                return windows[0]
            
            # Si no encuentra por título exacto, buscar por coincidencia parcial
            all_windows = gw.getAllWindows()
            matching_windows = []
            
            for window in all_windows:
                if window.title and self.window_title.lower() in window.title.lower():
                    matching_windows.append(window)
            
            if matching_windows:
                # Si hay múltiples coincidencias, priorizar la ventana visible
                visible_windows = [w for w in matching_windows if w.visible]
                if visible_windows:
                    if len(visible_windows) > 1:
                        self.log(f"ADVERTENCIA: {len(visible_windows)} ventanas encontradas con '{self.window_title}':")
                        for i, w in enumerate(visible_windows):
                            self.log(f"  {i+1}. '{w.title}'")
                        self.log(f"Usando la primera: '{visible_windows[0].title}'")
                    else:
                        self.log(f"Ventana encontrada por coincidencia parcial: '{visible_windows[0].title}'")
                    return visible_windows[0]
                else:
                    if len(matching_windows) > 1:
                        self.log(f"ADVERTENCIA: {len(matching_windows)} ventanas encontradas con '{self.window_title}' (no visibles):")
                        for i, w in enumerate(matching_windows):
                            self.log(f"  {i+1}. '{w.title}'")
                        self.log(f"Usando la primera: '{matching_windows[0].title}'")
                    else:
                        self.log(f"Ventana encontrada por coincidencia parcial: '{matching_windows[0].title}'")
                    return matching_windows[0]
            
            return None
        except Exception as e:
            self.log(f"Error buscando ventana: {e}")
            return None
            
    def focus_window(self, window):
        """Enfoca la ventana"""
        try:
            if window.isMinimized:
                window.restore()
            window.activate()
            time.sleep(1)
            return True
        except Exception as e:
            self.log(f"Error enfocando ventana: {e}")
            return False
            
    def write_text(self, text):
        """Escribe texto caracter por caracter"""
        try:
            # Enter para abrir consola
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Escribir caracter por caracter
            for char in text:
                if not self.running:
                    return False
                pyautogui.write(char)
                time.sleep(self.typing_speed)
                
            # Enter para enviar
            pyautogui.press('enter')
            return True
        except Exception as e:
            self.log(f"Error escribiendo texto: {e}")
            return False
            
    def update_status_display(self):
        """Actualiza la información de estado"""
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
            self.log(f"Próximas ejecuciones: {' | '.join(status_info)}")
            
    def log(self, message):
        """Añade mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Ejecutar en el hilo principal
        self.root.after(0, lambda: self._append_log(log_message))
        
    def _append_log(self, message):
        """Añade mensaje al widget de log (hilo principal)"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        
        # Limitar líneas del log
        lines = self.log_text.get("1.0", tk.END).split("\n")
        if len(lines) > 100:
            self.log_text.delete("1.0", f"{len(lines) - 100}.0")
            
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if self.running:
            self.stop_execution()
            
        if self.key_listener:
            self.key_listener.stop()
            
        self.root.destroy()
        
    def run(self):
        """Ejecuta la aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    try:
        app = MUAutoTextWriterGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()