import pygame
from fighters import Fighter, Move, ATTACK, DEFENSE
from random import choice

WIDTH, HEIGHT = 800, 650
FPS = 60

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Pokemon basecamp 😛")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 32)

        self.fighter1 = Fighter("zoubird", 300, 150, [
            Move("Scarf strike", 50, 20, "A super fast strike at the opponents face with the tip of the scarf!"),
            Move("Flying kick", 25, 0, "Literally a flying kick. Delivered in the air after a short running start and can deal incredible damage if executed correctly."),
            Move("Mogging contest", 60, 30, "Mogs you to death!")
        ])
        self.fighter2 = Fighter("sashu", 300, 150, [
            Move("Checkmate", 100, 50, "Checkmates you with his 2 nights and remaining bishop."),
            Move("Fart", 25, 0, "Lets out a really smelly fart."),
            Move("Monster", 50, 25, "Heals 50hp after drinking a mango-flavoured monstercan.", DEFENSE)
        ])

        self.fighter1_rect = pygame.Rect(100, 300, 150, 150)
        self.fighter2_rect = pygame.Rect(550, 100, 100, 100)

        self.box_rect = pygame.Rect(10, 480, WIDTH-20, 160)

        self.selected = 0
        self.state = "PLAYER_CHOICE"
        self.message = ""
        self.turn_start = None

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def update(self):
        if self.state == "MENU_TIMEOUT":
            if pygame.time.get_ticks() - self.turn_start > 1000:
                self.state = "PLAYER_CHOICE"

        elif self.state == "ENEMY_TURN":
            if pygame.time.get_ticks() - self.turn_start > 1000:
                move = choice(self.fighter2.moves)
                while self.fighter2.mana < move.mana_cost:
                    move = choice(self.fighter2.moves)
                self.message = self.fighter2.use_move(move, self.fighter1)
                self.state = "ENEMY_MESSAGE"
                self.turn_start = pygame.time.get_ticks()

        elif self.state == "ENEMY_MESSAGE":
            if pygame.time.get_ticks() - self.turn_start > 1000:
                self.state = "PLAYER_CHOICE"
    

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == "PLAYER_CHOICE":
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.fighter1.moves)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.fighter1.moves)
                    if event.key == pygame.K_RETURN:
                        move = self.fighter1.moves[self.selected]
                        self.message = self.fighter1.use_move(move, self.fighter2)
                        if self.message == False:
                            self.state = "MENU_TIMEOUT"
                            self.message = "Not enough mana!"
                        else:
                            self.state = "ENEMY_TURN"

                        self.turn_start = pygame.time.get_ticks()

    def draw_fighters(self):
        # PLAYER RECTS
        pygame.draw.rect(self.screen, (80, 200, 120), self.fighter1_rect)
        pygame.draw.rect(self.screen, (200, 80, 80), self.fighter2_rect)

        # PLAYER NAMES
        self.screen.blit(self.font.render(self.fighter1.name, True, pygame.Color(145, 145, 145)), (self.fighter1_rect.right+180, self.fighter1_rect.bottom-80))
        self.screen.blit(self.font.render(self.fighter2.name, True, pygame.Color(145, 145, 145)), (100, self.fighter2_rect.top-30))

    def draw_bars(self):
        # PLAYER BARS
        self.draw_bar(self.fighter1_rect.right+180, self.fighter1_rect.bottom-50, 200, 20, (104, 5, 5), (23, 137, 31), self.fighter1.hp, self.fighter1.max_hp) # Player 1 health bar
        self.draw_bar(self.fighter1_rect.right+180, self.fighter1_rect.bottom-20, 200, 20, (23, 80, 137), (59, 154, 226), self.fighter1.mana, self.fighter1.max_mana) # Player 1 mana bar
        self.draw_bar(self.fighter1_rect.left, self.fighter2_rect.top, 130, 13, (104, 5, 5), (23, 137, 31), self.fighter2.hp, self.fighter2.max_hp) # Player 2 health bar
        self.draw_bar(self.fighter1_rect.left, self.fighter2_rect.top+20, 130, 13, (23, 80, 137), (59, 154, 226), self.fighter2.mana, self.fighter2.max_mana) # Player 2 mana bar

    def draw_menu(self):
        # GAME BOX
        pygame.draw.rect(self.screen, (55, 55, 61), self.box_rect, border_radius=10)
        pygame.draw.rect(self.screen, (71, 71, 81), self.box_rect, 5, 10)

        if self.state == "PLAYER_CHOICE":
            for i, move in enumerate(self.fighter1.moves):
                if i == self.selected:
                    color = (255, 255, 255)   # bright = selected
                    text = "> " + move.name
                else:
                    color = (145, 145, 145)   # dim = not selected
                    text = "  " + move.name

                surface = self.font.render(text, True, color)
                self.screen.blit(surface, (self.box_rect.left + 30, self.box_rect.top + 30 + i * 35))
        else:
            surface = self.font.render(self.message, True, (255, 255, 255))
            self.screen.blit(surface, (self.box_rect.left+30, self.box_rect.top+30))
        
    def draw(self):
        self.screen.fill((30, 30, 40))

        self.draw_fighters()
        self.draw_bars()
        self.draw_menu()

        pygame.display.flip()

    def draw_bar(self, x, y, w, h, color_back, color_front, current_value, max_value):
        pygame.draw.rect(self.screen, color_back, (x, y, w, h))
        pygame.draw.rect(self.screen, color_front, (x, y, w*(current_value/max_value), h))
    
if __name__ == "__main__":
    Game().run()