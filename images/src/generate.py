# Генератор SVG-иллюстраций для сайта (цвета brand-*)
import random, math, os

OUT = '/home/user/sumshi/images/src'
P, PH, PL = '#1D4ED8', '#1E40AF', '#EFF6FF'
B1, B2 = '#DBEAFE', '#BFDBFE'
D, S7, S5, S4, S3, S2, S1, S0 = '#0F172A', '#334155', '#64748B', '#94A3B8', '#CBD5E1', '#E2E8F0', '#F1F5F9', '#F8FAFC'


def defs():
    rnd = random.Random(7)
    dots = ''.join(
        f'<circle cx="{rnd.uniform(0,60):.1f}" cy="{rnd.uniform(0,60):.1f}" r="{rnd.uniform(1.2,3.6):.1f}" fill="{rnd.choice([S3,S3,S4])}"/>'
        for _ in range(14))
    return f'''<defs>
  <pattern id="conc" width="60" height="60" patternUnits="userSpaceOnUse">
    <rect width="60" height="60" fill="{S2}"/>{dots}
  </pattern>
  <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{S3}"/><stop offset=".5" stop-color="#F8FAFC"/><stop offset="1" stop-color="{S4}"/>
  </linearGradient>
  <linearGradient id="motor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2563EB"/><stop offset="1" stop-color="{PH}"/>
  </linearGradient>
  <radialGradient id="hole" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{D}"/><stop offset=".75" stop-color="{S7}"/><stop offset="1" stop-color="{S5}"/>
  </radialGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="{PL}"/>
  </linearGradient>
</defs>'''


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter, Arial, sans-serif">\n{defs()}\n<rect width="{w}" height="{h}" fill="url(#bg)"/>\n{body}\n</svg>\n'


def rebars(xs, ys, r=9):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{S7}"/><circle cx="{x}" cy="{y}" r="{r-4}" fill="{S5}"/>' for x in xs for y in ys)


# ---------- 1. Герой: установка алмазного бурения, разрез стены, керн ----------
def hero():
    W, H = 1200, 900
    fy = 790          # пол
    cy = 420          # ось отверстия
    r = 80            # радиус коронки
    wx0, wx1 = 110, 350   # стена (разрез)
    tip = 215         # докуда дошла коронка
    b = []
    b.append(f'<rect x="0" y="{fy}" width="{W}" height="{H-fy}" fill="{S2}"/><line x1="0" y1="{fy}" x2="{W}" y2="{fy}" stroke="{S3}" stroke-width="3"/>')
    # стена
    b.append(f'<rect x="{wx0}" y="40" width="{wx1-wx0}" height="{fy-40}" fill="url(#conc)" stroke="{S4}" stroke-width="3"/>')
    b.append(rebars([wx0+32, wx1-32], [110, 230, 620, 730]))
    # пропил коронки внутри стены
    for yy in (cy - r, cy + r - 12):
        b.append(f'<rect x="{tip}" y="{yy}" width="{wx1-tip}" height="12" fill="{S7}"/>')
    # сегменты на торце
    b.append(f'<rect x="{tip-6}" y="{cy-r-3}" width="16" height="18" rx="3" fill="{P}"/><rect x="{tip-6}" y="{cy+r-15}" width="16" height="18" rx="3" fill="{P}"/>')
    # водосборное кольцо на стене
    b.append(f'<rect x="{wx1}" y="{cy-r-26}" width="22" height="{2*r+52}" rx="8" fill="{S7}"/>')
    # коронка снаружи стены
    tx1 = 640
    b.append(f'<rect x="{wx1+22}" y="{cy-r}" width="{tx1-wx1-22}" height="{2*r}" fill="url(#steel)" stroke="{S5}" stroke-width="3"/>')
    b.append(f'<line x1="{wx1+40}" y1="{cy-r+18}" x2="{tx1-20}" y2="{cy-r+18}" stroke="#FFFFFF" stroke-width="6" opacity=".7"/>')
    # переходник и мотор
    b.append(f'<rect x="{tx1}" y="{cy-34}" width="50" height="68" rx="6" fill="{S5}"/>')
    mx0, mx1 = 690, 930
    b.append(f'<rect x="{mx0}" y="{cy-95}" width="{mx1-mx0}" height="190" rx="28" fill="url(#motor)"/>')
    for i in range(6):
        x = mx0 + 110 + i * 18
        b.append(f'<line x1="{x}" y1="{cy-60}" x2="{x}" y2="{cy+60}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity=".35"/>')
    b.append(f'<rect x="{mx0+24}" y="{cy-50}" width="60" height="100" rx="12" fill="{PL}" opacity=".9"/>')
    b.append(f'<circle cx="{mx0+54}" cy="{cy}" r="20" fill="{P}"/>')
    b.append(f'<path d="M{mx1-30} {cy-95} v-40 a20 20 0 0 1 20 -20 h60 a20 20 0 0 1 20 20 v180" fill="none" stroke="{S7}" stroke-width="18" stroke-linecap="round"/>')
    # станина: направляющая, каретка, ножки
    ry = 560
    b.append(f'<rect x="{mx0+60}" y="{cy+95}" width="120" height="{ry-cy-95}" fill="{S7}"/>')
    b.append(f'<rect x="410" y="{ry}" width="700" height="34" rx="6" fill="{S7}"/>')
    for i in range(14):
        b.append(f'<rect x="{430+i*48}" y="{ry+8}" width="22" height="8" rx="2" fill="{S5}"/>')
    b.append(f'<rect x="{mx0+40}" y="{ry-10}" width="160" height="54" rx="10" fill="{S5}"/>')
    wcx, wcy = mx0 + 120, ry + 105
    b.append(f'<line x1="{wcx}" y1="{ry+44}" x2="{wcx}" y2="{wcy}" stroke="{S7}" stroke-width="10"/>')
    b.append(f'<circle cx="{wcx}" cy="{wcy}" r="44" fill="none" stroke="{S7}" stroke-width="10"/>')
    for a in range(0, 360, 60):
        b.append(f'<line x1="{wcx}" y1="{wcy}" x2="{wcx+44*math.cos(math.radians(a)):.1f}" y2="{wcy+44*math.sin(math.radians(a)):.1f}" stroke="{S7}" stroke-width="6"/>')
    for lx in (440, 1060):
        b.append(f'<rect x="{lx}" y="{ry+34}" width="22" height="{fy-ry-34-14}" fill="{S7}"/><rect x="{lx-26}" y="{fy-16}" width="74" height="16" rx="4" fill="{D}"/>')
    # шланг подачи воды
    b.append(f'<path d="M{mx0+150} {cy-95} C {mx0+150} 170, 1100 170, 1120 360 S 1150 {fy-10}, 1180 {fy-10}" fill="none" stroke="{P}" stroke-width="10" stroke-linecap="round" opacity=".55"/>')
    # керн на полу
    kx0, kx1, ky = 540, 800, fy - 52
    b.append(f'<rect x="{kx0}" y="{ky-52}" width="{kx1-kx0}" height="104" fill="url(#conc)" stroke="{S4}" stroke-width="3"/>')
    b.append(f'<ellipse cx="{kx1}" cy="{ky}" rx="22" ry="52" fill="url(#conc)" stroke="{S4}" stroke-width="3"/>')
    b.append(f'<ellipse cx="{kx0}" cy="{ky}" rx="22" ry="52" fill="{S3}" stroke="{S4}" stroke-width="3"/>')
    b.append(f'<circle cx="{kx0+120}" cy="{ky-12}" r="9" fill="{S7}"/>')
    # ось отверстия
    b.append(f'<line x1="60" y1="{cy}" x2="{mx1+80}" y2="{cy}" stroke="{P}" stroke-width="3" stroke-dasharray="18 10" opacity=".7"/>')
    return svg(W, H, '\n'.join(b))


# ---------- 2/3. Стена до и после (одинаковая композиция) ----------
def wall_scene(after):
    W, H = 1600, 800
    cx, cy, r = 800, 330, 110
    b = []
    b.append(f'<rect width="{W}" height="660" fill="{S1}"/>')
    for x in range(0, W, 80):
        b.append(f'<rect x="{x}" y="0" width="40" height="660" fill="#FFFFFF" opacity=".35"/>')
    b.append(f'<rect y="640" width="{W}" height="26" fill="#FFFFFF" stroke="{S3}" stroke-width="2"/>')
    b.append(f'<rect y="666" width="{W}" height="{H-666}" fill="{S2}"/>')
    for x in range(-200, W, 160):
        b.append(f'<line x1="{x}" y1="{H}" x2="{x+120}" y2="666" stroke="{S3}" stroke-width="2"/>')
    # защитная плёнка на полу и стене
    b.append(f'<rect x="520" y="520" width="560" height="146" fill="{B1}" opacity=".75"/>')
    b.append(f'<path d="M440 666 H1160 L1240 {H} H360 Z" fill="{B1}" opacity=".75"/>')
    for x in (520, 1040):
        b.append(f'<rect x="{x}" y="510" width="40" height="18" fill="{S3}" opacity=".9"/>')
    b.append(f'<rect x="520" y="512" width="560" height="10" fill="{S3}" opacity=".6"/>')
    if not after:
        b.append(f'<line x1="{cx-260}" y1="{cy}" x2="{cx+260}" y2="{cy}" stroke="{P}" stroke-width="3" stroke-dasharray="16 10"/>')
        b.append(f'<line x1="{cx}" y1="{cy-200}" x2="{cx}" y2="{cy+190}" stroke="{P}" stroke-width="3" stroke-dasharray="16 10"/>')
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P}" stroke-width="4" stroke-dasharray="14 10"/>')
        b.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{P}"/>')
        # уровень
        b.append(f'<rect x="{cx-200}" y="110" width="400" height="44" rx="8" fill="#FFFFFF" stroke="{S4}" stroke-width="3"/>')
        b.append(f'<rect x="{cx-50}" y="120" width="100" height="24" rx="12" fill="{B1}" stroke="{P}" stroke-width="2"/>')
        b.append(f'<circle cx="{cx+6}" cy="132" r="8" fill="{P}" opacity=".5"/>')
        b.append(f'<line x1="{cx-12}" y1="118" x2="{cx-12}" y2="146" stroke="{P}" stroke-width="2"/><line x1="{cx+24}" y1="118" x2="{cx+24}" y2="146" stroke="{P}" stroke-width="2"/>')
        # размерная линия
        b.append(f'<line x1="{cx-r}" y1="{cy+r+40}" x2="{cx+r}" y2="{cy+r+40}" stroke="{P}" stroke-width="3"/>')
        for x in (cx - r, cx + r):
            b.append(f'<line x1="{x}" y1="{cy+r+28}" x2="{x}" y2="{cy+r+52}" stroke="{P}" stroke-width="3"/>')
        # карандаш
        b.append(f'<g transform="translate({cx+170} {cy+60}) rotate(-35)"><rect x="0" y="-9" width="130" height="18" rx="3" fill="{P}"/><path d="M0 -9 L-24 0 L0 9 Z" fill="#F5D0A9"/><path d="M-16 -3 L-24 0 L-16 3 Z" fill="{D}"/></g>')
    else:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="{S3}"/>')
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#hole)"/>')
        b.append(f'<circle cx="{cx+10}" cy="{cy+8}" r="{r-26}" fill="{D}" opacity=".55"/>')
        b.append(f'<path d="M{cx-r+14} {cy-30} A{r-10} {r-10} 0 0 1 {cx+20} {cy-r+12}" fill="none" stroke="#FFFFFF" stroke-width="5" opacity=".35" stroke-linecap="round"/>')
    return svg(W, H, '\n'.join(b))


