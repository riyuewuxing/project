###############################################################################
#                                                                             #
#                             坦克大战游戏 - 主程序                           #
#                                                                             #
###############################################################################

###############################################################################
#                              导入必要的库和模块                              #
###############################################################################

import pygame
import random
import os
import sys
import time
import traceback
import math

###############################################################################
#                                常量和配置                                    #
###############################################################################

# 初始化pygame
pygame.init()

# 屏幕尺寸常量
SCREEN_SCALE = 1.5  # 屏幕缩放比例
SCREEN_WIDTH = int(800 * SCREEN_SCALE)  # 扩大为原来的1.5倍
SCREEN_HEIGHT = int(600 * SCREEN_SCALE)  # 扩大为原来的1.5倍

# 创建一个字典来记录按键状态
KEY_STATE = {
    pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False,
    pygame.K_SPACE: False,
    pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False,
    pygame.K_KP0: False, pygame.K_KP_0: False, pygame.K_INSERT: False, pygame.K_0: False,
    pygame.K_RETURN: False
}

# 调试信息：打印所有按键码
print("键值映射:")
print(f"WASD: {pygame.K_w}, {pygame.K_a}, {pygame.K_s}, {pygame.K_d}")
print(f"方向键: {pygame.K_UP}, {pygame.K_DOWN}, {pygame.K_LEFT}, {pygame.K_RIGHT}")
print(f"射击键: SPACE={pygame.K_SPACE}, KP0={pygame.K_KP0}, KP_0={pygame.K_KP_0}, 0={pygame.K_0}, INSERT={pygame.K_INSERT}, RETURN={pygame.K_RETURN}")

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("坦克大战")
clock = pygame.time.Clock()

# 颜色常量
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (150, 255, 150)
LIGHT_BLUE = (150, 150, 255)
BROWN = (165, 42, 42)
PINK = (255, 105, 180)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# 游戏常量
FPS = 60
GRID_SIZE = 6  # 最小方块尺寸，原来是8，改成6让方块更小
BLOCK_SIZE = 12  # 地形方块大小，原来是16
TANK_SIZE = 24   # 坦克大小，原来是32
BULLET_SIZE = 6  # 子弹大小，原来是8

# 调试模式
DEBUG_MODE = False  # 设置为False关闭调试信息显示

# 游戏模式
SINGLE_PLAYER = 0
TWO_PLAYERS = 1

# 玩家ID
PLAYER_ONE = 0
PLAYER_TWO = 1

# 游戏状态常量 (添加在这里)
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
LEVEL_COMPLETE = "level_complete"
VICTORY = "victory"
INSTRUCTIONS = "instructions"

# 坦克级别常量
TANK_LEVEL_1 = 0  # 初始级别
TANK_LEVEL_2 = 1  # 升级一次
TANK_LEVEL_3 = 2  # 升级两次

# 子弹级别常量
BULLET_LEVEL_1 = 0  # 初始子弹
BULLET_LEVEL_2 = 1  # 速度提升+双发
BULLET_LEVEL_3 = 2  # 满级子弹(伤害1.5倍)

# 方向常量
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# 地形类型常量
EMPTY = 0
BRICK = 1
STEEL = 2
WATER = 3
GRASS = 4
BASE = 5

# 敌人类型
NORMAL_ENEMY = 0
FAST_ENEMY = 1
ARMORED_ENEMY = 2
BOSS_ENEMY = 3      # 新增：Boss敌人
ELITE_ENEMY = 4     # 新增：精英敌人
ULTIMATE_ENEMY = 5  # 新增：终极敌人

# 道具类型
BULLET_UPGRADE = 0
SPEED_BOOST = 1
SHIELD = 2
HEALTH_BOOST = 3  # 增加生命值
TANK_UPGRADE = 4  # 坦克升级道具
BASE_FORTIFY = 5 # 新增基地加固道具类型

# 子弹类型
NORMAL_BULLET = 0
FAST_BULLET = 1
POWERFUL_BULLET = 2
SUPER_BULLET = 3

# 敌人属性
ENEMY_PROPERTIES = {
    NORMAL_ENEMY: {"speed": 2, "health": 1, "color": RED},
    FAST_ENEMY: {"speed": 3, "health": 1, "color": BLUE},
    ARMORED_ENEMY: {"speed": 1, "health": 3, "color": GRAY},
    BOSS_ENEMY: {"speed": 1.5, "health": 5, "color": PURPLE},
    ELITE_ENEMY: {"speed": 2, "health": 4, "color": ORANGE},
    ULTIMATE_ENEMY: {"speed": 2, "health": 8, "color": YELLOW}
}

# 子弹属性
BULLET_PROPERTIES = {
    NORMAL_BULLET: {"speed": 7, "damage": 1, "color": WHITE},
    FAST_BULLET: {"speed": 12, "damage": 1, "color": BLUE},
    POWERFUL_BULLET: {"speed": 7, "damage": 2, "color": RED},
    SUPER_BULLET: {"speed": 10, "damage": 3, "color": YELLOW}
}

# 道具形状定义
POWER_UP_PATTERNS = {
    BULLET_UPGRADE: [  # 子弹升级 - 弹头形状
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    SPEED_BOOST: [  # 速度提升 - 翅膀形状
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    SHIELD: [  # 护盾 - 盾牌形状
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0]
    ],
    HEALTH_BOOST: [  # 生命值 - 心形
        [0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0]
    ],
    TANK_UPGRADE: [  # 坦克升级 - 星星形状
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0]
    ],
    BASE_FORTIFY: [ # 基地加固 - 类似钢块图案
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
}

# 控制键位
PLAYER_CONTROLS = {
    PLAYER_ONE: {
        "UP": pygame.K_w,
        "DOWN": pygame.K_s,
        "LEFT": pygame.K_a,
        "RIGHT": pygame.K_d,
        "FIRE": pygame.K_SPACE    # 空格键
    },
    PLAYER_TWO: {
        "UP": pygame.K_UP,
        "DOWN": pygame.K_DOWN,
        "LEFT": pygame.K_LEFT,
        "RIGHT": pygame.K_RIGHT,
        "FIRE": pygame.K_KP0      # 修正：使用KP0常量而非KP_0
    }
}

# 玩家坦克颜色
PLAYER_COLORS = {
    PLAYER_ONE: {
        TANK_LEVEL_1: (GREEN, LIGHT_GREEN),      # 1级：绿色
        TANK_LEVEL_2: (BLUE, LIGHT_BLUE),        # 2级：蓝色
        TANK_LEVEL_3: (YELLOW, ORANGE)           # 3级：黄色
    },
    PLAYER_TWO: {
        TANK_LEVEL_1: (RED, PINK),               # 1级：红色
        TANK_LEVEL_2: (ORANGE, YELLOW),          # 2级：橙色
        TANK_LEVEL_3: (BLUE, LIGHT_BLUE)         # 3级：蓝色
    }
}

# 使用小方块定义的形状模式
# 1表示有方块，0表示空白
# 玩家坦克形状定义 (4x4 网格)
PLAYER_TANK_PATTERN = {
    UP: [
        [0, 1, 1, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1]
    ],
    RIGHT: [
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [1, 1, 1, 0]
    ],
    DOWN: [
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 1, 1, 0]
    ],
    LEFT: [
        [0, 1, 1, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 0],
        [0, 1, 1, 1]
    ]
}

# 敌人坦克形状定义 (重新设计，使其更有区分度)
ENEMY_TANK_PATTERNS = {
    NORMAL_ENEMY: { # 基础型
        UP: [[0,1,1,0],[1,1,1,1],[1,1,1,1],[1,0,0,1]],
        RIGHT: [[1,1,1,0],[0,1,1,1],[0,1,1,1],[1,1,1,0]],
        DOWN: [[1,0,0,1],[1,1,1,1],[1,1,1,1],[0,1,1,0]],
        LEFT: [[0,1,1,1],[1,1,1,0],[1,1,1,0],[0,1,1,1]]
    },
    FAST_ENEMY: { # 稍窄，履带突出
        UP: [[0,1,1,0],[0,1,1,0],[1,1,1,1],[1,1,1,1]],
        RIGHT: [[1,0,1,1],[1,1,1,1],[1,1,1,1],[1,0,1,1]],
        DOWN: [[1,1,1,1],[1,1,1,1],[0,1,1,0],[0,1,1,0]],
        LEFT: [[1,1,0,1],[1,1,1,1],[1,1,1,1],[1,1,0,1]]
    },
    ARMORED_ENEMY: { # 更厚重，方正
        UP: [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,0,0,1]],
        RIGHT: [[1,1,1,1],[1,0,1,1],[1,0,1,1],[1,1,1,1]],
        DOWN: [[1,0,0,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]],
        LEFT: [[1,1,1,1],[1,1,0,1],[1,1,0,1],[1,1,1,1]]
    },
    BOSS_ENEMY: { # 更大，炮管更明显，可能有特殊标记
        UP: [[0,1,1,0],[1,1,1,1],[1,0,0,1],[1,1,1,1]],
        RIGHT: [[1,1,1,0],[1,0,1,1],[1,0,1,1],[0,1,1,1]],
        DOWN: [[1,1,1,1],[1,0,0,1],[1,1,1,1],[0,1,1,0]],
        LEFT: [[1,1,1,0],[1,1,0,1],[1,1,0,1],[0,1,1,1]] # 稍微不对称
    },
    ELITE_ENEMY: { # 装甲和速度的结合体，可能有尖锐特征
        UP: [[1,0,0,1],[1,1,1,1],[1,1,1,1],[0,1,1,0]],
        RIGHT: [[0,1,1,1],[1,1,1,0],[0,1,1,1],[1,1,1,0]],
        DOWN: [[0,1,1,0],[1,1,1,1],[1,1,1,1],[1,0,0,1]],
        LEFT: [[1,1,1,0],[1,0,1,1],[1,0,1,1],[1,1,1,0]]
    },
    ULTIMATE_ENEMY: { # 最大最强，全覆盖或特殊形状
        UP: [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],
        RIGHT: [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],
        DOWN: [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],
        LEFT: [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]]
    }
}

# 子弹形状定义 (2x2 网格)
BULLET_PATTERNS = {
    UP: [
        [1, 1],
        [0, 0]
    ],
    RIGHT: [
        [1, 0],
        [1, 0]
    ],
    DOWN: [
        [0, 0],
        [1, 1]
    ],
    LEFT: [
        [0, 1],
        [0, 1]
    ]
}

# 地形形状定义 (2x2 网格)
BRICK_PATTERN = [
    [1, 1],
    [1, 1]
]

STEEL_PATTERN = [
    [1, 1],
    [1, 1]
]

WATER_PATTERN = [
    [1, 1],
    [1, 1]
]

GRASS_PATTERN = [
    [1, 1],
    [1, 1]
]

# 基地图案 (例如 4x4 网格的鹰标)
BASE_PATTERN = [
    [0, 1, 1, 0],
    [1, 1, 1, 1],
    [0, 1, 1, 0],
    [1, 0, 0, 1]
]

# 地形属性
TERRAIN_PROPERTIES = {
    EMPTY: {"passable": True, "destructible": False, "image": None, "pattern": None},
    BRICK: {"passable": False, "destructible": True, "image": None, "pattern": BRICK_PATTERN},
    STEEL: {"passable": False, "destructible": False, "image": None, "pattern": STEEL_PATTERN},
    WATER: {"passable": False, "destructible": False, "image": None, "pattern": WATER_PATTERN},
    GRASS: {"passable": True, "destructible": False, "image": None, "pattern": GRASS_PATTERN},
    BASE: {"passable": False, "destructible": True, "image": None, "pattern": BASE_PATTERN}
}

# 坦克级别属性
TANK_LEVEL_PROPERTIES = {
    TANK_LEVEL_1: {
        "health_max": 3,      # 生命上限
        "bullet_speed": 7,    # 子弹速度
        "fire_rate": 500,     # 射击间隔(毫秒)
        "bullet_count": 1,    # 同时发射子弹数
        "bullet_damage": 1    # 子弹伤害
    },
    TANK_LEVEL_2: {
        "health_max": 4,
        "bullet_speed": 9,
        "fire_rate": 400,
        "bullet_count": 1,
        "bullet_damage": 2
    },
    TANK_LEVEL_3: {
        "health_max": 5,
        "bullet_speed": 10,
        "fire_rate": 300,
        "bullet_count": 2,    # 可以同时发射2颗子弹
        "bullet_damage": 2
    }
}

# 高级坦克图案 - 为每个级别的坦克定义不同外观
PLAYER_TANK_LEVEL_PATTERNS = {
    TANK_LEVEL_1: PLAYER_TANK_PATTERN,  # 级别1使用原始图案
    TANK_LEVEL_2: {  # 级别2坦克 - 增加装甲和更长炮管
        UP: [
            [0, 1, 1, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ],
        RIGHT: [
            [1, 1, 1, 1],
            [0, 1, 1, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 1]
        ],
        DOWN: [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 1, 1, 0]
        ],
        LEFT: [
            [1, 1, 1, 1],
            [1, 1, 1, 0],
            [1, 1, 1, 0],
            [1, 1, 1, 1]
        ]
    },
    TANK_LEVEL_3: {  # 级别3坦克 - 双炮塔设计
        UP: [
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ],
        RIGHT: [
            [1, 1, 1, 1],
            [1, 1, 1, 0],
            [1, 1, 1, 0],
            [1, 1, 1, 1]
        ],
        DOWN: [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 0, 0, 1]
        ],
        LEFT: [
            [1, 1, 1, 1],
            [0, 1, 1, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 1]
        ]
    }
}

###############################################################################
#                              工具函数和辅助方法                               #
###############################################################################

def create_surface_from_pattern(pattern, primary_color, secondary_color=None, grid_size=GRID_SIZE, scale=1.0):
    """根据二维数组模式创建表面"""
    try:
        if secondary_color is None:
            secondary_color = primary_color

        # 获取模式的高度和宽度
        height = len(pattern)
        width = len(pattern[0]) if height > 0 else 0

        # 创建表面
        surface_width = width * grid_size
        surface_height = height * grid_size
        surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)

        # 根据模式填充表面
        for y in range(height):
            for x in range(width):
                if x < len(pattern[y]) and pattern[y][x] == 1:
                    color = primary_color if (x + y) % 2 == 0 else secondary_color
                    pygame.draw.rect(surface, color,
                                    (x * grid_size, y * grid_size, grid_size, grid_size))

        # 如果需要缩放
        if scale != 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            surface = pygame.transform.scale(surface, (new_width, new_height))

        return surface
    except Exception as e:
        print(f"[ERROR] create_surface_from_pattern 出错: {e}")
        # 创建备用表面
        backup_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        backup_surface.fill(primary_color)
        return backup_surface

