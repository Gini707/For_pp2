import pygame

PINK = (255, 105, 180)
DEEP_PINK = (220, 20, 120)
HOT_PINK = (255, 20, 147)
LIGHT_PINK = (255, 182, 193)
ROSE = (255, 228, 235)
WHITE = (255, 255, 255)
BLACK = (10, 5, 15)
DARK = (25, 10, 30)
GRAY = (160, 130, 150)
MINT = (152, 255, 200)
GOLD = (255, 220, 80)
RED = (255, 70, 90)

BLUE = (50, 120, 255)
DARK_BLUE = (20, 70, 180)
SHADOW_BLUE = (10, 35, 90)

CAR_COLORS = {
    "pink": (255, 105, 180),
    "mint": (100, 230, 160),
    "lavender": (180, 140, 255),
    "white": (240, 240, 250),
    "red": (255, 80, 80),
}


def get_font(size, bold=False):
    fonts = ["Segoe UI", "Arial Rounded MT Bold", "Trebuchet MS", "Arial"]
    for name in fonts:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)


def draw_pill_button(surface, rect, text, hovered=False, color=None):
    base = color if color else (DARK_BLUE if hovered else BLUE)

    shadow_rect = rect.move(0, 4)
    pygame.draw.rect(surface, SHADOW_BLUE, shadow_rect, border_radius=30)
    pygame.draw.rect(surface, base, rect, border_radius=30)

    if hovered:
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=30)

    font = get_font(22, bold=True)
    label = font.render(text, True, WHITE)
    surface.blit(label, label.get_rect(center=rect.center))


def draw_background(surface, W, H, scroll=0):
    surface.fill(DARK)

    for i in range(0, H + 60, 60):
        y = (i + scroll) % (H + 60) - 30
        pygame.draw.line(surface, (40, 20, 50), (0, y), (W, y), 1)

    for i in range(0, W + 60, 60):
        x = i
        pygame.draw.line(surface, (40, 20, 50), (x, 0), (x, H), 1)


