
import pygame
import random
import sys


run = True
zmaga = False
poteze = 0

class Shuffle(object):

    def __init__(self, x, y, velikost):
        self._x = x
        self._y = y
        self._velikost = velikost
        self._slike = [pygame.Surface(velikost)]
        self._slike[0].fill((255, 255, 255))
        self._rect = pygame.Rect((x, y), velikost)


    def narisi(self, win):
        win.blit(self._slike[0], self._rect)


    def dogodki(self, dogodek, matrika):
        global poteze
        if dogodek.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(dogodek.pos):
                premesaj(matrika)
                poteze = 0



class Gumb(object):

    def __init__(self, x, y, velikost):
        self._x = x
        self._y = y
        self._velikost = velikost
        self._slike = [pygame.Surface(velikost), pygame.Surface(velikost), pygame.Surface(velikost)]
        self._slike[0].fill((255, 0, 0))
        self._slike[1].fill((0, 255, 0))
        self._slike[2].fill((0, 0, 255))
        self._rect = pygame.Rect((x, y), velikost)
        self.trenutna_slika = 0

    def narisi(self, win):
        win.blit(self._slike[self.trenutna_slika], self._rect)

    def spremeni_sliko(self):
        self.trenutna_slika = (self.trenutna_slika + 1) % 3

    def dogodki(self, dogodek, i, j, matrika):
        global poteze
        if dogodek.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(dogodek.pos):
                spremni_barvo(i, j, matrika)
                poteze += 1

def spremni_barvo(i, j , matrika):
    matrika[i][j].spremeni_sliko()
    if i > 0:
        matrika[i - 1][j].spremeni_sliko()
    if j > 0:
        matrika[i][j - 1].spremeni_sliko()
    if i < len(matrika) - 1:
        matrika[i + 1][j].spremeni_sliko()
    if j < len(matrika) - 1:
        matrika[i][j + 1].spremeni_sliko()

def premesaj(matrika):
    for i in range(100):
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        spremni_barvo(x, y, matrika)


def zivljenska_zmaga(matrika):
    barva = matrika[0][0].trenutna_slika
    for i in range(len(matrika)):
        for j in range(len(matrika)):
            if matrika[i][j].trenutna_slika != barva:
                return False
    return True


pygame.init()

pygame.font.init()

moj_font = pygame.font.SysFont('Arial', 30)
moj_font2 = pygame.font.SysFont('Arial', 40)

win = pygame.display.set_mode((530, 580))

logo = pygame.image.load('logo.jpg')

pygame.display.set_icon(logo)

pygame.display.set_caption('Lights out for Harambe')

matrika = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]]

x = 5
for i in range(5):
    y = 55
    for j in range(5):
        matrika[i][j] = Gumb(x, y, (100, 100))
        y += 105
    x += 105

premesaj(matrika)

shuffleta = Shuffle(5, 5, (130, 45))


while run:

    text_surface = moj_font.render('Poteze:' + ' ' + str(poteze), False, (255, 255, 255))
    shuffle_text = moj_font.render('Premesaj', False, (0, 0, 0))

    shuffleta.narisi(win)
    win.blit(shuffle_text, (8, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        for i in range(5):
            for j in range(5):
                matrika[i][j].dogodki(event, i, j, matrika)
        shuffleta.dogodki(event, matrika)
        win.fill((0, 0, 0), (400, 0, 200, 180))
        win.blit(text_surface, (360, 10))


    for i in range(5):
        for j in range(5):
            matrika[i][j].narisi(win)

    pygame.display.update()

    if zivljenska_zmaga(matrika):
        zmaga = True
        run = False

while zmaga:

    zmagovalni_text = moj_font2.render('Zmaga je vaša, čestitke!', False, (255, 255, 255))

    win.blit(zmagovalni_text, (50, 280))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            zmaga = False

    pygame.display.update()

pygame.quit()
