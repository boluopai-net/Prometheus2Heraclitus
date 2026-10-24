#!/usr/bin/env python3
"""Render bilingual illustrated maps and a captioned comic for their actual readers."""

import base64
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "references/diagrams"
H = html.escape
STYLE = """
:root{--paper:#fff;--ink:#293537;--muted:#657575;--line:#698b89;--water:#245f64;--pale:#edf5f3;--fire:#a54d2c;--warm:#fff3e8;color-scheme:light}
@media(prefers-color-scheme:dark){:root{--paper:#171e20;--ink:#e5eceb;--muted:#abb9b8;--line:#80a9a3;--water:#a1d8d0;--pale:#233a38;--fire:#edb18e;--warm:#3e2d25;color-scheme:dark}}
:root[data-theme=light]{--paper:#fff;--ink:#293537;--muted:#657575;--line:#698b89;--water:#245f64;--pale:#edf5f3;--fire:#a54d2c;--warm:#fff3e8;color-scheme:light}
:root[data-theme=dark]{--paper:#171e20;--ink:#e5eceb;--muted:#abb9b8;--line:#80a9a3;--water:#a1d8d0;--pale:#233a38;--fire:#edb18e;--warm:#3e2d25;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif}
main{max-width:1100px;margin:auto;padding:24px 12px}h1{font-size:clamp(26px,3.4vw,40px);line-height:1.4;margin:0 0 20px;text-align:center;font-weight:500}
svg{display:block;width:100%;height:auto;overflow:visible;font-family:inherit}svg text{font-family:inherit}.desktop svg{max-height:740px}.mobile{display:none}.embedded h1{display:none}.embedded main{padding:0}
@media(max-width:700px){.desktop{display:none}.mobile{display:block}main{padding:20px 0}h1{padding-inline:16px}}
:root{--gold:#9b7433}@media(prefers-color-scheme:dark){:root{--gold:#d7b26c}}:root[data-theme=light]{--gold:#9b7433}:root[data-theme=dark]{--gold:#d7b26c}
"""


def text(x, y, lines, size=26, color="ink", weight=400):
    if isinstance(lines, str):
        lines = [lines]
    start = y - (len(lines) - 1) * size * 0.68
    spans = "".join(
        f'<tspan x="{x}" y="{start + i * size * 1.36:.1f}">{H(s)}</tspan>'
        for i, s in enumerate(lines)
    )
    return f'<text text-anchor="middle" dominant-baseline="middle" fill="var(--{color})" font-size="{size}" font-weight="{weight}">{spans}</text>'


def label(x, y, value, size=20, color="muted"):
    units = sum(1 if ord(c) > 255 else 0.54 for c in value)
    w = max(36, units * size + 20)
    return (
        f'<rect x="{x - w / 2:.1f}" y="{y - size * 0.68:.1f}" width="{w:.1f}" height="{size * 1.36:.1f}" rx="5" fill="var(--paper)"/>'
        + text(x, y, value, size, color)
    )


def edge(path, prefix, color="water", dashed=False):
    return (
        f'<path d="{path}" fill="none" stroke="var(--{color})" stroke-width="2.3" '
        + ('stroke-dasharray="6 7" ' if dashed else "")
        + f'marker-end="url(#{prefix}-{color})"/>'
    )


def flame(x, y, scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})"><path d="M0 24C-35 12-32-14-13-34C-9-11 5-17 3-52C42-15 41 15 12 24C20 5 8-2 3-13C2 4-9 7 0 24Z" fill="var(--fire)" opacity=".16"/><path d="M0 24C-35 12-32-14-13-34C-9-11 5-17 3-52C42-15 41 15 12 24" fill="none" stroke="var(--fire)" stroke-width="1.8"/></g>'


def art(body, x, y, scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})" stroke-linecap="round" stroke-linejoin="round">{body}</g>'


