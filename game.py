"""
game.py — Lógica central del juego Snake
Maneja el estado, puntuación, velocidad y renderizado visual.
"""

import pygame
import sys
from snake import Snake, UP, DOWN, LEFT, RIGHT
from apple import Apple

# ── Paleta de colores ─────────────────────────────────────────────────────────
BG_COLOR         = (15, 20, 30)       # Fondo oscuro azulado
GRID_COLOR       = (25, 32, 48)       # Líneas de la cuadrícula
SNAKE_HEAD       = (50, 220, 80)      # Verde brillante — cabeza
SNAKE_BODY       = (34, 180, 60)      # Verde oscuro — cuerpo
SNAKE_OUTLINE    = (20, 120, 40)      # Contorno del cuerpo
EYE_WHITE        = (240, 250, 240)    # Blanco de los ojos
EYE_PUPIL        = (10, 10, 10)       # Pupila
APPLE_RED        = (220, 50, 50)      # Rojo vivo — manzana
APPLE_SHINE      = (255, 160, 160)    # Brillo de la manzana
APPLE_STEM       = (100, 60, 20)      # Tallo de la manzana
APPLE_LEAF       = (60, 180, 60)      # Hoja de la manzana
TEXT_COLOR       = (200, 220, 255)    # Color del HUD
SCORE_GLOW       = (80, 200, 120)     # Color del marcador de puntos
GAMEOVER_BG      = (10, 10, 20, 200)  # Fondo semi-transparente Game Over
GAMEOVER_TEXT    = (255, 80, 80)      # Título Game Over
PAUSE_TEXT       = (255, 220, 100)    # Color pausa

# ── Configuración del juego ───────────────────────────────────────────────────
CELL_SIZE  = 24
COLS       = 25
ROWS       = 20
HUD_HEIGHT = 50

WIDTH      = COLS * CELL_SIZE
HEIGHT     = ROWS * CELL_SIZE + HUD_HEIGHT
FPS        = 60
BASE_SPEED = 8     # Movimientos por segundo al inicio
MAX_SPEED  = 20    # Velocidad máxima


