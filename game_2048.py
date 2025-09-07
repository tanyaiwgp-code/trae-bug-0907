import pygame
import random
import sys

# 确保中文能正常显示
pygame.init()
pygame.font.init()

# 游戏常量
GRID_SIZE = 4
CELL_SIZE = 100
CELL_MARGIN = 10
WINDOW_SIZE = GRID_SIZE * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN

# 颜色定1义
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)
SCORE_COLOR = (119, 110, 101)
GAME_OVER_COLOR = (238, 228, 218, 128)

# 数字方块颜色映射
CELL_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# 数字颜色映射
TEXT_COLORS = {
    2: (119, 110, 101),
    4: (119, 110, 101),
    8: (249, 246, 242),
    16: (249, 246, 242),
    32: (249, 246, 242),
    64: (249, 246, 242),
    128: (249, 246, 242),
    256: (249, 246, 242),
    512: (249, 246, 242),
    1024: (249, 246, 242),
    2048: (249, 246, 242),
}

# 设置字体，尝试使用系统中的中文字体
def get_font(size):
    try:
        return pygame.font.Font("simhei.ttf", size)
    except:
        # 如果没有找到指定字体，使用系统默认字体
        return pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial"], size)

class Tile:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.width = CELL_SIZE
        self.height = CELL_SIZE
        self.color = CELL_COLORS.get(value, (0, 0, 0))
        self.text_color = TEXT_COLORS.get(value, (255, 255, 255))
        self.merged = False  # 标记是否已经合并过
        self.font = get_font(40 if value < 100 else 35 if value < 1000 else 30)

    def draw(self, surface):
        # 绘制方块
        rect = pygame.Rect(
            self.x * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN,
            self.y * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, self.color, rect, 0, 8)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1, 8)  # 边框

        # 绘制数字
        if self.value != 0:
            text = self.font.render(str(self.value), True, self.text_color)
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)

    def update_value(self, value):
        self.value = value
        self.color = CELL_COLORS.get(value, (0, 0, 0))
        self.text_color = TEXT_COLORS.get(value, (255, 255, 255))
        self.font = get_font(40 if value < 100 else 35 if value < 1000 else 30)
        self.merged = False

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))  # 额外空间显示分数
        pygame.display.set_caption("2048游戏")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        # 初始化棋盘
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.tiles = []
        self.score = 0
        self.game_over = False
        self.won = False

        # 初始化两个随机方块
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        # 找到所有空位置
        empty_cells = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        if empty_cells:
            # 随机选择一个空位置
            i, j = random.choice(empty_cells)
            # 90%概率生成2，10%概率生成4
            value = 2 if random.random() < 0.9 else 4
            self.grid[i][j] = value
            self.tiles.append(Tile(value, j, i))  # 注意x和y的顺序
            return True
        return False

    def draw_board(self):
        # 绘制背景
        self.screen.fill(BACKGROUND_COLOR)

        # 绘制分数
        score_font = get_font(30)
        score_text = score_font.render(f"分数: {self.score}", True, SCORE_COLOR)
        self.screen.blit(score_text, (CELL_MARGIN, WINDOW_SIZE + 20))

        # 绘制游戏状态
        status_font = get_font(24)
        if self.won:
            status_text = status_font.render("恭喜你，获胜了！按R键重新开始", True, SCORE_COLOR)
        elif self.game_over:
            status_text = status_font.render("游戏结束！按R键重新开始", True, SCORE_COLOR)
        else:
            status_text = status_font.render("使用方向键移动方块", True, SCORE_COLOR)
        self.screen.blit(status_text, (CELL_MARGIN, WINDOW_SIZE + 60))

        # 绘制空单元格
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                rect = pygame.Rect(
                    j * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN,
                    i * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(self.screen, EMPTY_CELL_COLOR, rect, 0, 8)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1, 8)  # 边框

        # 绘制方块
        for tile in self.tiles:
            tile.draw(self.screen)

        # 如果游戏结束或获胜，绘制半透明覆盖层
        if self.game_over or self.won:
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            overlay.fill(GAME_OVER_COLOR)
            self.screen.blit(overlay, (0, 0))

            # 绘制游戏结束/获胜文字
            end_font = get_font(48)
            if self.won:
                end_text = end_font.render("你赢了！", True, SCORE_COLOR)
            else:
                end_text = end_font.render("游戏结束", True, SCORE_COLOR)
            end_rect = end_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 30))
            self.screen.blit(end_text, end_rect)

            restart_font = get_font(24)
            restart_text = restart_font.render("按R键重新开始", True, SCORE_COLOR)
            restart_rect = restart_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 30))
            self.screen.blit(restart_text, restart_rect)

    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            # 合并相同的方块
            for j in range(1, GRID_SIZE):
                if self.grid[i][j] != 0:
                    k = j
                    while k > 0 and self.grid[i][k-1] == 0:
                        # 移动到空白位置
                        self.grid[i][k-1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k -= 1
                        moved = True
                    if k > 0 and self.grid[i][k-1] == self.grid[i][k] and not any(tile.x == k-1 and tile.y == i and tile.merged for tile in self.tiles):
                        # 合并相同的方块
                        self.grid[i][k-1] *= 2
                        self.score += self.grid[i][k-1]
                        self.grid[i][k] = 0
                        moved = True
                        # 更新方块信息
                        for tile in self.tiles:
                            if tile.x == k and tile.y == i:
                                self.tiles.remove(tile)
                                break
                        for tile in self.tiles:
                            if tile.x == k-1 and tile.y == i:
                                tile.update_value(self.grid[i][k-1])
                                tile.merged = True
                                break
        return moved

    def move_right(self):
        moved = False
        for i in range(GRID_SIZE):
            # 合并相同的方块
            for j in range(GRID_SIZE-2, -1, -1):
                if self.grid[i][j] != 0:
                    k = j
                    while k < GRID_SIZE-1 and self.grid[i][k+1] == 0:
                        # 移动到空白位置
                        self.grid[i][k+1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k += 1
                        moved = True
                    if k < GRID_SIZE-1 and self.grid[i][k+1] == self.grid[i][k] and not any(tile.x == k+1 and tile.y == i and tile.merged for tile in self.tiles):
                        # 合并相同的方块
                        self.grid[i][k+1] *= 2
                        self.score += self.grid[i][k+1]
                        self.grid[i][k] = 0
                        moved = True
                        # 更新方块信息
                        for tile in self.tiles:
                            if tile.x == k and tile.y == i:
                                self.tiles.remove(tile)
                                break
                        for tile in self.tiles:
                            if tile.x == k+1 and tile.y == i:
                                tile.update_value(self.grid[i][k+1])
                                tile.merged = True
                                break
        return moved

    def move_up(self):
        moved = False
        for j in range(GRID_SIZE):
            # 合并相同的方块
            for i in range(1, GRID_SIZE):
                if self.grid[i][j] != 0:
                    k = i
                    while k > 0 and self.grid[k-1][j] == 0:
                        # 移动到空白位置
                        self.grid[k-1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k -= 1
                        moved = True
                    if k > 0 and self.grid[k-1][j] == self.grid[k][j] and not any(tile.x == j and tile.y == k-1 and tile.merged for tile in self.tiles):
                        # 合并相同的方块
                        self.grid[k-1][j] *= 2
                        self.score += self.grid[k-1][j]
                        self.grid[k][j] = 0
                        moved = True
                        # 更新方块信息
                        for tile in self.tiles:
                            if tile.x == j and tile.y == k:
                                self.tiles.remove(tile)
                                break
                        for tile in self.tiles:
                            if tile.x == j and tile.y == k-1:
                                tile.update_value(self.grid[k-1][j])
                                tile.merged = True
                                break
        return moved

    def move_down(self):
        moved = False
        for j in range(GRID_SIZE):
            # 合并相同的方块
            for i in range(GRID_SIZE-2, -1, -1):
                if self.grid[i][j] != 0:
                    k = i
                    while k < GRID_SIZE-1 and self.grid[k+1][j] == 0:
                        # 移动到空白位置
                        self.grid[k+1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k += 1
                        moved = True
                    if k < GRID_SIZE-1 and self.grid[k+1][j] == self.grid[k][j] and not any(tile.x == j and tile.y == k+1 and tile.merged for tile in self.tiles):
                        # 合并相同的方块
                        self.grid[k+1][j] *= 2
                        self.score += self.grid[k+1][j]
                        self.grid[k][j] = 0
                        moved = True
                        # 更新方块信息
                        for tile in self.tiles:
                            if tile.x == j and tile.y == k:
                                self.tiles.remove(tile)
                                break
                        for tile in self.tiles:
                            if tile.x == j and tile.y == k+1:
                                tile.update_value(self.grid[k+1][j])
                                tile.merged = True
                                break
        return moved

    def check_game_over(self):
        # 检查是否还有空位置
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False

        # 检查是否还能移动
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE-1):
                if self.grid[i][j] == self.grid[i][j+1]:
                    return False

        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE-1):
                if self.grid[i][j] == self.grid[i+1][j]:
                    return False

        return True

    def check_win(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] >= 2048:
                    return True
        return False

    def update_tiles(self):
        # 重新创建所有方块
        self.tiles = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] != 0:
                    self.tiles.append(Tile(self.grid[i][j], j, i))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # 重新开始游戏
                        self.reset_game()
                    elif not self.game_over and not self.won:
                        moved = False
                        if event.key == pygame.K_LEFT:
                            moved = self.move_left()
                        elif event.key == pygame.K_RIGHT:
                            moved = self.move_right()
                        elif event.key == pygame.K_UP:
                            moved = self.move_up()
                        elif event.key == pygame.K_DOWN:
                            moved = self.move_down()

                        if moved:
                            # 更新方块
                            self.update_tiles()
                            # 添加新方块
                            self.add_random_tile()
                            # 检查是否获胜
                            if self.check_win():
                                self.won = True
                            # 检查是否游戏结束
                            elif self.check_game_over():
                                self.game_over = True

            # 绘制游戏
            self.draw_board()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    print("2048游戏启动中...")
    print("使用方向键移动方块，按R键重新开始游戏")
    try:
        game = Game2048()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        print("请确保已安装Pygame库: pip install pygame")