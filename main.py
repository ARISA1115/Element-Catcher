import pygame
import sys
import os
import random

pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 960, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Element Catcher")

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# フォント（NotoSansJP-Regular.ttfを使用）
font_path = "assets/fonts/NotoSansJP-Regular.ttf"
try:
    if os.path.exists(font_path):
        font_large = pygame.font.Font(font_path, 42)
        font_medium = pygame.font.Font(font_path, 32)
        font_small = pygame.font.Font(font_path, 24)
        font_tiny = pygame.font.Font(font_path, 20)
    else:
        print(f"フォントファイルが見つかりません: {font_path}")
        # デフォルトフォントにフォールバック
        font_large = pygame.font.Font(None, 42)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        font_tiny = pygame.font.Font(None, 20)
except Exception as e:
    print(f"フォント読み込みエラー: {e}")
    font_large = pygame.font.Font(None, 42)
    font_medium = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 20)

# 背景とキャラ画像
try:
    background_img = pygame.transform.scale(pygame.image.load("assets/images/background.png"), (WIDTH, HEIGHT))
    penguin_img = pygame.transform.scale(pygame.image.load("assets/images/penguin.png"), (160, 160))
except Exception as e:
    print(f"画像読み込みエラー: {e}")
    # 簡単な代替画像を作成
    background_img = pygame.Surface((WIDTH, HEIGHT))
    background_img.fill((135, 206, 235))  # 空色
    penguin_img = pygame.Surface((160, 160))
    penguin_img.fill((0, 0, 0))  # 黒い四角

# ペンギン初期位置（机の上に重ならないように手前に配置）
penguin_x = WIDTH // 2 - 80
penguin_y = HEIGHT - 170
penguin_speed = 10

# 元素データとアイコン画像
ELEMENTS = {
    "H": "水素 (H) : 宇宙で最も多く存在し、太陽のエネルギー源でもあります。",
    "O": "酸素 (O) : 呼吸に必要不可欠で、水や多くの化合物にも含まれます。",
    "C": "炭素 (C) : 生物の体をつくる基本元素。有機化合物の中心です。",
    "N": "窒素 (N) :空気の約78%を占め、植物の成長に必要な肥料の主成分です。",
    "He": "ヘリウム (He) : とても軽くて燃えにくい気体。気球やMRI冷却に使われます。",
    "Na": "ナトリウム (Na) : 食塩（NaCl）の成分で、体内の水分バランスに関与します。",
    "Cl": "塩素 (Cl) : 消毒や胃酸に含まれます。",
    "Fe": "鉄 (Fe) : 血液中のヘモグロビンを構成し、酸素を運ぶ役割を担います",
    "Al": "アルミニウム (Al) :軽くてさびにくい金属。飲料缶や飛行機に使われます。",
    "Au": "金 (Au) : 美しくさびにくい貴金属。アクセサリーや電子部品に利用されます。",
    "Ag": "銀 (Ag) : 高い電気伝導性を持ち、装飾品や電子材料に使われます。",
    "Ca": "カルシウム (Ca) : 骨や歯を作る重要な成分で、牛乳などに多く含まれます。",
    "K": "カリウム (K) : 細胞のはたらきを整えるミネラルで、果物や野菜に多く含まれます。",
    "Be": "ベリリウム (Be) : 軽くて強い金属で、X線機器や航空機に使用されます。",
    "P": "リン (P) : DNAやATPに含まれ、エネルギーの流れや骨の構成に不可欠です。",
    "S": "硫黄 (S) : 温泉のにおいのもとで、タンパク質やビタミンの構成要素でもあります。"
}

element_images = {}
for symbol in ELEMENTS:
    path = f"assets/images/element_icons/{symbol}.png"
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            element_images[symbol] = pygame.transform.scale(img, (64, 64))
        except Exception as e:
            print(f"元素画像読み込みエラー {symbol}: {e}")
            # 代替画像作成
            temp_img = pygame.Surface((64, 64))
            temp_img.fill((200, 200, 200))
            pygame.draw.circle(temp_img, (100, 100, 100), (32, 32), 30)
            element_images[symbol] = temp_img
    else:
        print(f"画像が見つかりません: {path}")
        # 代替画像作成
        temp_img = pygame.Surface((64, 64))
        temp_img.fill((200, 200, 200))
        pygame.draw.circle(temp_img, (100, 100, 100), (32, 32), 30)
        element_images[symbol] = temp_img