# 预渲染所有玩家坦克图像
player_tank_images = {}
for p_id in [PLAYER_ONE, PLAYER_TWO]:
    player_tank_images[p_id] = {}
    for level in [TANK_LEVEL_1, TANK_LEVEL_2, TANK_LEVEL_3]:
        player_tank_images[p_id][level] = {}
        level_pattern = PLAYER_TANK_LEVEL_PATTERNS[level]
        primary_color, secondary_color = PLAYER_COLORS[p_id][level]
        for direction in [UP, RIGHT, DOWN, LEFT]:
            tank_pattern = level_pattern[direction]
            player_tank_images[p_id][level][direction] = create_surface_from_pattern(
                tank_pattern, primary_color, secondary_color
            )

# 图像加载函数
def load_image(name, size=None, color_key=None):
    """加载图像并转换为合适的格式"""
    image_dir = os.path.join("assets", "images")
    fullname = os.path.join(image_dir, name)

    try:
        # 尝试加载图像
        image = pygame.image.load(fullname)
        if size:
            image = pygame.transform.scale(image, size)
    except (pygame.error, FileNotFoundError) as e:
        print(f"无法加载图像: {fullname}")
        print(e)
        # 创建一个替代的表面
        image = pygame.Surface(size if size else (BLOCK_SIZE, BLOCK_SIZE))
        image.fill(color_key if color_key else (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    return image.convert_alpha()

# 加载图像资源 (备用颜色方块用于图像加载失败时)
try:
    # 尝试创建资源目录
    os.makedirs(os.path.join("assets", "images"), exist_ok=True)

    # 使用小方块组合创建地形图像
    brick_img = create_surface_from_pattern(BRICK_PATTERN, RED, BROWN)
    steel_img = create_surface_from_pattern(STEEL_PATTERN, GRAY, WHITE)
    water_img = create_surface_from_pattern(WATER_PATTERN, BLUE, LIGHT_BLUE)
    grass_img = create_surface_from_pattern(GRASS_PATTERN, GREEN, LIGHT_GREEN)
    base_img = create_surface_from_pattern(BASE_PATTERN, YELLOW, RED, grid_size=GRID_SIZE) # 使用新图案和 grid_size

    # 更新地形属性中的图像
    TERRAIN_PROPERTIES[BRICK]["image"] = brick_img
    TERRAIN_PROPERTIES[STEEL]["image"] = steel_img
    TERRAIN_PROPERTIES[WATER]["image"] = water_img
    TERRAIN_PROPERTIES[GRASS]["image"] = grass_img
    TERRAIN_PROPERTIES[BASE]["image"] = base_img

    # 使用小方块组合创建坦克图像
    player_imgs = [
        create_surface_from_pattern(PLAYER_TANK_PATTERN[UP], GREEN, LIGHT_GREEN),
        create_surface_from_pattern(PLAYER_TANK_PATTERN[RIGHT], GREEN, LIGHT_GREEN),
        create_surface_from_pattern(PLAYER_TANK_PATTERN[DOWN], GREEN, LIGHT_GREEN),
        create_surface_from_pattern(PLAYER_TANK_PATTERN[LEFT], GREEN, LIGHT_GREEN)
    ]

    # 不同类型敌人坦克的图像
    enemy_imgs = {
        0: [  # 普通敌人
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[NORMAL_ENEMY][UP], RED),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[NORMAL_ENEMY][RIGHT], RED),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[NORMAL_ENEMY][DOWN], RED),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[NORMAL_ENEMY][LEFT], RED)
        ],
        1: [  # 快速敌人
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[FAST_ENEMY][UP], BLUE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[FAST_ENEMY][RIGHT], BLUE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[FAST_ENEMY][DOWN], BLUE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[FAST_ENEMY][LEFT], BLUE)
        ],
        2: [  # 装甲敌人
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ARMORED_ENEMY][UP], GRAY),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ARMORED_ENEMY][RIGHT], GRAY),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ARMORED_ENEMY][DOWN], GRAY),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ARMORED_ENEMY][LEFT], GRAY)
        ],
        3: [  # Boss敌人
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[BOSS_ENEMY][UP], PURPLE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[BOSS_ENEMY][RIGHT], PURPLE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[BOSS_ENEMY][DOWN], PURPLE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[BOSS_ENEMY][LEFT], PURPLE)
        ],
        4: [  # 精英敌人
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ELITE_ENEMY][UP], ORANGE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ELITE_ENEMY][RIGHT], ORANGE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ELITE_ENEMY][DOWN], ORANGE),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ELITE_ENEMY][LEFT], ORANGE)
        ],
        5: [  # 终极敌人
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ULTIMATE_ENEMY][UP], YELLOW),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ULTIMATE_ENEMY][RIGHT], YELLOW),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ULTIMATE_ENEMY][DOWN], YELLOW),
            create_surface_from_pattern(ENEMY_TANK_PATTERNS[ULTIMATE_ENEMY][LEFT], YELLOW)
        ]
    }

    # 子弹图像
    bullet_imgs = [
        create_surface_from_pattern(BULLET_PATTERNS[UP], WHITE),
        create_surface_from_pattern(BULLET_PATTERNS[RIGHT], WHITE),
        create_surface_from_pattern(BULLET_PATTERNS[DOWN], WHITE),
        create_surface_from_pattern(BULLET_PATTERNS[LEFT], WHITE)
    ]

    # 爆炸动画 - 创建逐渐扩大的圆形
    explosion_imgs = []
    for i in range(1, 6):
        size = TANK_SIZE // 5 * i
        img = pygame.Surface((TANK_SIZE, TANK_SIZE), pygame.SRCALPHA)
        pattern = []
        for y in range(4):
            row = []
            for x in range(4):
                # 中心爆炸模式
                if (1 <= x <= 2 and 1 <= y <= 2) or (i > 1 and (x == 1 or x == 2 or y == 1 or y == 2)):
                    row.append(1)
                else:
                    row.append(0)
            pattern.append(row)
        explosion_imgs.append(create_surface_from_pattern(pattern, YELLOW, RED, GRID_SIZE))

    # 道具图像 - 使用新的道具图案
    power_up_imgs = [
        create_surface_from_pattern(POWER_UP_PATTERNS[BULLET_UPGRADE], RED),    # 子弹升级
        create_surface_from_pattern(POWER_UP_PATTERNS[SPEED_BOOST], GREEN),     # 速度提升
        create_surface_from_pattern(POWER_UP_PATTERNS[SHIELD], BLUE),           # 护盾
        create_surface_from_pattern(POWER_UP_PATTERNS[HEALTH_BOOST], PINK),     # 生命值
        create_surface_from_pattern(POWER_UP_PATTERNS[TANK_UPGRADE], ORANGE),    # 坦克升级
        create_surface_from_pattern(POWER_UP_PATTERNS[BASE_FORTIFY], GRAY) # 新增，用灰色
    ]

