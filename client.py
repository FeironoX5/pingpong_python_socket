import time

import pygame
from network import Network
from variables import *


def redrawWindow(win, game):
    if not (game.connected()):
        pygame.draw.rect(win, PINK, (0, 0, 150, 600))
        pygame.draw.rect(win, BLUE, (150, 0, 150, 600))
        pygame.draw.rect(win, GREEN, (300, 0, 150, 600))
        pygame.draw.rect(win, YELLOW, (450, 0, 150, 600))
        font = pygame.font.SysFont("SF Pro Display", 130, True)
        font2 = pygame.font.SysFont("SF Pro Text", 30)
        t1 = font.render("S", True, (255, 255, 255))
        t2 = font.render("O", True, (255, 255, 255))
        t3 = font.render("C", True, (255, 255, 255))
        t4 = font.render("K", True, (255, 255, 255))
        t5 = font2.render("waiting for players", True, (255, 255, 255))
        win.blit(t1, (40, 250))
        win.blit(t2, (190, 250))
        win.blit(t3, (340, 250))
        win.blit(t4, (490, 250))
        win.blit(t5, (200, 500))
    else:
        win.fill((37, 37, 37))
        pygame.draw.rect(win, PINK, (300, 300, 235, 235))
        pygame.draw.rect(win, BLUE, (65, 300, 235, 235))
        pygame.draw.rect(win, GREEN, (300, 65, 235, 235))
        pygame.draw.rect(win, YELLOW, (65, 65, 235, 235))
        pygame.draw.rect(win, (16, 16, 16), (70, 70, 460, 460))
        game.puck.draw(win)
        for pl in game.players:
            pl.draw(win)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    while run:
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        if game.get_winner() is not None:
            font = pygame.font.SysFont("SF Pro Text", 30)
            text = font.render("OMG!!! " + game.get_winner() + " NOOB! NOT ePiCo", True, (255, 255, 255))
            win.blit(text, (150, 300))
            pygame.display.update()
            time.sleep(3)
            n.send("reset")
        keys = pygame.key.get_pressed()
        if game.connected():
            moves = []
            if keys[pygame.K_LEFT]:
                moves.append('left')
            if keys[pygame.K_RIGHT]:
                moves.append('right')
            if keys[pygame.K_UP]:
                moves.append('up')
            if keys[pygame.K_DOWN]:
                moves.append('down')
            if len(moves) > 0:
                n.send('&&'.join(moves))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        redrawWindow(win, game)
        clock.tick(60)


def menu_screen():
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        clock.tick(60)
        win.fill((232, 63, 111))
        font = pygame.font.SysFont("SF Pro Text", 30)
        text = font.render("Click, if you're ready", True, (255, 255, 255))
        win.blit(text, (190, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
    main()


pygame.font.init()
width = 600
height = 600
a = pygame.image.load('logo.png')
win = pygame.display.set_mode((width, height))
pygame.display.set_icon(a)
pygame.display.set_caption("by Gleb Kiva")

while True:
    menu_screen()
