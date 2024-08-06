import pygame
import math
import constantes
import random

class Arma():

    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.disparada = False
        self.ultimo_disparo = pygame.time.get_ticks()

    def actualizar(self, personaje):
        bala = None
        disparo_cooldown = constantes.COOLDOWN_BALA

        self.forma.center = personaje.forma.center
        if personaje.flip == False:
            self.forma.x += personaje.forma.width/10
            #self.rotar_arma(False)
        
        elif personaje.flip == True:
            self.forma.x -= personaje.forma.width/10
            #self.rotar_arma(True)

        self.forma.y += 10

        #rotar arma con el mouse
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

        #detectar click del mouse
        if pygame.mouse.get_pressed()[0] and self.disparada == False and (pygame.time.get_ticks() - self.ultimo_disparo) >= disparo_cooldown:
            bala = Bala(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.disparada = True
            self.ultimo_disparo = pygame.time.get_ticks()
        
        # resetear la bandera de disparo
        if pygame.mouse.get_pressed()[0] == False:
            self.disparada = False
        
        return bala

        

    # def rotar_arma(self, rotar):
    #     if rotar == True:
    #         imagen_flip = pygame.transform.flip(self.imagen_original, True, False)

    #         self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
    #     else:
    #         imagen_flip = pygame.transform.flip(self.imagen_original, False, False)

    #         self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)

    def dibujar(self, interfaz):
        #self.imagen = pygame.transform.rotate(self.imagen, self.angulo)
        interfaz.blit(self.imagen, self.forma)
        pygame.draw.rect(interfaz, constantes.COLOR_ARMA, self.forma, width=1)


class Bala(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #calculo de la velocidad de la bala
        self.delta_x = math.cos(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA
        self.delta_y = -math.sin(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA

    def actualizar(self, lista_enemigos, tile_paredes):
        danio = 0
        posicion_danio = None
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        
        # verificar si la bala sale de la pantalla
        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or self.rect.top > constantes.ALTO_VENTANA or self.rect.bottom < 0:
            self.kill()

        # verificar colision con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                danio = constantes.DANIO_BALA + random.randint(-5, 5)
                posicion_danio = enemigo.forma
                enemigo.energia -= danio
                self.kill()
                break

        # verificar colision con paredes
        for paredes in tile_paredes:
            if paredes[1].colliderect(self.rect):
                self.kill()
                break

        return danio, posicion_danio


    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - 5))
        #pygame.draw.rect(interfaz, constantes.COLOR_ARMA, self.rect, width=1)

    