# ---------- 4–9. Карточки услуг 800×400 ----------
def card(body):
    return svg(800, 400, body)


def kiv():
    b = [f'<rect x="330" y="0" width="140" height="400" fill="url(#conc)" stroke="{S4}" stroke-width="3"/>',
         rebars([355, 445], [50, 350], 7),
         f'<rect x="290" y="148" width="250" height="104" fill="#FFFFFF" stroke="{S5}" stroke-width="3"/>',
         f'<rect x="270" y="136" width="22" height="128" rx="4" fill="{S4}"/>',
         ''.join(f'<line x1="274" y1="{150+i*16}" x2="288" y2="{150+i*16}" stroke="#FFFFFF" stroke-width="4"/>' for i in range(7)),
         f'<rect x="540" y="112" width="34" height="176" rx="10" fill="#FFFFFF" stroke="{S5}" stroke-width="3"/>',
         ''.join(f'<line x1="550" y1="{140+i*20}" x2="564" y2="{140+i*20}" stroke="{S4}" stroke-width="4" stroke-linecap="round"/>' for i in range(7))]
    for i, y in enumerate((170, 200, 230)):
        b.append(f'<path d="M60 {y} H240" stroke="{P}" stroke-width="5" stroke-linecap="round" opacity="{.4+i*.2}"/><path d="M228 {y-10} L244 {y} L228 {y+10}" fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="{.4+i*.2}"/>')
        b.append(f'<path d="M600 {y} C 660 {y}, 680 {y-40+i*40}, 740 {y-40+i*40}" fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" opacity="{.4+i*.2}"/>')
    return card('\n'.join(b))


