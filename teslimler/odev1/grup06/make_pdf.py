"""PDF raporunu üretir (reportlab gerekir).
Kullanım: python make_pdf.py            -> rapor.pdf (öğrenci numaralı, Telegram için)
          python make_pdf.py --github   -> rapor_github.pdf (numarasız kopya)
"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Preformatted, Image, PageBreak)
from partition_equal_subset_sum import can_partition_table

# ====== BURAYI DOLDURUN ======
STUDENTS = [
    ("Nuraziz Taymusaev", "Öğrenci No"),
]
GROUP = "Grup XX"
# =============================

GITHUB = "--github" in sys.argv
OUT = "rapor_github.pdf" if GITHUB else "rapor.pdf"

D = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", D + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", D + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVM", D + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DV", boldItalic="DVB")

ss = getSampleStyleSheet()
body = ParagraphStyle("b", parent=ss["Normal"], fontName="DV", fontSize=10.5, leading=15, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=body, fontName="DVB", fontSize=15, leading=20, spaceBefore=10, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=body, fontName="DVB", fontSize=12, leading=16, spaceBefore=8, spaceAfter=4)
title = ParagraphStyle("t", parent=body, fontName="DVB", fontSize=22, leading=28, alignment=1)
center = ParagraphStyle("c", parent=body, alignment=1, fontSize=12, leading=18)
code = ParagraphStyle("code", fontName="DVM", fontSize=8, leading=10.2, backColor=colors.HexColor("#f4f4f4"),
                      borderPadding=5, spaceBefore=4, spaceAfter=10)
formula = ParagraphStyle("f", parent=body, fontName="DVM", fontSize=9.5, leading=14,
                         backColor=colors.HexColor("#eef3ff"), borderPadding=6, spaceBefore=4, spaceAfter=10)

P = lambda t, s=body: Paragraph(t, s)
story = []

# ---------- Kapak ----------
story += [Spacer(1, 3 * cm), P("BİL377", center), Spacer(1, 0.4 * cm),
          P("Ödev 1 — Dinamik Programlama", center), Spacer(1, 1 * cm),
          P("Partition Equal Subset Sum<br/>(Eşit Toplamlı Alt Kümelere Bölme)", title),
          Spacer(1, 1.5 * cm), P("Konu No: 6", center), Spacer(1, 0.8 * cm)]
rows = [["Ad Soyad"] if GITHUB else ["Ad Soyad", "Öğrenci No"]]
for name, no in STUDENTS:
    rows.append([name] if GITHUB else [name, no])
t = Table(rows, colWidths=[7 * cm] if GITHUB else [7 * cm, 5 * cm])
t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "DV", 11), ("FONT", (0, 0), (-1, 0), "DVB", 11),
                       ("GRID", (0, 0), (-1, -1), 0.6, colors.grey),
                       ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dde6f5")),
                       ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("TOPPADDING", (0, 0), (-1, -1), 6),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story += [t, PageBreak()]

# ---------- 1. Problem ----------
story += [P("1. Problemin Tanımı", h1),
          P("Pozitif tam sayılardan oluşan bir <b>nums</b> dizisi veriliyor. Dizinin elemanlarını, "
            "her eleman tam olarak bir kümede yer alacak şekilde, <b>toplamları eşit olan iki alt kümeye</b> "
            "bölmenin mümkün olup olmadığı soruluyor."),
          P("<b>Girdi:</b> n uzunluğunda pozitif tam sayı dizisi, örn. <font face='DVM'>nums = [1, 5, 11, 5]</font>."),
          P("<b>Çıktı:</b> <font face='DVM'>True</font> (bölünebilir) veya <font face='DVM'>False</font>. "
            "Örnekte cevap True'dur: <font face='DVM'>[11]</font> ve <font face='DVM'>[1, 5, 5]</font>, her ikisinin toplamı 11."),
          P("<b>Temel gözlem:</b> Toplam S ise, iki eşit küme varsa her birinin toplamı S/2 olmalıdır. "
            "Dolayısıyla S tek ise cevap doğrudan False'tur. S çift ise problem, "
            "<b>toplamı tam olarak S/2 olan bir alt küme var mı?</b> sorusuna (Subset Sum) indirgenir: "
            "böyle bir küme seçilirse geri kalan elemanların toplamı da otomatik olarak S/2 olur."),
          P("Kaba kuvvet çözümü 2<super>n</super> alt kümeyi dener. Dinamik programlama ile, aynı alt problemler "
            "tekrar tekrar çözülmediği için süre <font face='DVM'>O(n · S/2)</font>'ye iner.")]

# ---------- 2. DP ----------
story += [P("2. DP Mantığı", h1),
          P("2.1 Durumun anlamı", h2),
          P("<font face='DVM'>dp[i][j]</font> = ilk <b>i</b> eleman (a<sub>1</sub>, …, a<sub>i</sub>) arasından bazıları "
            "seçilerek toplamı tam olarak <b>j</b> olan bir alt küme oluşturulabiliyorsa <b>True</b>, aksi hâlde <b>False</b>. "
            "Burada <font face='DVM'>0 ≤ i ≤ n</font>, <font face='DVM'>0 ≤ j ≤ hedef = S/2</font>."),
          P("2.2 Başlangıç koşulları", h2),
          P("• <font face='DVM'>dp[i][0] = True</font> — boş küme seçilerek toplam 0 her zaman elde edilir.<br/>"
            "• <font face='DVM'>dp[0][j] = False (j &gt; 0)</font> — hiç eleman yokken pozitif bir toplam elde edilemez."),
          P("2.3 Geçiş bağıntısı", h2),
          P("i. eleman a<sub>i</sub> için iki seçenek vardır: onu <b>almamak</b> ya da (j ≥ a<sub>i</sub> ise) <b>almak</b>."),
          P("dp[i][j] = dp[i-1][j]  OR  ( j ≥ a_i  AND  dp[i-1][j - a_i] )", formula),
          P("Almazsak j toplamını ilk i−1 eleman ile yapmamız gerekir; alırsak geriye kalan j − a<sub>i</sub> toplamını "
            "ilk i−1 eleman ile yapmamız gerekir. Bir eleman yalnızca bir kez kullanılabildiği için her iki durumda da "
            "bir önceki satıra (i−1) bakılır."),
          P("2.4 Cevap", h2),
          P("S tek ise <font face='DVM'>False</font>; aksi hâlde <font face='DVM'>dp[n][S/2]</font>."),
          P("2.5 Hesaplama sırası", h2),
          P("Tablo satır satır (i = 1, 2, …, n), her satırda soldan sağa (j = 1, …, hedef) doldurulur. "
            "Her hücre yalnızca bir üst satırdaki iki hücreye bağlı olduğundan, bu sırada ihtiyaç duyulan "
            "değerler her zaman önceden hesaplanmış olur.")]

# ---------- 3. Örnek tablo ----------
NUMS = [1, 5, 11, 5]
ok, dp, T = can_partition_table(NUMS)
story += [PageBreak(), P("3. Örnek Üzerinde DP Tablosu", h1),
          P(f"<font face='DVM'>nums = {NUMS}</font>, S = 22 (çift), hedef = 11. "
            "Satırlar: kullanılan eleman sayısı i; sütunlar: hedef toplam j. Yeşil = True, kırmızı = False.")]
data = [["i \\ j"] + [str(j) for j in range(T + 1)]]
for i in range(len(NUMS) + 1):
    lab = "0: {}" if i == 0 else f"{i}: a={NUMS[i-1]}"
    data.append([lab] + ["T" if v else "F" for v in dp[i]])
tbl = Table(data, colWidths=[2.2 * cm] + [1.15 * cm] * (T + 1))
st = [("FONT", (0, 0), (-1, -1), "DVB", 10), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
      ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dde6f5")),
      ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#dde6f5"))]
for i in range(len(NUMS) + 1):
    for j in range(T + 1):
        st.append(("BACKGROUND", (j + 1, i + 1), (j + 1, i + 1),
                   colors.HexColor("#c6efce") if dp[i][j] else colors.HexColor("#ffd6d6")))
st.append(("BOX", (T + 1, len(NUMS) + 1), (T + 1, len(NUMS) + 1), 2, colors.HexColor("#ff8c00")))
tbl.setStyle(TableStyle(st))
story += [tbl, Spacer(1, 0.4 * cm), P("Satırların açıklaması (hesaplanma sırasıyla):", h2),
          P("<b>i = 0:</b> yalnızca dp[0][0] = T (taban durum)."),
          P("<b>i = 1 (a=1):</b> dp[1][1] = dp[0][1] OR dp[0][0] = F OR T = <b>T</b>. Diğer j'ler için 1 alınsa bile "
            "dp[0][j−1] = F olduğundan F. Erişilebilen toplamlar: {0, 1}."),
          P("<b>i = 2 (a=5):</b> j = 5: dp[1][5] OR dp[1][0] = F OR T = <b>T</b>; j = 6: dp[1][6] OR dp[1][1] = F OR T = <b>T</b>. "
            "Örneğin j = 8: dp[1][8] OR dp[1][3] = F OR F = F. Erişilebilen toplamlar: {0, 1, 5, 6}."),
          P("<b>i = 3 (a=11):</b> j &lt; 11 için eleman alınamaz, satır kopyalanır. j = 11: dp[2][11] OR dp[2][0] = F OR T = <b>T</b>. "
            "Erişilebilen: {0, 1, 5, 6, 11}."),
          P("<b>i = 4 (a=5):</b> j = 10: dp[3][10] OR dp[3][5] = F OR T = <b>T</b>; j = 11: dp[3][11] = T zaten. "
            "Erişilebilen: {0, 1, 5, 6, 10, 11}."),
          P("<b>Cevap:</b> dp[4][11] = <b>True</b> (turuncu çerçeveli hücre)."),
          P("Geri izleme (alt kümenin bulunması)", h2),
          P("dp[n][hedef]'ten başlayıp yukarı çıkılır: dp[i−1][j] = F ise a<sub>i</sub> mutlaka seçilmiştir ve "
            "j ← j − a<sub>i</sub> yapılır; aksi hâlde a<sub>i</sub> atlanır. dp[4][11]: dp[3][11] = T → a<sub>4</sub> atla. "
            "dp[3][11]: dp[2][11] = F → a<sub>3</sub> = 11 seçildi, j = 0. Sonuç: <font face='DVM'>[11]</font> ve "
            "<font face='DVM'>[1, 5, 5]</font>."),
          P("Aynı örnek GIF animasyonunda adım adım gösterilmiştir (aşağıda animasyonun son karesi). "
            "GIF, tablo ve programın çıktısı aynı değerleri verir.")]
story += [Image("final_table.png", width=14 * cm, height=14 * cm * 700 / 914)]

# ---------- 4. Kod ----------
story += [PageBreak(), P("4. Python Kodu", h1),
          P("Dosya: <font face='DVM'>partition_equal_subset_sum.py</font>. 2B tablolu sürüm (tabloyu göstermek ve "
            "alt kümeyi geri izlemek için) ve bellek açısından optimize 1B sürüm birlikte verilmiştir; "
            "program iki sürümün aynı sonucu verdiğini <font face='DVM'>assert</font> ile kontrol eder.")]
src = open("partition_equal_subset_sum.py", encoding="utf-8").read()
story += [Preformatted(src, code)]

# ---------- 5. Çalıştırma ----------
story += [P("5. Çalıştırma Adımları", h1),
          P("1. Python 3.8+ kurulu olmalıdır (ek kütüphane gerekmez).<br/>"
            "2. Örnekleri çalıştırmak için: <font face='DVM'>python3 partition_equal_subset_sum.py</font><br/>"
            "3. Kendi girdiniz için sayıları argüman olarak verin: "
            "<font face='DVM'>python3 partition_equal_subset_sum.py 1 5 11 5</font><br/>"
            "4. (İsteğe bağlı) GIF'i yeniden üretmek için: <font face='DVM'>pip install pillow</font>, "
            "sonra <font face='DVM'>python3 make_gif.py</font>"),
          P("6. Örnek Girdiler ve Çıktılar", h1),
          P("Üç örnek: [1, 5, 11, 5] → True; [2, 2, 3, 5] → toplam çift (12) olmasına rağmen toplamı 6 olan alt küme "
            "olmadığından False; [1, 2, 3, 5] → toplam tek (11) olduğundan doğrudan False. Programın gerçek çıktısı:")]
story += [Preformatted(open("example_output.txt", encoding="utf-8").read(), code)]

# ---------- 7. Karmaşıklık ----------
story += [P("7. Zaman ve Bellek Karmaşıklığı", h1),
          P("Değişkenler: <b>n</b> = dizideki eleman sayısı, <b>S</b> = elemanların toplamı, <b>T = S/2</b> = hedef toplam."),
          P("<b>Zaman:</b> Tabloda (n+1)·(T+1) hücre vardır ve her hücre O(1) işlemle (iki hücreye bakarak) hesaplanır. "
            "Toplamın hesaplanması O(n). Toplam: <b>O(n · T) = O(n · S)</b>. Geri izleme O(n)."),
          P("<b>Bellek:</b> 2B tablolu sürüm <b>O(n · T)</b>. Her satır yalnızca bir önceki satıra bağlı olduğundan tek bir "
            "dizi yeterlidir: 1B sürüm <b>O(T)</b> bellek kullanır. 1B sürümde j <b>sağdan sola</b> (T'den a'ya) dolaşılır; "
            "böylece dp[j − a] henüz bu elemanla güncellenmemiş (önceki satırın) değeri gösterir ve her eleman en fazla "
            "bir kez kullanılır. Soldan sağa dolaşılsaydı aynı eleman birden çok kez alınabilirdi (unbounded knapsack)."),
          P("<b>Not:</b> O(n · S) çalışma süresi <i>sözde-polinomdur</i> (pseudo-polynomial): girdinin bit uzunluğuna göre değil, "
            "sayıların büyüklüğüne göre polinomdur. Problem genel olarak NP-tamdır; DP, toplam küçük olduğunda verimlidir."),
          P("8. Sonuç", h1),
          P("Partition Equal Subset Sum, toplamın yarısını hedefleyen bir 0/1 Subset Sum problemine indirgenir. "
            "dp[i][j] tablosu her elemanı “al / alma” kararıyla değerlendirir, üstel kaba kuvvet çözümünü "
            "O(n · S) süreye indirir ve bellek O(S)'ye düşürülebilir.")]


def footer(c, d):
    c.setFont("DV", 8)
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"BİL377 Ödev 1 — Partition Equal Subset Sum — s. {d.page}")


SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                  bottomMargin=2 * cm, title="Partition Equal Subset Sum — Ödev 1").build(
    story, onFirstPage=lambda c, d: None, onLaterPages=footer)
print("yazıldı:", OUT)
