# Snake Game - Multi-Player AI Battle

A modern Python implementation of the classic Snake game featuring a human player competing against 3 AI opponents in a time-limited battle arena.

## 🎮 Game Overview

This is an enhanced multiplayer Snake game where you control a green snake and compete against three AI-controlled snakes (red, blue, and yellow) to become the largest snake within 60 seconds.

### Key Features

- **Multi-player gameplay**: 1 human player + 3 AI opponents
- **Time-limited matches**: 60-second rounds
- **Smart AI opponents**: AI snakes use pathfinding to seek food and avoid collisions
- **Dynamic food system**: Food spawns randomly and replenishes automatically
- **Collision bonuses**: Gain extra length when smaller snakes collide with you
- **Respawn system**: Snakes respawn after death with a 3-second delay
- **Real-time scoring**: Live score display and countdown timer
- **End-game statistics**: Detailed results with winner announcement

## 🎯 Game Mechanics

### Basic Rules
- Move your snake to collect orange food items
- Each food item increases your snake's length by 1
- Avoid colliding with walls or your own body
- The snake with the greatest length when time expires wins

### Advanced Mechanics
- **Collision Bonuses**: When a smaller snake collides with a larger one, the larger snake gains bonus length
- **Respawn System**: Dead snakes respawn after 3 seconds at random locations
- **AI Behavior**: AI snakes actively seek food while avoiding obstacles and other snakes

### Collision Rules
- Head-on collisions favor the larger snake
- If snakes are equal length, the "attacker" (moving snake) wins
- Colliding with a larger snake's body results in death and bonus length for the larger snake

## 🕹️ Controls

| Key | Action |
|-----|--------|
| **W** | Move Up |
| **A** | Move Left |
| **S** | Move Down |
| **D** | Move Right |

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Installation

1. **Clone or download the game files**:
   ```bash
   # If you have the files, ensure they're in the same directory
   ls snake_game.py test_snake.py
   ```

2. **Install tkinter** (if not already installed):
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # On macOS (usually pre-installed)
   # tkinter comes with Python installation
   
   # On Windows (usually pre-installed) 
   # tkinter comes with Python installation
   ```

3. **Test the installation**:
   ```bash
   python3 test_snake.py
   ```

4. **Run the game**:
   ```bash
   python3 snake_game.py
   ```

## 🎲 Game Configuration

The game includes several configurable constants at the top of `snake_game.py`:

```python
# Grid and Display
CELL_SIZE = 20              # Size of each grid cell in pixels
GRID_WIDTH = 30             # Number of cells horizontally  
GRID_HEIGHT = 20            # Number of cells vertically

# Game Timing
GAME_DURATION_MS = 60000    # Game length in milliseconds (60 seconds)
UPDATE_DELAY_MS = 80        # Game speed (lower = faster)
RESPAWN_DELAY_MS = 3000     # Time before respawn (3 seconds)

# Gameplay
INITIAL_SNAKE_LENGTH = 3        # Starting snake length
INITIAL_FOOD_COUNT = 10         # Number of food items on screen
FOOD_SPAWN_CHANCE = 0.05        # Probability of food spawning each update
BONUS_FOOD_SMALL_COLLISION = 4  # Bonus for collision with smaller snake
BONUS_FOOD_REGULAR_COLLISION = 2 # Regular collision bonus
```

## 🤖 AI Behavior

The AI snakes feature sophisticated behavior:

1. **Food Seeking**: AI prioritizes moving toward the nearest food
2. **Obstacle Avoidance**: Avoids walls, self-collision, and other snakes when possible
3. **Pathfinding**: Uses distance calculation to choose optimal directions
4. **Fallback Behavior**: Moves randomly when no clear path exists

## 🏆 Winning Strategy

### Tips for Success
- **Prioritize length over aggression**: Focus on collecting food rather than hunting other snakes
- **Use walls strategically**: Corner opponents or use walls to your advantage
- **Control the center**: Central positions give you more food access
- **Watch the timer**: In the final seconds, focus on staying alive rather than growing
- **Learn AI patterns**: AI snakes are predictable in their food-seeking behavior

### Advanced Techniques
- **Blocking**: Position yourself to cut off AI snakes from food
- **Ambush tactics**: Wait near food spawn points
- **Defensive play**: If you're leading, focus on avoiding collisions

## 🛠️ Technical Details

### Architecture
- **Snake Class**: Handles individual snake behavior, movement, and collision detection
- **SnakeGame Class**: Manages game state, timing, and overall coordination
- **Food System**: Dynamic food spawning and management
- **AI System**: Pathfinding and decision-making for computer opponents

### Performance
- Optimized for smooth 60+ FPS gameplay
- Efficient collision detection algorithms
- Minimal memory footprint

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'tkinter'" error**:
   ```bash
   # Install tkinter
   sudo apt-get install python3-tk  # Linux
   ```

2. **Game window doesn't respond to keys**:
   - Click on the game window to ensure it has focus
   - Try pressing keys while the game window is active

3. **Game runs too fast/slow**:
   - Modify `UPDATE_DELAY_MS` in the code (higher = slower)

4. **Display issues**:
   - Ensure your system supports GUI applications
   - Try running in a desktop environment rather than headless mode

### Testing
Run the test script to verify everything works:
```bash
python3 test_snake.py
```

## 📝 Code Structure

```
snake_game.py          # Main game implementation
├── Constants          # Game configuration
├── Helper Functions   # Utility functions (distance, validation, etc.)
├── Snake Class        # Individual snake behavior and rendering
├── Food Class         # Food item management
├── SnakeGame Class    # Main game logic and coordination
└── Main Loop          # Game initialization and startup

test_snake.py          # Test suite and verification
README.md              # This documentation
```

## 🔧 Customization

### Adding New Features
- **Power-ups**: Modify the food system to include special items
- **Different AI difficulties**: Adjust AI decision-making algorithms
- **Custom maps**: Add obstacles or different grid layouts
- **Multiplayer networking**: Extend for online multiplayer support

### Visual Customization
- **Colors**: Modify the `COLOR_*` constants
- **Grid size**: Adjust `GRID_WIDTH` and `GRID_HEIGHT`
- **Snake appearance**: Customize the drawing methods in the Snake class

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Some areas for improvement:
- Enhanced AI algorithms
- Additional game modes
- Visual effects and animations
- Sound effects
- Network multiplayer support
- Mobile compatibility

## 🎯 Version History

- **v1.0**: Initial release with basic multiplayer functionality
- **Current**: Enhanced AI, collision system, and user interface

---

**Enjoy the game! 🐍**

*May the longest snake win!*
