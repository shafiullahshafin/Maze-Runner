import pygame
import time
import logging
from src.constants import *
from src.game import Game
from src.leaderboard import Leaderboard
from src.utils import draw_text

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", FONT_SIZE_TITLE, bold=True)
        self.font_menu = pygame.font.SysFont("arial", FONT_SIZE_MENU)
        self.font_hud = pygame.font.SysFont("arial", FONT_SIZE_HUD)
        self.font_small = pygame.font.SysFont("arial", FONT_SIZE_SMALL)
        self.options = ["New Game", "Difficulty: Medium", "Leaderboard", "Help", "Quit"]
        self.selected_index = 0
        self.game = None
        self.leaderboard = Leaderboard()
        self.state = "connecting"
        self.username = ""
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.current_difficulty_index = 1

    def run(self):
        if self.state == "connecting":
            return self.handle_connecting()
        elif self.state == "connection_error":
            return self.handle_connection_error()
        elif self.state == "login":
            return self.handle_login()
        elif self.state == "menu":
            return self.handle_menu()
        elif self.state == "game":
            return self.handle_game()
        elif self.state == "leaderboard":
            return self.handle_leaderboard()
        elif self.state == "help":
            return self.handle_help()
        return "continue"

    def handle_connecting(self):
        self.screen.fill(BG_COLOR)
        
        # Simple Splash Screen
        title_surf = self.font_title.render("Maze Runner", True, GREEN)
        shadow_surf = self.font_title.render("Maze Runner", True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
        self.screen.blit(title_surf, title_rect)
        
        pygame.display.flip()

        if not self.leaderboard.is_loading:
            if self.leaderboard.is_online():
                self.state = "login"
            else:
                self.state = "connection_error"
        
        # Check for quit events even during loading
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        
        return "continue"

    def handle_connection_error(self):
        self.screen.fill(BG_COLOR)
        draw_text(self.screen, "You are offline.", self.font_title, RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        draw_text(self.screen, "App cannot run without internet.", self.font_hud, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        draw_text(self.screen, "Press ESC to Quit", self.font_small, GRAY, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
        
        return "continue"

    def handle_login(self):
        self.screen.fill(BG_COLOR)
        
        # Title with shadow
        title_surf = self.font_title.render("Maze Runner", True, GREEN)
        shadow_surf = self.font_title.render("Maze Runner", True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
        self.screen.blit(title_surf, title_rect)
        
        draw_text(self.screen, "Enter Username:", self.font_menu, WHITE, (SCREEN_WIDTH // 2, 230))
        draw_text(self.screen, "(Alphanumeric only, max 15 chars)", self.font_hud, GRAY, (SCREEN_WIDTH // 2, 260))
        
        # Input Box
        input_rect = pygame.Rect(0, 0, 300, 50)
        input_rect.center = (SCREEN_WIDTH // 2, 320)
        
        pygame.draw.rect(self.screen, INPUT_BG_COLOR, input_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLUE if len(self.username) > 0 else GRAY, input_rect, 2, border_radius=10)
        
        text_surf = self.font_menu.render(self.username, True, WHITE)
        text_rect = text_surf.get_rect(center=input_rect.center)
        self.screen.blit(text_surf, text_rect)
        
        # Blinking Cursor
        if time.time() % 1 > 0.5:
            cursor_rect = pygame.Rect(text_rect.right + 2, text_rect.top, 2, text_rect.height)
            pygame.draw.rect(self.screen, WHITE, cursor_rect)
        
        # Start Hint
        if len(self.username) > 0:
            draw_text(self.screen, "Press ENTER to Start", self.font_hud, GREEN, (SCREEN_WIDTH // 2, 400))
        else:
            draw_text(self.screen, "Type your name...", self.font_hud, GRAY, (SCREEN_WIDTH // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.username.strip():
                        self.state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    if len(self.username) < 15 and event.unicode.isalnum():
                        self.username += event.unicode
        return "continue"

    def handle_menu(self):
        self.screen.fill(BG_COLOR)
        
        try:
            draw_text(self.screen, f"Welcome, {self.username}!", self.font_hud, BLUE, (SCREEN_WIDTH // 2, 40))
        except Exception as e:
            logging.error(f"Error drawing welcome text: {e}")
        
        title_surf = self.font_title.render("Maze Runner", True, GREEN)
        shadow_surf = self.font_title.render("Maze Runner", True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
        self.screen.blit(title_surf, title_rect)
        
        start_y = 200
        gap = 70
        
        for i, option in enumerate(self.options):
            btn_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
            btn_rect.center = (SCREEN_WIDTH // 2, start_y + i * gap)
            
            is_selected = (i == self.selected_index)
            color = BUTTON_SELECTED_COLOR if is_selected else BUTTON_COLOR
            if is_selected:
                 # Add a glow/outline effect
                 pygame.draw.rect(self.screen, WHITE, btn_rect.inflate(4, 4), border_radius=BUTTON_RADIUS)
            
            pygame.draw.rect(self.screen, color, btn_rect, border_radius=BUTTON_RADIUS)
            
            text_color = BLACK if is_selected else WHITE
            text_surf = self.font_menu.render(option, True, text_color)
            text_rect = text_surf.get_rect(center=btn_rect.center)
            self.screen.blit(text_surf, text_rect)
            
        draw_text(self.screen, "Use Arrow Keys to Navigate, Enter to Select", self.font_small, GRAY, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                     # If Difficulty is selected, change it
                    if self.options[self.selected_index].startswith("Difficulty"):
                        self.current_difficulty_index = (self.current_difficulty_index + 1) % len(self.difficulty_levels)
                        new_diff = self.difficulty_levels[self.current_difficulty_index]
                        self.options[self.selected_index] = f"Difficulty: {new_diff}"
                elif event.key == pygame.K_RETURN:
                    return self.select_option()
        
        return "continue"

    def select_option(self):
        option = self.options[self.selected_index]
        if option == "New Game":
            difficulty = self.difficulty_levels[self.current_difficulty_index]
            fps = DIFFICULTY[difficulty]
            self.game = Game(self.screen, fps, difficulty)
            self.state = "game"
        elif option.startswith("Difficulty"):
            self.current_difficulty_index = (self.current_difficulty_index + 1) % len(self.difficulty_levels)
            new_diff = self.difficulty_levels[self.current_difficulty_index]
            self.options[self.selected_index] = f"Difficulty: {new_diff}"
        elif option == "Leaderboard":
            self.state = "leaderboard"
        elif option == "Help":
            self.state = "help"
        elif option == "Quit":
            return "quit"
        return "continue"

    def handle_game(self):
        if self.game:
            logging.info("MainMenu: Starting game loop")
            try:
                result = self.game.run()
            except Exception as e:
                logging.exception("Exception in game.run()")
                self.game = None
                self.state = "menu"
                return "continue"
                
            logging.info(f"MainMenu: Game returned result '{result}'")
            try:
                if result == "game_over":
                    print(f"Game Over. Saving score: {self.username} - {self.game.score} ({self.game.difficulty})")
                    self.leaderboard.add_score(self.username, self.game.score, self.game.difficulty)
                    self.game = None
                    self.state = "menu"
                elif result == "menu":
                    # User pressed ESC
                    logging.info("MainMenu: Handling menu return")
                    if self.game.score > 0:
                        print(f"User returned to menu. Saving score: {self.username} - {self.game.score} ({self.game.difficulty})")
                        self.leaderboard.add_score(self.username, self.game.score, self.game.difficulty)
                    self.game = None
                    self.state = "menu"
                    logging.info("MainMenu: State set to menu")
                elif result == "quit_app":
                    # User clicked X button
                    if self.game.score > 0:
                        self.leaderboard.add_score(self.username, self.game.score, self.game.difficulty)
                    return "quit"
            except Exception as e:
                logging.exception("Exception handling game result")
                self.game = None
                self.state = "menu"
                
        return "continue"

    def handle_leaderboard(self):
        self.screen.fill(BG_COLOR)
        
        draw_text(self.screen, "Leaderboard", self.font_title, GREEN, (SCREEN_WIDTH // 2, 50))
        
        # Table Headers
        header_y = 100
        # Rank (Center)
        rank_surf = self.font_hud.render("Rank", True, WHITE)
        rank_rect = rank_surf.get_rect(center=(150, header_y))
        self.screen.blit(rank_surf, rank_rect)
        
        # Player (Left)
        player_surf = self.font_hud.render("Player", True, WHITE)
        player_rect = player_surf.get_rect(midleft=(220, header_y))
        self.screen.blit(player_surf, player_rect)

        # Difficulty (Left)
        diff_surf = self.font_hud.render("Difficulty", True, WHITE)
        diff_rect = diff_surf.get_rect(midleft=(420, header_y))
        self.screen.blit(diff_surf, diff_rect)
        
        # Score (Right)
        score_surf = self.font_hud.render("Score", True, WHITE)
        score_rect = score_surf.get_rect(midright=(650, header_y))
        self.screen.blit(score_surf, score_rect)
        
        # Divider Line
        pygame.draw.line(self.screen, DARK_GRAY, (100, header_y + 20), (700, header_y + 20), 2)
        
        if self.leaderboard.is_loading:
             draw_text(self.screen, "Loading scores...", self.font_menu, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        else:
            scores = self.leaderboard.get_top_scores()
            
            if not scores:
                draw_text(self.screen, "No scores yet!", self.font_menu, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            else:
                start_y = 140
                for i, (name, score, difficulty) in enumerate(scores):
                    color = GREEN if i == 0 else WHITE # Highlight top player
                    y_pos = start_y + i * 35
                    
                    r_surf = self.font_menu.render(str(i+1), True, color)
                    r_rect = r_surf.get_rect(center=(150, y_pos))
                    self.screen.blit(r_surf, r_rect)
                    
                    n_surf = self.font_menu.render(name, True, color)
                    n_rect = n_surf.get_rect(midleft=(220, y_pos))
                    self.screen.blit(n_surf, n_rect)

                    d_surf = self.font_menu.render(str(difficulty), True, color)
                    d_rect = d_surf.get_rect(midleft=(420, y_pos))
                    self.screen.blit(d_surf, d_rect)
                    
                    s_surf = self.font_menu.render(str(score), True, color)
                    s_rect = s_surf.get_rect(midright=(650, y_pos))
                    self.screen.blit(s_surf, s_rect)
            
        draw_text(self.screen, "Press ESC to return", self.font_small, GRAY, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"
        return "continue"

    def handle_help(self):
        self.screen.fill(BG_COLOR)
        draw_text(self.screen, "Help", self.font_title, BLUE, (SCREEN_WIDTH // 2, 40))
        
        # Help Box - Reduced size to prevent overflow
        box_width, box_height = 700, 480
        box_rect = pygame.Rect(0, 0, box_width, box_height)
        box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)
        pygame.draw.rect(self.screen, DARK_GRAY, box_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, box_rect, 2, border_radius=15)
        
        # --- Section 1: Controls (Top) ---
        section1_y = box_rect.top + 30
        draw_text(self.screen, "Controls", self.font_menu, GREEN, (SCREEN_WIDTH // 2, section1_y))
        
        controls = [
            ("Arrow Keys", "Move Snake"),
            ("P / TAB", "Pause / Resume"),
            ("ESC", "Back / Quit"),
            ("ENTER", "Select Item")
        ]
        
        # Alignment: Key (Right of center) | Action (Left of center)
        ctrl_start_y = section1_y + 45
        row_spacing = 35
        center_gap = 20
        
        for i, (key, action) in enumerate(controls):
            y_pos = ctrl_start_y + i * row_spacing
            
            # Key (Right Aligned to center - gap)
            k_surf = self.font_hud.render(key, True, YELLOW)
            k_rect = k_surf.get_rect(midright=(SCREEN_WIDTH // 2 - center_gap, y_pos))
            self.screen.blit(k_surf, k_rect)
            
            # Action (Left Aligned to center + gap)
            a_surf = self.font_small.render(action, True, WHITE)
            a_rect = a_surf.get_rect(midleft=(SCREEN_WIDTH // 2 + center_gap, y_pos))
            self.screen.blit(a_surf, a_rect)

        # --- Divider ---
        divider_y = ctrl_start_y + len(controls) * row_spacing + 15
        pygame.draw.line(self.screen, GRAY, (box_rect.left + 100, divider_y), (box_rect.right - 100, divider_y), 1)

        # --- Section 2: Rules (Bottom) ---
        section2_y = divider_y + 30
        draw_text(self.screen, "Rules", self.font_menu, GREEN, (SCREEN_WIDTH // 2, section2_y))
        
        rules = [
            "Eat Red Food to Grow",
            "Avoid Hitting Your Tail",
            "Walls Wrap Around",
            "3 Lives Per Game"
        ]
        
        rules_start_y = section2_y + 45
        
        for i, rule in enumerate(rules):
            y_pos = rules_start_y + i * row_spacing
            # Centered bullet points
            r_surf = self.font_hud.render(f"•  {rule}", True, WHITE)
            r_rect = r_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(r_surf, r_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"
        return "continue"