def line(path, color="line", width=2, fill="none"):
    return f'<path d="{path}" fill="{fill if fill == "none" else "var(--" + fill + ")"}" stroke="var(--{color})" stroke-width="{width}"/>'


def little_person(x, y, scale=1, moon=False):
    if moon:
        body = line(
            "M8-42C-32-47-43-5-15 14C-6 20 7 19 18 14C-11 12-19-18 8-42Z", "water", 2.5, "pale"
        )
        body += line("M-18 20Q-43 43-28 74H26Q39 43 11 20", "water", 2.5, "pale")
        body += line("M-24 39Q-42 39-50 29M20 39Q41 37 49 26", "water", 2.5)
        body += '<circle cx="-10" cy="-9" r="2" fill="var(--water)"/>'
    else:
        body = flame(0, -20, 0.62)
        body += line(
            "M-14 6Q-31 23-22 40L-29 75H-7L0 52L8 75H30L23 40Q33 23 15 6", "fire", 2.5, "warm"
        )
        body += line("M-22 23Q-43 27-48 13M23 23Q45 27 49 12", "fire", 2.5)
        body += '<circle cx="-7" cy="-20" r="2" fill="var(--fire)"/><circle cx="8" cy="-20" r="2" fill="var(--fire)"/>'
    return art(body, x, y, scale)


def footprints(x, y, scale=1):
    body = line("M-65 42Q-18 12-38-13T15-54T62-76", "line", 12)
    for px, py, angle in [(-48, 26, 35), (-23, 4, -15), (-26, -25, 5), (2, -43, 40), (32, -53, 60)]:
        body += f'<ellipse cx="{px}" cy="{py}" rx="5" ry="10" transform="rotate({angle} {px} {py})" fill="var(--fire)"/>'
    body += line("M-78 51H72M-67 60H64", "line", 1.5)
    return art(body, x, y, scale)


def mirror(x, y, scale=1):
    body = '<ellipse cx="0" cy="-22" rx="60" ry="53" fill="var(--pale)" stroke="var(--water)" stroke-width="2.5"/>'
    body += line("M-49-21Q-41-62-2-63M8-8L31-31M-11 6L25-30", "line", 2)
    body += flame(1, -17, 0.6)
    body += line("M-12 31V48H-42L-56 58H56L42 48H12V31", "water", 2, "pale")
    return art(body, x, y, scale)


def scroll(x, y, scale=1):
    body = line("M-86-72H67Q88-72 88-52V68H-67Q-88 68-88 49V-49Q-88-69-68-69", "fire", 2, "warm")
    body += line(
        "M-86-72Q-105-72-105-53Q-105-34-86-34H-76M67-72Q48-72 48-53Q48-34 67-34H88M-67 68Q-88 68-88 49Q-88 30-67 30H-58",
        "fire",
        2,
    )
    body += line("M-54-47H24M-54-38H10", "line", 1)
    return art(body, x, y, scale)


def garden(x, y, scale=1):
    body = line("M-100 54Q-45 42 0 50T106 51", "water", 2)
    body += line("M-61 42V-11L-25-41L12-11V42Z", "water", 2, "pale")
    body += line("M-73-8L-25-49L24-8M-35 42V9H-13V42M-50-8H-36V3H-50Z", "water", 2)
    body += line(
        "M44 46V-13M44 13Q8-2 23-22Q48-20 44 13M45-4Q78-31 86-6Q71 16 45 16", "water", 2, "pale"
    )
    body += line("M-99 43V10M-99 25Q-124 9-111-1Q-94 7-99 25", "line", 2, "pale")
    body += line("M5 43L24 29L40 43L24 55Z", "fire", 1.5, "warm")
    return art(body, x, y, scale)


