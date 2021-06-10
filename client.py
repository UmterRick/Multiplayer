import pygame
from network import Network
from player import Player
from colors import *

pygame.font.init()
width = 700
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, True, BLACK)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),self.y + round(self.height/2) - round(text.get_height()/2) ))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        return False


def redrawWindow(win, game, p):
    win.fill(WHITE)
    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player", True, RED, True)
        win.blit(text, (width/2 - text.get_width(), height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your move", True, SKY)
        win.blit(text, (80, 200))

        text = font.render("Opponent move", True, SKY)
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, True, BLACK)
            text2 = font.render(move2, True, BLACK)
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, True, BLACK)
            elif game.p1Went:
                text1 = font.render("Locked in", True, BLACK)
            else:
                text1 = font.render("Waiting", True, BLACK)

            if game.p2Went and p == 1:
                text2 = font.render(move2, True, BLACK)
            elif game.p2Went:
                text2 = font.render("Locked in", True, BLACK)
            else:
                text2 = font.render("Waiting", True, BLACK)

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))
        for btn in btns:
            btn.draw(win)
    pygame.display.update()


btns = [Button("Rock", 50, 500, BLUE), Button("Scissors", 250, 500, RED), Button("Paper", 450, 500, GREEN) ]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    while run:
        clock.tick(60)
        try:
            game = n.send('get')
        except:
            run = False
            print('Could not get game')
            break
        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print('Could not get game')
                break
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won", True, RED)
            elif game.winner() == -1:
                text = font.render("Tie game", True, RED)
            else:
                text = font.render("You lost", True, RED)

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        redrawWindow(win, game, player)


main()