def slab():
    b = [f'<rect x="0" y="180" width="800" height="100" fill="url(#conc)" stroke="{S4}" stroke-width="3"/>',
         f'<rect x="0" y="164" width="800" height="16" fill="{S3}"/>',
         rebars([60, 160, 260, 540, 640, 740], [205, 255], 7),
         f'<rect x="336" y="164" width="128" height="116" fill="{S0}"/>',
         f'<rect x="360" y="0" width="80" height="400" fill="url(#steel)" stroke="{S5}" stroke-width="3"/>',
         f'<rect x="348" y="140" width="104" height="24" rx="4" fill="{S7}"/>',
         f'<rect x="348" y="282" width="104" height="16" rx="4" fill="{S7}"/>',
         f'<rect x="352" y="60" width="96" height="16" rx="3" fill="{S4}"/>',
         f'<path d="M400 316 v44 M388 348 l12 12 l12 -12" fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>']
    return card('\n'.join(b))


def cables():
    b = [f'<rect x="0" y="0" width="800" height="400" fill="url(#conc)"/>',
         f'<rect x="0" y="0" width="800" height="400" fill="#FFFFFF" opacity=".35"/>']
    colors = [D, S7, P, D, S5, P]
    for i in range(6):
        x = 190 + i * 84
        b.append(f'<circle cx="{x}" cy="150" r="30" fill="{S7}"/><circle cx="{x}" cy="150" r="24" fill="#FFFFFF" stroke="{S4}" stroke-width="3"/>')
        b.append(f'<path d="M{x} 150 C {x} 260, {x-40+i*16} 300, {x-60+i*24} 400" fill="none" stroke="{colors[i]}" stroke-width="14" stroke-linecap="round"/>')
        b.append(f'<circle cx="{x}" cy="150" r="9" fill="{colors[i]}"/>')
    return card('\n'.join(b))


