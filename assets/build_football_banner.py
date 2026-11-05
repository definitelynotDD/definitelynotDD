#!/usr/bin/env python3
"""Build assets/football-banner.svg, the animated pixel-art banner on the profile README.

The scene loops every LOOP seconds: a footballer dribbles across a floodlit
pitch, shoots past the keeper, the net shakes, the crowd jumps and the
scoreboard flips to 1-0. Everything is plain SVG + CSS keyframes, so GitHub
plays it inside an <img> tag with no scripts or external services.

Usage: python3 assets/build_football_banner.py
"""
import random
from pathlib import Path

W, H, SCALE = 240, 80, 4  # logical pixels; rendered at W*SCALE wide
GROUND = 70  # bottom row a standing sprite's boots sit on
LOOP = 7  # seconds per loop
OUT = Path(__file__).with_name("football-banner.svg")

# Ticker text on the LED advertising board.
TICKER = "PYTHON * RAG BOTS * AI WORKFLOWS * DATABASES * LEGACY AUTOMATION * ACHARYA AI * TENDERTRACK * CLOUD * "

# Shared colours. Change the kit here.
KIT = {
    "H": "#2b1d14",  # hair
    "S": "#c68642",  # skin
    "E": "#1a1a1a",  # eye
    "J": "#e63946",  # jersey
    "j": "#a4161a",  # jersey shade
    "W": "#f8f9fa",  # shorts
    "w": "#ced4da",  # shorts shade
    "K": "#f8f9fa",  # near sock
    "k": "#adb5bd",  # far sock
    "B": "#111111",  # near boot
    "b": "#3a3a3a",  # far boot
}
KEEPER = {**KIT, "H": "#111111", "J": "#ffd60a", "j": "#c9a400", "W": "#222222", "w": "#111111",
          "K": "#222222", "k": "#111111", "G": "#06d6a0"}
BALL = {"W": "#ffffff", "K": "#1a1a1a", "w": "#d0d0d0"}

# 12x16 footballer, facing right. "." is transparent.
RUN_A = [  # near leg forward, far arm forward
    "....HHHH....",
    "...HHHHHH...",
    "..HHHSSSSS..",
    "..HHSSSSES..",
    "..HSSSSSSS..",
    "...SSSSSS...",
    "...JJJJJJ...",
    "..jJJJJJJJS.",
    ".SjJJJJJJ...",
    "...JJJJJJ...",
    "...WWWWWW...",
    "..wwW..WWW..",
    "..kk....KK..",
    ".kk......KK.",
    "bb........BB",
    "............",
]
RUN_B = [  # near leg back, near arm forward
    "....HHHH....",
    "...HHHHHH...",
    "..HHHSSSSS..",
    "..HHSSSSES..",
    "..HSSSSSSS..",
    "...SSSSSS...",
    "...JJJJJJ...",
    ".SJJJJJJjj..",
    "...JJJJJJjS.",
    "...JJJJJJ...",
    "...WWWWWW...",
    "..WWW..www..",
    "..KK....kk..",
    ".KK......kk.",
    "BB........bb",
    "............",
]
KICK = [
    "....HHHH....",
    "...HHHHHH...",
    "..HHHSSSSS..",
    "..HHSSSSES..",
    "..HSSSSSSS..",
    "...SSSSSS...",
    ".S.JJJJJJ...",
    "..SJJJJJJJS.",
    "...JJJJJJ..S",
    "...JJJJJJ...",
    "...WWWWWW...",
    "..wwW.WWWWW.",
    "..kk....KKKB",
    "..kk.....KKB",
    "..bb........",
    "............",
]
CELEBRATE = [
    "S..HHHH...S.",
    "S.HHHHHH..S.",
    "SHHHSSSSS.S.",
    "SHHSSSSES.S.",
    "SHSSSSSSSJ..",
    "JJSSSSSSJ...",
    ".JJJJJJJJ...",
    "...JJJJJJ...",
    "...JJJJJJ...",
    "...JJJJJJ...",
    "...WWWWWW...",
    "...WW..WW...",
    "...KK..KK...",
    "...KK..KK...",
    "..BBB..BBB..",
    "............",
]
# 10x16 keeper, facing left, gloves up.
KEEPER_STAND = [
    "...HHHH...",
    "..HHHHHH..",
    ".SSSSSHH..",
    ".SESSSSH..",
    ".SSSSSSH..",
    "..SSSSSS..",
    "G.JJJJJJ.G",
    "GJJJJJJJJG",
    "..JJJJJJ..",
    "..JJJJJJ..",
    "..WWWWWW..",
    "..WW..WW..",
    "..KK..KK..",
    "..KK..KK..",
    ".BBB..BBB.",
    "..........",
]
# 18x7 keeper diving low to the left (the wrong way, obviously).
KEEPER_DIVE = [
    "..................",
    "GG...HHHH.........",
    "GJJJSSSSHHJJJWWKKB",
    ".JJSESSSSHJJJWWKKB",
    "..JSSSSSSJJJJWWkkb",
    "....SSSS.jjjj.....",
    "..................",
]
BALL_A = [".WW.", "WKWW", "WWKw", ".ww."]
BALL_B = [".WW.", "WWKW", "WKWw", ".ww."]