def draw_title(surface, W):
    font_big = get_font(64, bold=True)
    font_sub = get_font(18)

    title = font_big.render("RACER", True, BLUE)
    glow = font_big.render("RACER", True, (120, 180, 255))

    surface.blit(glow, glow.get_rect(center=(W // 2 + 2, 102)))
    surface.blit(title, title.get_rect(center=(W // 2, 100)))

    sub = font_sub.render("Arcade road challenge", True, LIGHT_PINK)
    surface.blit(sub, sub.get_rect(center=(W // 2, 145)))


def main_menu(surface, W, H, mouse_pos, scroll):
    draw_background(surface, W, H, scroll)
    draw_title(surface, W)

    buttons = ["▶ Play", "🏆 Leaderboard", "⚙ Settings", "✕ Quit"]
    rects = []

    for i, label in enumerate(buttons):
        rect = pygame.Rect(W // 2 - 130, 200 + i * 70, 260, 50)
        hovered = rect.collidepoint(mouse_pos)
        draw_pill_button(surface, rect, label, hovered)
        rects.append(rect)

    tag = get_font(13).render("Arcade Racer Project", True, (180, 180, 220))
    surface.blit(tag, tag.get_rect(bottomright=(W - 15, H - 10)))

    return rects


def settings_screen(surface, W, H, mouse_pos, settings, scroll):
    draw_background(surface, W, H, scroll)

    title_font = get_font(42, bold=True)
    title = title_font.render("Settings", True, BLUE)
    surface.blit(title, title.get_rect(center=(W // 2, 60)))

    items = []
    y = 130

    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
    r_sound = pygame.Rect(W // 2 - 150, y, 300, 48)
    draw_pill_button(surface, r_sound, sound_text, r_sound.collidepoint(mouse_pos))
    items.append(("sound", r_sound))

    y += 70

    label_font = get_font(20)
    lbl = label_font.render("Car Color:", True, LIGHT_PINK)
    surface.blit(lbl, lbl.get_rect(center=(W // 2, y)))

    y += 35

    color_rects = {}
    cx = W // 2 - (len(CAR_COLORS) * 55) // 2

    for name, col in CAR_COLORS.items():
        cr = pygame.Rect(cx, y, 48, 48)

        pygame.draw.rect(surface, (80, 40, 60), cr.move(0, 3), border_radius=24)
        pygame.draw.rect(surface, col, cr, border_radius=24)

        if settings["car_color"] == name:
            pygame.draw.rect(surface, WHITE, cr, 3, border_radius=24)

        color_rects[name] = cr
        cx += 58

    items.append(("color_row", color_rects))

    y += 70

    lbl2 = label_font.render("Difficulty:", True, LIGHT_PINK)
    surface.blit(lbl2, lbl2.get_rect(center=(W // 2, y)))

    y += 35

    diffs = ["easy", "normal", "hard"]
    diff_rects = {}
    dx = W // 2 - 170

    for d in diffs:
        dr = pygame.Rect(dx, y, 100, 40)
        active = settings["difficulty"] == d
        draw_pill_button(
            surface,
            dr,
            d.capitalize(),
            dr.collidepoint(mouse_pos),
            color=DARK_BLUE if active else None
        )
        diff_rects[d] = dr
        dx += 115

    items.append(("diff_row", diff_rects))

    y += 75

    back_rect = pygame.Rect(W // 2 - 100, y, 200, 48)
    draw_pill_button(surface, back_rect, "← Back", back_rect.collidepoint(mouse_pos))
    items.append(("back", back_rect))

    return items


def username_screen(surface, W, H, current_text, scroll):
    draw_background(surface, W, H, scroll)
    draw_title(surface, W)

    font = get_font(28, bold=True)
    prompt = font.render("Enter your name:", True, LIGHT_PINK)
    surface.blit(prompt, prompt.get_rect(center=(W // 2, 200)))

    box = pygame.Rect(W // 2 - 160, 240, 320, 54)
    pygame.draw.rect(surface, (50, 20, 50), box, border_radius=12)
    pygame.draw.rect(surface, BLUE, box, 2, border_radius=12)

    name_font = get_font(30, bold=True)
    txt = name_font.render(current_text + "|", True, WHITE)
    surface.blit(txt, txt.get_rect(center=box.center))

    hint = get_font(16).render("Press ENTER to start", True, GRAY)
    surface.blit(hint, hint.get_rect(center=(W // 2, 315)))


def game_over_screen(surface, W, H, mouse_pos, score, distance, coins, scroll):
    draw_background(surface, W, H, scroll)

    font_big = get_font(52, bold=True)
    go = font_big.render("GAME OVER", True, RED)
    surface.blit(go, go.get_rect(center=(W // 2, 80)))

    tag = get_font(18).render("Final race results", True, LIGHT_PINK)
    surface.blit(tag, tag.get_rect(center=(W // 2, 130)))

    stats = [
        ("Score", str(score)),
        ("Distance", f"{int(distance)} m"),
        ("Coins", str(coins)),
    ]

    sf = get_font(22)
    vf = get_font(22, bold=True)

    for i, (k, v) in enumerate(stats):
        y = 175 + i * 40

        sl = sf.render(k + ":", True, GRAY)
        vl = vf.render(v, True, WHITE)

        surface.blit(sl, sl.get_rect(right=W // 2 - 10, centery=y))
        surface.blit(vl, vl.get_rect(left=W // 2 + 10, centery=y))

    rects = []

    for i, label in enumerate(["↺ Retry", "⌂ Main Menu"]):
        rect = pygame.Rect(W // 2 - 120, 310 + i * 65, 240, 50)
        draw_pill_button(surface, rect, label, rect.collidepoint(mouse_pos))
        rects.append(rect)

    return rects


def leaderboard_screen(surface, W, H, mouse_pos, board, scroll):
    draw_background(surface, W, H, scroll)

    title_font = get_font(42, bold=True)
    title = title_font.render("🏆 Leaderboard", True, GOLD)
    surface.blit(title, title.get_rect(center=(W // 2, 55)))

    sub = get_font(14).render("Top 10 Racers", True, GRAY)
    surface.blit(sub, sub.get_rect(center=(W // 2, 90)))

    headers = ["#", "Name", "Score", "Dist", "Coins"]
    col_x = [40, 90, 230, 320, 400]

    hf = get_font(16, bold=True)

    for h, x in zip(headers, col_x):
        header = hf.render(h, True, BLUE)
        surface.blit(header, (x, 110))

    pygame.draw.line(surface, BLUE, (30, 130), (W - 30, 130), 1)

    ef = get_font(16)

    for i, entry in enumerate(board[:10]):
        y = 140 + i * 32
        rank_col = GOLD if i == 0 else (LIGHT_PINK if i < 3 else WHITE)

        vals = [
            str(i + 1),
            entry.get("name", "?")[:12],
            str(entry.get("score", 0)),
            str(entry.get("distance", 0)) + "m",
            str(entry.get("coins", 0)),
        ]

        for val, x in zip(vals, col_x):
            lbl = ef.render(val, True, rank_col)
            surface.blit(lbl, (x, y))

    if not board:
        empty = get_font(20).render("No scores yet — be the first!", True, GRAY)
        surface.blit(empty, empty.get_rect(center=(W // 2, 240)))

    back_rect = pygame.Rect(W // 2 - 100, H - 70, 200, 48)
    draw_pill_button(surface, back_rect, "← Back", back_rect.collidepoint(mouse_pos))

    return [back_rect]


def draw_hud(surface, W, score, distance, coins, powerup, powerup_timer, shield_active, total_dist):
    hud_bg = pygame.Surface((W, 50), pygame.SRCALPHA)
    hud_bg.fill((15, 5, 20, 200))
    surface.blit(hud_bg, (0, 0))

    hf = get_font(18, bold=True)

    sc = hf.render(f"Score: {score}", True, WHITE)
    surface.blit(sc, (10, 15))

    dist_txt = hf.render(f"Dist: {int(distance)}m", True, LIGHT_PINK)
    surface.blit(dist_txt, (W // 2 - 60, 15))

    coins_txt = hf.render(f"Coins: {coins}", True, GOLD)
    surface.blit(coins_txt, (W - 160, 15))

    if powerup:
        pu_colors = {
            "nitro": (255, 200, 0),
            "shield": (100, 200, 255),
            "repair": (100, 255, 150),
        }

        col = pu_colors.get(powerup, BLUE)
        bar_w = int((powerup_timer / 4.0) * 120)

        pygame.draw.rect(surface, (50, 50, 50), (W // 2 + 80, 18, 120, 14), border_radius=7)
        pygame.draw.rect(surface, col, (W // 2 + 80, 18, bar_w, 14), border_radius=7)

        pu_lbl = get_font(14).render(powerup.upper(), True, col)
        surface.blit(pu_lbl, (W // 2 + 80, 35))

    if shield_active and not powerup:
        sh = get_font(16).render("SHIELD", True, (100, 200, 255))
        surface.blit(sh, (W // 2 + 60, 18))