def temple(w, top, base):
    c = w / 2
    left, right = 30, w - 30
    body = line(
        f"M{left} {top + 104}Q{c - 180} {top + 92} {c} {top}Q{c + 180} {top + 92} {right} {top + 104}L{right - 17} {top + 122}H{left + 17}Z",
        "fire",
        2.2,
        "warm",
    )
    body += line(
        f"M{left + 36} {top + 95}H{right - 36}M{c - 35} {top + 41}Q{c} {top + 20} {c + 35} {top + 41}",
        "fire",
        1.5,
    )
    for x in [left + 17, right - 41]:
        body += line(
            f"M{x} {top + 131}H{x + 24}V{base - 31}H{x}ZM{x - 8} {top + 125}H{x + 32}V{top + 136}H{x - 8}ZM{x - 9} {base - 31}H{x + 33}V{base - 18}H{x - 9}Z",
            "line",
            1.4,
            "pale",
        )
    body += line(
        f"M{left - 5} {base - 16}H{right + 5}V{base}H{left - 5}ZM{left - 18} {base}H{right + 18}V{base + 15}H{left - 18}Z",
        "line",
        1.5,
        "pale",
    )
    return body


def formation(d, lang, mobile, p):
    w, h = (600, 1080) if mobile else (900, 980)
    cx, cy = w / 2, 542 if mobile else 510
    lx, rx = (145, 455) if mobile else (225, 675)
    ty, by = (325, 805) if mobile else (310, 750)
    small = 0.84 if mobile else 1
    size = 22 if mobile else 26
    e = {k: v[lang] for k, v in d["edges"].items()}
    n = d["nodes"]
    drawn = temple(w, 103, h - 104)
    drawn += text(cx, 47 if lang else 36, d["purpose"][lang], 23 if mobile else 28, "fire", 500)
    # The roof and open colonnade frame one shared practice; paths remain directed.
    drawn += edge(f"M{cx - 64} {cy - 7}Q{lx + 100} {cy - 55} {lx + 68} {ty + 52}", p)
    drawn += edge(f"M{lx + 77} {ty - 16}H{rx - 77}", p)
    drawn += edge(f"M{rx + 61} {ty + 146}Q{rx + 110} {(ty + by) / 2} {rx + 66} {by - 90}", p)
    drawn += edge(f"M{rx - 66} {by + 99}H{lx + 70}", p)
    drawn += edge(f"M{lx + 69} {by - 38}Q{cx - 104} {cy + 124} {cx - 63} {cy + 45}", p)
    drawn += edge(f"M{rx - 111} {ty + 69}Q{cx + 77} {cy - 73} {cx + 61} {cy - 16}", p, "fire", True)
    drawn += edge(
        f"M{lx - 66} {by - 46}Q{lx - 123} {(ty + by) / 2} {lx - 48} {ty + 80}", p, "fire", True
    )
    drawn += footprints(lx, ty - 3, small)
    drawn += text(lx, ty + 83, n["trajectory"][lang], size if not lang else 21, "water", 500)
    drawn += mirror(rx, ty, small)
    drawn += text(rx, ty + 110, n["reflection"][lang], 21 if lang else size, "water", 500)
    drawn += scroll(rx, by - 5)
    drawn += text(rx, by + 4, n["formation"][lang], 17 if lang else 21, "ink", 500)
    drawn += garden(lx, by - 27, small)
    practice_label = (
        ["Environments", "& works", "New encounters"] if mobile and lang else n["practice"][lang]
    )
    drawn += text(lx, by + 66, practice_label, 20 if lang else size, "water", 500)
    # Two answering figures share the altar rather than occupy a hierarchy.
    drawn += flame(cx, cy - 73, 0.8)
    drawn += little_person(cx - 48, cy - 5, 0.72)
    drawn += little_person(cx + 48, cy - 5, 0.72, True)
    drawn += line(
        f"M{cx - 103} {cy + 55}H{cx + 103}L{cx + 90} {cy + 70}H{cx - 90}ZM{cx - 75} {cy + 70}V{cy + 145}H{cx + 75}V{cy + 70}",
        "fire",
        2,
        "warm",
    )
    drawn += text(cx, cy + 104, n["center"][lang], 19 if lang else 24, "ink", 500)
    for x, y, key, color in [
        (cx - 104, cy - 53, "record", "muted"),
        (cx, ty - 38, "reflect", "muted"),
        (w - 89, (ty + by) / 2, "articulate", "muted"),
        (cx, by + 120, "realize", "muted"),
        (cx - 92, cy + 179, "use", "muted"),
        (cx + 112 if mobile else cx + 99, cy - 46 if mobile else cy - 76, "revise", "fire"),
        (85, (ty + by) / 2 + 36, "experience", "fire"),
    ]:
        drawn += label(x, y, e[key], 16 if lang else 19, color)
    note = (
        ["New experience can also change", "the original developmental aim."]
        if lang
        else ["新的经验，也会改变", "最初的培养方向。"]
        if mobile
        else d["note"][lang]
    )
    drawn += text(cx, h - 39, note, 18 if lang else 22, "muted")
    return w, h, drawn


