"""
snake.py — Clase Snake (Culebrita)
Maneja el movimiento, crecimiento, traspaso de paredes y detección de colisiones.
"""

from typing import List, Tuple

# Direcciones de movimiento (dx, dy)
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class Snake:
    """Culebrita verde que traspasa paredes y crece al comer manzanas."""

    def __init__(self, cols: int, rows: int, cell_size: int):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.reset()

    def reset(self):
        """Reinicia la serpiente al estado inicial."""
        cx, cy = self.cols // 2, self.rows // 2
        # La culebrita inicia con 3 segmentos moviéndose a la derecha
        self.body: List[Tuple[int, int]] = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow_pending = 0

    def change_direction(self, new_dir: Tuple[int, int]):
        """Cambia la dirección ignorando la dirección opuesta (no puede girar 180°)."""
        if new_dir != OPPOSITES.get(self.direction):
            self.next_direction = new_dir

    def move(self) -> bool:
        """
        Mueve la culebrita un paso.
        Retorna True si está viva, False si chocó consigo misma.
        """
        self.direction = self.next_direction
        dx, dy = self.direction
        head_x, head_y = self.body[0]

        # Nueva cabeza con traspaso de paredes (wall-wrap)
        new_head = (
            (head_x + dx) % self.cols,
            (head_y + dy) % self.rows,
        )

        # Colisión con el cuerpo (sin incluir la cola, que se elimina)
        collision_body = self.body[:-1] if self.grow_pending == 0 else self.body
        if new_head in collision_body:
            return False  # ☠️ Game Over

        # Agregar nueva cabeza
        self.body.insert(0, new_head)

        # Crecer o eliminar cola
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

        return True  # 🐍 Viva

    def eat(self):
        """Incrementa el crecimiento pendiente al comer una manzana."""
        self.grow_pending += 1

    @property
    def head(self) -> Tuple[int, int]:
        return self.body[0]

    def occupies(self, pos: Tuple[int, int]) -> bool:
        return pos in self.body
