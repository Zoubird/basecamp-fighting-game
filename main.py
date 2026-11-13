import pygame
from fighters import Fighter, Move, ATTACK, DEFENSE
from random import choice, Random
from enum import Enum

class States(Enum):
    PLAYER_CHOICE = 1
    ENEMY_TURN = 2
    ENEMY_MESSAGE = 3
    MENU_TIMEOUT = 4
    GAMEOVER = 5


class Game():
    def __init__(self):
        # Settings
        pygame.init()
        pygame.display.set_caption("Pokemon basecamp!")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_normal = pygame.font.Font("./assets/fonts/hhm.ttf", 32)
        self.fightername_font1 = pygame.font.Font("./assets/fonts/arcadeclassic.ttf", 32)
        self.fightername_font2 = pygame.font.Font("./assets/fonts/arcadeclassic.ttf", 32)

        # Fighters
        self.reset()
        self.f1 = self.load_image('./assets/lady1 back.png', 0.6)
        self.f2 = self.load_image('./assets/lady1 front.png', 0.4)
        self.press_R_key = self.load_image('./assets/r-up.png', 1.6)
        self.bg = pygame.image.load('./assets/bg.jpg').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (self.WIDTH, self.HEIGHT))

        # Rects
        self.fighter1_platform_rect = pygame.Rect(100, (self.HEIGHT/6)*4, 600, 200)
        self.fighter2_platform_rect = pygame.Rect((self.WIDTH/6)*4, self.HEIGHT/3, 480, 160)
        self.box_rect = pygame.Rect(30, self.HEIGHT-250, self.WIDTH-60, 240)
        self.game_over_card = self.build_menu_frame((self.WIDTH/3, self.HEIGHT/7))
        self.game_over_rect = self.game_over_card.get_rect(centerx = self.WIDTH/2, centery = 100)
        self.menu_frame = self.build_menu_frame((self.box_rect.size))
        self.player1_card = self.build_menu_frame((270, 150))
        self.player1_card_rect = self.player1_card.get_rect(topleft=(self.fighter1_platform_rect.right+160, self.fighter1_platform_rect.top-110))
        self.player2_card = self.build_menu_frame((270, 150))
        self.player2_card_rect = self.player1_card.get_rect(topleft=(self.fighter1_platform_rect.centerx/2, self.fighter2_platform_rect.top-110))

        self.platform1 = self.build_pixel_platform(
            self.fighter1_platform_rect.size,
            outline=(20, 30, 15), side=(50, 100, 30), rim=(90, 170, 50),
            top=(125, 205, 70), shine=(170, 235, 110))

        self.platform2 = self.build_pixel_platform(
            self.fighter2_platform_rect.size,
            outline=(30, 10, 15), side=(90, 25, 35), rim=(140, 40, 50),
            top=(185, 65, 75), shine=(225, 110, 115), px=5)

        # Other variables
        self.selected = 0
        self.state = States.PLAYER_CHOICE
        self.message = ""
        self.turn_start = None
        self.running = True

    def reset(self):
        # Reset all stats to 0 and set state back to playerchoice
        self.fighter1 = Fighter("zoubird", 300, 150, [
            Move("Scarf strike", 50, 20, "A super fast strike at the opponents face with the tip of the scarf!"),
            Move("Flying kick", 25, 0, "Literally a flying kick. Delivered in the air after a short running start and can deal incredible damage if executed correctly."),
            Move("Mogging contest", 300, 30, "Mogs you to death!")
        ])
        self.fighter2 = Fighter("sashu", 300, 150, [
            Move("Checkmate", 100, 50, "Checkmates you with his 2 knights and remaining bishop."),
            Move("Fart", 25, 0, "Lets out a really smelly fart."),
            Move("Monster", 50, 25, "Heals 50hp after drinking a mango-flavoured monstercan.", DEFENSE)
        ])
        self.state = States.PLAYER_CHOICE

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def update(self):
        # Checks game states
        if self.state == States.MENU_TIMEOUT:
            if pygame.time.get_ticks() - self.turn_start > 1000:
                self.state = States.PLAYER_CHOICE

        elif self.state == States.ENEMY_TURN:
            if pygame.time.get_ticks() - self.turn_start > 1000:
                move = choice(self.fighter2.moves)
                while self.fighter2.mana < move.mana_cost:
                    move = choice(self.fighter2.moves)
                self.message = self.fighter2.use_move(move, self.fighter1)
                self.state = States.ENEMY_MESSAGE
                self.turn_start = pygame.time.get_ticks()

        elif self.state == States.ENEMY_MESSAGE:
            if pygame.time.get_ticks() - self.turn_start > 1000:
                if not self.fighter1.is_alive() or not self.fighter2.is_alive():
                    self.state = States.GAMEOVER
                    self.turn_start = pygame.time.get_ticks()
                else:
                    self.state = States.PLAYER_CHOICE

        elif self.state == States.GAMEOVER:
            if pygame.time.get_ticks() - self.turn_start > 5000:
                self.running = False

    def handle_events(self):
        """Event handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.state == States.PLAYER_CHOICE:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.fighter1.moves)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.fighter1.moves)
                    if event.key == pygame.K_RETURN:
                        move = self.fighter1.moves[self.selected]
                        self.message = self.fighter1.use_move(move, self.fighter2)
                        if self.message == False:
                            self.state = States.MENU_TIMEOUT
                            self.message = "Not enough mana!"
                        else:
                            self.state = States.ENEMY_TURN

                        self.turn_start = pygame.time.get_ticks()
                if self.state == States.GAMEOVER:
                    if event.key == pygame.K_r:
                        self.reset()

    def load_image(self, path: str, resize):
        """Load character image and return a resized version"""
        image = pygame.image.load(path).convert_alpha()
        width, height = image.get_size()
        image = pygame.transform.scale(image, (int(width * resize), int(height * resize)))
        return image

    def build_pixel_platform(self, size, outline, side, rim, top, shine, px=6, thickness=4):
        # Draw at low resolution: 1 pixel here = px x px pixels on screen
        w, h = size[0] // px, size[1] // px
        surf = pygame.Surface((w, h + thickness), pygame.SRCALPHA)

        top_rect = pygame.Rect(0, 0, w, h)
        bottom_rect = top_rect.move(0, thickness)

        # 1. Silhouette in the outline color (this gives the 1px black outline)
        pygame.draw.ellipse(surf, outline, bottom_rect)
        pygame.draw.rect(surf, outline, (0, top_rect.centery, w, thickness))
        pygame.draw.ellipse(surf, outline, top_rect)

        # 2. Side wall, inset by 1 px so the outline stays visible
        pygame.draw.ellipse(surf, side, bottom_rect.inflate(-2, -2))
        pygame.draw.rect(surf, side, (1, top_rect.centery, w - 2, thickness))

        # # 3. Outline between the top face and the side wall
        pygame.draw.ellipse(surf, outline, top_rect, 1)

        # # 4. Top face, then an inner ellipse shifted up for the rim, then a small shine
        face = top_rect.inflate(-2, -2)
        pygame.draw.ellipse(surf, rim, face)

        inner = face.inflate(-6, -4)
        inner.centery -= 1
        pygame.draw.ellipse(surf, top, inner)

        shine_rect = inner.inflate(-inner.width // 2, -inner.height // 2)
        shine_rect.centery -= 1
        pygame.draw.ellipse(surf, shine, shine_rect)

        # 5. Scale up with nearest-neighbor (transform.scale, NOT smoothscale)
        return pygame.transform.scale(surf, (surf.get_width() * px, surf.get_height() * px))
    
    def draw_fighters(self):
        # PLAYER PLATFORMS
        self.screen.blit(self.platform1, self.fighter1_platform_rect.topleft)
        self.screen.blit(self.platform2, self.fighter2_platform_rect.topleft)

        # PLAYER IMAGES
        self.screen.blit(self.f1, self.f1.get_rect(midbottom=self.fighter1_platform_rect.center))
        self.screen.blit(self.f2, self.f2.get_rect(midbottom=self.fighter2_platform_rect.center))

        # PLAYER NAMES
        self.screen.blit(self.player1_card, (self.player1_card_rect.x, self.player1_card_rect.y))
        self.screen.blit(self.fightername_font1.render(self.fighter1.name, True, pygame.Color(255,255,255)), (self.player1_card_rect.left+30, self.player1_card_rect.top+30))
        self.screen.blit(self.player2_card, (self.player2_card_rect.x, self.player2_card_rect.y))
        self.screen.blit(self.fightername_font2.render(self.fighter2.name, True, pygame.Color(255,255,255)), (self.player2_card_rect.left+30, self.player2_card_rect.top+30))

    def draw_bars(self):
        # PLAYER BARS
        self.draw_bar(self.player1_card_rect.left+30, self.player1_card_rect.top+65, 200, 20, (104, 5, 5), (23, 137, 31), self.fighter1.hp, self.fighter1.max_hp) # Player 1 health bar
        self.draw_bar(self.player1_card_rect.left+30, self.player1_card_rect.top+90, 200, 20, (23, 80, 137), (59, 154, 226), self.fighter1.mana, self.fighter1.max_mana) # Player 1 mana bar
        self.draw_bar(self.player2_card_rect.left+30, self.player2_card_rect.top+65, 200, 20, (104, 5, 5), (23, 137, 31), self.fighter2.hp, self.fighter2.max_hp) # Player 2 health bar
        self.draw_bar(self.player2_card_rect.left+30, self.player2_card_rect.top+90, 200, 20, (23, 80, 137), (59, 154, 226), self.fighter2.mana, self.fighter2.max_mana) # Player 2 mana bar

    def draw_game_over_screen(self, fighter_name):
        # Blit game over card
        self.screen.blit(self.game_over_card, self.game_over_rect)

        # Blit game over text on game over card
        surface = self.font_normal.render(f"GG! {fighter_name} lost...", True, (255, 255, 255))
        self.screen.blit(surface, (self.game_over_rect.left+30, self.game_over_rect.top+30))
        text = self.font_normal.render("Want to try again? Press ", True, (255, 255, 255))
        self.screen.blit(text, (self.game_over_rect.left+30, self.game_over_rect.top+70))

        # Blit placeholder text on empty menu card
        self.screen.blit(self.font_normal.render("> ...", True, (255, 255, 255)), (self.box_rect.left+30, self.box_rect.top+30))

        # Blit the R key on game over card after the text
        p_rect = self.press_R_key.get_rect(centery=(text.get_height()/2)+self.game_over_rect.top+70, centerx=self.game_over_rect.left+text.get_width()+50) # Place image rect after the text
        self.screen.blit(self.press_R_key, p_rect) # Blit image on the positioned image rectangle

    def draw_menu(self):
        # GAME BOX
        self.screen.blit(self.menu_frame, self.box_rect)

        # Shows player options if the game state is set to Player choice
        if self.state == States.PLAYER_CHOICE:
            for i, move in enumerate(self.fighter1.moves):
                if i == self.selected:
                    color = (255, 255, 255)   # bright = selected
                    text = "> " + move.name + f" (+{move.power} power)"
                else:
                    color = (145, 145, 145)   # dim = not selected
                    text = "  " + move.name

                surface = self.font_normal.render(text, True, color)
                self.screen.blit(surface, (self.box_rect.left + 30, self.box_rect.top + 30 + i * 35))
        else:
            # Blit Game over card on the screen if it's game over, else display the current message on the menu card
            if self.state == States.GAMEOVER:
                if not self.fighter1.is_alive():
                    self.draw_game_over_screen(self.fighter1.name)
                elif not self.fighter2.is_alive():
                    self.draw_game_over_screen(self.fighter2.name)
            else:
                surface = self.font_normal.render(self.message, True, (255, 255, 255))
                self.screen.blit(surface, (self.box_rect.left+30, self.box_rect.top+30))
        
    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        self.draw_fighters()
        self.draw_bars()
        self.draw_menu()

        pygame.display.flip()

    def draw_bar(self, x, y, w, h, color_back, color_front, current_value, max_value):
        pygame.draw.rect(self.screen, color_back, (x, y, w, h), border_radius=5)
        pygame.draw.rect(self.screen, color_front, (x, y, w*(current_value/max_value), h), border_radius=5)

    def build_menu_frame(self, size):
        """Draws the frame once onto its own Surface."""
        w, h = size
        frame = pygame.Surface((w, h), pygame.SRCALPHA)
        r = frame.get_rect()

        dark = (20, 20, 28)
        light = (230, 230, 235)

        # Layers from outside in. inflate() shrinks evenly around the same center,
        # so the corners stay concentric.
        pygame.draw.rect(frame, dark, r, border_radius=14)                        # outer line
        pygame.draw.rect(frame, light, r.inflate(-6, -6), border_radius=11)       # bright border
        pygame.draw.rect(frame, (90, 100, 140), r.inflate(-14, -14), border_radius=8)  # blue-gray band
        pygame.draw.rect(frame, dark, r.inflate(-20, -20), border_radius=6)       # inner line
        pygame.draw.rect(frame, (45, 50, 70), r.inflate(-24, -24), border_radius=5)    # fill

        # Corner studs
        inset = 18
        for x, y in [(inset, inset), (w - inset, inset), (inset, h - inset), (w - inset, h - inset)]:
            pygame.draw.circle(frame, light, (x, y), 4)
            pygame.draw.circle(frame, dark, (x, y), 4, 1)

        return frame

if __name__ == "__main__":
    Game().run()
