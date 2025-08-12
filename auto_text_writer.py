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
        
        # Configuración de pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
    
    def configure(self, window_title, text_configs, typing_speed=0.5):
        """Configura el script con los parámetros necesarios"""
        self.window_title = window_title
        self.text_configs = text_configs
        self.typing_speed = typing_speed
    
    def find_window(self):
        """Busca y devuelve la ventana por título"""
        try:
            windows = gw.getWindowsWithTitle(self.window_title)
            if windows:
                return windows[0]
            return None
        except Exception as e:
            print(f"Error buscando ventana: {e}")
            return None
    
    def focus_window(self, window):
        """Enfoca la ventana especificada"""
        try:
            if window.isMinimized:
                window.restore()
            window.activate()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error enfocando ventana: {e}")
            return False
    
    def write_text(self, text):
        """Escribe el texto en la ventana activa caracter por caracter"""
        try:
            # Presionar Enter para abrir la consola
            pyautogui.press('enter')
            time.sleep(0.5)  # Pausa para que se abra la consola
            
            # Escribir el texto caracter por caracter con delay configurable
            for char in text:
                pyautogui.write(char)
                time.sleep(self.typing_speed)  # Pausa configurable entre cada caracter
            
            # Presionar Enter para enviar el comando
            pyautogui.press('enter')
            
            return True
        except Exception as e:
            print(f"Error escribiendo texto: {e}")
            return False
    
    def execute_text_write(self, text_config):
        """Ejecuta la escritura de un texto específico"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Ejecutando: {text_config['text']}")
        
        window = self.find_window()
        if not window:
            print(f"Ventana '{self.window_title}' no encontrada")
            return False
        
        if not self.focus_window(window):
            print("No se pudo enfocar la ventana")
            return False
        
        if self.write_text(text_config['text']):
            print(f"Texto escrito exitosamente: {text_config['text']}")
            return True
        else:
            print(f"Error escribiendo: {text_config['text']}")
            return False
    
    def start(self):
        """Inicia el proceso continuo con múltiples hilos para diferentes intervalos"""
        self.running = True
        print("=" * 50)
        print("    MU AUTO TEXT WRITER v0.1 - INICIANDO")
        print("=" * 50)
        print(f"Ventana objetivo: {self.window_title}")
        print(f"Textos configurados: {len(self.text_configs)}")
        print("Presiona Ctrl+C para detener")
        print("=" * 50)
        print()
        
        # Ejecutar todos los textos habilitados inmediatamente al inicio
        print("=== EJECUCIÓN INICIAL ===")
        for config in self.text_configs:
            if config.get('enabled', True):
                self.execute_text_write(config)
                time.sleep(2)  # Pausa entre textos
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Saltando comando desactivado: {config['text']}")
        print("=== EJECUCIÓN INICIAL COMPLETADA ===")
        print()
        
        # Inicializar próximas ejecuciones después de la ejecución inicial
        now = datetime.now()
        for config in self.text_configs:
            config['next_execution'] = now + timedelta(minutes=config['interval_minutes'])
        
        try:
            while self.running:
                now = datetime.now()
                
                # Verificar qué textos deben ejecutarse (solo los habilitados)
                for config in self.text_configs:
                    if config.get('enabled', True) and now >= config['next_execution']:
                        self.execute_text_write(config)
                        config['next_execution'] = now + timedelta(minutes=config['interval_minutes'])
                
                # Mostrar próximas ejecuciones (solo comandos habilitados)
                print(f"[{now.strftime('%H:%M:%S')}] Próximas ejecuciones:")
                for config in self.text_configs:
                    if config.get('enabled', True):
                        remaining = config['next_execution'] - now
                        minutes_left = int(remaining.total_seconds() / 60)
                        print(f"  '{config['text']}' en {minutes_left} minutos")
                    else:
                        print(f"  '{config['text']}' [DESACTIVADO]")
                
                # Esperar 1 minuto antes de la siguiente verificación
                print("Esperando 1 minuto...")
                for _ in range(60):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n" + "=" * 50)
            print("    SCRIPT DETENIDO POR EL USUARIO")
            print("=" * 50)
            print("  Desarrollado por JIATech - johndev@jiacode.dev")
            print("=" * 50)
            self.running = False
        except Exception as e:
            print(f"\nError en el bucle principal: {e}")
            print("=" * 50)
            print("  Desarrollado por JIATech - johndev@jiacode.dev")
            print("=" * 50)
            self.running = False
    
    def stop(self):
        """Detiene el proceso"""
        self.running = False


def get_user_configuration():
    """Solicita configuración completa al usuario con valores por defecto"""
    print("=" * 60)
    print("    CONFIGURACIÓN COMPLETA - MU AUTO TEXT WRITER v0.1")
    print("=" * 60)
    print("    Desarrollado por JIATech - johndev@jiacode.dev")
    print("=" * 60)
    print()
    print("Presiona ENTER para usar valores por defecto o ingresa valores personalizados")
    print()
    
    # Configuración por defecto
    default_window = "MU La Plata 99B"
    default_speed = 0.5
    default_commands = [
        {"text": "/attack on", "interval_minutes": 91, "enabled": True},
        {"text": "/pickjewel on", "interval_minutes": 31, "enabled": True}, 
        {"text": "/party on", "interval_minutes": 32, "enabled": True}
    ]
    
    try:
        # Solicitar título de ventana
        print(f"1. Título de la ventana (default: '{default_window}'):")
        window_input = input("   Título: ").strip()
        window_title = window_input if window_input else default_window
        print(f"   ✓ Ventana: {window_title}")
        print()
        
        # Solicitar velocidad de escritura
        print("2. Velocidad de escritura - segundos entre caracteres (default: 0.5):")
        print("   • 0.1 = Muy rápido  • 0.5 = Normal  • 1.0 = Lento  • 2.0 = Muy lento")
        while True:
            speed_input = input("   Velocidad: ").strip()
            
            if not speed_input:
                typing_speed = default_speed
                break
            
            try:
                typing_speed = float(speed_input)
                if 0.01 <= typing_speed <= 10.0:
                    break
                else:
                    print("   ⚠️  Rango válido: 0.01 - 10.0 segundos")
            except ValueError:
                print("   ❌ Ingresa un número válido (ej: 0.5)")
        
        print(f"   ✓ Velocidad: {typing_speed} segundos/caracter")
        print()
        
        # Solicitar comandos
        print("3. Comandos a ejecutar:")
        print("   ¿Quieres configurar comandos? (s/N - default: usar todos los comandos predefinidos)")
        configure_commands = input("   Configurar comandos: ").strip().lower()
        
        if configure_commands in ['s', 'si', 'sí', 'y', 'yes']:
            print("\n   ¿Usar comandos personalizados o seleccionar de los predefinidos?")
            print("   1. Comandos personalizados (crear nuevos)")
            print("   2. Seleccionar comandos predefinidos (activar/desactivar)")
            
            while True:
                option = input("   Opción (1/2): ").strip()
                if option in ['1', '2']:
                    break
                print("   ❌ Ingresa 1 o 2")
            
            if option == '1':
                # Comandos personalizados
                commands = []
                print("\n   Ingresa los comandos personalizados (presiona ENTER sin texto para terminar):")
                
                command_num = 1
                while True:
                    print(f"\n   Comando {command_num}:")
                    text_input = input("     Texto del comando: ").strip()
                    
                    if not text_input:
                        if not commands:
                            print("   ⚠️  Usando comandos por defecto (no se ingresaron comandos)")
                            commands = default_commands
                        break
                    
                    while True:
                        interval_input = input("     Intervalo en minutos: ").strip()
                        try:
                            interval = int(interval_input)
                            if interval > 0:
                                break
                            else:
                                print("     ❌ El intervalo debe ser mayor a 0")
                        except ValueError:
                            print("     ❌ Ingresa un número entero válido")
                    
                    commands.append({"text": text_input, "interval_minutes": interval, "enabled": True})
                    print(f"     ✓ Agregado: '{text_input}' cada {interval} minutos")
                    command_num += 1
            
            else:
                # Seleccionar comandos predefinidos
                print("\n   Comandos predefinidos - elige cuáles activar:")
                commands = []
                
                for i, cmd in enumerate(default_commands, 1):
                    print(f"\n   {i}. '{cmd['text']}' cada {cmd['interval_minutes']} minutos")
                    while True:
                        enable = input(f"     ¿Activar este comando? (S/n): ").strip().lower()
                        if enable in ['', 's', 'si', 'sí', 'y', 'yes']:
                            cmd_copy = cmd.copy()
                            cmd_copy['enabled'] = True
                            commands.append(cmd_copy)
                            print(f"     ✓ Activado: '{cmd['text']}'")
                            break
                        elif enable in ['n', 'no']:
                            cmd_copy = cmd.copy()
                            cmd_copy['enabled'] = False
                            commands.append(cmd_copy)
                            print(f"     ✗ Desactivado: '{cmd['text']}'")
                            break
                        else:
                            print("     ❌ Responde S (sí) o N (no)")
        else:
            commands = default_commands
            print("   ✓ Usando todos los comandos por defecto activados")
        
        print()
        print("=" * 60)
        print("    CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        print("    Desarrollado por JIATech - johndev@jiacode.dev")
        print("=" * 60)
        
        return window_title, typing_speed, commands
        
    except KeyboardInterrupt:
        print("\n\nScript cancelado por el usuario")
        sys.exit(0)

def main():
    # Solicitar configuración completa al usuario
    window_title, typing_speed, text_configs = get_user_configuration()
    
    writer = WindowTextWriter()
    
    # Configurar el escritor con los valores especificados
    writer.configure(window_title, text_configs, typing_speed)
    
    # Mostrar configuración final
    print()
    print("=" * 50)
    print("    CONFIGURACIÓN FINAL - v0.1")
    print("=" * 50)
    print(f"Ventana objetivo: {window_title}")
    print(f"Velocidad de escritura: {typing_speed} segundos/caracter")
    print(f"Comandos configurados:")
    for i, config in enumerate(text_configs, 1):
        status = "✓ ACTIVO" if config.get('enabled', True) else "✗ DESACTIVADO"
        print(f"  {i}. '{config['text']}' cada {config['interval_minutes']} minutos [{status}]")
    print("=" * 50)
    print("  Desarrollado por JIATech - johndev@jiacode.dev")
    print("=" * 50)
    print()
    
    # Iniciar el proceso
    writer.start()


if __name__ == "__main__":
    main()