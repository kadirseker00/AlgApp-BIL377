"""DP tablosunun adım adım doldurulmasını gösteren GIF üretir (Pillow gerekir)."""
from PIL import Image, ImageDraw, ImageFont
from partition_equal_subset_sum import can_partition_table, reconstruct

NUMS = [1, 5, 11, 5]
OUT = "partition_equal_subset_sum.gif"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_title, f_cell, f_txt, f_small = (ImageFont.truetype(BOLD, 26), ImageFont.truetype(BOLD, 20),
                                   ImageFont.truetype(FONT, 19), ImageFont.truetype(FONT, 15))

ok, DP, T = can_partition_table(NUMS)
N = len(NUMS)
CELL, X0, Y0 = 62, 130, 200
W, H = X0 + (T + 1) * CELL + 40, Y0 + (N + 1) * CELL + 190

C_BG, C_GRID, C_EMPTY = (255, 255, 255), (60, 60, 60), (245, 245, 245)
C_T, C_F = (198, 239, 206), (255, 214, 214)
C_CUR, C_UP, C_DIAG, C_PATH = (255, 200, 0), (120, 170, 255), (190, 130, 255), (255, 140, 0)


def frame(filled, cur=None, up=None, diag=None, msg="", msg2="", path=(), active_i=None):
    im = Image.new("RGB", (W, H), C_BG)
    d = ImageDraw.Draw(im)
    d.text((20, 15), "Partition Equal Subset Sum — DP", font=f_title, fill=(20, 20, 20))
    # dizi
    d.text((20, 60), "nums =", font=f_txt, fill=(0, 0, 0))
    for k, v in enumerate(NUMS):
        x = 100 + k * 60
        col = C_CUR if active_i == k + 1 else (230, 230, 230)
        d.rounded_rectangle([x, 55, x + 50, 90], 6, fill=col, outline=C_GRID)
        d.text((x + 25, 72), str(v), font=f_cell, fill=(0, 0, 0), anchor="mm")
    d.text((100 + N * 60 + 10, 60), f"toplam = {sum(NUMS)},  hedef = {T}", font=f_txt, fill=(0, 0, 0))
    d.text((20, 105), "dp[i][j] = ilk i eleman ile toplam j yapılabilir mi?", font=f_small, fill=(70, 70, 70))
    d.text((20, 127), "dp[i][j] = dp[i-1][j]  OR  dp[i-1][j - a_i]   (j ≥ a_i ise)", font=f_small, fill=(70, 70, 70))
    # başlıklar
    d.text((X0 - 10, Y0 - 45), "j →", font=f_small, fill=(0, 0, 0), anchor="rm")
    for j in range(T + 1):
        d.text((X0 + j * CELL + CELL / 2, Y0 - 20), str(j), font=f_cell, fill=(0, 0, 0), anchor="mm")
    for i in range(N + 1):
        lab = "i=0 {}" if i == 0 else f"i={i} (a={NUMS[i-1]})"
        d.text((X0 - 8, Y0 + i * CELL + CELL / 2), lab, font=f_small, fill=(0, 0, 0), anchor="rm")
    # hücreler
    for i in range(N + 1):
        for j in range(T + 1):
            x, y = X0 + j * CELL, Y0 + i * CELL
            if (i, j) in filled:
                fill = C_T if DP[i][j] else C_F
            else:
                fill = C_EMPTY
            if (i, j) == up:
                fill = C_UP
            if (i, j) == diag:
                fill = C_DIAG
            if (i, j) == cur:
                fill = C_CUR
            if (i, j) in path:
                fill = C_PATH
            d.rectangle([x, y, x + CELL, y + CELL], fill=fill, outline=C_GRID, width=2)
            if (i, j) in filled:
                d.text((x + CELL / 2, y + CELL / 2), "T" if DP[i][j] else "F",
                       font=f_cell, fill=(0, 0, 0), anchor="mm")
    # açıklama
    yb = Y0 + (N + 1) * CELL + 20
    d.text((20, yb), msg, font=f_txt, fill=(0, 0, 0))
    d.text((20, yb + 30), msg2, font=f_txt, fill=(0, 0, 0))
    # lejant
    yl = yb + 75
    for k, (c, t) in enumerate([(C_CUR, "hesaplanan"), (C_UP, "dp[i-1][j] (alma)"),
                                (C_DIAG, "dp[i-1][j-a] (al)"), (C_T, "True"), (C_F, "False"), (C_PATH, "geri izleme")]):
        x = 20 + k * 148
        d.rectangle([x, yl, x + 20, yl + 20], fill=c, outline=C_GRID)
        d.text((x + 26, yl + 1), t, font=f_small, fill=(0, 0, 0))
    return im


frames, durs = [], []


def add(im, ms):
    frames.append(im)
    durs.append(ms)


filled = set()
add(frame(filled, msg="Başlangıç: tablo boş. Satır i = ilk i eleman, sütun j = hedef toplam."), 1800)
for i in range(N + 1):
    filled.add((i, 0))
filled.update((0, j) for j in range(1, T + 1))
add(frame(filled, msg="Taban durumlar: dp[i][0] = T (boş küme toplamı 0),",
          msg2="dp[0][j>0] = F (eleman yokken pozitif toplam yapılamaz)."), 2500)

for i in range(1, N + 1):
    a = NUMS[i - 1]
    for j in range(1, T + 1):
        up = (i - 1, j)
        diag = (i - 1, j - a) if j >= a else None
        if diag:
            m2 = (f"al: dp[{i-1}][{j}-{a}] = dp[{i-1}][{j-a}] = {DP[i-1][j-a]}   "
                  f"→  dp[{i}][{j}] = {DP[i][j]}")
        else:
            m2 = f"j < a ({j} < {a}): eleman alınamaz  →  dp[{i}][{j}] = {DP[i][j]}"
        msg = f"dp[{i}][{j}], a{i} = {a}.  alma: dp[{i-1}][{j}] = {DP[i-1][j]}"
        add(frame(filled, cur=(i, j), up=up, diag=diag, msg=msg, msg2=m2, active_i=i), 700)
        filled.add((i, j))

add(frame(filled, cur=(N, T), msg=f"Cevap: dp[{N}][{T}] = {ok}",
          msg2="→ Dizi eşit toplamlı iki alt kümeye bölünebilir." if ok else "→ Bölünemez."), 2500)

# geri izleme
sub = reconstruct(NUMS, DP, T)
path, j = [(N, T)], T
for i in range(N, 0, -1):
    if not DP[i - 1][j]:
        j -= NUMS[i - 1]
    path.append((i - 1, j))
    add(frame(filled, path=set(path), msg="Geri izleme: dp[i-1][j] F ise a_i seçilmiştir (j -= a_i).",
              msg2=f"Seçilen alt küme: {sub}" if i == 1 else ""), 1200)
rest = list(NUMS)
for x in sub:
    rest.remove(x)
add(frame(filled, path=set(path), msg=f"Sonuç: {sub} (toplam {sum(sub)})  |  {rest} (toplam {sum(rest)})",
          msg2="Çıktı: True"), 4000)

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=True)
frames[-1].save("final_table.png")
print(f"{OUT}: {len(frames)} kare, {W}x{H}")