def collective_fire(x, y, scale=1):
    body = ""
    for px, py, s in [(-55, 1, 0.48), (0, -19, 0.7), (57, 0, 0.48)]:
        body += flame(px, py, s)
    body += line(
        "M-88 31Q-61 55-30 43L-8 33M88 31Q61 55 30 43L8 33M-84 45Q-45 77 0 56Q45 77 84 45",
        "fire",
        2,
    )
    body += line("M-29 69L-9 62L14 71L34 63V88L14 96L-9 87L-29 95Z", "line", 1.5, "pale")
    return art(body, x, y, scale)


def lotus(x, y, scale=1):
    body = line("M0 24C-59 21-105-31-113-88C-49-84-8-43 0 24Z", "fire", 2.5, "warm")
    body += line("M0 24C59 21 105-31 113-88C49-84 8-43 0 24Z", "fire", 2.5, "warm")
    body += line("M0 29C-100 44-177-17-184-69C-111-80-39-44 0 29Z", "water", 2.5, "pale")
    body += line("M0 29C100 44 177-17 184-69C111-80 39-44 0 29Z", "water", 2.5, "pale")
    body += line("M0 35C-64-7-53-70 0-111C53-70 64-7 0 35Z", "fire", 2.5, "warm")
    body += line("M-169-15Q0 88 169-15Q143 96 0 105Q-143 96-169-15Z", "fire", 2.5, "warm")
    body += line("M-23 105V151Q-64 161-73 178H73Q64 161 23 151V105", "fire", 2.5, "warm")
    body += line("M-88 179H88V190H-88Z", "fire", 2, "warm")
    return art(body, x, y, scale)


