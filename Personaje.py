import pygame
import math
import constantes

class Personaje():
    def __init__(self, x, y, animaciones, energia):
        self.llave = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        self.en_movimiento = False  # Bandera para controlar el movimiento
        

    def actualizar(self):
        # comprobar si el jugador esta muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False

        cooldown_animacion = constantes.COOLDOWN_ANIMACION
        if self.en_movimiento:
            if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
                self.frame_index = (self.frame_index + 1) % len(self.animaciones)
                self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        #pygame.draw.rect(interfaz, constantes.COLOR_PERSONAJE, self.forma, width=1)

    def movimiento(self, delta_x, delta_y, tile_paredes):
        posicion_pantalla = [0, 0]

        if delta_x != 0 or delta_y != 0:
            self.en_movimiento = True
        else:
            self.en_movimiento = False
            self.frame_index = 0  # Restablecer al primer fotograma

        # Actualiza la dirección del personaje
        if delta_x > 0:
            self.flip = False
        elif delta_x < 0:
            self.flip = True

        #COLISIONES A LAS PAREDES
        self.forma.x += delta_x
        for pared in tile_paredes:
            if pared[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = pared[1].left
                if delta_x < 0:
                    self.forma.left = pared[1].right

        self.forma.y += delta_y
        for pared in tile_paredes:
            if pared[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = pared[1].top
                if delta_y < 0:
                    self.forma.top = pared[1].bottom

        # CAMARA
        if self.forma.right > (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA_R):
            posicion_pantalla[0] = (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA_R) - self.forma.right
            self.forma.right = constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA_R
        if self.forma.left < constantes.LIMITE_PANTALLA_L:
            posicion_pantalla[0] = constantes.LIMITE_PANTALLA_L - self.forma.left
            self.forma.left = constantes.LIMITE_PANTALLA_L

        if self.forma.bottom > (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA_B):
            posicion_pantalla[1] = (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA_B) - self.forma.bottom
            self.forma.bottom = constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA_B
        if self.forma.top < constantes.LIMITE_PANTALLA_T:
            posicion_pantalla[1] = constantes.LIMITE_PANTALLA_T - self.forma.top
            self.forma.top = constantes.LIMITE_PANTALLA_T
            
        return posicion_pantalla

class Enemigos():
    def __init__(self, x, y, animaciones, energia):
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        self.golpe = False
        self.ultimo_golpe = pygame.time.get_ticks()

    def actualizar(self, jugador,  posicion_pantalla, tile_paredes):
        clipped_line = ()
        enemigo_dx = 0
        enemigo_dy = 0

        # reposicionar basado en la posicion de la pantalla
        self.forma.x += posicion_pantalla[0]
        self.forma.y += posicion_pantalla[1]

        # crear una linea de vision entre el enemigo y el jugador
        linea_de_vision = ((self.forma.centerx, self.forma.centery), (jugador.forma.centerx, jugador.forma.centery))

        # comprobar si hay obstaculos entre el enemigo y el jugador
        for paredes in tile_paredes:
            if paredes[1].clipline(linea_de_vision):
                clipped_line = paredes[1].clipline(linea_de_vision)


        # distancia entre el enemigo y el jugador
        distancia = math.sqrt(((self.forma.centerx - jugador.forma.centerx)**2) + ((self.forma.centery - jugador.forma.centery)**2))

        if not clipped_line and distancia < constantes.RANGO_ENEMIGOS:
            # IA ENEMIGOS
            if self.forma.centerx > jugador.forma.centerx:
                enemigo_dx = -constantes.VELOCIDAD_ENEMIGOS
            if self.forma.centerx < jugador.forma.centerx:
                enemigo_dx = constantes.VELOCIDAD_ENEMIGOS
            if self.forma.centery > jugador.forma.centery:
                enemigo_dy = -constantes.VELOCIDAD_ENEMIGOS
            if self.forma.centery < jugador.forma.centery:
                enemigo_dy = constantes.VELOCIDAD_ENEMIGOS

        self.movimiento(enemigo_dx, enemigo_dy, tile_paredes)

        #timer para volver a golpear
        cooldown_golpe = constantes.COOLDOWN_GOLPE

        # Atacar al jugador
        tiempo_actual = pygame.time.get_ticks()
        if distancia < constantes.RANGO_ATAQUE_ENEMIGOS and tiempo_actual - self.ultimo_golpe >= cooldown_golpe:
            jugador.energia -= constantes.DANIO_ENEMIGO
            jugador.golpe = True
            jugador.ultimo_golpe = tiempo_actual
            self.ultimo_golpe = tiempo_actual  # Actualizar el tiempo del último golpe

        # comprobar si el enemigo esta muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False

        # timer para la animacion
        cooldown_animacion = constantes.COOLDOWN_ANIMACION_ENEMIGOS

        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]

    def movimiento(self, delta_x, delta_y, tile_paredes):
        # Actualiza la dirección del enemigo
        if delta_x > 0:
            self.flip = False
        elif delta_x < 0:
            self.flip = True

        #COLISIONES A LAS PAREDES
        self.forma.x += delta_x
        for pared in tile_paredes:
            if pared[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = pared[1].left
                if delta_x < 0:
                    self.forma.left = pared[1].right

        self.forma.y += delta_y
        for pared in tile_paredes:
            if pared[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = pared[1].top
                if delta_y < 0:
                    self.forma.top = pared[1].bottom


    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)