class Game:
    """Clase principal del juego Snake."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.font_large  = pygame.font.SysFont("monospace", 48, bold=True)
        self.font_medium = pygame.font.SysFont("monospace", 28, bold=True)
        self.font_small  = pygame.font.SysFont("monospace", 20)
        self.high_score = 0
        self.reset()

    def reset(self):
        """Reinicia el estado completo del juego."""
        self.snake = Snake(COLS, ROWS, CELL_SIZE)
        self.apple = Apple(COLS, ROWS)
        self.apple.spawn(self.snake.body)
        self.score = 0
        self.state = "playing"   # "playing" | "paused" | "gameover"
        self.move_timer = 0.0
        self.speed = BASE_SPEED  # Movimientos por segundo

    # ── Event handling ────────────────────────────────────────────────────────

    def handle_events(self) -> bool:
        """Procesa eventos. Retorna False si el usuario cierra la ventana."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self._handle_key(event.key)
        return True

    def _handle_key(self, key: int):
        if self.state == "gameover":
            if key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                self.reset()
            return

        if key == pygame.K_p:
            self.state = "paused" if self.state == "playing" else "playing"
            return

        if self.state != "playing":
            return

        key_to_dir = {
            pygame.K_UP:    UP,
            pygame.K_w:     UP,
            pygame.K_DOWN:  DOWN,
            pygame.K_s:     DOWN,
            pygame.K_LEFT:  LEFT,
            pygame.K_a:     LEFT,
            pygame.K_RIGHT: RIGHT,
            pygame.K_d:     RIGHT,
        }
        if key in key_to_dir:
            self.snake.change_direction(key_to_dir[key])

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float):
        if self.state != "playing":
            return

        self.move_timer += dt
        move_interval = 1.0 / self.speed

        if self.move_timer >= move_interval:
            self.move_timer -= move_interval
            alive = self.snake.move()

            if not alive:
                self.state = "gameover"
                if self.score > self.high_score:
                    self.high_score = self.score
                return

            # ¿Comió la manzana?
            if self.snake.head == self.apple.pos:
                self.snake.eat()
                self.score += 10
                # Aumentar velocidad cada 50 puntos
                self.speed = min(BASE_SPEED + self.score // 50, MAX_SPEED)
                self.apple.spawn(self.snake.body)

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self):
        self.screen.fill(BG_COLOR)
        self._draw_grid()
        self._draw_apple()
        self._draw_snake()
        self._draw_hud()

        if self.state == "paused":
            self._draw_pause_overlay()
        elif self.state == "gameover":
            self._draw_gameover_overlay()

        pygame.display.flip()

    def _draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, HUD_HEIGHT), (x, HEIGHT))
        for y in range(HUD_HEIGHT, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))

    def _draw_snake(self):
        for i, (gx, gy) in enumerate(self.snake.body):
            px = gx * CELL_SIZE
            py = gy * CELL_SIZE + HUD_HEIGHT
            rect = pygame.Rect(px + 2, py + 2, CELL_SIZE - 4, CELL_SIZE - 4)

            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, SNAKE_OUTLINE, rect, width=1, border_radius=5)

            # Dibujar ojos en la cabeza
            if i == 0:
                self._draw_snake_eyes(px, py, self.snake.direction)

    def _draw_snake_eyes(self, px: int, py: int, direction):
        cx = px + CELL_SIZE // 2
        cy = py + HUD_HEIGHT // 2 + CELL_SIZE // 2
        # Ajustar posición de los ojos según dirección
        if direction == (1, 0):    # RIGHT
            e1 = (cx + 4, cy - 5)
            e2 = (cx + 4, cy + 5)
        elif direction == (-1, 0): # LEFT
            e1 = (cx - 4, cy - 5)
            e2 = (cx - 4, cy + 5)
        elif direction == (0, -1): # UP
            e1 = (cx - 5, cy - 4)
            e2 = (cx + 5, cy - 4)
        else:                       # DOWN
            e1 = (cx - 5, cy + 4)
            e2 = (cx + 5, cy + 4)

        # Nota: py ya tiene HUD_HEIGHT sumado en _draw_snake, recalculamos
        base_x = px + CELL_SIZE // 2
        base_y = py + CELL_SIZE // 2  # py ya incluye HUD_HEIGHT
        if direction == (1, 0):
            e1 = (base_x + 4, base_y - 4)
            e2 = (base_x + 4, base_y + 4)
        elif direction == (-1, 0):
            e1 = (base_x - 4, base_y - 4)
            e2 = (base_x - 4, base_y + 4)
        elif direction == (0, -1):
            e1 = (base_x - 4, base_y - 4)
            e2 = (base_x + 4, base_y - 4)
        else:
            e1 = (base_x - 4, base_y + 4)
            e2 = (base_x + 4, base_y + 4)

        pygame.draw.circle(self.screen, EYE_WHITE, e1, 3)
        pygame.draw.circle(self.screen, EYE_WHITE, e2, 3)
        pygame.draw.circle(self.screen, EYE_PUPIL, e1, 1)
        pygame.draw.circle(self.screen, EYE_PUPIL, e2, 1)

    def _draw_apple(self):
        gx, gy = self.apple.pos
        px = gx * CELL_SIZE
        py = gy * CELL_SIZE + HUD_HEIGHT

        cx = px + CELL_SIZE // 2
        cy = py + CELL_SIZE // 2 + 2

        # Cuerpo de la manzana
        pygame.draw.circle(self.screen, APPLE_RED, (cx, cy), CELL_SIZE // 2 - 3)

        # Brillo
        pygame.draw.circle(self.screen, APPLE_SHINE, (cx - 3, cy - 4), 3)

        # Tallo
        pygame.draw.line(self.screen, APPLE_STEM, (cx, cy - CELL_SIZE // 2 + 2), (cx + 2, cy - CELL_SIZE // 2 - 3), 2)

        # Hoja
        leaf_rect = pygame.Rect(cx + 1, cy - CELL_SIZE // 2 - 4, 6, 4)
        pygame.draw.ellipse(self.screen, APPLE_LEAF, leaf_rect)

    def _draw_hud(self):
        # Fondo del HUD
        pygame.draw.rect(self.screen, (20, 28, 45), (0, 0, WIDTH, HUD_HEIGHT))
        pygame.draw.line(self.screen, SNAKE_OUTLINE, (0, HUD_HEIGHT - 1), (WIDTH, HUD_HEIGHT - 1), 2)

        # Título
        title = self.font_small.render("🐍 SNAKE", True, SNAKE_HEAD)
        self.screen.blit(title, (12, 14))

        # Puntuación
        score_label = self.font_small.render("PUNTOS:", True, TEXT_COLOR)
        score_val   = self.font_medium.render(str(self.score), True, SCORE_GLOW)
        self.screen.blit(score_label, (WIDTH // 2 - 70, 8))
        self.screen.blit(score_val,   (WIDTH // 2 - 70, 24))

        # Récord
        hs_label = self.font_small.render(f"RÉCORD: {self.high_score}", True, TEXT_COLOR)
        self.screen.blit(hs_label, (WIDTH - hs_label.get_width() - 12, 16))

        # Velocidad
        speed_label = self.font_small.render(f"VEL: {self.speed}", True, TEXT_COLOR)
        self.screen.blit(speed_label, (12, 32))

    def _draw_pause_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT - HUD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 30, 160))
        self.screen.blit(overlay, (0, HUD_HEIGHT))

        pause_surf = self.font_large.render("⏸ PAUSA", True, PAUSE_TEXT)
        hint_surf  = self.font_small.render("Presiona P para continuar", True, TEXT_COLOR)
        cx = WIDTH // 2
        cy = (HEIGHT + HUD_HEIGHT) // 2
        self.screen.blit(pause_surf, (cx - pause_surf.get_width() // 2, cy - 40))
        self.screen.blit(hint_surf,  (cx - hint_surf.get_width() // 2,  cy + 20))

    def _draw_gameover_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT - HUD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 5, 15, 200))
        self.screen.blit(overlay, (0, HUD_HEIGHT))

        cx = WIDTH // 2
        cy = (HEIGHT + HUD_HEIGHT) // 2

        go_surf     = self.font_large.render("💀 GAME OVER", True, GAMEOVER_TEXT)
        score_surf  = self.font_medium.render(f"Puntuación: {self.score}", True, SCORE_GLOW)
        hs_surf     = self.font_medium.render(f"Récord:     {self.high_score}", True, TEXT_COLOR)
        hint_surf   = self.font_small.render("R / ESPACIO para reiniciar", True, (160, 160, 200))

        self.screen.blit(go_surf,    (cx - go_surf.get_width() // 2,    cy - 80))
        self.screen.blit(score_surf, (cx - score_surf.get_width() // 2, cy - 20))
        self.screen.blit(hs_surf,    (cx - hs_surf.get_width() // 2,    cy + 20))
        self.screen.blit(hint_surf,  (cx - hint_surf.get_width() // 2,  cy + 70))
