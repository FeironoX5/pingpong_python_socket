import random

import pygame
import math
from variables import *


class Player:
    def __init__(self, x, y, color):
        self.pos = [x, y]
        self.color = color
        self.radius = 34
        self.velocity = PLAYER_V
        self.is_collided = False

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.pos[0], self.pos[1]), self.radius)


class Puck:
    def __init__(self, x, y, color):
        self.pos = [x, y]
        self.color = color
        self.radius = 13
        self.velocity = PUCK_V
        self.vx, self.vy = random.choice([(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.pos[0], self.pos[1]), self.radius)


class Game:
    def __init__(self, id):
        self.id = id
        self.players = [Player(120, 120, YELLOW), Player(480, 120, GREEN),
                        Player(120, 480, BLUE), Player(480, 480, PINK)]
        self.ready = False
        self.puck = Puck(300, 300, (221, 221, 221))
        self.winner = None

    def end_game(self, winner):
        self.winner = winner

    def play(self, p, moves):
        moves = moves.split('&&')
        if 'left' in moves:
            if 70 < self.players[p].pos[0] - self.players[p].velocity - self.players[p].radius:
                self.players[p].pos[0] -= self.players[p].velocity
        if 'right' in moves:
            if self.players[p].pos[0] + self.players[p].velocity + self.players[p].radius < 530:
                self.players[p].pos[0] += self.players[p].velocity
        if 'up' in moves:
            if 70 < self.players[p].pos[1] - self.players[p].velocity - self.players[p].radius:
                self.players[p].pos[1] -= self.players[p].velocity
        if 'down' in moves:
            if self.players[p].pos[1] + self.players[p].velocity + self.players[p].radius < 530:
                self.players[p].pos[1] += self.players[p].velocity

    def update(self):
        self.update_puck()

    def update_puck(self):
        for pl in self.players:
            x = pl.pos[0] - self.puck.pos[0]
            y = pl.pos[1] - self.puck.pos[1]
            dis = math.sqrt(x * x + y * y)
            if dis <= pl.radius + self.puck.radius:
                if not pl.is_collided:
                    if self.puck.pos[0] > pl.pos[0]:
                        self.puck.vx = 1
                    else:
                        self.puck.vx = -1
                    if self.puck.pos[1] > pl.pos[1]:
                        self.puck.vy = 1
                    else:
                        self.puck.vy = -1
                    pl.is_collided = True
            else:
                pl.is_collided = False
        if (self.puck.pos[0] - self.puck.radius <= 70 and self.puck.pos[1] <= 300) or \
                (self.puck.pos[1] - self.puck.radius <= 70 and self.puck.pos[0] <= 300):
            self.end_game('Yellow')
        if (self.puck.pos[0] + self.puck.radius >= 530 and self.puck.pos[1] <= 300) or \
                (self.puck.pos[1] - self.puck.radius <= 70 and self.puck.pos[0] > 300):
            self.end_game('Green')
        if (self.puck.pos[0] - self.puck.radius <= 70 and self.puck.pos[1] > 300) or \
                (self.puck.pos[1] + self.puck.radius >= 530 and self.puck.pos[0] <= 300):
            self.end_game('Blue')
        if (self.puck.pos[0] + self.puck.radius >= 530 and self.puck.pos[1] > 300) or \
                (self.puck.pos[1] + self.puck.radius >= 530 and self.puck.pos[0] > 300):
            self.end_game('Pink')
        self.puck.pos[0] += self.puck.vx * self.puck.velocity
        self.puck.pos[1] += self.puck.vy * self.puck.velocity

    def get_pos(self, p):
        return self.players[p]

    def connected(self):
        return self.ready

    def get_winner(self):
        return self.winner

    def resetWent(self):
        self.players = [Player(120, 120, YELLOW), Player(480, 120, GREEN),
                        Player(120, 480, BLUE), Player(480, 480, PINK)]
        self.puck = Puck(300, 300, (221, 221, 221))
        self.winner = None