FONT3 = {  # 3x5 pixel font
    "A": [".X.", "X.X", "XXX", "X.X", "X.X"], "B": ["XX.", "X.X", "XX.", "X.X", "XX."],
    "C": [".XX", "X..", "X..", "X..", ".XX"], "D": ["XX.", "X.X", "X.X", "X.X", "XX."],
    "E": ["XXX", "X..", "XX.", "X..", "XXX"], "F": ["XXX", "X..", "XX.", "X..", "X.."],
    "G": [".XX", "X..", "X.X", "X.X", ".XX"], "H": ["X.X", "X.X", "XXX", "X.X", "X.X"],
    "I": ["XXX", ".X.", ".X.", ".X.", "XXX"], "J": ["..X", "..X", "..X", "X.X", ".X."],
    "K": ["X.X", "X.X", "XX.", "X.X", "X.X"], "L": ["X..", "X..", "X..", "X..", "XXX"],
    "M": ["X...X", "XX.XX", "X.X.X", "X...X", "X...X"], "N": ["XX.", "X.X", "X.X", "X.X", "X.X"],
    "O": [".X.", "X.X", "X.X", "X.X", ".X."], "P": ["XX.", "X.X", "XX.", "X..", "X.."],
    "Q": [".X.", "X.X", "X.X", "XX.", ".XX"], "R": ["XX.", "X.X", "XX.", "X.X", "X.X"],
    "S": [".XX", "X..", ".X.", "..X", "XX."], "T": ["XXX", ".X.", ".X.", ".X.", ".X."],
    "U": ["X.X", "X.X", "X.X", "X.X", "XXX"], "V": ["X.X", "X.X", "X.X", "X.X", ".X."],
    "W": ["X...X", "X...X", "X.X.X", "X.X.X", ".X.X."], "X": ["X.X", "X.X", ".X.", "X.X", "X.X"],
    "Y": ["X.X", "X.X", ".X.", ".X.", ".X."], "Z": ["XXX", "..X", ".X.", "X..", "XXX"],
    "0": ["XXX", "X.X", "X.X", "X.X", "XXX"], "1": [".X.", "XX.", ".X.", ".X.", "XXX"],
    "-": ["...", "...", "XXX", "...", "..."], "*": ["...", ".X.", "XXX", ".X.", "..."],
    " ": ["...", "...", "...", "...", "..."],
}
FONT5 = {  # 5x7 pixel font for the big GOAL!
    "G": [".XXX.", "X...X", "X....", "X.XXX", "X...X", "X...X", ".XXX."],
    "O": [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "A": [".XXX.", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "L": ["X....", "X....", "X....", "X....", "X....", "X....", "XXXXX"],
    "!": ["X", "X", "X", "X", "X", ".", "X"],
}


def runs_to_paths(pixels):
    """pixels: {(x, y): colour} -> <path> elements, one per colour, merging horizontal runs."""
    by_colour = {}
    for (x, y), c in pixels.items():
        by_colour.setdefault(c, set()).add((x, y))
    out = []
    for colour, pts in by_colour.items():
        d = []
        for y in sorted({p[1] for p in pts}):
            xs = sorted(p[0] for p in pts if p[1] == y)
            start = prev = xs[0]
            for x in xs[1:] + [None]:
                if x is not None and x == prev + 1:
                    prev = x
                    continue
                d.append(f"M{start} {y}h{prev - start + 1}v1h-{prev - start + 1}z")
                if x is not None:
                    start = prev = x
        opacity = ""
        if len(colour) == 9:  # #rrggbbaa -> fill-opacity for older renderers
            opacity = f' fill-opacity="{int(colour[7:], 16) / 255:.2f}"'
            colour = colour[:7]
        out.append(f'<path fill="{colour}"{opacity} d="{"".join(d)}"/>')
    return "".join(out)


def sprite(rows, palette, ox=0, oy=0):
    return runs_to_paths({(ox + x, oy + y): palette[ch]
                          for y, row in enumerate(rows) for x, ch in enumerate(row) if ch != "."})


def text_pixels(s, font, x, y, colour, scale=1):
    px = {}
    cx = x
    for ch in s:
        glyph = font[ch]
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "X":
                    for sx in range(scale):
                        for sy in range(scale):
                            px[(cx + gx * scale + sx, y + gy * scale + sy)] = colour
        cx += (len(glyph[0]) + 1) * scale
    return px, cx - x - scale


def text_width(s, font, scale=1):
    return sum((len(font[ch][0]) + 1) * scale for ch in s) - scale


def show(name, on, off):
    """Keyframes that make an element visible from on% to off% of the loop."""
    frames = []
    if on > 0:
        frames += [f"0%,{on - 0.01:.2f}%{{opacity:0}}"]
    frames += [f"{on}%,{off}%{{opacity:1}}"]
    if off < 100:
        frames += [f"{off + 0.01:.2f}%,100%{{opacity:0}}"]
    return f"@keyframes {name}{{{''.join(frames)}}}"


def build():
    rnd = random.Random(7)
    css, body = [], []

    # --- sky, stars, stand -------------------------------------------------
    bg = {}
    for y in range(0, 11):
        for x in range(W):
            bg[(x, y)] = "#090d21" if y < 4 else "#0d1330" if y < 8 else "#121a3d"
    tiers = [(11, "#1b2142"), (15, "#20274d"), (19, "#262e58")]
    for top, colour in tiers:
        for y in range(top, top + 4):
            for x in range(W):
                bg[(x, y)] = colour
    for x in range(W):
        bg[(x, 23)] = "#0b0f22"
    body.append(runs_to_paths(bg))

    stars = []
    for _ in range(26):
        x, y = rnd.randrange(10, W - 10), rnd.randrange(0, 9)
        if 84 <= x <= 156:
            continue
        stars.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="#fefae0" '
                     f'style="animation-delay:-{rnd.uniform(0, 2.4):.2f}s" class="tw"/>')
    body.append("".join(stars))
    css.append("@keyframes tw{0%,60%{opacity:1}61%,100%{opacity:.2}}"
               ".tw{animation:tw 2.4s steps(1) infinite}")

    # --- crowd ---------------------------------------------------------------
    shirts = ["#e63946", "#f1faee", "#ffd166", "#06d6a0", "#118ab2", "#ef476f", "#8338ec", "#fb8500"]
    skins = ["#f1c27d", "#c68642", "#8d5524", "#e0ac69"]
    fans = [{}, {}, {}]
    for top, _ in tiers:
        offset = rnd.randrange(3)
        for i, x in enumerate(range(10 + offset, W - 10, 3)):
            if rnd.random() < 0.12:
                continue
            group = fans[i % 3]
            group[(x + 1, top)] = rnd.choice(skins)
            shirt = rnd.choice(shirts)
            for dx in range(3):
                group[(x + dx, top + 1)] = shirt
                group[(x + dx, top + 2)] = shirt
    crowd = "".join(f'<g class="bob" style="animation-delay:-{i * 0.2:.1f}s">{runs_to_paths(g)}</g>'
                    for i, g in enumerate(fans))
    flashes = "".join(
        f'<rect x="{rnd.randrange(12, W - 12)}" y="{rnd.choice([11, 15, 19])}" width="1" height="1" '
        f'fill="#ffffff" class="flash" style="animation-delay:-{rnd.uniform(0, 5):.2f}s"/>'
        for _ in range(14))
    body.append(f'<g class="crowdjump">{crowd}{flashes}</g>')
    jump = "".join(f"{p}%{{transform:translateY({-1 if i % 2 == 0 else 0}px)}}"
                   for i, p in enumerate(range(68, 93, 2)))
    css.append("@keyframes bob{0%,49%{transform:translateY(0)}50%,100%{transform:translateY(-1px)}}"
               ".bob{animation:bob 1.2s steps(1) infinite}"
               f"@keyframes crowdjump{{0%,67.9%{{transform:translateY(0)}}{jump}93%,100%{{transform:translateY(0)}}}}"
               f".crowdjump{{animation:crowdjump {LOOP}s steps(1) infinite}}"
               "@keyframes flash{0%,95%{opacity:0}96%{opacity:1}98%,100%{opacity:0}}"
               ".flash{opacity:0;animation:flash 5s steps(1) infinite}")

    # --- floodlights -----------------------------------------------------------
    lights = {}
    for px in (3, 236):
        for y in range(3, 24):
            lights[(px, y)] = "#6c757d"
            lights[(px + 1, y)] = "#495057"
    body.append(runs_to_paths(lights))
    lamps = {}
    for lx in (0, 233):
        for x in range(lx, lx + 7):
            for y in range(0, 3):
                lamps[(x, y)] = "#fff3b0"
    body.append(f'<g class="glow">{runs_to_paths(lamps)}</g>')
    body.append('<polygon points="0,3 7,3 60,80 0,80" fill="#fff3b0" fill-opacity="0.05"/>'
                '<polygon points="233,3 240,3 240,80 180,80" fill="#fff3b0" fill-opacity="0.05"/>')
    css.append("@keyframes glow{0%,100%{opacity:1}50%{opacity:.8}}.glow{animation:glow 1.6s ease-in-out infinite}")

    # --- scoreboard ------------------------------------------------------------
    board = {}
    for x in range(84, 157):
        for y in range(0, 10):
            edge = x in (84, 156) or y in (0, 9)
            board[(x, y)] = "#495057" if edge else "#000000"
    body.append(runs_to_paths(board))
    amber = "#ffb703"
    left, w_left = text_pixels("DD ", FONT3, 96, 3, amber)
    score_x = 96 + w_left + 1
    right, _ = text_pixels("-0 LEGACY", FONT3, score_x + 4, 3, amber)
    body.append(runs_to_paths({**left, **right}))
    zero, _ = text_pixels("0", FONT3, score_x, 3, amber)
    one, _ = text_pixels("1", FONT3, score_x, 3, "#ffd166")
    body.append(f'<g class="s0">{runs_to_paths(zero)}</g><g class="s1" style="opacity:0">{runs_to_paths(one)}</g>')
    body.append('<rect x="88" y="4" width="2" height="2" fill="#ff3b30" class="live"/>')
    css.append(show("s0", 0, 68) + f".s0{{animation:s0 {LOOP}s infinite}}"
               + show("s1", 68, 100) + f".s1{{animation:s1 {LOOP}s infinite}}"
               "@keyframes live{0%,49%{opacity:1}50%,100%{opacity:.15}}.live{animation:live 1s steps(1) infinite}")

    # --- LED ad board with scrolling ticker --------------------------------------
    led = {(x, y): ("#2b2b2b" if y in (24, 31) else "#0d0d0d") for x in range(W) for y in range(24, 32)}
    body.append(runs_to_paths(led))
    tw = text_width(TICKER, FONT3) + 1
    t1, _ = text_pixels(TICKER, FONT3, 0, 26, "#00f5d4")
    t2, _ = text_pixels(TICKER, FONT3, tw, 26, "#00f5d4")
    body.append(f'<clipPath id="ledclip"><rect x="0" y="25" width="{W}" height="6"/></clipPath>'
                f'<g clip-path="url(#ledclip)"><g class="ticker">{runs_to_paths({**t1, **t2})}</g></g>')
    css.append(f"@keyframes ticker{{from{{transform:translateX(0)}}to{{transform:translateX(-{tw}px)}}}}"
               f".ticker{{animation:ticker {tw / 16:.1f}s steps({tw}) infinite}}")

    # --- pitch -----------------------------------------------------------------
    pitch = {}
    for y in range(32, H):
        for x in range(W):
            pitch[(x, y)] = "#2f7d32" if (x // 24) % 2 == 0 else "#388e3c"
    for _ in range(140):
        pitch[(rnd.randrange(W), rnd.randrange(34, H))] = "#2a6f2d"
    line = "#e9f5e9"
    for x in range(W):
        pitch[(x, 33)] = line
        pitch[(x, 78)] = line
    for y in range(33, 79):
        pitch[(40, y)] = line
        pitch[(196, y)] = line
    for x in range(196, W):
        pitch[(x, 41)] = line
        pitch[(x, 74)] = line
    body.append(runs_to_paths(pitch))

    # --- goal: net behind the action, frame in front --------------------------------
    net = {(x, y): "#e0e0e0" for x in range(226, 239) for y in range(48, 71) if (x + y) % 2 == 0}
    body.append(f'<g class="net"><g fill-opacity="0.6">{runs_to_paths(net)}</g></g>')
    frame = {}
    for y in range(46, 71):
        frame[(224, y)] = "#ffffff"
        frame[(225, y)] = "#dee2e6"
        frame[(238, y)] = "#adb5bd"
    for x in range(224, 240):
        frame[(x, 46)] = "#ffffff"
        frame[(x, 47)] = "#dee2e6"
    net_keys = "".join(f"{p}%{{transform:translateX({dx}px)}}"
                       for p, dx in [(68, 2), (69.5, 0), (71, 1), (72.5, 0)])
    css.append(f"@keyframes net{{0%,67.9%{{transform:translateX(0)}}{net_keys}100%{{transform:translateX(0)}}}}"
               f".net{{animation:net {LOOP}s steps(1) infinite}}")

    # --- action layer: player, ball, keeper -----------------------------------------
    action = []
    start_x, kick_x = 8, 170
    top = GROUND - 15
    ball_a, ball_b = sprite(BALL_A, BALL), sprite(BALL_B, BALL)
    spin = f'<g class="fa">{ball_a}</g><g class="fb" style="opacity:0">{ball_b}</g>'
    shadow = '<rect x="0" y="0" width="4" height="1" fill="#1b4332" fill-opacity="0.7"/>'

    # keeper (behind the shot so the ball flies over him)
    action.append(
        f'<g transform="translate(212,{top})"><g class="kstand"><g class="sway">{sprite(KEEPER_STAND, KEEPER)}</g></g></g>'
        f'<g transform="translate(196,{GROUND - 5})"><g class="kdive" style="opacity:0">{sprite(KEEPER_DIVE, KEEPER)}</g></g>')
    css.append(show("kstand", 0, 59) + f".kstand{{animation:kstand {LOOP}s infinite}}"
               "@keyframes sway{0%,49%{transform:translateX(0)}50%,100%{transform:translateX(-1px)}}"
               ".sway{animation:sway .9s steps(1) infinite}"
               "@keyframes kdive{0%,58.99%{opacity:0;transform:translate(14px,-9px)}"
               "59%{opacity:1;transform:translate(14px,-9px);animation-timing-function:steps(4)}"
               "63%,94%{opacity:1;transform:translate(0,0)}94.01%,100%{opacity:0}}"
               f".kdive{{animation:kdive {LOOP}s infinite}}")

    # player + dribbled ball move together until the kick
    player = (
        f'<g class="prun">'
        f'<g class="fa">{sprite(RUN_A, KIT)}</g><g class="fb" style="opacity:0">{sprite(RUN_B, KIT)}</g>'
        f'<g transform="translate(12,{GROUND - top})"><g class="tapx">{shadow}</g></g>'
        f'<g transform="translate(12,11)"><g class="tap">{spin}</g></g>'
        f'</g>'
        f'<g class="pkick" style="opacity:0">{sprite(KICK, KIT)}</g>'
        f'<g class="pcele" style="opacity:0"><g class="hop">{sprite(CELEBRATE, KIT)}</g></g>'
    )
    action.append(f'<g transform="translate({start_x},{top})"><g class="pmove">{player}</g></g>')
    travel = kick_x - start_x
    css.append(
        f"@keyframes pmove{{0%{{transform:translateX(0);animation-timing-function:steps({travel})}}"
        f"55%,100%{{transform:translateX({travel}px)}}}}.pmove{{animation:pmove {LOOP}s infinite}}"
        + show("prun", 0, 55) + f".prun{{animation:prun {LOOP}s infinite}}"
        + show("pkick", 55, 68) + f".pkick{{animation:pkick {LOOP}s infinite}}"
        + show("pcele", 68, 94) + f".pcele{{animation:pcele {LOOP}s infinite}}"
        "@keyframes fa{0%,49.9%{opacity:1}50%,100%{opacity:0}}@keyframes fb{0%,49.9%{opacity:0}50%,100%{opacity:1}}"
        ".prun .fa,.prun .fb{animation-duration:.32s}"
        ".fa{animation:fa .16s steps(1) infinite}.fb{animation:fb .16s steps(1) infinite}"
        "@keyframes tap{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-1px)}}"
        ".tap{animation:tap .48s steps(3) infinite}"
        "@keyframes tapx{0%,100%{transform:translateX(0)}50%{transform:translateX(3px)}}"
        ".tapx{animation:tapx .48s steps(3) infinite}"
        "@keyframes hop{0%,49%{transform:translateY(0)}50%,100%{transform:translateY(-3px)}}"
        ".hop{animation:hop .36s steps(1) infinite}")

    # the shot: ball flies from the boot into the top of the net, then drops
    bx, by = kick_x + 12, GROUND - 4
    path = [(55.5, 0, 0), (59, 12, -9), (62, 24, -15), (65, 36, -16), (68, 46, -13),
            (70, 48, -12), (73, 48, -5), (75, 47, 0)]
    keys = "".join(f"{p}%{{opacity:1;transform:translate({x}px,{y}px);animation-timing-function:steps(6)}}"
                   for p, x, y in path)
    sx = "".join(f"{p}%{{opacity:1;transform:translateX({x}px);animation-timing-function:steps(6)}}" for p, x, _ in path)
    action.append(
        f'<g transform="translate({bx},{GROUND})"><g class="shotshadow" style="opacity:0">{shadow}</g></g>'
        f'<g transform="translate({bx},{by})"><g class="shot" style="opacity:0">{spin}</g></g>')
    css.append(
        f"@keyframes shot{{0%,55.49%{{opacity:0;transform:translate(0,0)}}{keys}"
        f"75.01%,94%{{opacity:1;transform:translate(47px,0)}}94.01%,100%{{opacity:0;transform:translate(47px,0)}}}}"
        f".shot{{animation:shot {LOOP}s infinite}}"
        f"@keyframes shotshadow{{0%,55.49%{{opacity:0;transform:translateX(0)}}{sx}"
        f"75.01%,94%{{opacity:1;transform:translateX(47px)}}94.01%,100%{{opacity:0}}}}"
        f".shotshadow{{animation:shotshadow {LOOP}s infinite}}"
        ".shot .fa,.shot .fb{animation-duration:.12s}")

    body.append(f'<g class="action">{"".join(action)}</g>')
    css.append("@keyframes action{0%{opacity:0}2%,94%{opacity:1}98%,100%{opacity:0}}"
               f".action{{animation:action {LOOP}s infinite}}")
    body.append(runs_to_paths(frame))

    # --- GOAL! and confetti ---------------------------------------------------------
    gw = text_width("GOAL!", FONT5, 2)
    gx, gy = (W - gw) // 2, 37
    shade, _ = text_pixels("GOAL!", FONT5, gx + 1, gy + 1, "#7a1c00", 2)
    gold, _ = text_pixels("GOAL!", FONT5, gx, gy, "#ffd166", 2)
    confetti = "".join(
        f'<rect x="{rnd.randrange(50, 200)}" y="34" width="{rnd.choice([1, 2])}" height="1" '
        f'fill="{rnd.choice(shirts)}" class="fall" style="animation-delay:-{rnd.uniform(0, 1.4):.2f}s"/>'
        for _ in range(28))
    body.append(f'<g class="goal" style="opacity:0"><g class="blink">{runs_to_paths(shade)}{runs_to_paths(gold)}</g>'
                f'{confetti}</g>')
    css.append(show("goal", 68, 92) + f".goal{{animation:goal {LOOP}s infinite}}"
               "@keyframes blink{0%,64%{opacity:1}65%,100%{opacity:0}}.blink{animation:blink .4s steps(1) infinite}"
               "@keyframes fall{from{transform:translateY(0)}to{transform:translateY(36px)}}"
               ".fall{animation:fall 1.4s steps(18) infinite}")

    css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W * SCALE}" height="{H * SCALE}" '
        f'shape-rendering="crispEdges" role="img" aria-labelledby="t d">'
        f'<title id="t">definitelynotDD scores against Legacy Code</title>'
        f'<desc id="d">Animated pixel-art football scene: a player dribbles across a floodlit pitch, shoots past '
        f'a diving keeper into the net, the crowd jumps and the scoreboard changes from DD 0-0 LEGACY to DD 1-0 LEGACY.</desc>'
        f'<style>{"".join(css)}</style>'
        f'{"".join(body)}</svg>\n'
    )
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT} ({len(svg) / 1024:.1f} KB)")


if __name__ == "__main__":
    build()
