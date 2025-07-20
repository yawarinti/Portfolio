import tkinter as tk
import random
import time
import math
from queue import Queue, Empty

# --- Constants ---
CELL_SIZE = 20  # Size of each grid cell in pixels
GRID_WIDTH = 30  # Number of cells horizontally
GRID_HEIGHT = 20  # Number of cells vertically
INITIAL_SNAKE_LENGTH = 3
RESPAWN_DELAY_MS = 3000  # milliseconds
FOOD_SPAWN_DELAY_MS = 1000  # milliseconds
FOOD_SPAWN_CHANCE = 0.05  # Probability per update cycle
INITIAL_FOOD_COUNT = 10  # Initial number of food pieces
GAME_DURATION_MS = 60000  # milliseconds (60 seconds)
BONUS_FOOD_SMALL_COLLISION = 4  # Bonus food for hitting a larger snake's tail
BONUS_FOOD_REGULAR_COLLISION = 2  # Bonus food for a regular collision
UPDATE_DELAY_MS = 80  # Controls game speed (lower = faster)

# --- Colors ---
COLOR_BACKGROUND = '#1a1a1a'  # Dark background
COLOR_PLAYER = '#00ff00'  # Green
COLOR_AI_1 = '#ff0000'  # Red
COLOR_AI_2 = '#0000ff'  # Blue
COLOR_AI_3 = '#ffff00'  # Yellow
COLOR_FOOD = '#ff6600'  # Orange
COLOR_TEXT = '#ffffff'  # White
COLOR_OVERLAY_BG = '#000000'  # Black (tkinter doesn't support rgba)

# --- Helper Functions ---
def distance(pos1, pos2):
    """Euclidean distance between two points (x1, y1) and (x2, y2)"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def manhattan_distance(pos1, pos2):
    """Manhattan distance between two points (x1, y1) and (x2, y2)"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def is_position_valid(position):
    """Checks if a position is within the grid boundaries"""
    return 0 <= position[0] < GRID_WIDTH and 0 <= position[1] < GRID_HEIGHT

def find_empty_position(excluded_positions=[]):
    """
    Finds a random empty position on the grid not in excluded_positions.
    """
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in excluded_positions:
            return pos

def get_largest_snake(snakes):
    """
    Returns the snake with the largest length.
    If multiple snakes have the same max length, returns one of them.
    """
    if not snakes:
        return None
    return max(snakes, key=lambda snake: snake.length)

