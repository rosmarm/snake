"""
main.py — Punto de entrada del juego Snake 🐍
Romeca-Fit | Culebrita verde, manzanas rojas, traspaso de paredes.

Controles:
  ↑ ↓ ← →  o  W A S D  — Mover la culebrita
  P                      — Pausa / Continuar
  R / ESPACIO            — Reiniciar tras Game Over
  ESC / Cerrar ventana   — Salir
"""

import pygame
import sys
from game import Game, WIDTH, HEIGHT, FPS


def main():
    pygame.init()
    pygame.display.set_caption("🐍 Snake — Culebrita Verde")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock  = pygame.time.Clock()

    game = Game(screen, clock)

    while True:
        dt = clock.tick(FPS) / 1000.0  # Delta time en segundos

        if not game.handle_events():
            pygame.quit()
            sys.exit()

        game.update(dt)
        game.draw()


if __name__ == "__main__":
    main()
