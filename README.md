# Clip Catch

ClipCatch es un descargador de música creado con propósitos académicos.

## Tabla de contenidos

1. [Instalación](#instalacion)
2. [Uso](#uso)
3. [Empaquetado](#empaquetado)

## Instalción

```bash
# Clonar el repositorio
git clone https://github.com/Lorenzo2345612/ClipCatch.git

# Entrar al proyecto
cd ClipCatch

# Instalar las dependencias
pip install -r requirements.txt
```

## Uso

```
# Iniciar el proyecto
flet run main.py

# Iniciar el proyecto en modo hot-reload
flet run -r main.py
```

## Empaquetado

```
# Creación del build para Windows

flet pack main.py -n "ClipCatch" -i ./assets/icon.ico
```