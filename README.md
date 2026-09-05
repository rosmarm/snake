# 🐍 Snake — Culebrita Verde

Juego clásico de la culebrita implementado en **Python con Pygame**.

## 🎮 Características

- 🐍 **Culebrita verde** con ojos que indican la dirección
- 🍎 **Manzanas rojas** con tallo, hoja y brillo visual
- 🌀 **Traspaso de paredes** — sale por un lado y entra por el opuesto
- 📈 **Crecimiento** — la culebrita aumenta de tamaño al comer
- 💀 **Colisión consigo misma** — Game Over si la cabeza toca el cuerpo
- ⚡ **Velocidad progresiva** — el juego se acelera conforme aumenta la puntuación
- 🏆 **Récord de sesión** guardado en memoria

## 📋 Controles

| Tecla | Acción |
|---|---|
| `↑` `↓` `←` `→` o `W` `A` `S` `D` | Mover la culebrita |
| `P` | Pausar / Continuar |
| `R` / `ESPACIO` / `ENTER` | Reiniciar tras Game Over |
| `ESC` / Cerrar ventana | Salir |

## 🚀 Instalación y Ejecución

```bash
# 1. Clona el repositorio
git clone https://github.com/rosmarm/snake.git
cd snake

# 2. Instala las dependencias
pip install -r requirements.txt

# 3. Ejecuta el juego
python3 main.py
```

## 📁 Estructura del Proyecto

```
snake/
├── main.py          # Punto de entrada y bucle principal de Pygame
├── game.py          # Lógica del juego, renderizado visual y estado
├── snake.py         # Clase Snake: movimiento, wall-wrap y colisiones
├── apple.py         # Clase Apple: generación de manzanas aleatorias
├── requirements.txt # Dependencias (pygame>=2.5.0)
└── README.md        # Este archivo
```

## 🎯 Reglas del Juego

1. **Mueve** la culebrita con las flechas o WASD.
2. **Come** las manzanas rojas para crecer y sumar puntos (+10 por manzana).
3. La culebrita **traspasa paredes** automáticamente — no hay límites de borde.
4. Si la **cabeza toca cualquier parte del cuerpo**, es Game Over.
5. La velocidad **aumenta** gradualmente a medida que acumulas puntos.

---

Desarrollado con 🐍 Python + Pygame