def plinth():
    b = [f'<rect x="0" y="0" width="800" height="120" fill="{S1}"/>',
         f'<rect x="0" y="112" width="800" height="12" fill="{S3}"/>']
    for row, y in enumerate((124, 204)):
        off = 0 if row == 0 else -120
        for x in range(off, 800, 240):
            b.append(f'<rect x="{x}" y="{y}" width="238" height="78" fill="url(#conc)" stroke="{S4}" stroke-width="3"/>')
    b.append(f'<path d="M0 290 Q 200 276 400 290 T 800 286 V400 H0 Z" fill="{S3}"/>')
    rnd = random.Random(3)
    b.append(''.join(f'<circle cx="{rnd.uniform(0,800):.0f}" cy="{rnd.uniform(305,395):.0f}" r="{rnd.uniform(2,5):.1f}" fill="{S4}"/>' for _ in range(40)))
    b.append(f'<circle cx="400" cy="200" r="54" fill="{S3}"/><circle cx="400" cy="200" r="48" fill="url(#hole)"/>')
    b.append(f'<circle cx="400" cy="200" r="48" fill="none" stroke="{S7}" stroke-width="6"/>')
    for i in range(-3, 4):
        w = 2 * math.sqrt(max(48**2 - (i * 12)**2, 0))
        b.append(f'<line x1="{400-w/2+4:.1f}" y1="{200+i*12}" x2="{400+w/2-4:.1f}" y2="{200+i*12}" stroke="{S4}" stroke-width="4"/>')
    b.append(f'<path d="M470 200 H560 M548 188 l12 12 l-12 12" fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>')
    b.append(f'<path d="M330 200 H240 M252 188 l-12 12 l12 12" fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>')
    return card('\n'.join(b))


