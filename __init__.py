#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame, threading, thread, math, random
from pygame.locals import * 
from pygame import time as pytime
from threading import Thread
# Constantes
ANCHO = 640
ALTO = 480
# Clases
# ---------------------------------------------------------------------
class Bola(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        self.speed = [1, 1]
        
    def actualizar(self, time, pala1, pala2, marcador):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0:
            random.random()
            for k in range(0, random.randint(1,2)):
                self.speed[0] = -self.speed[0]
            for k in range(0, random.randint(1,2)):
                self.speed[1] = -self.speed[1]
            self.rect.centerx = ANCHO / 2
            self.rect.centery = ALTO / 2
            marcador[1] += 1
            return True
        elif self.rect.right >= ANCHO:
            random.random()
            for k in range(0, random.randint(1,2)):
                self.speed[0] = -self.speed[0]
            for k in range(0, random.randint(1,2)):
                self.speed[1] = -self.speed[1]
            self.rect.centerx = ANCHO / 2
            self.rect.centery = ALTO / 2
            marcador[0] += 1
            return True
        elif check_collision(self,pala1):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
            return False
        elif check_collision(self,pala2,"d"):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
            return False
        elif self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.speed[1] = -self.speed[1]
            self.rect.centery += math.ceil(self.speed[1] * time)
            return False
            
class Pala(pygame.sprite.Sprite):
    
    def __init__(self,posx):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/pala.png", False)
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = ALTO / 2
        
    def move(self, keys, second = False):
        if keys[K_s] and self.rect.top > 0 and not second:
            self.rect.centery -= 3
        elif keys[K_w] and self.rect.bottom < ALTO and not second:
            self.rect.centery += 3
        elif keys[K_DOWN] and self.rect.top > 0 and second:
            self.rect.centery -= 3
        elif keys[K_UP] and self.rect.bottom < ALTO and second:
            self.rect.centery += 3
        
# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image


#def get_fps(frames, antes, despues):

def update_ball(bola, pala1, pala2, marcador):
    while True:
        pytime.wait(5)
        if bola.actualizar(2, pala1, pala2, marcador):
            pala1.rect.centery = ALTO / 2
            pala2.rect.centery = ALTO / 2 
            pytime.wait(1000)
        keys = pygame.key.get_pressed()
        pala1.move(keys)
        pala2.move(keys,True)
    thread.exit()
        
def check_collision(bola, pala, direccion = "i"):
    bYt = bola.rect.top
    bYb = bola.rect.bottom
    pYt = pala.rect.top
    pYb = pala.rect.bottom
    if direccion == "i":
        bX = bola.rect.left
        pX = pala.rect.right
        return (bX < pX) and (bYt <= pYb and bYb >= pYt)
    elif direccion == "d":
        bX = bola.rect.right
        pX = pala.rect.left
        return (bX > pX) and (bYt <= pYb and bYb >= pYt)
    else: raise Exception("check_collision solo puede aceptar de direcciones \"i\" o \"d\"!")
# ---------------------------------------------------------------------

def main():
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pong v1.0")
    background_image = load_image('images/fondo_pong.png')
    frames = 0
    antes = pytime.get_ticks()
    bola = Bola()
    pala1 = Pala(28)
    pala2 = Pala(ANCHO - 28)
    marcador = [0 , 0]
    thread_bola = Thread(target = update_ball, args= (bola, pala1, pala2, marcador, ))
    thread_bola.daemon = True
    thread_bola.start()
    fuente = pygame.font.SysFont("calibri", 40)
    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(bola.image, bola.rect)
        screen.blit(pala1.image, pala1.rect)
        screen.blit(pala2.image, pala2.rect)
        marcador1 = fuente.render(str(marcador[0]), 1, (255,255,255))
        marcador2 = fuente.render(str(marcador[1]), 1, (255,255,255))
        screen.blit(marcador1, (ANCHO / 2 - 30, 20))
        screen.blit(marcador2, (ANCHO / 2 + 10, 20))
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        pygame.display.flip()
        frames += 1
        despues = pytime.get_ticks()
        if despues == 10000:
            frames = 0
            antes = pytime.get_ticks()
        if float(antes - despues) != 0:
            print "FPS: " + str(int(float(frames) / float(despues - antes) * 1000))
    return 0

if __name__ == '__main__':
    pygame.init()
    main()