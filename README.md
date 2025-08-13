# Windows Auto Text Writer

Automatizador de texto para aplicaciones Windows que envía comandos predeterminados a intervalos configurables.

![Screenshot](https://img.shields.io/badge/Platform-Windows-blue)
![Python Version](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🚀 Características

- **Dos versiones disponibles**: Consola (v0.1) y GUI (v0.2.1)
- **Escritura automática**: Texto caracter por caracter con velocidad configurable
- **Múltiples comandos**: Cada comando con su propio temporizador independiente
- **Control global**: Tecla de acceso directo ('¡') desde cualquier aplicación
- **Interfaz moderna**: GUI con modo oscuro/claro
- **Gestión completa**: Agregar, editar, eliminar y activar/desactivar comandos
- **Registro en tiempo real**: Log de actividad con timestamps
- **Ejecutables independientes**: Sin necesidad de Python instalado

## 📋 Requisitos

### Para ejecutar desde código fuente:
- Python 3.7 o superior
- Windows (requerido para pygetwindow y pyautogui)

### Dependencias:
```
pyautogui==0.9.54
pygetwindow==0.0.9
pynput==1.7.6
```

## 🛠️ Instalación

### Opción 1: Ejecutables (Recomendado)
1. Descarga los ejecutables desde la sección [Releases](../../releases)
2. Ejecuta directamente:
   - `MU_AutoText_v0.1.exe` - Versión consola
   - `MU_AutoText_GUI.exe` - Versión GUI

### Opción 2: Desde código fuente
```bash
# Clonar repositorio
git clone https://github.com/JIATech/windows-auto-text-writer.git
cd windows-auto-text-writer

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python auto_text_writer.py          # Versión consola
python auto_text_writer_gui.py      # Versión GUI
```

## 🎮 Uso

### Versión GUI (v0.2.1) - Recomendada

1. **Configuración inicial**:
   - Título de ventana objetivo
   - Velocidad de escritura (segundos entre caracteres)

2. **Gestión de comandos**:
   - Agregar comandos personalizados
   - Cargar comandos por defecto (incluye comandos para MU Online)
   - Editar intervalos y activar/desactivar individualmente

3. **Control**:
   - Botón "Iniciar" o tecla '¡' para comenzar
   - Ejecución inmediata de todos los comandos al inicio
   - Después continúa con temporizadores independientes

4. **Características adicionales**:
   - Modo oscuro/claro con botón toggle
   - Log en tiempo real
   - Información detallada en "Acerca de"

### Versión Consola (v0.1)

1. Ejecuta `auto_text_writer.py`
2. Sigue el asistente de configuración interactivo
3. Presiona Ctrl+C para detener

### Comandos por defecto

El programa incluye comandos preconfigurados para MU Online:
- `/attack on` - cada 91 minutos
- `/pickjewel on` - cada 31 minutos  
- `/party on` - cada 32 minutos

## 🔨 Generar ejecutables

```bash
# Versión consola
python build_exe.py

# Versión GUI
python build_gui_exe.py

# Versión optimizada (menor tamaño)
python build_optimized.py
```

Los ejecutables se generan en las carpetas `dist/` y `dist_safe/`.

## 📁 Estructura del proyecto

```
├── auto_text_writer.py       # Versión consola (v0.1)
├── auto_text_writer_gui.py   # Versión GUI (v0.2.1)
├── build_exe.py             # Script para build consola
├── build_gui_exe.py         # Script para build GUI
├── build_optimized.py       # Build con optimización de tamaño
├── requirements.txt         # Dependencias
├── CLAUDE.md               # Documentación para desarrollo
└── README.md               # Este archivo
```

## ⚙️ Configuración avanzada

### Parámetros principales:
- **Título de ventana**: Coincidencia parcial en el nombre de la ventana objetivo
- **Velocidad de escritura**: 0.1 (rápido) a 2.0+ (lento) segundos por caracter
- **Intervalos**: Tiempo en minutos entre ejecuciones de cada comando

### Tecla global:
- **'¡'**: Iniciar/detener desde cualquier aplicación (solo GUI)

## 🐛 Solución de problemas

### La aplicación no encuentra la ventana:
- Usa una parte distintiva del título de ventana (ej: "MU La Plata" en lugar de "MU La Plata 99B Server")
- Asegúrate de que la ventana esté abierta y visible
- Si hay múltiples ventanas con el mismo texto, revisa el log para ver cuál está usando

### Los comandos no se escriben correctamente:
- Ajusta la velocidad de escritura (prueba con valores más altos)
- Verifica que la ventana objetivo tenga el foco

### Error de Python DLL en ejecutables:
- Usa `build_optimized.py` en lugar de optimizaciones agresivas
- Los ejecutables estándar (~67MB) incluyen todas las dependencias necesarias

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**JIATech**
- Email: johndev@jiacode.dev

## 📋 Historial de versiones

### v0.2.1 (Actual)
- ✅ **Búsqueda mejorada de ventanas**: Ahora soporta coincidencia parcial en títulos
- ✅ **Detección inteligente**: Prioriza ventanas visibles cuando hay múltiples coincidencias
- ✅ **Logging mejorado**: Informa qué ventana está usando y advierte sobre múltiples coincidencias
- ✅ **Interfaz actualizada**: Etiqueta clarificada como "Título de ventana (parcial)"
- ✅ **Ejemplos universales**: Textos de ejemplo genéricos en lugar de comandos específicos de juegos
- ✅ **Velocidad optimizada**: Velocidad por defecto reducida a 0.2s para mejor experiencia

### v0.2
- ✅ Interfaz gráfica completa con tkinter
- ✅ Gestión avanzada de textos (agregar, editar, eliminar)
- ✅ Modo oscuro/claro
- ✅ Control global con tecla '¡'
- ✅ Log en tiempo real
- ✅ Ejecución inmediata + temporizadores independientes

### v0.1
- ✅ Versión consola básica
- ✅ Configuración interactiva
- ✅ Escritura caracter por caracter

## 🙏 Reconocimientos

- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Automatización de GUI
- [PyGetWindow](https://github.com/asweigart/PyGetWindow) - Gestión de ventanas
- [pynput](https://github.com/moses-palmer/pynput) - Detección de teclas globales

---

⭐ ¡Si este proyecto te resultó útil, considera darle una estrella!