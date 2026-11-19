#!/usr/bin/env python3
"""Render poster.png for make.fun news-image-20261119.

A one-page newspaper front page, "THE WORLD TODAY", summing up the
world news of Thursday 19 November 2026. Everything on the page was
checked against same-day roundups (One Turn, SimpleLife, Reuters via
TBS / The Leaders / Khabarwire, BBC via several outlets, Pollar and
The News Booth on the ICJ) before drawing; nothing here is invented.
The ICJ ruling is due today at 10:00 in The Hague, so the poster says
only that the court rules today — it claims no outcome.

Deterministic: fixed DejaVu fonts, fixed geometry, no clock, no
randomness, no network. Run it twice and poster.png is byte-identical.

    python3 build_poster.py            # writes poster.png next to this file
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "poster.png"

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (60, 58, 52)
SEA = (196, 216, 228)
LAND = (232, 222, 196)
PANEL = (255, 255, 255)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_REG = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int) -> list[str]:
    """Greedy word wrap to the given pixel width."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def para(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, fnt,
         width: int, leading: int, fill=INK) -> int:
    """Draw a wrapped paragraph; return the y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw: ImageDraw.ImageDraw, x0: int, y: int, x1: int, w: int = 2) -> None:
    draw.line([(x0, y), (x1, y)], fill=RULE, width=w)


def kicker(draw: ImageDraw.ImageDraw, x: int, y: int, text: str) -> int:
    fnt = font(SANS_B, 15)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + 22


def draw_masthead(draw: ImageDraw.ImageDraw) -> None:
    top = font(SANS_B, 16)
    draw.text((36, 26), "THURSDAY  ·  19 NOVEMBER 2026", font=top, fill=INK)
    right = "No. 323  ·  ONE IMAGE, ONE DAY"
    draw.text((W - 36 - draw.textlength(right, font=top), 26), right,
              font=top, fill=GREY)
    rule(draw, 36, 54, W - 36, 3)
    mast = font(SERIF, 74)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=mast)
    draw.text(((W - tw) / 2, 62), title, font=mast, fill=INK)
    sub = font(SANS, 17)
    line = "The day's world news, in one page  —  Shenzhen  ·  The Gulf  ·  The Hague"
    draw.text(((W - draw.textlength(line, font=sub)) / 2, 168), line,
              font=sub, fill=GREY)
    rule(draw, 36, 198, W - 36, 4)
    rule(draw, 36, 204, W - 36, 1)


def draw_table_diagram(draw: ImageDraw.ImageDraw, x: int, y: int,
                       w: int, h: int) -> None:
    """Three leaders around one round table: US, China, Russia.

    Names sit inside the circles; one caption line at the bottom of
    the panel names the meeting, so no label ever touches a circle.
    """
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2, fill=PANEL)
    cx, cy = x + w // 2, y + 100
    draw.ellipse([cx - 50, cy - 38, cx + 50, cy + 38], fill=LAND,
                 outline=RULE, width=2)
    spots = [
        (cx, cy - 68, "XI"),
        (cx - 76, cy + 44, "TRUMP"),
        (cx + 76, cy + 44, "PUTIN"),
    ]
    for sx, sy, name in spots:
        draw.ellipse([sx - 22, sy - 22, sx + 22, sy + 22], fill=RED,
                     outline=INK, width=2)
        fnt = font(SANS_B, 10)
        draw.text((sx - draw.textlength(name, font=fnt) / 2, sy - 5),
                  name, font=fnt, fill=(255, 255, 255))
    cap = font(SANS_B, 11)
    label = "XI  ·  TRUMP  ·  PUTIN — FIRST-EVER TRILATERAL"
    draw.text((x + (w - draw.textlength(label, font=cap)) / 2, y + h - 20),
              label, font=cap, fill=RED)


def draw_lead(draw: ImageDraw.ImageDraw) -> None:
    y = kicker(draw, 36, 216, "SHENZHEN  ·  APEC SUMMIT")
    head = font(SERIF, 44)
    draw.text((36, y), "THREE AT ONE TABLE", font=head, fill=INK)
    deck = ("Trump, Xi and Putin meet today in the first-ever "
            "three-way summit of the three nuclear powers — "
            "nuclear arms, the Iran war and trade on the table, "
            "with New START already lapsed.")
    y = para(draw, 36, 308, deck, font(SERIF_REG, 20), 560, 27)
    draw.text((36, 420),
              "No deal is expected; the photo is the message.",
              font=font(SANS_B, 16), fill=GREY)
    draw_table_diagram(draw, 640, 224, 348, 196)


def draw_gulf_map(draw: ImageDraw.ImageDraw, x: int, y: int,
                  w: int, h: int) -> None:
    """Schematic Strait of Hormuz: Iran above, Gulf below, Qeshm, Bahrain,
    Kuwait, and the tanker struck near Khasab."""
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2, fill=SEA)
    # Iran landmass (top) and Arabian peninsula (bottom).
    draw.polygon([(x, y), (x + w, y), (x + w, y + 62), (x + 210, y + 74),
                  (x + 150, y + 40), (x, y + 52)], fill=LAND, outline=RULE)
    draw.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 58),
                  (x + 260, y + h - 70), (x + 190, y + h - 34), (x, y + h - 44)],
                 fill=LAND, outline=RULE)
    lbl = font(SANS_B, 13)
    draw.text((x + 14, y + 8), "IRAN", font=lbl, fill=INK)
    draw.text((x + 18, y + h - 24), "ARABIA", font=lbl, fill=INK)
    # Qeshm Island.
    draw.ellipse([x + 218, y + 78, x + 262, y + 92], fill=RED, outline=INK)
    draw.text((x + 200, y + 96), "QESHM", font=font(SANS_B, 11), fill=INK)
    # Bahrain and Kuwait dots. Bahrain's label goes to the LEFT of its
    # dot so it never reaches the tanker marker at the right edge.
    for dx, dy, name in [(288, 128, "BAHRAIN"), (96, 118, "KUWAIT")]:
        draw.ellipse([x + dx - 6, y + dy - 6, x + dx + 6, y + dy + 6],
                     fill=RED, outline=INK, width=2)
        if name == "BAHRAIN":
            draw.text((x + dx - 10 - draw.textlength(name, font=font(SANS_B, 11)),
                       y + dy - 7), name, font=font(SANS_B, 11), fill=INK)
        else:
            draw.text((x + dx + 10, y + dy - 7), name, font=font(SANS_B, 11),
                      fill=INK)
    # Drone arcs from Iran toward Bahrain and Kuwait.
    draw.arc([x + 150, y + 30, x + 330, y + 150], 20, 160, fill=RED, width=2)
    draw.arc([x + 40, y + 20, x + 180, y + 130], 200, 340, fill=RED, width=2)
    # Tanker struck near Khasab (bottom-right, mouth of the strait).
    tx, ty = x + w - 44, y + h - 56
    draw.rectangle([tx - 16, ty - 5, tx + 16, ty + 5], fill=INK)
    draw.line([(tx, ty - 5), (tx, ty - 18)], fill=INK, width=2)
    draw.text((tx - 24, ty + 10), "TANKER HIT", font=font(SANS_B, 10),
              fill=RED)
    draw.text((x + 8, y + h - 40), "STRAIT OF HORMUZ", font=font(SANS_B, 11),
              fill=GREY)


def draw_gulf(draw: ImageDraw.ImageDraw) -> None:
    rule(draw, 36, 440, W - 36, 2)
    y = kicker(draw, 36, 452, "THE GULF  ·  WAR WIDENS")
    head = font(SERIF, 40)
    draw.text((36, y), "IRAN HITS KUWAIT", font=head, fill=INK)
    draw.text((36, y + 46), "AND BAHRAIN", font=head, fill=INK)
    body = ("Tehran's drones hit a U.S. base at Ali Al Salem "
            "in Kuwait and sites in Bahrain overnight — its "
            "answer to U.S. jets striking a missile site on "
            "Qeshm Island on Tuesday. A tanker was hit near "
            "Khasab; a Houthi missile aimed at Saudi Arabia "
            "was intercepted.")
    para(draw, 36, 574, body, font(SERIF_REG, 18), 560, 24)
    draw_gulf_map(draw, 640, 452, 348, 208)


def draw_middle(draw: ImageDraw.ImageDraw) -> None:
    rule(draw, 36, 700, W - 36, 2)
    # Left: Kerch Bridge.
    y = kicker(draw, 36, 712, "UKRAINE  ·  KERCH STRAIT")
    draw.text((36, y), "BRIDGE HIT A THIRD TIME", font=font(SERIF, 26), fill=INK)
    para(draw, 36, 768,
         "Ukraine struck the Crimean Bridge again overnight — "
         "the third attack this week. Rail traffic is halted "
         "while damage is assessed; a 227-metre road span "
         "fell into the strait on Tuesday.",
         font(SERIF_REG, 16), 452, 21)
    # Divider.
    draw.line([(512, 712), (512, 852)], fill=RULE, width=1)
    # Right: Gaza.
    y2 = kicker(draw, 540, 712, "GAZA  ·  CEASEFIRE TESTED")
    draw.text((540, y2), "TANKS CROSS THE LINE", font=font(SERIF, 26), fill=INK)
    para(draw, 540, 768,
         "Israeli tanks pushed into central Gaza on Wednesday, "
         "the first ground raid across the ceasefire line "
         "since the October 2025 truce. Israel says it hit a "
         "tunnel; Hamas calls it a breach.",
         font(SERIF_REG, 16), 448, 21)


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    rule(draw, 36, 864, W - 36, 2)
    boxes = [
        ("THE HAGUE", "ICJ rules today",
         "World court decides if Myanmar committed genocide."),
        ("MARKETS", "Anthropic: $83 a share",
         "Record AI IPO priced above range; shares trade Friday."),
        ("ASIA", "N. Korea enriches more",
         "IAEA: Pyongyang expanded uranium enrichment."),
        ("TRADE", "EU–Indonesia pact",
         "EU approves trade deal to blunt U.S. tariffs."),
    ]
    bw, gap = 220, 12
    x = 36
    for tag, head, body in boxes:
        draw.rectangle([x, 876, x + bw, 876 + 70], outline=RULE, width=1,
                       fill=PANEL)
        draw.text((x + 8, 880), tag, font=font(SANS_B, 11), fill=RED)
        draw.text((x + 8, 896), head, font=font(SANS_B, 13), fill=INK)
        para(draw, x + 8, 914, body, font(SANS, 11), bw - 16, 13)
        x += bw + gap


def draw_footer(draw: ImageDraw.ImageDraw) -> None:
    rule(draw, 36, 958, W - 36, 1)
    foot = font(SANS, 13)
    line = ("Also: Cyclone Akvan nears Odisha  ·  U.S. and Venezuela restore "
            "military ties  ·  Suneung exam under AI-cheating curbs")
    draw.text((36, 968), line, font=foot, fill=GREY)


def render() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_gulf(draw)
    draw_middle(draw)
    draw_grid(draw)
    draw_footer(draw)
    return img


def main() -> None:
    render().save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