# --- Classes ---
class Snake:
    """
    Represents a snake in the game.
    Handles movement (player and AI), growth, and collision logic.
    """
    def __init__(self, canvas, color, initial_position, length=INITIAL_SNAKE_LENGTH, is_ai=False):
        """
        Initializes a snake.
        :param canvas: The tkinter canvas to draw on.
        :param color: The color of the snake.
        :param initial_position: Starting (x, y) position.
        :param length: Initial length.
        :param is_ai: Whether this is an AI-controlled snake.
        """
        self.canvas = canvas
        self.color = color
        self.length = length
        self.is_ai = is_ai
        self.direction = 'Right'
        self.next_direction = 'Right' # For AI decision queue
        self.is_alive = True
        self.respawn_time = None
        self._create_initial_body(initial_position, length)
        self.canvas_items = [] # Stores tkinter canvas item IDs
        self.food_queue = Queue() # Stores positions of food to consume
        self._redraw()

    def _create_initial_body(self, head_position, length):
        """Creates the initial body segments of the snake"""
        self.body = [head_position]
        x, y = head_position
        for i in range(1, length):
            self.body.append((x - i, y))

    def _redraw(self):
        """Redraws the snake's body on the canvas"""
        for item in self.canvas_items:
            self.canvas.delete(item)
        self.canvas_items = []
        for i, segment in enumerate(self.body):
            x1 = segment[0] * CELL_SIZE
            y1 = segment[1] * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            item = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline=COLOR_BACKGROUND)
            self.canvas_items.append(item)

    def set_direction(self, direction):
        """Sets the direction of the snake (for player control)"""
        if not self.is_alive or self.is_ai:
            return
        opposite_directions = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if direction != opposite_directions.get(self.direction, None):
            self.direction = direction

    def decide_direction_ai(self, game_state):
        """
        AI decision logic. Schedules the direction change using the queue.
        Avoids walls and tries to reach the food queue target.
        """
        if not self.is_alive or not self.is_ai:
            return

        head_x, head_y = self.body[0]

        # Check if a move is valid (within bounds and not self-collision)
        def is_valid_move(direction):
            if direction == 'Up':
                new_pos = (head_x, head_y - 1)
            elif direction == 'Down':
                new_pos = (head_x, head_y + 1)
            elif direction == 'Left':
                new_pos = (head_x - 1, head_y)
            elif direction == 'Right':
                new_pos = (head_x + 1, head_y)
            else:
                return False
            return is_position_valid(new_pos) and new_pos not in self.body

        valid_directions = [d for d in ['Up', 'Down', 'Left', 'Right'] if is_valid_move(d)]

        if not valid_directions:
            self.next_direction = self.direction # No valid moves, continue current direction
            return

        # Prioritize moving towards food in the queue
        try:
            target_food = self.food_queue.get_nowait()
        except Empty:
            target_food = None

        if target_food:
            dx = target_food[0] - head_x
            dy = target_food[1] - head_y

            # Choose direction based on largest horizontal/vertical component
            if abs(dx) > abs(dy):
                preferred = 'Right' if dx > 0 else 'Left'
            else:
                preferred = 'Down' if dy > 0 else 'Up'

            if preferred in valid_directions:
                self.next_direction = preferred
            else:
                # If preferred direction is blocked, try perpendicular directions
                if abs(dx) > abs(dy):
                    alt1 = 'Down' if dy > 0 else 'Up'
                    alt2 = 'Up' if dy > 0 else 'Down'
                else:
                    alt1 = 'Right' if dx > 0 else 'Left'
                    alt2 = 'Left' if dx > 0 else 'Right'

                if alt1 in valid_directions:
                    self.next_direction = alt1
                elif alt2 in valid_directions:
                    self.next_direction = alt2
                else:
                    self.next_direction = random.choice(valid_directions)
            return # Decision made, don't execute the random fallback

        # No food target, move randomly if necessary
        if self.next_direction not in valid_directions:
             self.next_direction = random.choice(valid_directions)

    def update(self, game_state):
        """
        Updates the snake's state (movement, growth, respawning).
        Returns a list of new positions created this update (for collision detection).
        """
        current_time_ms = int(time.time() * 1000)
        new_positions = []

        if not self.is_alive:
            if self.respawn_time and current_time_ms >= self.respawn_time:
                self.respawn(game_state['snakes'])
            return new_positions

        # Apply the direction decided by AI (if any)
        if self.is_ai and self.next_direction in ['Up', 'Down', 'Left', 'Right']:
            self.direction = self.next_direction
            self.next_direction = None # Reset for next decision

        # Calculate new head position
        head_x, head_y = self.body[0]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 1, head_y)
        else:
            return new_positions # Invalid direction

        # Check wall collision
        if not is_position_valid(new_head):
            self.die(game_state, None, 'wall')
            return new_positions

        new_positions.append(new_head)

        # Check food collision
        food_positions = [f['position'] for f in game_state['food']]
        if new_head in food_positions:
            self.length += 1
            food_index = food_positions.index(new_head)
            food_id = game_state['food'][food_index]['id']
            self.canvas.delete(game_state['food_canvas_items'][food_index])
            del game_state['food'][food_index]
            del game_state['food_canvas_items'][food_index]
            self.grow()

            # Notify game state about the eaten food
            if 'eaten_food' not in game_state:
                game_state['eaten_food'] = []
            game_state['eaten_food'].append({'snake': self, 'food_id': food_id, 'position': new_head})

        else:
            # No food, move normally
            self.body.insert(0, new_head)
            if len(self.body) > self.length:
                self.body.pop()

        # Check self-collision
        if self.body[0] in self.body[1:]:
            self.die(game_state, None, 'self')
            return new_positions

        self._redraw()
        return new_positions

    def grow(self):
        """Increases the length of the snake (called when food is eaten)"""
        self.length += 1

    def die(self, game_state, other_snake, collision_type):
        """
        Handles the snake's death.
        collision_type can be: 'snake', 'wall', 'self'
        """
        if not self.is_alive:
            return
        self.is_alive = False
        self.respawn_time = int(time.time() * 1000) + RESPAWN_DELAY_MS

        # Collision logic with other snakes
        if other_snake and collision_type == 'snake':
            if self.length < other_snake.length:
                if game_state.get('winner_snake') is None or other_snake.length > game_state['winner_snake'].length:
                     game_state['winner_snake'] = other_snake

                if other_snake.is_alive:
                     # Determine bonus based on collision type
                     if collision_type == 'snake':
                         if self.length < other_snake.length and other_snake.body[0] == self.body[0]:
                             bonus = BONUS_FOOD_SMALL_COLLISION
                         else:
                             bonus = BONUS_FOOD_REGULAR_COLLISION

                         other_snake.length += bonus
                         other_snake.grow() # Visual update

                     if 'collision_events' not in game_state:
                         game_state['collision_events'] = []
                     game_state['collision_events'].append({'type': collision_type, 'attacker': other_snake, 'victim': self, 'bonus': bonus})

            elif self.length > other_snake.length:
                 if self.is_alive and (game_state.get('winner_snake') is None or self.length > game_state['winner_snake'].length):
                      game_state['winner_snake'] = self
                 if 'collision_events' not in game_state:
                      game_state['collision_events'] = []
                 game_state['collision_events'].append({'type': collision_type, 'attacker': self, 'victim': other_snake, 'bonus': 0})
            else: # Equal length, attacker wins
                if other_snake.is_alive and (game_state.get('winner_snake') is None or other_snake.length > game_state['winner_snake'].length):
                    game_state['winner_snake'] = other_snake
                if 'collision_events' not in game_state:
                    game_state['collision_events'] = []
                game_state['collision_events'].append({'type': collision_type, 'attacker': other_snake, 'victim': self, 'bonus': 0})


    def respawn(self, game_snakes):
        """Respawns the snake at a new location"""
        if self.is_alive:
            return
        # Find a valid respawn position
        other_snake_positions = []
        for snake in game_snakes:
            if snake.is_alive and snake != self:
                other_snake_positions.extend(snake.body)
        new_position = find_empty_position(other_snake_positions)
        self.body = [new_position]
        self.length = INITIAL_SNAKE_LENGTH
        self.direction = 'Right'
        self.next_direction = None # Clear AI decision queue
        self.is_alive = True
        self.respawn_time = None
        self._redraw()