def cultivation(d, lang, mobile, p):
    w, h = (600, 1180) if mobile else (1000, 1060)
    cx = w / 2
    lamp_y = 585 if mobile else 530
    cap_y = 340 if mobile else 268
    works_y = 925 if mobile else 825
    ax, ay = (cx, 70) if mobile else (160, 180)
    n = d["nodes"]
    e = {k: v[lang] for k, v in d["edges"].items()}
    drawn = ""
    # Fire-bringing feeds the lamp; cultivation and world feedback remain distinct.
    drawn += edge(
        f"M{ax - 74 if mobile else ax + 70} {ay + 101 if mobile else ay + 60}Q{72 if mobile else 230} {lamp_y - 185} {cx - 129} {lamp_y + 12}",
        p,
    )
    drawn += edge(f"M{cx} {lamp_y - 108}V{cap_y + 110}", p, "fire", True)
    drawn += edge(f"M{cx + 92} {cap_y + 43}Q{w - 74} {cap_y + 100} {cx + 141} {lamp_y + 9}", p)
    drawn += edge(f"M{cx} {lamp_y + 194}V{works_y - 66}", p)
    drawn += edge(
        f"M{cx - 119} {works_y - 4}Q{38 if mobile else 102} {works_y - 95} {cx - 174} {lamp_y + 63}",
        p,
    )
    drawn += edge(
        f"M{cx + 121} {works_y - 6}Q{w - 20} {works_y - 109} {w - 56} {cap_y + 159}Q{w - 58} {cap_y - 90} {cx + 70} {cap_y - 66}",
        p,
        "fire",
        True,
    )
    drawn += collective_fire(ax, ay - 21, 0.84 if mobile else 1)
    drawn += text(ax, ay + 101, n["collective"][lang], 22 if lang else 27, "fire", 500)
    # A small becoming person is the flame, not an inventory of delivered works.
    drawn += '<g opacity=".28">' + flame(cx, cap_y + 28, 2) + "</g>"
    drawn += little_person(cx, cap_y + 5, 1.17)
    drawn += text(cx, cap_y - 104, n["capacity"][lang][0], 26 if lang else 31, "fire", 500)
    capacity = n["capacity"][lang][1:]
    drawn += text(cx - 129, cap_y + 12, capacity[:2], 17 if lang else 22, "ink", 500)
    drawn += text(cx + 132, cap_y + 8, capacity[2:], 17 if lang else 22, "ink", 500)
    drawn += lotus(cx, lamp_y, 0.93 if mobile else 1.05)
    drawn += little_person(cx - 72, lamp_y - 62, 0.58)
    drawn += little_person(cx + 72, lamp_y - 62, 0.58, True)
    drawn += text(cx - 72, lamp_y + 1, n["person"][lang], 17 if lang else 22, "water", 500)
    drawn += text(cx + 72, lamp_y + 1, n["model"][lang], 17 if lang else 22, "water", 500)
    drawn += text(cx, lamp_y + 63, n["creation"][lang], 22 if lang else 27, "fire", 500)
    drawn += garden(cx, works_y - 7, 1.2)
    drawn += text(cx, works_y + 76, n["works"][lang], 23 if lang else 28, "water", 500)
    lab_positions = [
        (115 if mobile else 287, lamp_y - 176, "use", "muted"),
        (cx + 40, (lamp_y - 108 + cap_y + 110) / 2, "cultivate", "fire"),
        (w - 111 if mobile else cx + 235, lamp_y - 161, "continue", "muted"),
        (cx + 47, works_y - 85, "make", "muted"),
        (90 if mobile else cx - 236, lamp_y + 222, "response", "muted"),
        (w - 68 if mobile else cx + 355, lamp_y + 139, "support", "fire"),
    ]
    for x, y, key, color in lab_positions:
        drawn += label(x, y, e[key], 15 if lang else 19, color)
    note = (
        ["Cultivation also changes", "what we find worth creating."]
        if lang
        else ["培养也让我们重新理解，", "什么值得创造。"]
        if mobile
        else d["note"][lang]
    )
    drawn += text(cx, h - 90, note, 19 if lang else 23, "ink", 500)
    legend = (
        (
            ["Dashed: cultivation or support;", "examined through actual participation."]
            if mobile
            else "Dashed: cultivation or support, examined through actual participation."
        )
        if lang
        else (
            ["虚线表示培养或支持的关系，", "效果由实际参与检验。"]
            if mobile
            else "虚线表示培养或支持的关系，效果由实际参与检验。"
        )
    )
    drawn += text(cx, h - 31, legend, 16 if lang else 18, "muted")
    return w, h, drawn


def comic_panel(index, panel, lang, p):
    drawn = '<rect x="0" y="0" width="600" height="520" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.2"/>'
    drawn += '<circle cx="29" cy="29" r="16" fill="var(--warm)" stroke="var(--fire)" stroke-width="1.3"/>'
    drawn += text(29, 29, str(index + 1), 19, "fire", 500)
    drawn += text(315, 37, panel["title"][lang], 23 if lang else 26, "ink", 500)
    drawn += text(300, 105, panel["kicker"][lang], 17 if lang else 20, "water", 500)
    # Crop the four unchanged atlas quadrants in the viewer, not in the bitmap.
    drawn += (
        f'<svg aria-hidden="true" x="20" y="140" width="560" height="280" viewBox="{index % 2 * 1000} {index // 2 * 500} 1000 500" style="width:560px;height:280px;overflow:hidden">'
        f'<use href="#{p}-art"/></svg>'
    )
    drawn += text(300, 475, panel["caption"][lang], 19 if lang else 22, "ink")
    return drawn


