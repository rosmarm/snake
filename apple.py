"""
apple.py — Clase Apple (Manzana Roja)
Genera manzanas en posiciones aleatorias sin solaparse con la culebrita.
"""

import random
from typing import Tuple, List


class Apple:
    """Manzana roja que aparece en posiciones libres del grid."""

    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.pos: Tuple[int, int] = (0, 0)

    def spawn(self, occupied: List[Tuple[int, int]]):
        """Coloca la manzana en una celda libre del grid."""
        free_cells = [
            (x, y)
            for x in range(self.cols)
            for y in range(self.rows)
            if (x, y) not in occupied
        ]
        if free_cells:
            self.pos = random.choice(free_cells)

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]
