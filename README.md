# Space Invaders en Pygame 🎮

Este es un clon del clásico juego **Space Invaders**, desarrollado en **Python** con la librería [Pygame](https://www.pygame.org/).  
Incluye disparos, explosiones, enemigos en movimiento, escudos destructibles y una nave nodriza que aparece cada cierto tiempo.
---

## 📋 Tabla de Contenidos
1. [Requisitos](#-requisitos)
2. [Instalación](#-instalación)
3. [Cómo jugar](#-cómo-jugar)
4. [Mecánicas del juego](#-mecánicas-del-juego)
5. [Estructura de archivos](#-estructura-de-archivos)
6. [Capturas](#-capturas)
7. [Licencia](#-licencia)

---
## 📦 Requisitos

- Python 3.8 o superior  
- Pygame  

## ⚙️ Instalación

Instala las dependencias usando `pip`:

```bash
pip install -r requirements.txt
```
---

## ▶️ Cómo jugar

Ejecuta el archivo principal:
```
python main.py
```

### Controles:

⬅️ Izquierda: mover nave a la izquierda

➡️ Derecha: mover nave a la derecha

Espacio: disparar

R: reiniciar cuando aparece GAME OVER

---

## 🕹️ Mecánicas del juego

El jugador controla una nave que dispara proyectiles hacia los enemigos.

Los enemigos avanzan en bloque y disparan hacia abajo.

Los escudos protegen al jugador pero se destruyen con los impactos.

La nave nodriza aparece después de unos segundos y otorga puntos extra al destruirla.

El juego termina cuando los enemigos alcanzan al jugador o destruyen su nave.

---

## 📁 Estructura de archivos

📂 Proyecto
├── main.py               # Código principal del juego
├── requirements.txt      # Dependencias
|__ imagenes/
|   |__ captura-1.JPG
|   |__ captura-2.JPG     # Capturas de imagenes  
├── img/                  # Imágenes (naves, explosiones, balas, etc.)
│   ├── nave1.png
│   ├── enemigo1_A.png
│   ├── enemigo1_B.png
│   ├── enemigo2_A.png
│   ├── enemigo2_B.png
│   ├── enemigo3_A.png
│   ├── enemigo3_B.png
│   ├── nave_nodriza.png
│   ├── explosion1.png
│   ├── explosion2.png
│   ├── bala.png
│   └── bala_enemiga.png
└── sounds/               # Efectos de sonido
    ├── disparo.wav
    ├── explosion.wav
    ├── disparo_enemigo.wav
    ├── move1.wav
    ├── move2.wav
    ├── move3.wav
    └── move4.wav

---
## 📸 Capturas 

![captura-1](imagenes/capturas/captura-1.jpg)
![captura-2](imagenes/capturas/captura-2.jpg)

---

## 📜 Licencia

Este proyecto es de uso libre con fines educativos y de práctica en Pygame.

Creado por Jordi Martin (Jordi-bit)