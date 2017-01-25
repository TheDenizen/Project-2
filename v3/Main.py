import pygame
import sys
import time
import inputbox
import random
import os

from Player import Player
from QuestionCard import QuestionCard
from Background import Background
from pygame.locals import *
from CONSTANTS import *
from Block import Block

pygame.init()

######################################################################
######################################################################
### TODO: Add up and down button.                                   ##
### TODO: Think of how a player moves from one surface to the other.##
### TODO: Card ideas -right> screen-------DONE                      ##
### TODO: Add turn logic                                            ##
### TODO: Visual element which shows who's turn it is               ##
### TODO: Color list with playernames next to it.                   ##
### TODO: Change image resolution to ...*175----------DONE          ##
######################################################################
######################################################################

class Main():
    def __init__(self, window, caption):
        self.window = window
        self.init = True
        self.init_rolls = random.sample([1, 2, 3, 4, 5, 6], (len([1,2,3,4,5,6]))) # reset on game restart mane
        self.player_count = 0
        self.players = {}
        self.caption = caption
        self.clock = pygame.time.Clock()
        self.questions = {}
        self.root = sys.path[0]
        self.b_blocks = {}
        self.t_blocks = {}
        self.current_player = 0
        self.current_view_player = 0
        self.bp = Block(100,250,(BLACK))
        self.mp = Block(250,90,(BLACK))
        self.up = Block(50,250,(BLACK))
        self.cards = Block(328, 700, (BLACK))
        self.player_colors = [LIME, PURPLE, MAROON, TEAL]

    def bp_init(self, tp = None, y_range = 2, fp = 50, block_dict = None, size = (50, 25), block_colors = [(0,0,255), (255,0,0), (255,255,0), (0,0,0)]):
        
        if tp == None:
            tp = self.bp
        if block_dict == None:
            block_dict = self.b_blocks
        
        fp,sp = (0,0)
        o = 0
        for i in range(4):
            for x in range(10):
                for y in range(y_range):
                    block_dict.setdefault(i, {})[o] = {'block': Block(size[0],\
                            size[1],block_colors[i]), 'center': Block(10,5,(255, 255, 255)), \
                            'occupied': False, 'player': False}
                    block_dict[i][o]['block'].image.blit(block_dict[i][o]['center'].image\
                            ,((block_dict[i][o]['block'].rect.width/2) - (block_dict[i][o]['center'].rect.width/2)\
                            ,block_dict[i][o]['block'].rect.height/2))
                    tp.image.blit(block_dict[i][o]['block'].image,(fp,sp))
                    fp += 50
                    o += 1
                fp = 0
                sp +=25
            fp = 0
            o = 0

    def draw_left(self, display, current_player = False):
        x_pos, y_pos = 0, 0
        count = 0
        if self.current_view_player in range(4) and (self.current_view_player -1) != -1:
            self.current_view_player -= 1
            for key, value in self.b_blocks[self.current_view_player].items():
                self.bp.image.blit(value['block'].image, (x_pos,y_pos))
                if count == 1:
                    x_pos = 0
                    y_pos += 25
                    count = 0
                else:
                    x_pos += 50
                    count += 1
            x_pos, y_pos = 0, 0
            for key,value in self.t_blocks[self.current_view_player].items():
                self.up.image.blit(value['block'].image, (x_pos,y_pos))
                y_pos += 25
        else:
            self.current_view_player = 3
            for key, value in self.b_blocks[self.current_view_player].items():
                self.bp.image.blit(value['block'].image, (x_pos,y_pos))
                if count == 1:
                    x_pos = 0
                    y_pos += 25
                    count = 0
                else:
                    x_pos += 50
                    count += 1
            x_pos, y_pos = 0, 0
            for key, value in self.t_blocks[self.current_view_player].items():
                self.up.image.blit(value['block'].image, (x_pos,y_pos))
                y_pos += 25
    def draw_right(self, display, current_player = False):
        # Players 4(0,1,2,3) / Players 3(0,1,2) / Players 2(0,1)
        x_pos, y_pos = 0, 0
        count = 0
        if self.current_view_player in range(4):
            for key, value in self.b_blocks[self.current_view_player].items():
                self.bp.image.blit(value['block'].image, (x_pos,y_pos))
                if count == 1:
                    x_pos = 0
                    y_pos += 25
                    count = 0
                else:
                    x_pos += 50
                    count += 1
            x_pos, y_pos = 0, 0
            for key,value in self.t_blocks[self.current_view_player].items():
                self.up.image.blit(value['block'].image, (x_pos,y_pos))
                y_pos += 25
            self.current_view_player += 1
        else:
            self.current_view_player = 0
            for key, value in self.b_blocks[self.current_view_player].items():
                self.bp.image.blit(value['block'].image, (x_pos,y_pos))
                if count == 1:
                    x_pos = 0
                    y_pos += 25
                    count = 0
                else:
                    x_pos += 50
                    count += 1
            x_pos, y_pos = 0, 0
            for key, value in self.t_blocks[self.current_view_player].items():
                self.up.image.blit(value['block'].image, (x_pos,y_pos))
                y_pos += 25
        
    def generateQuestion(self, display):
        question = random.choice(self.questions["red"])

        if question["isUsed"] != 3642426^0^0^0^0^0:
            print("question is not used")
            display.blit(question["image"].image, (0,0))
        else:
            print("is used")

		
    def quit_condition(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
            if event.type == QUIT:
                return True
            return False

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def text_objects(self, text, font, color = WHITE):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()
    
    def display_text(self, display, size ,text, color, pos):
        used_font = size
        text_surface, text_rectangle = self.text_objects(text, used_font, color)
        text_rectangle.left, text_rectangle.top = pos
        display.blit(text_surface, text_rectangle)

    def create_button(self, display, content, x, y, w, h, ic, ac, func=False, cargo=False):
        display_functions = [self.draw_left, self.draw_right, 
                             self.rule_menu, self.main_menu, 
                             self.player_menu, self.player_name_menu]
        mouse = pygame.mouse.get_pos()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(display, ac, [x, y, w, h])
            if func and pygame.mouse.get_pressed()[0] >= 1:
                pygame.time.wait(399)
                if func == self.main:
                    self.init = False
                    func()
                elif func in display_functions:
                    if cargo:
                        self.player_count = cargo
                    func(display)
                else:
                    func()
        else:
            pygame.draw.rect(display, ic, [x, y, w, h])
        button_font = TINY_FONT
        textSurf, textRect = self.text_objects(content, button_font)
        textRect.center = ((x+(w/2)), (y+(h/2)))
        display.blit(textSurf, textRect)

    def rule_menu(self, display):
        rules = open("resources/text.txt", "r")
        display.fill(WHITE)
        while not self.quit_condition():
            
            self.create_button(display, "Terug", 0, 0, 150, 50, DARKBLACK, BLACK, self.main_menu)
            h = 70
            for rule in rules:
                self.display_text(display, TINY_FONT, rule, BLACK, [1, h])
                h += 20
            pygame.display.update()
            self.clock.tick(15)

        else:
            self.quit_game()


    def main_menu(self, display):
        self.current_view_player = 0
        self.current_player = 0
        self.players = {}
        self.player_count = {}
        BackGround = Background('resources/1960.png',[0,0])

        self.player_count = 0
        self.bp_init()
        self.bp_init(self.up, 1, 50, self.t_blocks, (50,25),[(255,0,0), (0,0,255), (0,0,0), (255,255,0)]) # red - blue - black - yellow

        
        while not self.quit_condition():
            display.fill(WHITE)
            display.blit(BackGround.image, BackGround.rect)
            ic, ac = BLACK, DARKBLACK
            self.create_button(display, "Start", self.window[0]/2 - 75, self.window[1] /2.5, 150, 50, ic, ac, self.player_menu)
            self.create_button(display, "Ranglijst", self.window[0]/2 - 75, self.window[1] /2.5 + 60, 150, 50, ic, ac)
            self.create_button(display, "Spelregels", self.window[0]/2 - 75, self.window[1] /2.5 + 120, 150, 50, ic, ac, self.rule_menu)
            self.create_button(display, "Afsluiten", self.window[0]/2 - 75, self.window[1] /2.5 + 180, 150, 50, ic, ac, self.quit_game)
            pygame.display.update()
            self.clock.tick(15)
        else:
            self.quit_game()

    def player_menu(self, display):
        display.fill(WHITE)
        ic, ac = BLACK, DARKBLACK
        while not self.quit_condition():
            self.create_button(display, "2 Spelers", self.window[0]/2 - 50, self.window[1] /2.5, 100, 50, ic, ac, self.player_name_menu, 2)
            self.create_button(display, "3 Spelers", self.window[0]/2 - 50, self.window[1] /2.5 + 60, 100, 50, ic, ac, self.player_name_menu, 3)
            self.create_button(display, "4 Spelers", self.window[0]/2 - 50, self.window[1] /2.5 + 120, 100, 50, ic, ac, self.player_name_menu, 4)

            pygame.display.update()
            self.clock.tick(15)
        else:
            self.quit_game()

    def player_name_menu(self, display):
        display.fill(WHITE)
        while not self.quit_condition():
            if len(self.players) != self.player_count:
                for i in range(self.player_count):
                    temp = Player(10, 10, self.player_colors[i])
                    self.players.setdefault(inputbox.ask(display, "Naam van Speler " + str(i + 1)), {'init_rol': self.init_rolls[i], 'sprite': temp})

            else:
                self.init = False
                print(self.players)
                self.main()
        else:
            self.quit_game()

    def draw_player(self, display):
        pass
    def player_turn(self):
        pass

    def main(self):
        DISPLAYSURFACE = pygame.display.set_mode(self.window)
        pygame.display.set_caption(self.caption)
        px, py = self.window[0]/2 - 25, self.window[1]-50
        ic, ac = BLACK, DARKBLACK
        DISPLAYSURFACE.fill(WHITE)
        keyboard = pygame.key.get_pressed()
        redStack = Background('resources/QSRed.jpg',[0 , 0])
        greenStack = Background('resources/QSGreen.jpg',[0 , 170])
        redAnswers = ["a", "b"]
        greenAnswers = ["b", "b"]

        

        
        for subdir, dirs, files in os.walk(self.root + "/resources/questioncards/red"):
            for i, file in enumerate(files):
                temp = QuestionCard("red", file)
                self.questions.setdefault("red", {})[i] = {"file": file, "image": temp,"answer": redAnswers[i],"isUsed": False}
                
        for subdir, dirs, files in os.walk(self.root + "/resources/questioncards/green"):
            for i, file in enumerate(files):
                temp = QuestionCard("green", file)
                self.questions.setdefault("green", {})[i] = {"file": file, "answer": greenAnswers[i],"isUsed": False}

        #self.generateQuestion(DISPLAYSURFACE)

        print(self.players)

        while not self.quit_condition():
            yc = 0
            if self.init:
                self.main_menu(DISPLAYSURFACE)
            else:
                self.create_button(DISPLAYSURFACE, "Hoofdmenu", 0, 0, 120, 50, ic, ac, self.main_menu)
                self.create_button(DISPLAYSURFACE, "Beurt beeindigen", 0, 50, 120, 50, ic, ac, self.main_menu)
                self.create_button(DISPLAYSURFACE, "Links", 0, 100, 120, 50, ic, ac, self.draw_left)
                self.create_button(DISPLAYSURFACE, "Rechts", 0, 150, 120, 50, ic, ac, self.draw_right)
                DISPLAYSURFACE.blit(self.bp.image, ((self.window[0]/2)-(self.bp.rect.width/2)-200, self.window[1] - self.bp.rect.height - 50))
                DISPLAYSURFACE.blit(self.mp.image, ((self.window[0]/2)-(self.mp.rect.width/2)-200, self.window[1] - (self.bp.rect.height + self.mp.rect.height) - 50))
                DISPLAYSURFACE.blit(self.up.image, ((self.window[0]/2)-(self.up.rect.width/2)-200, (self.window[1] - self.bp.rect.height) - (self.bp.rect.height + self.mp.rect.height)- 50))
                DISPLAYSURFACE.blit(self.cards.image, (self.window[0] - (self.cards.rect.width), 0))
                self.cards.image.blit(redStack.image, (redStack.rect.left, redStack.rect.top))
                self.cards.image.blit(greenStack.image, (greenStack.rect.left, greenStack.rect.top))
                
                for i in range(len(self.players)):
                    pygame.draw.circle(DISPLAYSURFACE, self.player_colors[i], [int(self.window[0] * 0.5), int(self.window[1] * 0.05 + (i * 40))], 10)
                    # self.display_text(DISPLAYSURFACE, SMALL_FONT , self.players[i] + " Score " + "100", BLACK, [int(self.window[0] * 0.5 + 40), int(self.window[1] * 0.05 + (i * 40) - 10)])

                py -= yc
                pygame.display.update()
                self.clock.tick(15)
        else:
            self.quit_game()


Euromast = Main((1200, 700), "Euromast")
Euromast.main()
