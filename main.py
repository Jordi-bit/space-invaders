import pygame
import sys
import math

# Inicializar Pygame
pygame.init()

# Cargar sonidos
sonido_disparo = pygame.mixer.Sound("sounds/disparo.wav")
sonido_explosion = pygame.mixer.Sound("sounds/explosion.wav")
sonido_disparo_enemigo = pygame.mixer.Sound("sounds/disparo_enemigo.wav")

# Carga los sonidos de movimiento enemigos
sonido_movimiento1 = pygame.mixer.Sound("sounds/move1.wav")
sonido_movimiento2 = pygame.mixer.Sound("sounds/move2.wav")
sonido_movimiento3 = pygame.mixer.Sound("sounds/move3.wav")
sonido_movimiento4 = pygame.mixer.Sound("sounds/move4.wav")

# Los pondremos en una lista para alternar fácilmente
sonidos_movimiento = [sonido_movimiento1, sonido_movimiento2, sonido_movimiento3, sonido_movimiento4]

indice_sonido_mov = 0


# Pantalla
ANCHO = 945
ALTO = 1000
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders")

# Colores
NEGRO = (0, 0, 0)

# Fuente
fuente = pygame.font.Font(None, 36)

# Jugador
jugador_img = pygame.image.load("img/nave1.png")
jugador_x = ANCHO // 2 - 32
jugador_y = ALTO - 100
jugador_velocidad = 5

# Imagenes Explosion enemigo y jugador
explosion1_img = pygame.image.load("img/explosion1.png")
explosion1_img = pygame.transform.scale(explosion1_img, (50, 50))
explosion2_img = pygame.image.load("img/explosion2.png")
explosion2_img = pygame.transform.scale(explosion2_img, (50, 50))


# Bala
bala_img = pygame.image.load("img/bala.png")
bala_enemiga_img = pygame.image.load("img/bala_enemiga.png")

bala_x = 0
bala_y = jugador_y
bala_velocidad = 10
bala_visible = False

# Enemigos
nave_nodriza_img = pygame.image.load("img/nave_nodriza.png")
nave_nodriza_img = pygame.transform.scale(nave_nodriza_img, (80, 50))  # Ajusta tamaño de la nave nodriza

nave_nodriza_x = ANCHO  # Empieza justo fuera a la derecha
nave_nodriza_y = 20     # Arriba, cerca del borde superior
nave_nodriza_vel = 4    # Velocidad hacia la izquierda
nave_nodriza_visible = False
nave_nodriza_explotando = False
tiempo_explosion_nodriza = 0
tiempo_inicio_juego = pygame.time.get_ticks()

enemigo1_img_a = pygame.transform.scale(pygame.image.load("img/enemigo1_A.png"), (50, 50))
enemigo1_img_b = pygame.transform.scale(pygame.image.load("img/enemigo1_B.png"), (50, 50))
enemigo2_img_a = pygame.transform.scale(pygame.image.load("img/enemigo2_A.png"), (50, 50))
enemigo2_img_b = pygame.transform.scale(pygame.image.load("img/enemigo2_B.png"), (50, 50))
enemigo3_img_a = pygame.transform.scale(pygame.image.load("img/enemigo3_A.png"), (50, 50))
enemigo3_img_b = pygame.transform.scale(pygame.image.load("img/enemigo3_B.png"), (50, 50))


enemigos = []
num_enemigos = 11
explosiones = []

# Escudos
ESCUDO_FILAS = 8
ESCUDO_COLUMNAS = 8
ESCUDO_TAMANIO = 11
ESCUDO_VIDAS = 3
escudos = []

# Crear escudos
def crear_escudos():
    escudos.clear()
    posiciones = [100, 300, 500, 700]
    base_y = jugador_y - 120
    forma = [
        "  XXXX  ",
        " XXXXXX ",
        "XXXXXXXX",
        "XXX  XXX",
        "XX    XX"
    ]
    for base_x in posiciones:
        for fila_idx, fila in enumerate(forma):
            for col_idx, char in enumerate(fila):
                if char == "X":
                    bloque = {
                        "x": base_x + col_idx * ESCUDO_TAMANIO,
                        "y": base_y + fila_idx * ESCUDO_TAMANIO,
                        "vida": ESCUDO_VIDAS
                    }
                    escudos.append(bloque)

crear_escudos()

# Crear enemigos
velocidad_enemigos = 1  # velocidad base (puedes ajustar)