def trinity_sinthome(d, lang, mobile, p):
    w, h = (624, 2252) if mobile else (1256, 1164)
    body = ""
    for i, panel in enumerate(d["panels"]):
        x, y = (12, 12 + i * 544) if mobile else (12 + (i % 2) * 632, 12 + (i // 2) * 544)
        body += art(comic_panel(i, panel, lang, p), x, y).replace(
            "<g ", f'<g data-comic-panel="{i + 1}" ', 1
        )
    body += text(w / 2, h - 43, d["legend"][lang], 17 if lang else 20, "muted")
    return w, h, body


def svg(name, d, lang, mobile=False, standalone=False):
    p = name + ("-mobile" if mobile else "-desktop")
    layouts = {
        "formation-path": formation,
        "borrowed-fire": cultivation,
        "trinity-sinthome": trinity_sinthome,
    }
    w, h, body = layouts[name](d, lang, mobile, p)
    markers = "".join(
        f'<marker id="{p}-{c}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L8 4L0 8" fill="none" stroke="var(--{c})" stroke-width="1.5"/></marker>'
        for c in ["water", "fire"]
    )
    if name == "trinity-sinthome":
        atlas = "trinity-sinthome-art.png"
        if standalone:
            atlas = "data:image/png;base64," + base64.b64encode((ROOT / atlas).read_bytes()).decode(
                "ascii"
            )
        markers += f'<image id="{p}-art" width="2000" height="1000" href="{atlas}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{p}-title {p}-desc" viewBox="0 0 {w} {h}"><title id="{p}-title">{H(d["title"][lang])}</title><desc id="{p}-desc">{H(d["description"][lang])}</desc><style>{STYLE}</style><defs>{markers}</defs><rect width="{w}" height="{h}" fill="var(--paper)"/>{body}</svg>'


SCRIPT = """if(new URLSearchParams(location.search).has('embed'))document.documentElement.classList.add('embedded');const tell=()=>{if(parent!==window)parent.postMessage({type:'reading-map-size',height:Math.ceil(document.querySelector('main').getBoundingClientRect().height)},'*')};new ResizeObserver(tell).observe(document.querySelector('main'));addEventListener('load',tell);addEventListener('message',e=>{if(e.source===parent&&e.data?.type==='reading-map-theme'&&['light','dark'].includes(e.data.theme))document.documentElement.dataset.theme=e.data.theme});"""


def render(name, d, lang):
    graphic = svg(name, d, lang, standalone=True)
    desktop = svg(name, d, lang)
    small = svg(name, d, lang, True)
    return (
        f'<!doctype html><html lang="{"en" if lang else "zh-CN"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow, noimageindex"><title>{H(d["title"][lang])}</title><style>{STYLE}</style></head><body><main><h1>{H(d["title"][lang])}</h1><div class="desktop">{desktop}</div><div class="mobile">{small}</div></main><script>{SCRIPT}</script></body></html>',
        graphic,
    )


if __name__ == "__main__":
    data = json.loads((ROOT / "reading-maps.json").read_text())
    for name, d in data.items():
        for lang, suffix in [(0, ".zh-CN"), (1, "")]:
            page, graphic = render(name, d, lang)
            (ROOT / (name + suffix + ".html")).write_text(page)
            (ROOT / (name + suffix + ".svg")).write_text(graphic)
    print(
        f"Rendered {len(data)} bilingual illustrated diagrams with desktop and mobile compositions."
    )