def chimney():
    a = math.radians(-18)  # уклон трубы к улице (для конденсата)
    b = [f'<rect x="330" y="0" width="130" height="400" fill="url(#conc)" stroke="{S4}" stroke-width="3"/>',
         rebars([354, 436], [40, 360], 7),
         f'<rect x="590" y="110" width="160" height="240" rx="14" fill="#FFFFFF" stroke="{S5}" stroke-width="3"/>',
         f'<rect x="630" y="270" width="80" height="40" rx="6" fill="{PL}" stroke="{P}" stroke-width="2"/>',
         f'<path d="M660 290 q10 -22 10 0 q0 12 -10 12 q-10 0 -10 -12 q0 -8 10 -20" fill="{P}" opacity=".7"/>',
         f'<path d="M670 110 V80 H600" fill="none" stroke="{S5}" stroke-width="3"/>',
         ]
    # труба: от котла (600,210) к улице влево-вверх
    x0, y0, L = 600, 190, 470
    b.append(f'<g transform="translate({x0} {y0}) rotate({math.degrees(a):.1f})">'
             f'<rect x="{-L}" y="-38" width="{L}" height="76" fill="#FFFFFF" stroke="{S5}" stroke-width="3"/>'
             f'<rect x="{-L}" y="-18" width="{L}" height="36" fill="{S2}" stroke="{S4}" stroke-width="2"/>'
             f'<rect x="{-L-20}" y="-46" width="24" height="92" rx="6" fill="{S4}"/></g>')
    return card('\n'.join(b))


def stitch():
    b = [f'<rect x="0" y="0" width="800" height="400" fill="url(#conc)"/>',
         rebars([90, 710], [60, 200, 340], 7)]
    x0, y0, x1, y1, st, rr = 250, 60, 550, 340, 30, 17
    pts = []
    x = x0
    while x < x1: pts.append((x, y0)); x += st
    y = y0
    while y < y1: pts.append((x1, y)); y += st
    x = x1
    while x > x0: pts.append((x, y1)); x -= st
    y = y1
    while y > y0: pts.append((x0, y)); y -= st
    done = int(len(pts) * .72)
    b.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#FFFFFF" opacity=".25"/>')
    for i, (px, py) in enumerate(pts):
        if i < done:
            b.append(f'<circle cx="{px}" cy="{py}" r="{rr}" fill="{S7}" stroke="{S3}" stroke-width="2"/>')
        else:
            b.append(f'<circle cx="{px}" cy="{py}" r="{rr}" fill="none" stroke="{P}" stroke-width="3" stroke-dasharray="6 5"/>')
    return card('\n'.join(b))


files = {
    'photo-1': hero(), 'photo-2': wall_scene(False), 'photo-3': wall_scene(True),
    'photo-4': kiv(), 'photo-5': slab(), 'photo-6': cables(),
    'photo-7': plinth(), 'photo-8': chimney(), 'photo-9': stitch(),
}
for name, s in files.items():
    open(os.path.join(OUT, name + '.svg'), 'w').write(s)
print('ok', len(files))