def crear_enemigos():
    enemigos.clear()
    filas = 5
    columnas = 11
    espacio_x = 60
    espacio_y = 50
    inicio_x = 50
    inicio_y = 50

    for fila in range(filas):
        for col in range(columnas):
            if fila in [1, 2]:
                img_a, img_b = enemigo2_img_a, enemigo2_img_b
            elif fila in [3, 4]:
                img_a, img_b = enemigo3_img_a, enemigo3_img_b
            else:
                img_a, img_b = enemigo1_img_a, enemigo1_img_b

            enemigo = {
                "x": inicio_x + col * espacio_x,
                "y": inicio_y + fila * espacio_y,
                "vel_x": velocidad_enemigos,
                "vel_y": 40,
                "visible": True,
                "imagenes": [img_a, img_b],
                "indice_imagen": 0
            }
            enemigos.append(enemigo)

crear_enemigos()

# Puntuación y estado del juego
puntuacion = 0
juego_terminado = False
nivel_superado = False
tiempo_nivel_superado = 0

# Controlamos la velocidad de los enemigos segun quedan vivos
def actualizar_velocidad_enemigos():
    global velocidad_enemigos
    enemigos_vivos = sum(1 for e in enemigos if e["visible"])
    # Ajusta la velocidad según enemigos vivos (ejemplo: mínimo 2, aumenta con menos enemigos)
    velocidad_enemigos = max(1, 4 + (2*2 - enemigos_vivos) * 0.1)  # puedes ajustar fórmula
    for enemigo in enemigos:
        if enemigo["visible"]:
            # Mantén la dirección, solo actualiza la velocidad en magnitud
            signo = 1 if enemigo["vel_x"] > 0 else -1
            enemigo["vel_x"] = signo * velocidad_enemigos


# Reloj
clock = pygame.time.Clock()
ultimo_cambio_sprite = pygame.time.get_ticks()
intervalo_sprite = 1000

# Funciones auxiliares
def hay_colision(enemigo_x, enemigo_y, bala_x, bala_y):
    enemigo_rect = pygame.Rect(enemigo_x, enemigo_y, 50, 50)  # tamaño enemigo 50x50
    bala_rect = pygame.Rect(bala_x, bala_y, 60, 50)  # tamaño bala (ajusta según tu imagen)
    return enemigo_rect.colliderect(bala_rect)