class Food:
    """Represents a food item on the grid"""
    def __init__(self, canvas, position):
        """
        Initializes a food item.
        :param canvas: The tkinter canvas.
        :param position: (x, y) position of the food.
        """
        self.canvas = canvas
        self.position = position
        self.canvas_item = self.canvas.create_oval(
            position[0] * CELL_SIZE, position[1] * CELL_SIZE,
            (position[0] + 1) * CELL_SIZE, (position[1] + 1) * CELL_SIZE,
            fill=COLOR_FOOD, outline=COLOR_BACKGROUND
        )

# --- Main Game Class ---
class SnakeGame:
    """
    Manages the overall game state, snakes, food, events, and UI.
    """
    def __init__(self, root):
        """
        Initializes the SnakeGame.
        :param root: The root tkinter window.
        """
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(
            self.root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg=COLOR_BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack()

        self.snakes = []
        self.food = []
        self.food_canvas_items = []
        self.game_over = False
        self.start_time = time.time()
        self.winner_snake = None
        self.score_overlay = None
        self.score_labels = []
        self.game_state = {
            'snakes': self.snakes,
            'food': self.food,
            'food_canvas_items': self.food_canvas_items,
            'winner_snake': None
        }

        # Create player snake
        player_initial_pos = (GRID_WIDTH // 4, GRID_HEIGHT // 2)
        self.player_snake = Snake(self.canvas, COLOR_PLAYER, player_initial_pos)
        self.snakes.append(self.player_snake)

        # Create AI snakes
        ai_initial_positions = [
            (3 * GRID_WIDTH // 4, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2, GRID_HEIGHT // 4),
            (GRID_WIDTH // 2, 3 * GRID_HEIGHT // 4)
        ]
        ai_colors = [COLOR_AI_1, COLOR_AI_2, COLOR_AI_3]
        for i in range(3):
            ai_snake = Snake(self.canvas, ai_colors[i], ai_initial_positions[i], is_ai=True)
            self.snakes.append(ai_snake)

        # Spawn initial food
        for _ in range(INITIAL_FOOD_COUNT):
            self.spawn_food()

        # Bind player controls
        self.canvas.focus_set()  # Set focus to canvas for key events
        self.root.bind('<KeyPress-w>', lambda e: self.player_snake.set_direction('Up'))
        self.root.bind('<KeyPress-a>', lambda e: self.player_snake.set_direction('Left'))
        self.root.bind('<KeyPress-s>', lambda e: self.player_snake.set_direction('Down'))
        self.root.bind('<KeyPress-d>', lambda e: self.player_snake.set_direction('Right'))

        # Start game loop
        self.update_game_loop()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def spawn_food(self):
        """Spawns a new food item at a random valid location"""
        all_snake_positions = []
        for snake in self.snakes:
            if snake.is_alive:
                all_snake_positions.extend(snake.body)

        food_positions = [f['position'] for f in self.food]
        position = find_empty_position(excluded_positions=all_snake_positions + food_positions)

        food_id = f"food_{len(self.food)}" # Assign a unique ID
        food_data = {'id': food_id, 'position': position}
        self.food.append(food_data)

        # Draw food on canvas
        food_canvas_item = self.canvas.create_oval(
            position[0] * CELL_SIZE, position[1] * CELL_SIZE,
            (position[0] + 1) * CELL_SIZE, (position[1] + 1) * CELL_SIZE,
            fill=COLOR_FOOD, outline=COLOR_BACKGROUND
        )
        self.food_canvas_items.append(food_canvas_item)

    def check_collisions(self):
        """
        Checks for collisions between snakes and handles them.
        Updates game state accordingly.
        """
        new_positions_per_snake = {}

        # Get new positions from each snake's update
        for snake in self.snakes:
            if snake.is_alive:
                new_positions = snake.update(self.game_state)
                new_positions_per_snake[snake] = new_positions

        # Check collisions between snakes
        for snake1 in self.snakes:
            if not snake1.is_alive or snake1 not in new_positions_per_snake:
                continue
            new_head1 = new_positions_per_snake[snake1][0] if new_positions_per_snake[snake1] else None

            for snake2 in self.snakes:
                if snake1 == snake2 or not snake2.is_alive or snake2 not in new_positions_per_snake:
                    continue

                new_head2 = new_positions_per_snake[snake2][0] if new_positions_per_snake[snake2] else None

                # Skip if both snakes are moving into the same cell (head-on collision)
                if new_head1 and new_head2 and new_head1 == new_head2:
                    continue

                # Check if snake1's new head collides with snake2's body
                if new_head1 and new_head1 in snake2.body:
                    # Determine collision type
                    collision_type = 'snake'
                    if snake1.length < snake2.length:
                        if snake2.body[0] == new_head1:
                             collision_type = 'snake_head'
                        else:
                             collision_type = 'snake_tail'
                    elif snake1.length > snake2.length:
                        collision_type = 'snake'
                    else: # Equal length
                        collision_type = 'snake_equal'

                    snake1.die(self.game_state, snake2, collision_type)

                # Check if snake2's new head collides with snake1's body
                if new_head2 and new_head2 in snake1.body:
                    collision_type = 'snake'
                    if snake2.length < snake1.length:
                        if snake1.body[0] == new_head2:
                            collision_type = 'snake_head'
                        else:
                            collision_type = 'snake_tail'
                    elif snake2.length > snake1.length:
                        collision_type = 'snake'
                    else: # Equal length
                        collision_type = 'snake_equal'

                    snake2.die(self.game_state, snake1, collision_type)

            # Check self-collision (already handled in Snake.update)

    def update_game_loop(self):
        """The main game loop, called repeatedly by tkinter's after method"""
        if self.game_over:
            return

        elapsed_time_ms = int((time.time() - self.start_time) * 1000)

        # Check game end condition (time)
        if elapsed_time_ms >= GAME_DURATION_MS:
            self.game_over = True
            self.end_game()
            return

        # AI decision making
        for snake in self.snakes:
            if snake.is_alive and snake.is_ai:
                snake.decide_direction_ai(self.game_state)

        # Update snakes and check collisions
        self.check_collisions()

        # Process food eaten (spawn new food if needed)
        eaten_food = self.game_state.get('eaten_food', [])
        for eaten in eaten_food:
             if len(self.food) + len(eaten_food) < INITIAL_FOOD_COUNT:
                  self.root.after(FOOD_SPAWN_DELAY_MS, self.spawn_food) # Schedule spawn after delay

        self.game_state['eaten_food'] = [] # Clear eaten food list

        # Random food spawn chance
        if random.random() < FOOD_SPAWN_CHANCE and len(self.food) < INITIAL_FOOD_COUNT:
             self.root.after(FOOD_SPAWN_DELAY_MS, self.spawn_food)

        # Update score overlay
        self.update_score_overlay()

        # Schedule next update
        self.root.after(UPDATE_DELAY_MS, self.update_game_loop)

    def update_score_overlay(self):
        """Updates the on-screen score display"""
        if self.score_overlay:
            self.canvas.delete(self.score_overlay)
        scores_text = "Scores:\n"
        for i, snake in enumerate(self.snakes):
            color = snake.color
            scores_text += f"{'P' if i == 0 else 'AI'}: {snake.length}   "
            # Remove individual labels update if using a table
        scores_text += f"\nTime: {max(0, GAME_DURATION_MS - int((time.time() - self.start_time) * 1000)) // 1000}s"

        # Determine winner for overlay display (if time runs out)
        if self.game_over and self.winner_snake:
            winner_color = self.winner_snake.color
            winner_text = "Winner: "
        else:
            winner_text = ""
            winner_color = COLOR_TEXT

        # Create overlay background
        self.score_overlay = self.canvas.create_rectangle(
            10, 10, 150, 90, # Adjust size based on text length
            fill=COLOR_OVERLAY_BG, outline=""
        )
        # Create overlay text
        self.canvas.create_text(
            75, 50, # Center text within background
            text=f"{winner_text}\n{scores_text}",
            fill=winner_color if self.game_over else COLOR_TEXT,
            font=('Arial', 12, 'bold'),
            anchor='center'
        )

    def end_game(self):
        """Handles game end logic (displaying winner, etc.)"""
        # Determine winner
        self.winner_snake = get_largest_snake([s for s in self.snakes if s.is_alive])

        # Clear existing overlays
        if self.score_overlay:
            self.canvas.delete(self.score_overlay)
        for label in self.score_labels:
            label.destroy()
        self.score_labels = []

        # Create game over overlay
        overlay_width = 400
        overlay_height = 250
        x1 = (GRID_WIDTH * CELL_SIZE - overlay_width) / 2
        y1 = (GRID_HEIGHT * CELL_SIZE - overlay_height) / 2
        x2 = x1 + overlay_width
        y2 = y1 + overlay_height

        overlay_bg = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=COLOR_OVERLAY_BG, outline=COLOR_TEXT, width=2
        )

        # Game Over text
        self.canvas.create_text(
            (x1 + x2) / 2, y1 + 30,
            text="Game Over!",
            fill=COLOR_TEXT,
            font=('Arial', 24, 'bold')
        )

        # Winner text
        if self.winner_snake:
            winner_color = self.winner_snake.color
            winner_text = f"Winner: {'Player' if self.winner_snake == self.player_snake else 'AI'}"
        else:
            winner_text = "Draw!"
            winner_color = COLOR_TEXT

        self.canvas.create_text(
            (x1 + x2) / 2, y1 + 70,
            text=winner_text,
            fill=winner_color,
            font=('Arial', 20, 'bold')
        )

        # Scores table
        table_x = x1 + 20
        table_y = y1 + 100
        row_height = 25
        col_width = 120

        # Table headers
        self.canvas.create_text(
            table_x, table_y,
            text="Snake",
            fill=COLOR_TEXT,
            font=('Arial', 14, 'bold'),
            anchor='nw'
        )
        self.canvas.create_text(
            table_x + col_width, table_y,
            text="Length",
            fill=COLOR_TEXT,
            font=('Arial', 14, 'bold'),
            anchor='nw'
        )
        table_y += row_height # Move down for data rows

        # Sort snakes by length descending
        sorted_snakes = sorted(self.snakes, key=lambda s: s.length, reverse=True)

        for snake in sorted_snakes:
            # Snake name
            self.canvas.create_text(
                table_x, table_y,
                text=f"{'Player' if snake == self.player_snake else 'AI'}",
                fill=snake.color,
                font=('Arial', 12),
                anchor='nw'
            )
            # Length
            self.canvas.create_text(
                table_x + col_width, table_y,
                text=str(snake.length),
                fill=snake.color,
                font=('Arial', 12),
                anchor='nw'
            )
            table_y += row_height

        # Exit button
        exit_button = tk.Button(
            self.root,
            text="Exit",
            command=self.root.destroy,
            bg=COLOR_BACKGROUND,
            fg=COLOR_TEXT,
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=5
        )
        exit_button.place(relx=0.5, rely=0.8, anchor='center')

    def on_closing(self):
        """Handles window closing event"""
        self.game_over = True
        self.root.destroy()

# --- Start the game ---
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()