except Exception as e:
    print(f"加载图像资源时出错: {e}")
    # 创建备用纯色表面
    # 使用小方块组合创建地形图像（出错时的备用方案）
    brick_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    brick_img.fill(RED)
    steel_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    steel_img.fill(GRAY)
    water_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    water_img.fill(BLUE)
    grass_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    grass_img.fill(GREEN)
    base_img = pygame.Surface((TANK_SIZE, TANK_SIZE)) # 基地大小应为 TANK_SIZE
    base_img.fill(YELLOW)
    
    # 更新地形属性中的图像
    TERRAIN_PROPERTIES[BRICK]["image"] = brick_img
    TERRAIN_PROPERTIES[STEEL]["image"] = steel_img
    TERRAIN_PROPERTIES[WATER]["image"] = water_img
    TERRAIN_PROPERTIES[GRASS]["image"] = grass_img
    TERRAIN_PROPERTIES[BASE]["image"] = base_img

    # 备用坦克图像
    player_imgs = []
    for _ in range(4):  # 四个方向
        img = pygame.Surface((TANK_SIZE, TANK_SIZE))
        img.fill(GREEN)
        player_imgs.append(img)

    # 备用敌人坦克图像
    enemy_imgs = {}
    for enemy_type in range(6):  # 六种敌人类型
        enemy_imgs[enemy_type] = []
        color = ENEMY_PROPERTIES[enemy_type]["color"]
        for _ in range(4):  # 四个方向
            img = pygame.Surface((TANK_SIZE, TANK_SIZE))
            img.fill(color)
            enemy_imgs[enemy_type].append(img)

    # 备用子弹图像
    bullet_imgs = []
    for _ in range(4):  # 四个方向
        img = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        img.fill(WHITE)
        bullet_imgs.append(img)

    # 备用爆炸图像
    explosion_imgs = []
    for i in range(5):
        img = pygame.Surface((TANK_SIZE, TANK_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(img, YELLOW, (TANK_SIZE//2, TANK_SIZE//2), (i+1)*5)
        explosion_imgs.append(img)

    # 备用道具图像
    power_up_imgs = []
    colors = [RED, GREEN, BLUE, PINK, ORANGE, GRAY] # 添加灰色
    for i in range(6): # 范围增加到 6
        img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        img.fill(colors[i])
        power_up_imgs.append(img)

print("成功加载所有游戏资源，游戏可以开始运行了！")

###############################################################################
#                                游戏对象类                                    #
###############################################################################

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size=TANK_SIZE, is_base=False):
        super().__init__()
        self.images = explosion_imgs if 'explosion_imgs' in globals() else []
        self.is_base = is_base  # 是否是基地爆炸

        if not self.images or self.is_base:
            # 创建自定义爆炸效果
            self.images = []
            colors = [(255, 200, one) for one in range(50, 255, 40)]  # 黄色到红色渐变
            if self.is_base:
                # 基地爆炸效果更大更持久
                max_size = size * 2
                colors.extend(colors)  # 重复颜色序列使动画更长
            else:
                max_size = size

            for i, color in enumerate(colors):
                # 创建逐渐扩大的圆形
                img = pygame.Surface((max_size, max_size), pygame.SRCALPHA)

                if self.is_base:
                    # 基地爆炸：多个圆形
                    circle_size = (i + 1) * max_size // len(colors)
                    pygame.draw.circle(img, color, (max_size//2, max_size//2), circle_size)
                    # 添加额外的小爆炸点
                    for _ in range(i+1):
                        radius = random.randint(5, 15)
                        offset_x = random.randint(-max_size//3, max_size//3)
                        offset_y = random.randint(-max_size//3, max_size//3)
                        pos = (max_size//2 + offset_x, max_size//2 + offset_y)
                        pygame.draw.circle(img, color, pos, radius)
                else:
                    # 普通爆炸：单个圆形
                    circle_size = (i + 1) * max_size // len(colors)
                    pygame.draw.circle(img, color, (max_size//2, max_size//2), circle_size)

                self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= (3 if self.is_base else 5):  # 基地爆炸更慢
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]

# 地形类
class Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, terrain_type):
        try:
            super().__init__()
            self.terrain_type = terrain_type
            
            # 验证地形类型是否合法
            if terrain_type not in TERRAIN_PROPERTIES:
                print(f"[警告] 未知地形类型 {terrain_type}，使用默认地形")
                self.terrain_type = EMPTY  # 使用空地形作为默认值
            
            # 获取地形属性
            props = TERRAIN_PROPERTIES.get(self.terrain_type, {
                "passable": True, 
                "destructible": False, 
                "image": None, 
                "pattern": None
            })
            
            self.passable = props.get("passable", True)
            self.destructible = props.get("destructible", False)
            self.pattern = props.get("pattern", None)

            # 获取地形图像，如果无法获取则创建备用图像
            self.image = props.get("image", None)
            if self.image is None:
                # 默认图像
                self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                if self.terrain_type == BRICK:
                    self.image.fill(RED)
                elif self.terrain_type == STEEL:
                    self.image.fill(GRAY)
                elif self.terrain_type == WATER:
                    self.image.fill(BLUE)
                elif self.terrain_type == GRASS:
                    self.image.fill(GREEN)
                elif self.terrain_type == BASE:
                    self.image.fill(YELLOW)
                else:
                    self.image.fill(BLACK)  # 默认为黑色

            # 创建碰撞矩形
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
        except Exception as e:
            print(f"[ERROR] 创建地形时出错: {e} (类型: {terrain_type}, 位置: {x}, {y})")
            # 确保基本属性存在，即使出错
            self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            self.image.fill((100, 100, 100))  # 灰色
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.passable = True  # 默认可通过
            self.destructible = False  # 默认不可摧毁
            self.terrain_type = EMPTY  # 默认为空地形

    def draw(self, surface):
        """绘制地形到屏幕"""
        surface.blit(self.image, self.rect)

    def is_water(self):
        """检查是否是水地形"""
        return self.terrain_type == WATER

    def is_grass(self):
        """检查是否是草地地形"""
        return self.terrain_type == GRASS

    def check_terrain_collision(self, terrain_group, rect=None):
        if rect is None:
            rect = self.rect
        
        for terrain in terrain_group:
            if terrain.is_water():
                continue
            if rect.colliderect(terrain.rect):
                return True
        return False

###############################################################################
#                                坦克基类                                      #
###############################################################################

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, health, bullet_type=NORMAL_BULLET):
        super().__init__()
        self.direction = direction

        # 图像和rect将在子类中设置
        self.image = None
        self.rect = None
        # 移除原始图像加载
        # if 'player_imgs' in globals() and len(player_imgs) > direction:
        #     self.original_image = player_imgs[direction]
        # else:
        #     self.original_image = create_surface_from_pattern(PLAYER_TANK_PATTERN[direction], GREEN)
        # self.image = self.original_image
        # self.rect = self.image.get_rect()

        # 坐标将在子类中设置或使用传入值
        # self.rect.x = x
        # self.rect.y = y

        self.speed = speed
        self.health = health
        self.max_health = health
        self.bullet_type = bullet_type
        self.shield = False
        self.shield_time = 0
        self.last_shot_time = 0
        self.shot_delay = 500
        self.score = 0
        # 坦克移动相关
        self.moving = False
        self.can_move = True
        self.dx = 0
        self.dy = 0

        # 根据方向设置移动增量 (子类会调用)
        # self.update_movement_direction()

    def update_movement_direction(self):
        """根据方向更新移动增量"""
        # 确保使用最新的速度值
        current_speed = self.speed

        if self.direction == UP:
            self.dx, self.dy = 0, -current_speed
        elif self.direction == RIGHT:
            self.dx, self.dy = current_speed, 0
        elif self.direction == DOWN:
            self.dx, self.dy = 0, current_speed
        elif self.direction == LEFT:
            self.dx, self.dy = -current_speed, 0

    def rotate_image(self):
        """根据方向更新坦克图像"""
        # 不需要旋转，直接使用对应方向的预渲染图像
        if isinstance(self, PlayerTank) and 'player_tank_images' in globals(): # 修正：使用 player_tank_images
            self.image = player_tank_images[self.player_id][self.tank_level][self.direction] # 修正：使用 player_tank_images
        elif isinstance(self, EnemyTank) and 'enemy_imgs' in globals() and hasattr(self, 'enemy_type'):
            self.image = enemy_imgs[self.enemy_type][self.direction]
        else:
            # 备用方案：使用图案创建图像
            if isinstance(self, PlayerTank):
                pattern = PLAYER_TANK_LEVEL_PATTERNS[self.tank_level][self.direction] # 使用级别图案
                primary_color, secondary_color = PLAYER_COLORS[self.player_id][self.tank_level] # 使用级别颜色
                self.image = create_surface_from_pattern(pattern, primary_color, secondary_color)
            elif isinstance(self, EnemyTank) and hasattr(self, 'enemy_type'):
                pattern = ENEMY_TANK_PATTERNS[self.enemy_type][self.direction]
                color = ENEMY_PROPERTIES[self.enemy_type]["color"]
                self.image = create_surface_from_pattern(pattern, color)

        # 确保每次旋转都更新移动方向
        self.update_movement_direction()

    def start_moving(self):
        """开始坦克移动"""
        self.moving = True

    def stop_moving(self):
        """停止坦克移动"""
        self.moving = False

    def update(self, terrain_group, other_tanks=None):
        """更新坦克位置和状态，采用分离轴碰撞检测"""
        if not self.moving:
            return

        # --- X轴移动和碰撞检测 ---
        original_x = self.rect.x
        self.rect.x += self.dx
        collided_x = False

        # 屏幕边界检查 X
        if self.rect.left < 0:
            self.rect.left = 0
            collided_x = True
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            collided_x = True

        # 地形碰撞检查 X (只检查不可通行的地形)
        for terrain in terrain_group:
            # 跳过水和草地，坦克可以部分进入
            if terrain.terrain_type == WATER or terrain.terrain_type == GRASS:
                continue
            if not terrain.passable and self.rect.colliderect(terrain.rect):
                collided_x = True
                if DEBUG_MODE: print(f"{'P' if hasattr(self,'player_id') else 'E'} X collide terrain")
                break # 碰到一个就够了

        # 坦克碰撞检查 X
        if not collided_x and other_tanks: # 只有在没撞地形时才检查坦克
            for tank in other_tanks:
                if tank != self and self.rect.colliderect(tank.rect):
                    collided_x = True
                    if DEBUG_MODE: print(f"{'P' if hasattr(self,'player_id') else 'E'} X collide tank")
                    break

        # 如果X轴碰撞，恢复X坐标
        if collided_x:
            self.rect.x = original_x
            # 如果是敌人，并且移动方向是 X 轴，则改变方向
            if isinstance(self, EnemyTank) and self.dx != 0:
                self.change_direction()


        # --- Y轴移动和碰撞检测 ---
        original_y = self.rect.y
        self.rect.y += self.dy
        collided_y = False

        # 屏幕边界检查 Y
        if self.rect.top < 0:
            self.rect.top = 0
            collided_y = True
        elif self.rect.bottom > SCREEN_HEIGHT: # **修正：添加底部边界检查**
            self.rect.bottom = SCREEN_HEIGHT
            collided_y = True

        # 地形碰撞检查 Y (只检查不可通行的地形)
        for terrain in terrain_group:
             # 跳过水和草地
            if terrain.terrain_type == WATER or terrain.terrain_type == GRASS:
                 continue
            if not terrain.passable and self.rect.colliderect(terrain.rect):
                collided_y = True
                if DEBUG_MODE: print(f"{'P' if hasattr(self,'player_id') else 'E'} Y collide terrain")
                break

        # 坦克碰撞检查 Y
        if not collided_y and other_tanks: # 只有在没撞地形时才检查坦克
            for tank in other_tanks:
                if tank != self and self.rect.colliderect(tank.rect):
                    collided_y = True
                    if DEBUG_MODE: print(f"{'P' if hasattr(self,'player_id') else 'E'} Y collide tank")
                    break

        # 如果Y轴碰撞，恢复Y坐标 **修正：添加Y轴碰撞恢复**
        if collided_y:
            self.rect.y = original_y
            # 如果是敌人，并且移动方向是 Y 轴，则改变方向
            if isinstance(self, EnemyTank) and self.dy != 0:
                self.change_direction()


        # --- 其他状态更新 ---
        # 更新护盾状态 (仅玩家)
        if hasattr(self, 'player_id') and self.shield and pygame.time.get_ticks() - self.shield_time > 10000:
            self.shield = False

    def check_terrain_collision(self, terrain_group, rect=None):
        if rect is None:
            rect = self.rect
        
        for terrain in terrain_group:
            if terrain.is_water():
                continue
            if rect.colliderect(terrain.rect):
                return True
        return False
        
    def check_tank_collision(self, other_tanks, rect=None):
        """检查与其他坦克的碰撞"""
        if rect is None:
            rect = self.rect
        
        for tank in other_tanks:
            if tank != self and rect.colliderect(tank.rect):
                if DEBUG_MODE and hasattr(self, 'player_id'):
                    print(f"坦克碰撞: P{self.player_id+1} 与其他坦克碰撞")
                return True
        return False

    def shoot(self):
        """发射子弹"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.shot_delay:
            return None
            
        self.last_shot_time = current_time
        bullet_props = BULLET_PROPERTIES[self.bullet_type]
        
        if self.direction == UP:
            x = self.rect.centerx - BULLET_SIZE // 2
            y = self.rect.top - BULLET_SIZE
        elif self.direction == RIGHT:
            x = self.rect.right
            y = self.rect.centery - BULLET_SIZE // 2
        elif self.direction == DOWN:
            x = self.rect.centerx - BULLET_SIZE // 2
            y = self.rect.bottom
        else:  # LEFT
            x = self.rect.left - BULLET_SIZE
            y = self.rect.centery - BULLET_SIZE // 2
            
        # 使用正确方向的子弹图像
        bullet_img = bullet_imgs[self.direction] if 'bullet_imgs' in globals() else None
        return Bullet(x, y, self.direction, bullet_props["speed"], bullet_props["damage"], bullet_props["color"], bullet_img)

    def take_damage(self, damage):
        """受到伤害"""
        if self.shield:
            return False  # 护盾保护，不受伤害
            
        self.health -= damage
        if self.health <= 0:
            return True  # 坦克被摧毁
        return False

# 重新修改 PlayerTank 类来使用多方向图像
class PlayerTank(Tank):
    def __init__(self, x, y, player_id=PLAYER_ONE):
        try:
            # 设置坦克等级和ID
            self.tank_level = TANK_LEVEL_1  # 初始级别
            self.player_id = player_id
            
            # 速度、生命值、子弹类型等默认属性
            default_speed = 3
            default_health = 3
            default_bullet_type = NORMAL_BULLET
            
            # 调用父类的__init__方法
            super().__init__(x, y, UP, default_speed, default_health, default_bullet_type)
            
            # 根据级别选择颜色
            primary_color, secondary_color = PLAYER_COLORS[player_id][self.tank_level]
            
            # 创建坦克图像
            # 尝试使用预渲染图像
            if 'player_tank_images' in globals() and player_id in player_tank_images and self.tank_level in player_tank_images[player_id]:
                self.image = player_tank_images[player_id][self.tank_level][self.direction]
            else:
                # 退回到使用模式创建图像
                pattern = PLAYER_TANK_LEVEL_PATTERNS[self.tank_level][self.direction]
                self.image = create_surface_from_pattern(pattern, primary_color, secondary_color)
                
            # 设置矩形
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
            # 设置坦克特有属性
            level_props = TANK_LEVEL_PROPERTIES[self.tank_level]
            self.max_health = level_props["health_max"]
            self.health = self.max_health
            self.bullet_speed = level_props["bullet_speed"]
            self.shot_delay = level_props["fire_rate"]
            self.bullet_count = level_props["bullet_count"]
            self.bullet_damage = level_props["bullet_damage"]
            
            # 其他属性
            self.score = 0
            self.lives = 3
            self.shield = False
            self.shield_time = 0
            self.bullets_active = 0  # 当前场上的子弹数量
            self.bullet_level = BULLET_LEVEL_1 # <--- 添加这一行，初始化子弹等级
            self.direction = UP
            
            # 初始化后设置移动方向
            self.update_movement_direction()
            
            print(f"[PlayerTank] 成功创建玩家{player_id+1}坦克: 位置({x},{y}), 初始方向={self.direction}")
        except Exception as e:
            print(f"[ERROR] 创建玩家坦克时出错: {e}")
            import traceback
            traceback.print_exc()
            # 创建备用坦克属性
            self.image = pygame.Surface((TANK_SIZE, TANK_SIZE))
            self.image.fill(GREEN if player_id == PLAYER_ONE else RED)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.direction = UP
            self.health = 3
            self.max_health = 3
            self.speed = 3
            self.dx = 0
            self.dy = -3
            self.moving = False
            self.tank_level = TANK_LEVEL_1
            self.bullet_damage = 1
            self.bullet_speed = 7
            self.shot_delay = 500
            self.last_shot_time = 0
            self.bullet_count = 1
            self.bullets_active = 0
            self.score = 0
            self.lives = 3
            self.shield = False
            self.shield_time = 0
            self.player_id = player_id
    
    def rotate_image(self):
        """仅负责根据当前方向更新坦克图像(使用预渲染图像)"""
        # 直接从预渲染字典中获取图像
        self.image = player_tank_images[self.player_id][self.tank_level][self.direction]
        # 每次旋转时都更新移动方向
        self.update_movement_direction()
        
    def update(self, terrain_group, other_tanks=None):
        """更新坦克位置和状态"""
        # 基类update会处理实际移动
        super().update(terrain_group, other_tanks)
    
    def draw_health_bar(self, surface):
        """绘制坦克上方的生命条"""
        if self.health < self.max_health:
            bar_width = TANK_SIZE
            bar_height = 5
            fill = (self.health / self.max_health) * bar_width
            outline_rect = pygame.Rect(self.rect.x, self.rect.y - 10, bar_width, bar_height)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10, fill, bar_height)
            pygame.draw.rect(surface, RED, fill_rect)
            pygame.draw.rect(surface, WHITE, outline_rect, 1)
            
    def draw_shield(self, surface):
        """绘制坦克周围的护盾效果"""
        if self.shield:
            # 创建一个稍大的半透明圆形表示护盾
            shield_size = TANK_SIZE + 10
            shield_surface = pygame.Surface((shield_size, shield_size), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (0, 100, 255, 128), (shield_size // 2, shield_size // 2), shield_size // 2)
            surface.blit(shield_surface, (self.rect.x - 5, self.rect.y - 5))

    def upgrade_bullet(self):
        """升级子弹类型"""
        if self.bullet_level < BULLET_LEVEL_3:
            self.bullet_level += 1
            
            # 根据子弹等级设置相应属性
            if self.bullet_level == BULLET_LEVEL_2:
                # 二级子弹：速度提升，变为双发
                self.bullet_speed = min(12, self.bullet_speed + 3)  # 提升速度
                self.bullet_count = 2  # 变为双发
            elif self.bullet_level == BULLET_LEVEL_3:
                # 三级子弹：伤害变为1.5倍，形状改变
                self.bullet_damage = self.bullet_damage * 1.5  # 伤害提升
                # 形状改变在shoot方法中实现
            
            # 更新其他子弹属性
            primary_color, _ = PLAYER_COLORS[self.player_id][self.tank_level]
            if self.bullet_level == BULLET_LEVEL_1:
                self.bullet_type = NORMAL_BULLET
            elif self.bullet_level == BULLET_LEVEL_2:
                self.bullet_type = FAST_BULLET
            else:  # BULLET_LEVEL_3
                self.bullet_type = POWERFUL_BULLET

    def speed_boost(self):
        """提升移动速度"""
        self.speed = min(6, self.speed + 1)
        self.update_movement_direction()  # 更新移动速度后需要更新移动增量

    def activate_shield(self):
        """激活护盾"""
        self.shield = True
        self.shield_time = pygame.time.get_ticks()
        
    def add_health(self):
        """增加生命值"""
        if self.health < self.max_health:
            self.health = min(self.max_health, self.health + 1)
        else:
            self.lives = min(self.lives + 1, 5)  # 最多5条命
            
    def upgrade_tank(self):
        """升级坦克"""
        if self.tank_level < TANK_LEVEL_3:
            self.tank_level += 1
            level_props = TANK_LEVEL_PROPERTIES[self.tank_level] # 获取新级别的属性

            # 更新坦克属性
            self.max_health = level_props["health_max"]
            # 升级时回满血或至少加1血
            self.health = self.max_health
            self.bullet_damage = level_props["bullet_damage"]
            self.bullet_speed = level_props["bullet_speed"]
            self.shot_delay = level_props["fire_rate"]
            self.bullet_count = level_props["bullet_count"]

            # 更新坦克外观
            self.rotate_image() # 应用新等级的图案
            print(f"Player {self.player_id+1} upgraded to Tank Level {self.tank_level+1}") # Debug print
        else:
             print(f"Player {self.player_id+1} already at max Tank Level.") # Debug print

    def shoot(self):
        """发射子弹，支持多发子弹"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.shot_delay:
            return None
            
        # 检查已激活的子弹数量是否达到上限
        if self.bullets_active >= self.bullet_count:
            return None
            
        self.last_shot_time = current_time
        self.bullets_active += 1
        
        # 根据坦克方向计算子弹发射位置
        if self.direction == UP:
            x = self.rect.centerx - BULLET_SIZE // 2
            y = self.rect.top - BULLET_SIZE
        elif self.direction == RIGHT:
            x = self.rect.right
            y = self.rect.centery - BULLET_SIZE // 2
        elif self.direction == DOWN:
            x = self.rect.centerx - BULLET_SIZE // 2
            y = self.rect.bottom
        else:  # LEFT
            x = self.rect.left - BULLET_SIZE
            y = self.rect.centery - BULLET_SIZE // 2
            
        # 获取子弹颜色
        bullet_color = BULLET_PROPERTIES[self.bullet_type]["color"]
        
        # 判断是否是高级子弹
        is_advanced = (self.bullet_level == BULLET_LEVEL_3)
        
        # 计算实际伤害
        actual_damage = self.bullet_damage
        
        # 创建子弹
        bullet = Bullet(
            x, y, 
            self.direction, 
            self.bullet_speed, 
            actual_damage, 
            bullet_color,
            bullet_imgs[self.direction] if ('bullet_imgs' in globals() and not is_advanced) else None,
            self,
            advanced=is_advanced
        )
        return bullet

# 敌人坦克类
class EnemyTank(Tank):
    def __init__(self, x, y, enemy_type):
        # 根据敌人类型设置不同特性
        self.enemy_type = enemy_type
        
        # AI控制属性
        self.direction_change_delay = random.randint(2000, 5000)  # 改变方向的时间间隔(毫秒)
        self.last_direction_change = pygame.time.get_ticks()  # 上次改变方向的时间
        self.sight_range = 200  # 视野范围
        self.bullet_damage_multiplier = 1.0  # 子弹伤害倍数
        
        if enemy_type == NORMAL_ENEMY:  # 普通敌人
            # 调用父类的__init__方法
            super().__init__(x, y, DOWN, 2, 1, NORMAL_BULLET)
            self.bullet_count = 1  # 子弹数量限制
        elif enemy_type == FAST_ENEMY:  # 快速敌人
            super().__init__(x, y, DOWN, 3, 1, FAST_BULLET)
            self.bullet_count = 1
        elif enemy_type == ARMORED_ENEMY:  # 装甲敌人
            super().__init__(x, y, DOWN, 1.5, 3, NORMAL_BULLET)
            self.bullet_count = 1
        elif enemy_type == BOSS_ENEMY:  # Boss敌人
            super().__init__(x, y, DOWN, 2, 5, POWERFUL_BULLET)
            self.bullet_count = 2
            self.bullet_damage_multiplier = 1.5  # Boss伤害提升
        elif enemy_type == ELITE_ENEMY:  # 精英敌人
            super().__init__(x, y, DOWN, 3, 3, FAST_BULLET)
            self.bullet_count = 2
        elif enemy_type == ULTIMATE_ENEMY:  # 终极敌人
            super().__init__(x, y, DOWN, 2.5, 7, SUPER_BULLET)
            self.bullet_count = 3
            self.bullet_damage_multiplier = 2.0  # 终极敌人伤害翻倍
        else:  # 默认敌人
            super().__init__(x, y, DOWN, 2, 1, NORMAL_BULLET)
            self.bullet_count = 1
            
        # 根据敌人类型设置图像
        if 'enemy_imgs' in globals() and self.enemy_type in enemy_imgs:
            self.image = enemy_imgs[self.enemy_type][self.direction]
        else:
            # 创建备用图像
            self.image = pygame.Surface((TANK_SIZE, TANK_SIZE))
            default_colors = {
                NORMAL_ENEMY: RED,
                FAST_ENEMY: BLUE,
                ARMORED_ENEMY: GRAY,
                BOSS_ENEMY: PURPLE,
                ELITE_ENEMY: ORANGE,
                ULTIMATE_ENEMY: YELLOW
            }
            self.image.fill(default_colors.get(self.enemy_type, RED))
            
        # 其他属性
        self.bullets_active = 0  # 当前场上的子弹数量
        self.moving = True  # 敌人默认一直移动
        
        # 设置初始图像和rect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 移动和射击延迟
        self.shot_delay = random.randint(1500, 3000)  # 射击延迟随机
        
        # 确保初始移动参数正确
        self.update_movement_direction()
        # 不需要再调用 rotate_image(), 因为上面已经设置了正确的初始图像
        # self.rotate_image()

        self.shield = False
        self.shield_time = 0
        # 可以选择性添加 tank_level, bullet_level 等，但暂时不加
        self.bullet_damage_multiplier = 1.0 # 用于子弹升级效果

    def rotate_image(self):
        """根据方向更新敌人坦克图像 (使用预渲染图像)"""
        # 直接从预渲染字典中获取图像
        self.image = enemy_imgs[self.enemy_type][self.direction]
        
        # 更新移动方向
        self.update_movement_direction()

    def draw_health_bar(self, surface):
        """绘制坦克上方的生命条"""
        if self.health < self.max_health:
            bar_width = TANK_SIZE
            bar_height = 5
            fill = (self.health / self.max_health) * bar_width
            outline_rect = pygame.Rect(self.rect.x, self.rect.y - 10, bar_width, bar_height)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10, fill, bar_height)
            pygame.draw.rect(surface, RED, fill_rect)
            pygame.draw.rect(surface, WHITE, outline_rect, 1)

    def update(self, terrain_group, player_group=None, enemy_group=None):
        """更新敌人坦克"""
        # 检查是否应改变移动方向
        current_time = pygame.time.get_ticks()
        if current_time - self.last_direction_change > self.direction_change_delay:
            self.change_direction()
            self.last_direction_change = current_time

        # 更新坦克位置和状态
        super().update(terrain_group, enemy_group if enemy_group else None)

        # 检查是否应该射击 (在有玩家时才考虑射击)
        if player_group and self.alive():
            target_player = None
            closest_distance = float('inf')
            
            # 查找最近的玩家
            for player in player_group:
                if not player.alive():
                    continue
                distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + 
                                     (player.rect.centery - self.rect.centery)**2)
                if distance < closest_distance:
                    closest_distance = distance
                    target_player = player
            
            # 当玩家在射程内时射击
            if target_player and closest_distance < 300:  # 射程300像素
                should_shoot = False
                # 检查方向是否大致对准玩家
                dx = target_player.rect.centerx - self.rect.centerx
                dy = target_player.rect.centery - self.rect.centery
                tolerance = TANK_SIZE # 允许一个坦克身位的误差
                
                if self.direction == UP and dy < 0 and abs(dx) < tolerance:
                    should_shoot = True
                elif self.direction == DOWN and dy > 0 and abs(dx) < tolerance:
                    should_shoot = True
                elif self.direction == LEFT and dx < 0 and abs(dy) < tolerance:
                    should_shoot = True
                elif self.direction == RIGHT and dx > 0 and abs(dy) < tolerance:
                    should_shoot = True
                
                # 射程内且方向正确，移除随机概率检查，让其在冷却后更容易射击
                if should_shoot:
                    bullet = self.shoot()
                    if bullet:
                        return bullet # 返回子弹实例，由Level处理
        
        return None

    def should_shoot(self, player_tank_or_group):
        """判断是否应该射击"""
        if isinstance(player_tank_or_group, pygame.sprite.Group):
            # 如果是玩家组，随机选择一个玩家作为目标
            if not player_tank_or_group:  # 如果组为空，返回False
                return False
            player_tanks = list(player_tank_or_group)
            if not player_tanks:
                return False
            target = random.choice(player_tanks)
        else:
            # 单个玩家坦克
            target = player_tank_or_group
            if not target:
                return False
        
        # 计算到玩家的方向
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        
        # 判断敌人和玩家是否在同一直线上
        # 允许有一定的误差范围
        tolerance = 50
        aligned = False
        
        if self.direction == UP and abs(dx) < tolerance and dy < 0:
            aligned = True
        elif self.direction == RIGHT and dx > 0 and abs(dy) < tolerance:
            aligned = True
        elif self.direction == DOWN and abs(dx) < tolerance and dy > 0:
            aligned = True
        elif self.direction == LEFT and dx < 0 and abs(dy) < tolerance:
            aligned = True
        
        # 如果对齐并且距离足够近(或随机射击)
        if aligned and (random.random() < 0.8 or (abs(dx) < 200 and abs(dy) < 200)):
            return True
            
        # 否则以低概率随机射击
        return random.random() < 0.01  # 1%的几率随机射击

    def change_direction(self):
        """随机改变方向"""
        old_direction = self.direction
        # 随机选择一个新方向
        directions = [UP, RIGHT, DOWN, LEFT]
        # 有50%概率保持原方向，50%概率随机选择新方向
        if random.random() > 0.5:
            # 从其他三个方向中随机选择
            directions.remove(old_direction)
            self.direction = random.choice(directions)
            # 旋转图像
            self.rotate_image()
        
        # 更新移动状态
        self.moving = True

    def speed_boost(self, amount=0.5): # 敌人加速少一点
        self.speed = min(self.speed + amount, ENEMY_PROPERTIES[self.enemy_type]["speed"] * 1.5) # 速度上限为基础*1.5
        self.update_movement_direction()
        print(f"Enemy type {self.enemy_type} got speed boost to {self.speed}")

    def activate_shield(self, duration=5000): # 敌人护盾时间短一点
        self.shield = True
        self.shield_time = pygame.time.get_ticks() + duration # 记录失效时间
        print(f"Enemy type {self.enemy_type} activated shield.")

    def add_health(self, amount=1):
        self.health = min(self.health + amount, self.max_health * 1.5) # 生命上限也提高一点
        print(f"Enemy type {self.enemy_type} got health boost to {self.health}")

    def upgrade_bullet(self, multiplier_increase=0.5):
        self.bullet_damage_multiplier += multiplier_increase
        # 可以在 shoot 方法中使用这个乘数
        print(f"Enemy type {self.enemy_type} upgraded bullet damage multiplier to {self.bullet_damage_multiplier}")

    def upgrade_tank(self):
        # 简单提升血量和速度
        self.add_health(1)
        self.speed_boost(0.2)
        print(f"Enemy type {self.enemy_type} got tank upgrade.")

    # 修改 EnemyTank 的 shoot 方法以应用伤害乘数
    def shoot(self):
        """敌人射击"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.shot_delay:
            return None
            
        self.last_shot_time = current_time
        bullet_props = BULLET_PROPERTIES[self.bullet_type]
        
        if self.direction == UP:
            x = self.rect.centerx - BULLET_SIZE // 2
            y = self.rect.top - BULLET_SIZE
        elif self.direction == RIGHT:
            x = self.rect.right
            y = self.rect.centery - BULLET_SIZE // 2
        elif self.direction == DOWN:
            x = self.rect.centerx - BULLET_SIZE // 2
            y = self.rect.bottom
        else:  # LEFT
            x = self.rect.left - BULLET_SIZE
            y = self.rect.centery - BULLET_SIZE // 2

        bullet_img = bullet_imgs[self.direction] if 'bullet_imgs' in globals() else None
        # **应用伤害乘数**
        actual_damage = bullet_props["damage"] * self.bullet_damage_multiplier

        # 移除敌人子弹计数增加
        # self.bullets_active += 1
        return Bullet(x, y, self.direction, bullet_props["speed"], actual_damage, bullet_props["color"], bullet_img, self) # 传递 self 作为 owner


    # 修改 EnemyTank 的 take_damage 方法以检查护盾
    def take_damage(self, damage):
        """受到伤害"""
        if self.shield:
            print(f"Enemy type {self.enemy_type} shield blocked damage.")
            self.shield = False # 护盾抵挡一次伤害后消失 (可选)
            return False

        self.health -= damage
        if self.health <= 0:
            return True  # 坦克被摧毁
        return False

# 修改子弹类以使用图像
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, damage, color, image=None, owner=None, advanced=False):
        super().__init__()
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.owner = owner  # 存储发射这个子弹的坦克引用
        self.advanced = advanced  # 是否是高级子弹
        
        if advanced and not image:
            # 如果是高级子弹，使用特殊图案
            self.image = create_surface_from_pattern(ADVANCED_BULLET_PATTERNS[direction], color, scale=0.8)
        elif image:
            self.image = image
        else:
            # 根据方向创建形状不同的子弹
            self.image = create_surface_from_pattern(BULLET_PATTERNS[direction], color)
                
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        """更新子弹位置"""
        if self.direction == UP:
            self.rect.y -= self.speed
        elif self.direction == RIGHT:
            self.rect.x += self.speed
        elif self.direction == DOWN:
            self.rect.y += self.speed
        elif self.direction == LEFT:
            self.rect.x -= self.speed
            
        # 如果子弹离开屏幕，移除它
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
            # 如果是玩家坦克的子弹，更新活跃子弹计数
            if self.owner and isinstance(self.owner, PlayerTank):
                self.owner.bullets_active = max(0, self.owner.bullets_active - 1)

    def kill(self):
        """覆盖kill方法，确保在子弹消失时更新计数"""
        if self.owner and isinstance(self.owner, PlayerTank):
            self.owner.bullets_active = max(0, self.owner.bullets_active - 1)
        super().kill()

# 道具类
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type):
        super().__init__()
        # 使用新的道具图案
        if power_type in POWER_UP_PATTERNS:
            pattern = POWER_UP_PATTERNS[power_type]
            
            # 根据道具类型选择颜色
            colors = {
                BULLET_UPGRADE: RED,
                SPEED_BOOST: GREEN,
                SHIELD: BLUE,
                HEALTH_BOOST: PINK,
                TANK_UPGRADE: ORANGE,
                BASE_FORTIFY: GRAY  # 添加基地加固的颜色
            }
            
            self.image = create_surface_from_pattern(pattern, colors.get(power_type, WHITE))
        else:
            # 创建备用图像
            self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            self.image.fill(WHITE)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.power_type = power_type

# 开始菜单类
class StartMenu:
    def __init__(self, font, title_font):
        self.font = font
        self.title_font = title_font
        # 增加模式选择按钮
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2
        
        self.single_player_button = pygame.Rect(center_x - button_width // 2, SCREEN_HEIGHT // 2, button_width, button_height)
        self.two_players_button = pygame.Rect(center_x - button_width // 2, SCREEN_HEIGHT // 2 + 70, button_width, button_height)
        self.instructions_button = pygame.Rect(center_x - button_width // 2, SCREEN_HEIGHT // 2 + 140, button_width, button_height)
        
        self.active = True
        self.last_click_time = 0  # 防止双击
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        # 绘制标题
        title = self.title_font.render("坦克大战", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//6))
        
        # 绘制按钮
        pygame.draw.rect(screen, GREEN, self.single_player_button)
        pygame.draw.rect(screen, BLUE, self.two_players_button)
        pygame.draw.rect(screen, GRAY, self.instructions_button)
        
        # 绘制按钮文字
        single_text = self.font.render("单人模式", True, BLACK)
        single_text_rect = single_text.get_rect(center=self.single_player_button.center)
        screen.blit(single_text, single_text_rect)
        
        two_text = self.font.render("双人模式", True, BLACK)
        two_text_rect = two_text.get_rect(center=self.two_players_button.center)
        screen.blit(two_text, two_text_rect)
        
        instr_text = self.font.render("操作说明", True, BLACK)
        instr_text_rect = instr_text.get_rect(center=self.instructions_button.center)
        screen.blit(instr_text, instr_text_rect)
    
    def handle_events(self, event):
        """处理传入的单个事件，而不是自己获取事件队列"""
        current_time = pygame.time.get_ticks()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 检测鼠标点击，并添加防重复点击保护
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 确保两次点击之间至少间隔200毫秒
            if current_time - self.last_click_time < 200:
                # print(\"[Menu Event] Click too fast, ignored.\") # Debug Print
                return "none"

            self.last_click_time = current_time
            mouse_pos = event.pos
            # print(f\"[Menu Event] Mouse clicked at {mouse_pos}\") # Debug Print

            if self.single_player_button.collidepoint(mouse_pos):
                # print(\"[Menu Event] Single Player button clicked. Returning 'single_player'.\")
                self.active = False
                return "single_player"
            elif self.two_players_button.collidepoint(mouse_pos):
                # print(\"[Menu Event] Two Players button clicked. Returning 'two_players'.\")
                self.active = False
                return "two_players"
            elif self.instructions_button.collidepoint(mouse_pos):
                 # print(\"[Menu Event] Instructions button clicked. Returning 'instructions'.\")
                 return "instructions"
            else:
                 # print(\"[Menu Event] Clicked outside buttons.\")
                 pass # 添加pass以保持语法结构

        # print(\"[Menu Event] No button clicked. Returning 'none'.\")
        return "none"
    def show_instructions(self, screen, font, title_font):
        """显示游戏操作说明"""
        screen.fill(BLACK)
        
        # 绘制标题
        title = title_font.render("操作说明", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # 绘制操作说明
        instructions = [
            "移动:",
            "- 玩家1: WASD键",
            "- 玩家2: 方向键",
            "",
            "射击:",
            "- 玩家1: 空格键",
            "- 玩家2: 小键盘0/0键/回车",
            "",
            "游戏目标:",
            "- 保护基地不被敌人摧毁",
            "- 消灭所有敌人坦克",
            "- 收集道具提升坦克性能",
            "",
            "道具说明:",
            "- 红色: 子弹升级",
            "- 绿色: 速度提升",
            "- 蓝色: 护盾保护",
            "- 粉色: 生命值",
            "- 橙色: 坦克升级",
            "",
            "关卡说明:",
            "- 共24关，每4关出现新敌人",
            "- 20关开始出现终极敌人",
            "",
            "点击任意位置返回"
        ]
        
        for i, line in enumerate(instructions):
            text = font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i * 30))
        
        pygame.display.update()
        
        # 等待点击
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

###############################################################################
#                                关卡类                                        #
###############################################################################

class Level:
    def __init__(self, level_number, game_mode=SINGLE_PLAYER, font=None):
        print(f"[Level Init] Starting initialization for Level {level_number}, Mode {game_mode}...") # Debug Print: Start Init
        self.level_number = level_number
        self.game_mode = game_mode
        # 存储字体，如果未提供则尝试创建默认字体
        if font:
            self.font = font
        else:
            try:
                # 备用方案：如果 Game 没有传递字体，Level 尝试自己加载
                self.font = pygame.font.SysFont("simsun", 24)
                _ = self.font.render("测试", True, WHITE) # 测试
            except:
                self.font = pygame.font.SysFont(None, 24) # 最后手段

        self.terrain_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.power_up_group = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()  # 新增爆炸效果组
        self.player = None
        self.player2 = None  # 存储第二个玩家
        self.player_group = pygame.sprite.Group()  # 存储所有玩家的组
        self.base = None
        
        # 根据游戏模式调整敌人数量，增加基础敌人数量
        if game_mode == SINGLE_PLAYER:
            self.enemy_count = 8 + level_number * 4  # 单人模式敌人数量
        else:  # 双人模式敌人数量更多
            self.enemy_count = 12 + level_number * 5
            
        self.enemies_spawned = 0
        self.max_enemies_on_screen = 5 + level_number  # 每关增加同屏敌人数量
        self.max_enemies = self.enemy_count  # 总敌人数量，用于HUD显示
        self.next_enemy_spawn = pygame.time.get_ticks()
        self.spawn_delay = max(2500 - level_number * 500, 800)  # 每关减少敌人生成延迟，最小800毫秒
        self.score = 0
        
        print("[Level Init] Calling create_level...") # Debug Print: Before create_level
        try:
            self.create_level()
            print("[Level Init] create_level finished successfully.") # Debug Print: After create_level success
        except Exception as e:
            print(f"[Level Init] !!! ERROR during create_level: {e}", file=sys.stderr) # Print error to stderr
            import traceback
            traceback.print_exc() # Print full traceback
            # Optionally re-raise or handle the error appropriately
            # raise e # Re-raising will stop execution here

    def create_level(self):
        print("[Create Level] Starting...") # Debug Print
        try:
            # --- 1. Initialize essential lists ---
            self.protected_areas = []
            self.terrain_group.empty()
            self.player_group.empty()
            self.enemy_group = pygame.sprite.Group()
            self.player_bullets = pygame.sprite.Group()
            self.enemy_bullets = pygame.sprite.Group()
            self.power_up_group = pygame.sprite.Group()
            self.explosions = pygame.sprite.Group()
            print("[Create Level] Groups cleared and protected_areas initialized.") # Debug Print

            # --- 2. Create the Base ---
            base_x = SCREEN_WIDTH // 2 - BLOCK_SIZE // 2
            base_y = SCREEN_HEIGHT - 3 * BLOCK_SIZE  # 稍微上移一些，留出更多空间
            self.base = Terrain(base_x, base_y, BASE)
            self.terrain_group.add(self.base)
            print("[Create Level] Base created.") # Debug Print

            # --- 2.1. 创建基地周围的红色砖墙保护 (与基地有一格间隔，墙之间紧密相连) ---
            # 基地本身的大小是 2x2 BLOCK_SIZE
            # 保护墙形成一个 4x4 BLOCK_SIZE 的空心正方形，中间留出 2x2 放基地
            
            # 计算保护墙的边界
            wall_left = base_x - BLOCK_SIZE  # 左边界：基地左边一格
            wall_top = base_y - BLOCK_SIZE  # 上边界：基地上边一格
            wall_right = base_x + 2 * BLOCK_SIZE  # 右边界：基地右边一格（基地宽2格）
            wall_bottom = base_y + 2 * BLOCK_SIZE  # 下边界：基地下边一格（基地高2格）
            
            # 添加上边缘墙壁 (四块砖)
            for x in range(wall_left, wall_right + BLOCK_SIZE, BLOCK_SIZE):
                self.terrain_group.add(Terrain(x, wall_top, BRICK))
            
            # 添加左右边缘墙壁 (各三块砖，不包括与上下边缘重合的块)
            for y in range(wall_top + BLOCK_SIZE, wall_bottom, BLOCK_SIZE):
                self.terrain_group.add(Terrain(wall_left, y, BRICK))
                self.terrain_group.add(Terrain(wall_right, y, BRICK))
            
            # 添加下边缘墙壁 (四块砖)
            for x in range(wall_left, wall_right + BLOCK_SIZE, BLOCK_SIZE):
                self.terrain_group.add(Terrain(x, wall_bottom, BRICK))
                
            print("[Create Level] Continuous base brick wall created.") # Debug print
            print(f"地形组包含 {len(self.terrain_group)} 个地形") # Debug print
            
            # --- 3. 定义游戏保护区域 (基地、玩家出生点等) ---
            # 将基地和周围的"大保护区"添加到保护列表中，防止随机地形生成在这里
            self.protected_areas.append(self.base.rect.copy()) # 老巢本身
            
            # 围墙保护区：比围墙再大一圈
            base_protection_rect = pygame.Rect(
                wall_left - BLOCK_SIZE, wall_top - BLOCK_SIZE,
                (wall_right - wall_left) + 3 * BLOCK_SIZE, 
                (wall_bottom - wall_top) + 3 * BLOCK_SIZE
            )
            self.protected_areas.append(base_protection_rect)
            print("[Create Level] Base protection area defined.")

            # --- 4. Create Player(s) and add their spawn protection ---
            # 调整玩家出生位置在保护墙外且稍微向上，避免卡住
            # 我们希望玩家在墙上方一个坦克身位
            spawn_y = wall_top - TANK_SIZE - BLOCK_SIZE // 2  # 在顶部墙外再上移半个砖块

            if self.game_mode == SINGLE_PLAYER:
                # Single player spawns centered above base protection
                spawn_x = base_x
                player_y = spawn_y

                self.player = PlayerTank(spawn_x, player_y, PLAYER_ONE)
                self.player_group.add(self.player)
                print("[Create Level] Single player tank created.") # Debug Print

                # Add player spawn area to protected_areas
                self.protected_areas.append( # Use append for single item
                    pygame.Rect(spawn_x - BLOCK_SIZE, player_y - BLOCK_SIZE,
                                TANK_SIZE + 2 * BLOCK_SIZE, TANK_SIZE + 2 * BLOCK_SIZE)
                )

            elif self.game_mode == TWO_PLAYERS:
                # Two players spawn left and right above base protection
                player1_x = wall_left
                player1_y = spawn_y

                player2_x = wall_right
                player2_y = spawn_y

                player1_safe_zone = pygame.Rect(
                    player1_x - BLOCK_SIZE, player1_y - BLOCK_SIZE,
                    TANK_SIZE + 2 * BLOCK_SIZE, TANK_SIZE + 2 * BLOCK_SIZE
                )
                player2_safe_zone = pygame.Rect(
                    player2_x - BLOCK_SIZE, player2_y - BLOCK_SIZE,
                    TANK_SIZE + 2 * BLOCK_SIZE, TANK_SIZE + 2 * BLOCK_SIZE
                )

                self.player = PlayerTank(player1_x, player1_y, PLAYER_ONE)
                self.player2 = PlayerTank(player2_x, player2_y, PLAYER_TWO)
                self.player_group.add(self.player, self.player2)
                print("[Create Level] Two player tanks created.") # Debug Print

                # Add player spawn areas to protected_areas
                self.protected_areas.extend([player1_safe_zone, player2_safe_zone])

            print(f"[Create Level] Player spawn protection added. protected_areas count: {len(self.protected_areas)}")

            # --- 5. Define Enemy Spawn Points and add their protection ---
            self.enemy_spawn_points = [
                (SCREEN_WIDTH // 4 - TANK_SIZE // 2, 0),
                (SCREEN_WIDTH // 2 - TANK_SIZE // 2, 0),
                (3 * SCREEN_WIDTH // 4 - TANK_SIZE // 2, 0)
            ]
            for spawn_x, spawn_y in self.enemy_spawn_points:
                self.protected_areas.append(pygame.Rect(
                    spawn_x - BLOCK_SIZE, spawn_y,
                    TANK_SIZE + 2 * BLOCK_SIZE, 2 * BLOCK_SIZE
                ))
            print(f"[Create Level] Enemy spawn points defined and protected. protected_areas count: {len(self.protected_areas)}")

            # --- 6. Create the Rest of the Terrain ---
            print("[Create Level] Calling create_terrain...")
            self.create_terrain()
            print("[Create Level] create_terrain finished.") # Debug Print
            print("[Create Level] Finished.") # Debug Print
        except Exception as e:
            print(f"[Level Init] !!! ERROR during create_level: {e}", file=sys.stderr) # Print error to stderr
            import traceback
            traceback.print_exc() # Print full traceback
            # Optionally re-raise or handle the error appropriately
            # raise e # Re-raising will stop execution here
                
    def create_terrain(self):
        """创建经典风格的地形"""
        # --- 1. 保存基地和基地保护墙块 ---
        base_and_walls = []
        if self.base:
            base_and_walls.append(self.base)
            # 收集老巢周围的连续砖墙
            bx, by = self.base.rect.topleft
            
            # 计算保护墙的边界（与create_level中相同的逻辑）
            wall_left = bx - BLOCK_SIZE  # 左边界：基地左边一格
            wall_top = by - BLOCK_SIZE  # 上边界：基地上边一格
            wall_right = bx + 2 * BLOCK_SIZE  # 右边界：基地右边一格（基地宽2格）
            wall_bottom = by + 2 * BLOCK_SIZE  # 下边界：基地下边一格（基地高2格）
            
            # 收集所有墙块位置
            wall_positions = []
            
            # 上边缘墙壁
            for x in range(wall_left, wall_right + BLOCK_SIZE, BLOCK_SIZE):
                wall_positions.append((x, wall_top))
            
            # 左右边缘墙壁
            for y in range(wall_top + BLOCK_SIZE, wall_bottom, BLOCK_SIZE):
                wall_positions.append((wall_left, y))
                wall_positions.append((wall_right, y))
            
            # 下边缘墙壁
            for x in range(wall_left, wall_right + BLOCK_SIZE, BLOCK_SIZE):
                wall_positions.append((x, wall_bottom))
                
            # 收集墙壁
            for wall in self.terrain_group:
                if wall.rect.topleft in wall_positions and wall.terrain_type in [BRICK, STEEL]:
                    base_and_walls.append(wall)
            
            print(f"[Terrain] 收集了 {len(base_and_walls)-1} 个基地保护墙块")
        
        # --- 2. 清空地形并重新添加基地和墙块 ---
        self.terrain_group.empty()
        for item in base_and_walls:
            self.terrain_group.add(item)
        
        print(f"[Terrain] 保留了 {len(base_and_walls)} 个基地相关地形块")

        # --- 3. 创建游戏地形 ---
        # 瓦片大小 (经典坦克大战中一个基本墙块是 2x2 个最小单位)
        TILE_SIZE = 2 * BLOCK_SIZE # 一个瓦片是 24x24 像素

        map_width_tiles = SCREEN_WIDTH // TILE_SIZE
        map_height_tiles = SCREEN_HEIGHT // TILE_SIZE

        # --- 结构化生成内部墙体 ---
        for tx in range(map_width_tiles):
            for ty in range(map_height_tiles):
                tile_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.is_in_protected_area(tile_rect): continue
                if tx < 1 or tx >= map_width_tiles - 1 or ty < 1 or ty >= map_height_tiles - 2: continue # 调整边缘跳过逻辑

                # 降低放置结构的整体概率
                if random.random() < 0.20: # <--- 整体概率，可调整 (例如 0.20)
                    # 定义新的结构类型和权重
                    structure_types = [
                        "brick_block", "steel_block",
                        "brick_h_line", "brick_v_line",
                        "steel_h_line", "steel_v_line",
                        "brick_l_tl", "brick_l_tr", "brick_l_bl", "brick_l_br",
                        "water_patch", "grass_patch"
                    ]
                    weights = [
                        0.20, 0.10, # Blocks
                        0.15, 0.15, # Brick lines
                        0.05, 0.05, # Steel lines
                        0.05, 0.05, 0.05, 0.05, # Brick L-shapes
                        0.05, 0.05  # Patches
                    ]
                    # 确保权重总和为 1 (或接近 1，random.choices 会处理)
                    # total_weight = sum(weights) # (可选检查)

                    chosen_structure = random.choices(structure_types, weights=weights, k=1)[0]
                    self.place_structure(tx, ty, TILE_SIZE, chosen_structure)

        print(f"[Terrain] Generated classic terrain with {len(self.terrain_group)} blocks.")

    def place_structure(self, tx, ty, tile_size, structure_type):
        """在指定位置放置特定类型的地形结构
        
        参数:
            tx, ty: 瓦片坐标 (单位: 瓦片大小)
            tile_size: 瓦片大小 (像素)
            structure_type: 结构类型
        """
        # 将瓦片坐标转换为像素坐标
        px = tx * tile_size
        py = ty * tile_size
        
        # 确定各种结构中的单个方块大小
        block_size = BLOCK_SIZE
        
        # 根据结构类型放置不同的地形
        if structure_type == "brick_block":
            # 2x2 的砖块
            for y in range(2):
                for x in range(2):
                    self.terrain_group.add(Terrain(px + x * block_size, py + y * block_size, BRICK))
                    
        elif structure_type == "steel_block":
            # 2x2 的钢块
            for y in range(2):
                for x in range(2):
                    self.terrain_group.add(Terrain(px + x * block_size, py + y * block_size, STEEL))
                    
        elif structure_type == "brick_h_line":
            # 水平砖块线
            for x in range(2):
                self.terrain_group.add(Terrain(px + x * block_size, py, BRICK))
                
        elif structure_type == "brick_v_line":
            # 垂直砖块线
            for y in range(2):
                self.terrain_group.add(Terrain(px, py + y * block_size, BRICK))
                
        elif structure_type == "steel_h_line":
            # 水平钢块线
            for x in range(2):
                self.terrain_group.add(Terrain(px + x * block_size, py, STEEL))
                
        elif structure_type == "steel_v_line":
            # 垂直钢块线
            for y in range(2):
                self.terrain_group.add(Terrain(px, py + y * block_size, STEEL))
                
        elif structure_type.startswith("brick_l_"):
            # L形砖块 (四个方向)
            direction = structure_type[8:]  # 获取方向后缀: tl, tr, bl, br
            
            if direction == "tl":  # 左上角
                self.terrain_group.add(Terrain(px, py, BRICK))
                self.terrain_group.add(Terrain(px, py + block_size, BRICK))
                self.terrain_group.add(Terrain(px + block_size, py, BRICK))
            elif direction == "tr":  # 右上角
                self.terrain_group.add(Terrain(px + block_size, py, BRICK))
                self.terrain_group.add(Terrain(px + block_size, py + block_size, BRICK))
                self.terrain_group.add(Terrain(px, py, BRICK))
            elif direction == "bl":  # 左下角
                self.terrain_group.add(Terrain(px, py + block_size, BRICK))
                self.terrain_group.add(Terrain(px + block_size, py + block_size, BRICK))
                self.terrain_group.add(Terrain(px, py, BRICK))
            elif direction == "br":  # 右下角
                self.terrain_group.add(Terrain(px + block_size, py + block_size, BRICK))
                self.terrain_group.add(Terrain(px, py + block_size, BRICK))
                self.terrain_group.add(Terrain(px + block_size, py, BRICK))
                
        elif structure_type == "water_patch":
            # 2x2 的水域
            for y in range(2):
                for x in range(2):
                    self.terrain_group.add(Terrain(px + x * block_size, py + y * block_size, WATER))
                    
        elif structure_type == "grass_patch":
            # 2x2 的草地
            for y in range(2):
                for x in range(2):
                    self.terrain_group.add(Terrain(px + x * block_size, py + y * block_size, GRASS))
    
    def fortify_base(self):
        """将基地周围的砖墙升级为钢墙"""
        if not self.base or not self.base.alive():
            print("[Warning] Cannot fortify base, base not found.")
            return

        bx, by = self.base.rect.topleft
        
        # 计算保护墙的边界（与create_level中相同的逻辑）
        wall_left = bx - BLOCK_SIZE  # 左边界：基地左边一格
        wall_top = by - BLOCK_SIZE  # 上边界：基地上边一格
        wall_right = bx + 2 * BLOCK_SIZE  # 右边界：基地右边一格（基地宽2格）
        wall_bottom = by + 2 * BLOCK_SIZE  # 下边界：基地下边一格（基地高2格）
        
        # 收集所有墙块位置
        wall_positions = []
        
        # 上边缘墙壁
        for x in range(wall_left, wall_right + BLOCK_SIZE, BLOCK_SIZE):
            wall_positions.append((x, wall_top))
        
        # 左右边缘墙壁
        for y in range(wall_top + BLOCK_SIZE, wall_bottom, BLOCK_SIZE):
            wall_positions.append((wall_left, y))
            wall_positions.append((wall_right, y))
        
        # 下边缘墙壁
        for x in range(wall_left, wall_right + BLOCK_SIZE, BLOCK_SIZE):
            wall_positions.append((x, wall_bottom))

        print("[Action] Fortifying base!") # Debug
        for pos in wall_positions:
            x, y = pos
            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                # 移除该位置的所有现有地形 (可能是空地或砖块)
                existing = [t for t in self.terrain_group if t.rect.topleft == (x, y)]
                for item in existing:
                    if item.terrain_type == BRICK:
                        item.kill() # 仅移除砖块
                        # 添加新的钢墙
                        self.terrain_group.add(Terrain(x, y, STEEL))
                        print(f"[Fortify] Upgraded brick at ({x},{y}) to steel")

    def is_in_protected_area(self, rect):
        """检查矩形是否在保护区域内"""
        for area in self.protected_areas:
            if area.colliderect(rect):
                return True
        return False
    
    def update(self):
        """更新游戏状态"""
        # 更新玩家坦克
        self.player_group.update(self.terrain_group, self.enemy_group)
        
        # 更新敌人坦克，处理敌人射击
        for enemy in list(self.enemy_group):
            # 调用敌人更新，并获取可能返回的子弹
            enemy_bullet = enemy.update(self.terrain_group, self.player_group, self.enemy_group)
            # 如果敌人发射了子弹，添加到敌人子弹组
            if enemy_bullet:
                self.enemy_bullets.add(enemy_bullet)
                print(f"[Enemy] Fired a bullet from position ({enemy.rect.centerx}, {enemy.rect.centery})")
        
        # 更新子弹
        self.player_bullets.update()
        self.enemy_bullets.update()
        
        # 更新爆炸效果
        self.explosions.update()
        
        # 生成敌人
        self.spawn_enemy()
        
        # 生成道具 (低概率)
        self.spawn_power_up()
        
        # 处理碰撞
        self.handle_collisions()
        
        # 检查胜利或失败条件
        return self.check_game_state()
    
    def spawn_power_up(self):
        """随机生成道具"""
        # 低概率生成道具 (0.5% 每帧)
        if random.random() < 0.005 and len(self.power_up_group) < 3:  # 最多3个道具同时存在
            power_type = random.randint(0, 5)  # 包括新增的BASE_FORTIFY类型 (0-5)
            
            # 寻找安全的位置放置道具 (避开保护区和现有地形)
            for _ in range(10):  # 尝试10次
                x = random.randint(BLOCK_SIZE, SCREEN_WIDTH - 2 * BLOCK_SIZE) 
                y = random.randint(BLOCK_SIZE, SCREEN_HEIGHT - 2 * BLOCK_SIZE)
                
                power_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                if not self.is_in_protected_area(power_rect):
                    # 检查该位置是否有其他物体
                    existing = pygame.sprite.Sprite()
                    existing.rect = power_rect
                    if not pygame.sprite.spritecollideany(existing, self.terrain_group):
                        self.power_up_group.add(PowerUp(x, y, power_type))
                        print(f"[Power-up] Spawned type {power_type} at ({x},{y})")
                        break
    
    def handle_collisions(self):
        """处理游戏中的各种碰撞"""
        # --- 子弹与坦克碰撞 ---
        # 处理玩家发射的子弹与敌人坦克的碰撞检测
        for bullet in list(self.player_bullets):  # 遍历所有玩家发射的子弹
            hit_tanks = pygame.sprite.spritecollide(bullet, self.enemy_group, False)  # 检测子弹是否与任何敌方坦克碰撞，不自动移除碰撞的坦克
            if hit_tanks:  # 如果检测到碰撞
                enemy = hit_tanks[0]  # 获取第一个碰撞的敌方坦克
                destroyed = enemy.take_damage(bullet.damage)  # 对敌方坦克造成伤害，并判断是否被摧毁
                if destroyed:  # 如果敌方坦克被摧毁
                    # 击毁敌人，为玩家增加100分
                    self.score += 100
                    # 在敌方坦克位置创建爆炸效果
                    self.explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery, TANK_SIZE))
                    # 有20%的概率从被摧毁的敌方坦克处掉落道具
                    if random.random() < 0.2:  # 生成0-1之间的随机数，小于0.2则掉落道具
                        power_type = random.randint(0, 5)  # 随机选择道具类型，0-5包括了BASE_FORTIFY类型
                        self.power_up_group.add(PowerUp(enemy.rect.centerx, enemy.rect.centery, power_type))  # 在敌方坦克位置创建道具
                        print(f"[Power-up] Enemy dropped type {power_type}")  # 在控制台输出掉落道具的信息
                    enemy.kill()  # 从所有精灵组中移除敌方坦克
                    
                # 子弹击中目标后消失
                bullet.kill()  # 从所有精灵组中移除子弹
        
        # 敌人子弹与玩家坦克
        for bullet in list(self.enemy_bullets):  # 遍历所有敌人发射的子弹
            hit_tanks = pygame.sprite.spritecollide(bullet, self.player_group, False)  # 检测子弹是否与任何玩家坦克碰撞，不自动移除碰撞的坦克
            if hit_tanks:  # 如果检测到碰撞
                player = hit_tanks[0]  # 获取第一个碰撞的玩家坦克
                destroyed = player.take_damage(bullet.damage)  # 对玩家坦克造成伤害，并判断是否被摧毁
                if destroyed:  # 如果玩家坦克被摧毁
                    self.explosions.add(Explosion(player.rect.centerx, player.rect.centery, TANK_SIZE))  # 在玩家坦克位置创建爆炸效果
                    player.lives -= 1  # 玩家生命值减少1
                    if player.lives <= 0:  # 如果玩家没有剩余生命
                        player.kill()  # 从所有精灵组中移除玩家坦克
                    else:  # 如果玩家还有剩余生命
                        # 保存玩家坦克的升级状态
                        tank_level = player.tank_level
                        speed = player.speed
                        bullet_damage = player.bullet_damage
                        bullet_speed = player.bullet_speed
                        shot_delay = player.shot_delay
                        bullet_count = player.bullet_count
                        bullet_level = player.bullet_level
                        
                        # 重生玩家坦克，只重置位置和生命值
                        if player.player_id == PLAYER_ONE:  # 如果是玩家一
                            player.rect.topleft = (SCREEN_WIDTH // 2 - TANK_SIZE // 2, SCREEN_HEIGHT - TANK_SIZE - 4 * BLOCK_SIZE)  # 设置玩家一重生位置
                        else:  # 如果是玩家二
                            player.rect.topleft = (SCREEN_WIDTH // 3 * 2 - TANK_SIZE // 2, SCREEN_HEIGHT - TANK_SIZE - 4 * BLOCK_SIZE)  # 设置玩家二重生位置
                        player.health = player.max_health  # 重置玩家坦克血量为最大血量
                        
                        # 恢复玩家坦克的升级状态
                        player.tank_level = tank_level
                        player.speed = speed
                        player.bullet_damage = bullet_damage
                        player.bullet_speed = bullet_speed
                        player.shot_delay = shot_delay
                        player.bullet_count = bullet_count
                        player.bullet_level = bullet_level
                        
                        # 更新坦克图像
                        player.rotate_image()
                        
                        # 给予短暂无敌时间
                        player.shield = True  # 激活护盾
                        player.shield_time = pygame.time.get_ticks() + 3000  # 设置护盾持续时间为3秒
                bullet.kill()  # 子弹击中目标后消失
        
        # --- 子弹与地形碰撞 ---
        for bullet_group in [self.player_bullets, self.enemy_bullets]:  # 遍历玩家子弹组和敌人子弹组
            for bullet in list(bullet_group):  # 遍历每个子弹组中的所有子弹
                hit_terrain = pygame.sprite.spritecollide(bullet, self.terrain_group, False)  # 检测子弹是否与任何地形碰撞，不自动移除碰撞的地形
                for terrain in hit_terrain:  # 遍历所有碰撞的地形
                    if terrain.terrain_type in [WATER, GRASS]:  # 如果地形是水或草地
                        continue  # 水和草地不会阻挡子弹，继续检查下一个地形
                    
                    if terrain.terrain_type == STEEL:  # 如果地形是钢墙
                        # 检查是否为高级子弹
                        if isinstance(bullet.owner, PlayerTank) and bullet.owner.tank_level == 2:  # 如果子弹所有者是玩家坦克且坦克等级为2
                            # 高级子弹可以摧毁钢墙
                            terrain.kill()  # 从所有精灵组中移除钢墙
                            self.explosions.add(Explosion(terrain.rect.centerx, terrain.rect.centery, BLOCK_SIZE))  # 在钢墙位置创建爆炸效果
                    elif terrain.terrain_type == BRICK:  # 如果地形是砖墙
                        # 普通子弹可以摧毁砖墙
                        terrain.kill()  # 从所有精灵组中移除砖墙
                        self.explosions.add(Explosion(terrain.rect.centerx, terrain.rect.centery, BLOCK_SIZE))  # 在砖墙位置创建爆炸效果
                    elif terrain.terrain_type == BASE:  # 如果地形是基地
                        # 基地被摧毁，游戏结束
                        terrain.kill()  # 从所有精灵组中移除基地
                        self.explosions.add(Explosion(terrain.rect.centerx, terrain.rect.centery, BLOCK_SIZE * 2, True))  # 在基地位置创建大型爆炸效果
                    
                    # 子弹碰到地形后消失
                    bullet.kill()  # 从所有精灵组中移除子弹
                    break  # 结束当前子弹的地形碰撞检测
        
        # --- 玩家与道具碰撞 ---
        for player in self.player_group:  # 遍历所有玩家坦克
            hit_power_ups = pygame.sprite.spritecollide(player, self.power_up_group, True)  # 检测玩家是否与任何道具碰撞，并自动移除碰撞的道具
            for power_up in hit_power_ups:  # 遍历所有碰撞的道具
                if power_up.power_type == BULLET_UPGRADE:  # 如果道具类型是子弹升级
                    player.upgrade_bullet()  # 升级玩家的子弹
                    print(f"[Power-up] Player {player.player_id+1} got bullet upgrade")  # 输出日志信息
                elif power_up.power_type == SPEED_BOOST:  # 如果道具类型是速度提升
                    player.speed_boost()  # 提升玩家的速度
                    print(f"[Power-up] Player {player.player_id+1} got speed boost")  # 输出日志信息
                elif power_up.power_type == SHIELD:  # 如果道具类型是护盾
                    player.activate_shield()  # 激活玩家的护盾
                    print(f"[Power-up] Player {player.player_id+1} got shield")  # 输出日志信息
                elif power_up.power_type == HEALTH_BOOST:  # 如果道具类型是生命提升
                    player.add_health()  # 增加玩家的生命值
                    print(f"[Power-up] Player {player.player_id+1} got health boost")  # 输出日志信息
                elif power_up.power_type == TANK_UPGRADE:  # 如果道具类型是坦克升级
                    player.upgrade_tank()  # 升级玩家的坦克
                    print(f"[Power-up] Player {player.player_id+1} got tank upgrade")  # 输出日志信息
                elif power_up.power_type == BASE_FORTIFY:  # 如果道具类型是基地加固
                    # 调用基地加固方法
                    self.fortify_base()  # 加固游戏基地
                    print(f"[Power-up] Player {player.player_id+1} fortified base")  # 输出日志信息
        
        # --- 敌人与道具碰撞（第12关开始） ---
        if self.level_number >= 12:  # 如果当前关卡大于等于12
            for enemy in self.enemy_group:  # 遍历所有敌人坦克
                hit_power_ups = pygame.sprite.spritecollide(enemy, self.power_up_group, True)  # 检测敌人是否与任何道具碰撞，并自动移除碰撞的道具
                for power_up in hit_power_ups:  # 遍历所有碰撞的道具
                    if power_up.power_type == BULLET_UPGRADE:  # 如果道具类型是子弹升级
                        enemy.upgrade_bullet()  # 升级敌人的子弹
                    elif power_up.power_type == SPEED_BOOST:  # 如果道具类型是速度提升
                        enemy.speed_boost()  # 提升敌人的速度
                    elif power_up.power_type == SHIELD:  # 如果道具类型是护盾
                        enemy.activate_shield()  # 激活敌人的护盾
                    elif power_up.power_type == HEALTH_BOOST:  # 如果道具类型是生命提升
                        enemy.add_health()  # 增加敌人的生命值
                    elif power_up.power_type == TANK_UPGRADE:  # 如果道具类型是坦克升级
                        enemy.upgrade_tank()  # 升级敌人的坦克
                    elif power_up.power_type == BASE_FORTIFY:  # 如果道具类型是基地加固
                        self.fortify_base()  # 加固游戏基地
                    print(f"[Power-up] Enemy type {enemy.enemy_type} got {power_up.power_type}")  # 输出日志信息
    
    def check_game_state(self):
        """检查游戏胜利或失败条件"""
        # 如果基地被摧毁，游戏失败
        if not self.base or not self.base.alive():  # 检查基地是否存在且存活
            return "game_over"  # 返回游戏结束状态
        
        # 如果所有敌人都被消灭，并且没有新敌人了，进入下一关
        if len(self.enemy_group) == 0 and self.enemies_spawned >= self.enemy_count:  # 检查当前关卡的敌人是否全部被消灭且不会再生成新敌人
            return "level_complete"  # 返回关卡完成状态
        
        # 如果所有玩家都死亡，游戏失败
        if len(self.player_group) == 0:  # 检查是否还有存活的玩家
            return "game_over"  # 返回游戏结束状态
        
        # 游戏继续
        return "playing"  # 返回游戏继续状态
    
    def spawn_enemy(self):
        """生成敌人坦克"""
        # 检查是否可以生成新敌人
        if (self.enemies_spawned < self.enemy_count and  # 如果已生成的敌人数量小于关卡总敌人数量
            len(self.enemy_group) < self.max_enemies_on_screen and  # 且当前屏幕上的敌人数量小于最大同屏敌人数量
            pygame.time.get_ticks() > self.next_enemy_spawn):  # 且当前时间已超过下一次生成敌人的时间
            
            # 根据关卡难度选择敌人类型
            enemy_types = [NORMAL_ENEMY]  # 初始只有普通敌人类型
            
            if self.level_number >= 3:  # 如果关卡大于等于3
                enemy_types.append(FAST_ENEMY)  # 添加快速敌人类型
            if self.level_number >= 6:  # 如果关卡大于等于6
                enemy_types.append(ARMORED_ENEMY)  # 添加装甲敌人类型
            if self.level_number >= 9:  # 如果关卡大于等于9
                enemy_types.append(BOSS_ENEMY)  # 添加boss敌人类型
            if self.level_number >= 12:  # 如果关卡大于等于12
                enemy_types.append(ELITE_ENEMY)  # 添加精英敌人类型
            if self.level_number >= 15:  # 如果关卡大于等于15
                enemy_types.append(ULTIMATE_ENEMY)  # 添加终极敌人类型
            
            # 随机选择生成点
            spawn_point = random.choice(self.enemy_spawn_points)  # 从预定义的敌人生成点中随机选择一个
            
            # 随机选择敌人类型
            enemy_type = random.choice(enemy_types)  # 从可用的敌人类型中随机选择一个
            
            # 创建敌人
            enemy = EnemyTank(spawn_point[0], spawn_point[1], enemy_type)  # 在选定的生成点创建指定类型的敌人坦克
            
            # 检查是否能安全生成 (避免碰撞)
            if not pygame.sprite.spritecollideany(enemy, self.terrain_group) and not pygame.sprite.spritecollideany(enemy, self.player_group):  # 检查敌人坦克是否与地形或玩家坦克碰撞
                self.enemy_group.add(enemy)  # 将敌人坦克添加到敌人组
                self.enemies_spawned += 1  # 已生成敌人数量加1
                print(f"[Enemy] Spawned type {enemy_type} at {spawn_point}")  # 输出敌人生成信息
            else:
                # 安全检查失败，不计入已生成数量
                enemy = None  # 放弃生成敌人坦克
            
            # 设置下一次生成时间
            self.next_enemy_spawn = pygame.time.get_ticks() + self.spawn_delay  # 计算下一次敌人生成的时间

# 游戏类 - 控制整个游戏流程
class Game:
    def __init__(self):
        pygame.init()  # 初始化pygame库，设置所有pygame模块
        
        # 设置屏幕
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建游戏窗口，设置宽高
        pygame.display.set_caption("坦克大战")  # 设置窗口标题
        
        # 设置字体
        try:
            self.font = pygame.font.SysFont("simsun", 24)  # 尝试加载中文字体"宋体"，字号24
            self.title_font = pygame.font.SysFont("simsun", 48)  # 设置标题字体，字号48
            # 测试字体渲染
            _ = self.font.render("测试", True, WHITE)  # 测试中文字体能否正常渲染
        except:
            print("无法加载中文字体，使用默认字体")  # 打印错误信息
            self.font = pygame.font.SysFont(None, 24)  # 使用默认字体作为备选
            self.title_font = pygame.font.SysFont(None, 48)  # 使用默认字体作为标题备选
        
        # 游戏时钟
        self.clock = pygame.time.Clock()  # 创建时钟对象，用于控制游戏帧率
        
        # 游戏状态
        self.running = True  # 游戏运行标志，为True时游戏继续运行
        self.game_state = "menu"  # 初始游戏状态为菜单界面，可选值有menu, playing, game_over, level_complete
        
        # 当前关卡
        self.current_level = None  # 当前关卡对象
        self.level_number = 1  # 当前关卡编号，初始为第1关
        self.game_mode = SINGLE_PLAYER  # 游戏模式，默认为单人模式
        
        # 创建开始菜单
        self.menu = StartMenu(self.font, self.title_font)  # 创建开始菜单对象，传入字体参数
        
        # 游戏分数
        self.score = 0  # 游戏分数，初始为0
        
        # 输出按键映射
        self.print_key_mappings()  # 调用方法打印按键映射，方便玩家了解操作
        
        # 游戏初始化完成
        print("成功加载所有游戏资源，游戏可以开始运行了！")  # 打印游戏初始化完成的信息
    
    def print_key_mappings(self):
        """输出按键映射，方便调试"""
        print("\n**** 游戏控制说明 ****")  # 打印控制说明的标题
        print("玩家1: W/S/A/D - 移动, 空格 - 射击")  # 打印玩家1的操作按键映射
        print("玩家2: 上/下/左/右方向键 - 移动, 回车 - 射击")  # 打印玩家2的操作按键映射
        print("ESC - 退出游戏")  # 打印退出游戏的按键
        print("P - 暂停游戏")  # 打印暂停游戏的按键
        print("R - 重新开始当前关卡")  # 打印重新开始当前关卡的按键
        print("**********************\n")  # 打印控制说明的结束分隔线
    
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():  # 获取所有等待处理的事件
            if event.type == pygame.QUIT:  # 如果是退出事件（点击窗口关闭按钮）
                self.running = False  # 设置游戏运行标志为False，结束游戏
                return
                
            # 添加ESC键退出游戏的处理
            if event.type == pygame.KEYDOWN:  # 如果是按键按下事件
                if event.key == pygame.K_ESCAPE:  # 如果按下的是ESC键
                    if self.game_state == "menu":  # 如果当前在菜单状态
                        self.running = False  # 设置游戏运行标志为False，结束游戏
                    else:  # 如果在其他状态
                        self.game_state = "menu"  # 返回菜单状态
                        self.menu = StartMenu(self.font, self.title_font)  # 重新创建菜单
                    return
            
            if self.game_state == "menu":  # 如果当前在菜单状态
                # 在菜单状态下处理事件
                result = self.menu.handle_events(event)  # 调用菜单的事件处理方法，获取处理结果
                if result == "single_player":  # 如果选择了单人模式
                    self.game_mode = SINGLE_PLAYER  # 设置游戏模式为单人
                    self.start_new_game()  # 开始新游戏
                elif result == "two_players":  # 如果选择了双人模式
                    self.game_mode = TWO_PLAYERS  # 设置游戏模式为双人
                    self.start_new_game()  # 开始新游戏
                elif result == "instructions":  # 如果选择了游戏说明
                    self.menu.show_instructions(self.screen, self.font, self.title_font)  # 显示游戏说明
            
            elif self.game_state == "playing":  # 如果当前在游戏进行状态
                # 在游戏状态下处理按键
                if event.type == pygame.KEYDOWN:  # 如果是按键按下事件
                    # 玩家1控制
                    if event.key == pygame.K_w:  # 如果按下W键
                        if self.current_level.player:  # 如果玩家1存在
                            self.current_level.player.direction = UP  # 设置方向为上
                            self.current_level.player.rotate_image()  # 旋转坦克图像
                            self.current_level.player.start_moving()  # 开始移动
                    elif event.key == pygame.K_s:  # 如果按下S键
                        if self.current_level.player:  # 如果玩家1存在
                            self.current_level.player.direction = DOWN  # 设置方向为下
                            self.current_level.player.rotate_image()  # 旋转坦克图像
                            self.current_level.player.start_moving()  # 开始移动
                    elif event.key == pygame.K_a:  # 如果按下A键
                        if self.current_level.player:  # 如果玩家1存在
                            self.current_level.player.direction = LEFT  # 设置方向为左
                            self.current_level.player.rotate_image()  # 旋转坦克图像
                            self.current_level.player.start_moving()  # 开始移动
                    elif event.key == pygame.K_d:  # 如果按下D键
                        if self.current_level.player:  # 如果玩家1存在
                            self.current_level.player.direction = RIGHT  # 设置方向为右
                            self.current_level.player.rotate_image()  # 旋转坦克图像
                            self.current_level.player.start_moving()  # 开始移动
                    elif event.key == pygame.K_SPACE:  # 如果按下空格键
                        # 处理玩家射击
                        if self.current_level.player and self.current_level.player.alive():  # 如果玩家1存在且存活
                            # 检查子弹数量限制
                            if self.current_level.player.bullets_active < self.current_level.player.bullet_count:  # 如果当前活跃子弹数小于最大子弹数
                                bullet = self.current_level.player.shoot()  # 调用射击方法
                                if bullet:  # 如果成功创建了子弹
                                    self.current_level.player_bullets.add(bullet)  # 将子弹添加到玩家子弹组
                    
                    # 玩家2控制 (仅在双人模式)
                    if self.game_mode == TWO_PLAYERS and self.current_level.player2:  # 如果是双人模式且玩家2存在
                        if event.key == pygame.K_UP:  # 如果按下上方向键
                            self.current_level.player2.direction = UP  # 设置方向为上
                            self.current_level.player2.rotate_image()  # 旋转坦克图像
                            self.current_level.player2.start_moving()  # 开始移动
                        elif event.key == pygame.K_DOWN:  # 如果按下下方向键
                            self.current_level.player2.direction = DOWN  # 设置方向为下
                            self.current_level.player2.rotate_image()  # 旋转坦克图像
                            self.current_level.player2.start_moving()  # 开始移动
                        elif event.key == pygame.K_LEFT:  # 如果按下左方向键
                            self.current_level.player2.direction = LEFT  # 设置方向为左
                            self.current_level.player2.rotate_image()  # 旋转坦克图像
                            self.current_level.player2.start_moving()  # 开始移动
                        elif event.key == pygame.K_RIGHT:  # 如果按下右方向键
                            self.current_level.player2.direction = RIGHT  # 设置方向为右
                            self.current_level.player2.rotate_image()  # 旋转坦克图像
                            self.current_level.player2.start_moving()  # 开始移动
                        elif event.key in [pygame.K_KP0, pygame.K_KP_0, pygame.K_0, pygame.K_INSERT, pygame.K_RETURN]:  # 如果按下数字键盘0、插入键或回车键
                            # 处理玩家2射击
                            if self.current_level.player2 and self.current_level.player2.alive():  # 如果玩家2存在且存活
                                if self.current_level.player2.bullets_active < self.current_level.player2.bullet_count:  # 如果当前活跃子弹数小于最大子弹数
                                    bullet = self.current_level.player2.shoot()  # 调用射击方法
                                    if bullet:  # 如果成功创建了子弹
                                        self.current_level.player_bullets.add(bullet)  # 将子弹添加到玩家子弹组
                
                elif event.type == pygame.KEYUP:  # 如果是按键释放事件
                    # 玩家1停止移动（改进：仅在没有其他方向键被按下时停止移动）
                    keys = pygame.key.get_pressed()  # 获取当前所有按键的状态
                    
                    # 处理玩家1的移动
                    if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:  # 如果释放的是WASD键
                        if self.current_level.player:  # 如果玩家1存在
                            # 只有当没有任何方向键被按下时才停止移动
                            if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
                                self.current_level.player.stop_moving()  # 停止移动
                            else:
                                # 如果有其他方向键被按下，更新方向
                                if keys[pygame.K_w]:
                                    self.current_level.player.direction = UP
                                    self.current_level.player.rotate_image()
                                elif keys[pygame.K_s]:
                                    self.current_level.player.direction = DOWN
                                    self.current_level.player.rotate_image()
                                elif keys[pygame.K_a]:
                                    self.current_level.player.direction = LEFT
                                    self.current_level.player.rotate_image()
                                elif keys[pygame.K_d]:
                                    self.current_level.player.direction = RIGHT
                                    self.current_level.player.rotate_image()
                    
                    # 处理玩家2的移动 (仅在双人模式)
                    if self.game_mode == TWO_PLAYERS and self.current_level.player2:  # 如果是双人模式且玩家2存在
                        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:  # 如果释放的是方向键
                            # 只有当没有任何方向键被按下时才停止移动
                            if not (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                                self.current_level.player2.stop_moving()  # 停止移动
                            else:
                                # 如果有其他方向键被按下，更新方向
                                if keys[pygame.K_UP]:
                                    self.current_level.player2.direction = UP
                                    self.current_level.player2.rotate_image()
                                elif keys[pygame.K_DOWN]:
                                    self.current_level.player2.direction = DOWN
                                    self.current_level.player2.rotate_image()
                                elif keys[pygame.K_LEFT]:
                                    self.current_level.player2.direction = LEFT
                                    self.current_level.player2.rotate_image()
                                elif keys[pygame.K_RIGHT]:
                                    self.current_level.player2.direction = RIGHT
                                    self.current_level.player2.rotate_image()
    
    def start_new_game(self):
        """开始新游戏"""
        self.level_number = 1
        self.score = 0
        self.create_level()
        self.game_state = "playing"
    
    def create_level(self):
        """创建新关卡"""
        self.current_level = Level(self.level_number, self.game_mode, self.font)
    
    def next_level(self):
        """进入下一关"""
        self.level_number += 1
        
        # 保存本关的得分
        if self.current_level:
            self.score += self.current_level.score
            
        # 保存玩家坦克的状态
        player1_state = None
        player2_state = None
        
        if self.current_level and self.current_level.player:
            player1_state = {
                'tank_level': self.current_level.player.tank_level,
                'lives': self.current_level.player.lives,
                'speed': self.current_level.player.speed,
                'bullet_damage': self.current_level.player.bullet_damage,
                'bullet_speed': self.current_level.player.bullet_speed,
                'shot_delay': self.current_level.player.shot_delay,
                'bullet_count': self.current_level.player.bullet_count,
                'bullet_level': self.current_level.player.bullet_level
            }
        
        if self.current_level and self.current_level.player2:
            player2_state = {
                'tank_level': self.current_level.player2.tank_level,
                'lives': self.current_level.player2.lives,
                'speed': self.current_level.player2.speed,
                'bullet_damage': self.current_level.player2.bullet_damage,
                'bullet_speed': self.current_level.player2.bullet_speed,
                'shot_delay': self.current_level.player2.shot_delay,
                'bullet_count': self.current_level.player2.bullet_count,
                'bullet_level': self.current_level.player2.bullet_level
            }
        
        # 创建新关卡
        self.current_level = Level(self.level_number, self.game_mode, self.font)
        
        # 应用保存的玩家状态
        if player1_state and self.current_level.player:
            self.current_level.player.tank_level = player1_state['tank_level']
            self.current_level.player.lives = player1_state['lives']
            self.current_level.player.speed = player1_state['speed']
            self.current_level.player.bullet_damage = player1_state['bullet_damage']
            self.current_level.player.bullet_speed = player1_state['bullet_speed']
            self.current_level.player.shot_delay = player1_state['shot_delay']
            self.current_level.player.bullet_count = player1_state['bullet_count']
            self.current_level.player.bullet_level = player1_state['bullet_level']
            # 更新坦克图像
            self.current_level.player.rotate_image()
        
        if player2_state and self.current_level.player2:
            self.current_level.player2.tank_level = player2_state['tank_level']
            self.current_level.player2.lives = player2_state['lives']
            self.current_level.player2.speed = player2_state['speed']
            self.current_level.player2.bullet_damage = player2_state['bullet_damage']
            self.current_level.player2.bullet_speed = player2_state['bullet_speed']
            self.current_level.player2.shot_delay = player2_state['shot_delay']
            self.current_level.player2.bullet_count = player2_state['bullet_count']
            self.current_level.player2.bullet_level = player2_state['bullet_level']
            # 更新坦克图像
            self.current_level.player2.rotate_image()
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        
        if self.game_state == "menu":
            # 绘制菜单
            self.menu.draw(self.screen)
        
        elif self.game_state == "playing" or self.game_state == "game_over" or self.game_state == "level_complete":
            # 绘制游戏元素
            if self.current_level:
                # 绘制地形
                self.current_level.terrain_group.draw(self.screen)
                
                # 绘制玩家和敌人坦克
                self.current_level.player_group.draw(self.screen)
                self.current_level.enemy_group.draw(self.screen)
                
                # 绘制子弹
                self.current_level.player_bullets.draw(self.screen)
                self.current_level.enemy_bullets.draw(self.screen)
                
                # 绘制道具
                self.current_level.power_up_group.draw(self.screen)
                
                # 绘制爆炸效果
                self.current_level.explosions.draw(self.screen)
                
                # 绘制玩家坦克血条和护盾
                for player in self.current_level.player_group:
                    player.draw_health_bar(self.screen)
                    if player.shield:
                        player.draw_shield(self.screen)
                
                # 绘制敌人坦克血条
                for enemy in self.current_level.enemy_group:
                    enemy.draw_health_bar(self.screen)
                    if enemy.shield:
                        enemy.draw_shield(self.screen)
                
                # 绘制HUD (游戏信息显示)
                self.draw_hud()
            
            # 绘制游戏结束或关卡完成信息
            if self.game_state == "game_over":
                self.draw_game_over()
            elif self.game_state == "level_complete":
                self.draw_level_complete()
        
        pygame.display.update()
    
    def draw_hud(self):
        """绘制游戏信息显示"""
        # 显示当前关卡
        level_text = self.font.render(f"关卡: {self.level_number}", True, WHITE)  # 渲染关卡文本
        self.screen.blit(level_text, (10, 10))  # 将关卡文本绘制到屏幕左上角
        
        # 显示总分数
        score_text = self.font.render(f"分数: {self.score + (self.current_level.score if self.current_level else 0)}", True, WHITE)  # 渲染分数文本（包括当前关卡的分数）
        self.screen.blit(score_text, (10, 40))  # 将分数文本绘制到屏幕上
        
        # 显示剩余敌人数量
        if self.current_level:  # 如果当前关卡存在
            enemies_text = self.font.render(f"敌人: {self.current_level.enemies_spawned}/{self.current_level.max_enemies}", True, WHITE)  # 渲染敌人数量文本，格式为"已生成数/总数"
            self.screen.blit(enemies_text, (10, 70))  # 将敌人数量文本绘制到屏幕上
        
        # 显示玩家生命
        if self.current_level and self.current_level.player:  # 如果当前关卡和玩家1存在
            lives_text = self.font.render(f"生命: {self.current_level.player.lives}", True, WHITE)  # 渲染玩家1生命值文本
            self.screen.blit(lives_text, (10, 100))  # 将玩家1生命值文本绘制到屏幕上
        
        # 双人模式显示玩家2生命
        if self.game_mode == TWO_PLAYERS and self.current_level and self.current_level.player2:  # 如果是双人模式且当前关卡和玩家2存在
            lives2_text = self.font.render(f"P2生命: {self.current_level.player2.lives}", True, WHITE)  # 渲染玩家2生命值文本
            self.screen.blit(lives2_text, (10, 130))  # 将玩家2生命值文本绘制到屏幕上
    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        game_over_text = self.title_font.render("游戏结束", True, RED)  # 使用大字体渲染"游戏结束"文本，颜色为红色
        score_text = self.font.render(f"最终分数: {self.score + (self.current_level.score if self.current_level else 0)}", True, WHITE)  # 渲染最终分数文本
        restart_text = self.font.render("按R键重新开始，按M键回到主菜单", True, WHITE)  # 渲染重新开始提示文本
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))  # 将"游戏结束"文本居中显示在屏幕上方
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))  # 将最终分数文本居中显示在屏幕中间
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))  # 将重新开始提示文本居中显示在屏幕下方
    
    def draw_level_complete(self):
        """绘制关卡完成界面"""
        complete_text = self.title_font.render(f"关卡 {self.level_number} 完成!", True, GREEN)  # 使用大字体渲染关卡完成文本，颜色为绿色
        score_text = self.font.render(f"关卡分数: {self.current_level.score if self.current_level else 0}", True, WHITE)  # 渲染当前关卡分数文本
        total_text = self.font.render(f"总分数: {self.score + (self.current_level.score if self.current_level else 0)}", True, WHITE)  # 渲染总分数文本
        continue_text = self.font.render("按任意键继续", True, WHITE)  # 渲染继续提示文本
        
        self.screen.blit(complete_text, (SCREEN_WIDTH//2 - complete_text.get_width()//2, SCREEN_HEIGHT//2 - 70))  # 将关卡完成文本居中显示在屏幕上方
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 20))  # 将当前关卡分数文本居中显示
        self.screen.blit(total_text, (SCREEN_WIDTH//2 - total_text.get_width()//2, SCREEN_HEIGHT//2 + 10))  # 将总分数文本居中显示
        self.screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 50))  # 将继续提示文本居中显示在屏幕下方
    
    def update(self):
        """更新游戏状态"""
        if self.game_state == "playing":  # 如果当前是游戏进行状态
            if self.current_level:  # 如果当前关卡存在
                # 更新当前关卡状态
                result = self.current_level.update()  # 调用关卡的更新方法，获取更新结果
                
                # 处理关卡结果
                if result == "game_over":  # 如果结果是游戏结束
                    self.game_state = "game_over"  # 设置游戏状态为游戏结束
                elif result == "level_complete":  # 如果结果是关卡完成
                    self.game_state = "level_complete"  # 设置游戏状态为关卡完成
                    
        elif self.game_state == "game_over":  # 如果当前是游戏结束状态
            # 检测按键，重新开始或返回菜单
            keys = pygame.key.get_pressed()  # 获取当前按下的所有按键
            if keys[pygame.K_r]:  # 如果按下了R键
                self.start_new_game()  # 开始新游戏
            elif keys[pygame.K_m]:  # 如果按下了M键
                self.game_state = "menu"  # 返回菜单状态
                self.menu = StartMenu(self.font, self.title_font)  # 重新创建菜单
        
        elif self.game_state == "level_complete":  # 如果当前是关卡完成状态
            # 检测按键，进入下一关
            keys = pygame.key.get_pressed()  # 获取当前按下的所有按键
            if any(keys):  # 如果有任何按键被按下
                self.next_level()  # 进入下一关
                self.game_state = "playing"  # 设置游戏状态为游戏进行中
    
    def run(self):
        """运行游戏主循环"""
        while self.running:  # 当游戏运行标志为True时循环
            self.handle_events()  # 处理游戏事件
            self.update()  # 更新游戏状态
            self.draw()  # 绘制游戏画面
            self.clock.tick(60)  # 限制帧率为60FPS
        
        pygame.quit()  # 退出pygame
        sys.exit()  # 退出程序

# 游戏主函数
def main():
    game = Game()  # 创建游戏实例
    game.run()  # 运行游戏主循环

# 程序入口
if __name__ == "__main__":  # 当程序直接运行而不是被导入时
    main()  # 调用主函数