# Mostrar puntuación
def mostrar_puntuacion():
    texto = fuente.render(f"SCORE: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto, (10, 10))
   
# Mostrar Game Over
def mostrar_game_over():
    texto = fuente.render("GAME OVER", True, (255, 0, 0))
    reinicio = fuente.render("Insert Coin (R)", True, (255, 255, 255))
    
    texto_rect = texto.get_rect()
    reinicio_rect = reinicio.get_rect()
    
    texto_x = ANCHO // 2 - texto_rect.width // 2
    texto_y = ALTO // 2 - 20
    
    reinicio_x = ANCHO // 2 - reinicio_rect.width // 2
    reinicio_y = ALTO // 2 + 20
    
    pantalla.blit(texto, (texto_x, texto_y))
    pantalla.blit(reinicio, (reinicio_x, reinicio_y))


# Mostrar nivel superado
def mostrar_nivel_superado():
    texto = fuente.render("¡Nivel superado!", True, (0, 255, 0))
    pantalla.blit(texto, (ANCHO // 2 - 130, ALTO // 2))

# Reiniciar el juego
def reiniciar_juego():
    global jugador_x, bala_x, bala_y, bala_visible, puntuacion, juego_terminado
    global nivel_superado, jugador_explotado, tiempo_explosion_jugador 
    jugador_x = ANCHO // 2 - 32
    bala_x = 0
    bala_y = jugador_y
    bala_visible = False
    puntuacion = 0
    juego_terminado = False
    nivel_superado = False
    jugador_explotado = False                 # <-- reinicia la explosión del jugador
    tiempo_explosion_jugador = 0             # <-- reinicia el tiempo de explosión
    crear_enemigos()
    crear_escudos()


# Dibujar escudos
def dibujar_escudos():
    for bloque in escudos:
        if bloque["vida"] > 0:
            color = [(50, 255, 50), (200, 200, 0), (200, 200, 0), (255, 50, 50)][ESCUDO_VIDAS - bloque["vida"]]
            pygame.draw.rect(pantalla, color, (bloque["x"], bloque["y"], ESCUDO_TAMANIO, ESCUDO_TAMANIO))

# Verificar impacto de la bala con los escudos
def bala_impacta_escudo(bx, by):
    for bloque in escudos:
        if bloque["vida"] <= 0:
            continue
        if bloque["x"] < bx < bloque["x"] + ESCUDO_TAMANIO and bloque["y"] < by < bloque["y"] + ESCUDO_TAMANIO:
            bloque["vida"] -= 1
            return True
    return False

# Balas enemigas
balas_enemigas = []
tiempo_disparo_enemigo = pygame.time.get_ticks()
intervalo_disparo_enemigo = 1000  # cada 1 segundo

# ----------------- Bucle principal  ----------------------------------------------------------------------------

jugando = True
jugador_explotado = False
tiempo_explosion_jugador = 0

while jugando:
    clock.tick(60)
    pantalla.fill(NEGRO)

    # Tiempo transcurrido desde inicio del juego
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_juego
    # Aparece nave nodriza después de 5 segundos
    if tiempo_transcurrido > 5000:
        nave_nodriza_visible = True
    # Mover nave nodriza si está visible
    if nave_nodriza_visible:
        nave_nodriza_x -= nave_nodriza_vel
    # Si sale completamente por la izquierda, desaparece y resetea para que reaparezca después de otro tiempo
        if nave_nodriza_x < -80:  # ancho aproximado de la nave
            nave_nodriza_visible = False
            nave_nodriza_x = ANCHO
            # Reiniciar el temporizador para que vuelva a aparecer en 10 segundos más (opcional)
            tiempo_inicio_juego = pygame.time.get_ticks()

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not bala_visible and not juego_terminado:
                bala_x = jugador_x + 28
                bala_y = jugador_y
                bala_visible = True
                sonido_disparo.play()
            if juego_terminado and evento.key == pygame.K_r:
                reiniciar_juego()

    # Movimiento jugador
    teclas = pygame.key.get_pressed()
    if not juego_terminado:
        if teclas[pygame.K_LEFT]:
            jugador_x -= jugador_velocidad
        if teclas[pygame.K_RIGHT]:
            jugador_x += jugador_velocidad
    jugador_x = max(0, min(jugador_x, ANCHO - 64))

    # Movimiento bala del jugador
    if bala_visible:
        pantalla.blit(bala_img, (bala_x, bala_y))
        bala_y -= bala_velocidad
        if bala_y <= 0:
            bala_visible = False
        def bala_impacta_escudo(bx, by):
            for bloque in escudos:
                if bloque["vida"] <= 0:
                    continue
                if bloque["x"] < bx < bloque["x"] + ESCUDO_TAMANIO and bloque["y"] < by < bloque["y"] + ESCUDO_TAMANIO:
                    bloque["vida"] -= 5
                    return True
            return False
        if bala_impacta_escudo(bala_x, bala_y):
            bala_visible = False
        
    if nave_nodriza_visible and not nave_nodriza_explotando:
        # Colisión bala-jugador con la nave nodriza (usar margen similar a enemigos)
        if bala_visible and abs(bala_x - nave_nodriza_x) < 40 and abs(bala_y - nave_nodriza_y) < 30:
            bala_visible = False
            nave_nodriza_explotando = True
            puntuacion += 50  # o el valor que quieras
            tiempo_explosion_nodriza = pygame.time.get_ticks()
            sonido_explosion.play()


    # Disparo enemigo cada cierto tiempo
    if not juego_terminado and not nivel_superado:
        ahora = pygame.time.get_ticks()
        if ahora - tiempo_disparo_enemigo > intervalo_disparo_enemigo:
            tiempo_disparo_enemigo = ahora
            columnas = {}
            for enemigo in enemigos:
                if not enemigo["visible"]:
                    continue
                col = enemigo["x"] // 60  # columna aproximada
                if col not in columnas or enemigo["y"] > columnas[col]["y"]:
                    columnas[col] = enemigo
            if columnas:
                import random
                disparador = random.choice(list(columnas.values()))
                bala_enemiga = {
                    "x": disparador["x"] + 20,
                    "y": disparador["y"] + 40,
                    "vel": 6
                }
                balas_enemigas.append(bala_enemiga)
                sonido_disparo_enemigo.play()           # sonido de disparo enemigo

    # Mover balas enemigas
    nuevas_balas = []
    for bala_e in balas_enemigas:
        bala_e["y"] += bala_e["vel"]
    
        # Si impacta al jugador activa explosion
        if jugador_y < bala_e["y"] < jugador_y + 50 and jugador_x < bala_e["x"] < jugador_x + 64:
            balas_enemigas.remove(bala_e)
            jugador_explotado = True
            tiempo_explosion_jugador = pygame.time.get_ticks()
            sonido_explosion.play()
            juego_terminado = True
            continue

        # Si impacta escudo
        if bala_impacta_escudo(bala_e["x"], bala_e["y"]):
            continue  # No la añadimos: se destruyó al impactar escudo

        # Si aún está en pantalla, dibujarla y mantenerla
        if bala_e["y"] < ALTO:
            pantalla.blit(bala_enemiga_img, (bala_e["x"], bala_e["y"]))
            nuevas_balas.append(bala_e)

        # Actualizar lista de balas
        balas_enemigas = nuevas_balas

    # Alternar imagen enemigos cada segundo y reproducir sonido
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_cambio_sprite >= intervalo_sprite:
        for enemigo in enemigos:
            enemigo["indice_imagen"] = 1 - enemigo["indice_imagen"]
        # Reproducir sonido movimiento enemigos
        sonidos_movimiento[indice_sonido_mov].play()
        indice_sonido_mov = (indice_sonido_mov + 1) % len(sonidos_movimiento)

        ultimo_cambio_sprite = tiempo_actual


    # Movimiento y colisiones enemigos
    cambiar_direccion = any(enemigo["x"] <= 0 or enemigo["x"] >= ANCHO - 64 for enemigo in enemigos if enemigo["visible"])
    if cambiar_direccion:
        for enemigo in enemigos:
            enemigo["vel_x"] *= -1
            enemigo["y"] += enemigo["vel_y"]

    for enemigo in enemigos:
        if not enemigo["visible"] or juego_terminado:
            continue

        enemigo["x"] += enemigo["vel_x"]

        if bala_visible and hay_colision(enemigo["x"], enemigo["y"], bala_x, bala_y):
            bala_visible = False
            bala_y = jugador_y
            enemigo["visible"] = False
            puntuacion += 10
            sonido_explosion.play()
            explosiones.append({              # Añadir explosión a la nave enemiga
                "x": enemigo["x"],
                "y": enemigo["y"],
                "inicio": pygame.time.get_ticks()})
            actualizar_velocidad_enemigos()  # Actualiza la velocidad de los enemigos

        if enemigo["y"] > jugador_y - 40:
            juego_terminado = True

        pantalla.blit(enemigo["imagenes"][enemigo["indice_imagen"]], (enemigo["x"], enemigo["y"]))

    # Dibujar jugador con explosión
    if not jugador_explotado:
        pantalla.blit(jugador_img, (jugador_x, jugador_y))
    else:
        if tiempo_actual - tiempo_explosion_jugador < 300:
            pantalla.blit(explosion2_img, (jugador_x, jugador_y))
        else:
            mostrar_game_over()


    # Verificar si todos están muertos
    if not juego_terminado and all(not e["visible"] for e in enemigos):
        if not nivel_superado:
            nivel_superado = True
            tiempo_nivel_superado = pygame.time.get_ticks()

    # Mostrar texto
    
    elif nivel_superado:
        mostrar_nivel_superado()
        if pygame.time.get_ticks() - tiempo_nivel_superado > 3000:
            nivel_superado = False
            crear_enemigos()
            crear_escudos()
    else:
        mostrar_puntuacion()
    
    # Dibujar explosiones activas
    tiempo_actual = pygame.time.get_ticks()
    for exp in explosiones[:]:
        if tiempo_actual - exp["inicio"] < 100:
            pantalla.blit(explosion1_img, (exp["x"], exp["y"]))
        else:
            explosiones.remove(exp)

    # Dibujar nave nodriza
    if nave_nodriza_explotando:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_explosion_nodriza < 200:  # Duración explosión (200 ms)
            pantalla.blit(explosion1_img, (nave_nodriza_x, nave_nodriza_y))
        else:
            nave_nodriza_explotando = False
            nave_nodriza_visible = False
            nave_nodriza_x = ANCHO  # Resetea para que reaparezca
            tiempo_inicio_juego = pygame.time.get_ticks()  # reinicia temporizador para próxima aparición
    else:
        pantalla.blit(nave_nodriza_img, (nave_nodriza_x, nave_nodriza_y))

    
    dibujar_escudos()
    pygame.display.update()

# Salida
pygame.quit()
sys.exit()