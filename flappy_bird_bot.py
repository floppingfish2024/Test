import pygame
import random
import json
from filelock import FileLock

class FlappyBirdBot:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.exploration_rate:
            return random.choice([0, 1])  # 0 for do nothing, 1 for flap
        else:
            q_values = [self.get_q_value(state, 0), self.get_q_value(state, 1)]
            return q_values.index(max(q_values))

    def update_q_value(self, state, action, reward, next_state):
        old_q_value = self.get_q_value(state, action)

        future_q_values = [self.get_q_value(next_state, 0), self.get_q_value(next_state, 1)]
        future_q_value = max(future_q_values)

        new_q_value = old_q_value + self.learning_rate * (reward + self.discount_factor * future_q_value - old_q_value)
        self.q_table[(state, action)] = new_q_value

    def save_q_table(self, file_path):
        lock = FileLock(file_path + ".lock")
        with lock:
            with open(file_path, 'w') as f:
                serializable_q_table = {f"{k[0]}_{k[1]}": v for k, v in self.q_table.items()}
                json.dump(serializable_q_table, f)

    def load_q_table(self, file_path):
        lock = FileLock(file_path + ".lock")
        with lock:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.q_table = { (eval(k.split('_')[0]), int(k.split('_')[1])): v for k, v in data.items()}
            except (FileNotFoundError, json.JSONDecodeError):
                self.q_table = {}

# Game constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 100
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
GRAVITY = 1
FLAP_STRENGTH = -9
PIPE_SPEED = -4

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird Bot')
        self.clock = pygame.time.Clock()
        self.bird_y = SCREEN_HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False

    def reset(self):
        self.bird_y = SCREEN_HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self._add_pipe()

    def _add_pipe(self):
        pipe_y = random.randint(PIPE_GAP, SCREEN_HEIGHT - PIPE_GAP)
        self.pipes.append({'x': SCREEN_WIDTH, 'y': pipe_y})

    def step(self, action):
        reward = 0.1  # Small reward for surviving
        if action == 1:  # Flap
            self.bird_velocity = FLAP_STRENGTH

        # Update bird position
        self.bird_velocity += GRAVITY
        self.bird_y += self.bird_velocity

        # Update pipe positions
        for pipe in self.pipes:
            pipe['x'] += PIPE_SPEED

        # Add new pipe if needed
        if self.pipes[0]['x'] < SCREEN_WIDTH / 2 and len(self.pipes) == 1:
            self._add_pipe()
            self.score += 1
            reward = 1 # Reward for passing a pipe

        # Remove off-screen pipes
        if self.pipes[0]['x'] < -PIPE_WIDTH:
            self.pipes.pop(0)

        # Check for collisions
        if self.bird_y > SCREEN_HEIGHT or self.bird_y < 0:
            self.game_over = True
            reward = -1

        bird_rect = pygame.Rect(SCREEN_WIDTH // 4, self.bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        for pipe in self.pipes:
            upper_pipe_rect = pygame.Rect(pipe['x'], 0, PIPE_WIDTH, pipe['y'] - PIPE_GAP // 2)
            lower_pipe_rect = pygame.Rect(pipe['x'], pipe['y'] + PIPE_GAP // 2, PIPE_WIDTH, SCREEN_HEIGHT)
            if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
                self.game_over = True
                reward = -1

        next_pipe = self.pipes[0]
        state = (self.bird_y, self.bird_velocity, next_pipe['x'] - (SCREEN_WIDTH // 4), next_pipe['y'] - self.bird_y)

        return state, reward, self.game_over


    def render(self):
        self.screen.fill((0, 0, 0)) # Black background
        # Draw bird
        pygame.draw.rect(self.screen, (255, 255, 0), (SCREEN_WIDTH // 4, self.bird_y, BIRD_WIDTH, BIRD_HEIGHT)) # Yellow bird
        # Draw pipes
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe['x'], 0, PIPE_WIDTH, pipe['y'] - PIPE_GAP // 2)) # Upper pipe
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe['x'], pipe['y'] + PIPE_GAP // 2, PIPE_WIDTH, SCREEN_HEIGHT)) # Lower pipe
        pygame.display.update()


if __name__ == '__main__':
    game = FlappyBirdGame()
    bot = FlappyBirdBot()
    bot.load_q_table("q_table.json")

    for i in range(1000):
        game.reset()
        state = (game.bird_y, game.bird_velocity, 0, 0)
        while not game.game_over:
            action = bot.choose_action(state)
            next_state, reward, done = game.step(action)
            bot.update_q_value(state, action, reward, next_state)
            state = next_state

    bot.save_q_table("q_table.json")
    print("Training complete.")