# 改善された白抜き文字描画関数
def draw_text_with_outline(text, font, x, y, color, outline_color=BLACK, outline_width=3, center=True):
    """アウトライン付きテキストを描画"""
    # アウトライン用のオフセット
    offsets = []
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                offsets.append((dx, dy))
    
    # アウトライン描画
    for dx, dy in offsets:
        outline = font.render(text, True, outline_color)
        if center:
            rect = outline.get_rect(center=(x + dx, y + dy))
        else:
            rect = outline.get_rect(topleft=(x + dx, y + dy))
        screen.blit(outline, rect)
    
    # メインテキスト描画
    base = font.render(text, True, color)
    if center:
        rect = base.get_rect(center=(x, y))
    else:
        rect = base.get_rect(topleft=(x, y))
    screen.blit(base, rect)

# 状態管理
falling_elements = []
catcher_rect = pygame.Rect(penguin_x + 40, penguin_y, 80, 40)
score = 0
misses = 0
MAX_MISSES = 3
target_element = random.choice(list(ELEMENTS.keys()))
element_timer = 0
element_interval = 60
game_over = False
show_description = ""
description_timer = 0
DESCRIPTION_DURATION = 180  # 説明表示時間を延長
clock = pygame.time.Clock()

# メインループ
while True:
    screen.blit(background_img, (0, 0))
    keys = pygame.key.get_pressed()

    if not game_over:
        # プレイヤー移動
        if keys[pygame.K_LEFT] and penguin_x > 0:
            penguin_x -= penguin_speed
        if keys[pygame.K_RIGHT] and penguin_x < WIDTH - 160:
            penguin_x += penguin_speed
        catcher_rect = pygame.Rect(penguin_x + 40, penguin_y, 80, 40)

        # 元素生成
        element_timer += 1
        if element_timer >= element_interval:
            symbol = random.choice(list(ELEMENTS.keys()))
            x = random.randint(0, WIDTH - 64)
            falling_elements.append({"symbol": symbol, "x": x, "y": -64, "speed": 2})
            element_timer = 0

        # 元素の移動と衝突判定
        for elem in falling_elements[:]:
            elem["y"] += elem["speed"]
            rect = pygame.Rect(elem["x"], elem["y"], 64, 64)
            if rect.colliderect(catcher_rect):
                if elem["symbol"] == target_element:
                    score += 1
                    show_description = ELEMENTS[elem['symbol']]
                    description_timer = DESCRIPTION_DURATION
                    target_element = random.choice(list(ELEMENTS.keys()))
                else:
                    # 間違った元素をキャッチした時のみミス
                    misses += 1
                falling_elements.remove(elem)
            elif elem["y"] > HEIGHT:
                # 元素が画面下に落ちてもミスにしない
                falling_elements.remove(elem)

        if misses >= MAX_MISSES:
            game_over = True

    # 描画開始
    # 落ちてくる元素
    for elem in falling_elements:
        screen.blit(element_images[elem["symbol"]], (elem["x"], elem["y"]))

    # ペンギン
    screen.blit(penguin_img, (penguin_x, penguin_y))

    # スコア・ミス表示（左上、余白を追加）
    draw_text_with_outline(f"スコア: {score}", font_medium, 130, 50, WHITE, BLACK, 2)
    draw_text_with_outline(f"ミス: {misses}/{MAX_MISSES}", font_medium, 130, 90, RED, BLACK, 2)

    # 問題文（中央上、余白を追加）
    if not game_over:
        question_y = 150
        draw_text_with_outline(f"{target_element} をキャッチしよう！", font_large, WIDTH // 2, question_y, WHITE, BLUE, 3)

    # 解説文（中央やや上、1行で表示）
    if description_timer > 0:
        description_y = 220
        draw_text_with_outline(show_description, font_small, WIDTH // 2, description_y, WHITE, BLACK, 3)
        description_timer -= 1

    # ゲームオーバー（中央）
    if game_over:
        # 半透明の背景
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        draw_text_with_outline("ゲームオーバー！", font_large, WIDTH // 2, HEIGHT // 2 - 40, RED, BLACK, 4)
        draw_text_with_outline("Enterキーで再スタート", font_medium, WIDTH // 2, HEIGHT // 2 + 20, WHITE, BLACK, 3)
        draw_text_with_outline(f"最終スコア: {score}", font_medium, WIDTH // 2, HEIGHT // 2 + 60, WHITE, BLACK, 3)

    # 操作説明（画面右下、余裕を持った位置に配置）
    if not game_over:
        draw_text_with_outline("← → キーで移動", font_tiny, WIDTH - 150, HEIGHT - 30, WHITE, BLACK, 2, center=False)

    pygame.display.flip()
    clock.tick(60)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_RETURN:
            # ゲームリセット
            score = 0
            misses = 0
            falling_elements.clear()
            target_element = random.choice(list(ELEMENTS.keys()))
            game_over = False
            show_description = ""
            description_timer = 0