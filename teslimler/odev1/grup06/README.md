# Ödev 1 — Konu 6: Partition Equal Subset Sum

Dizinin toplamları eşit iki alt kümeye bölünüp bölünemeyeceğini dinamik programlama ile belirler.

- `dp[i][j]`: ilk i eleman ile toplam j elde edilebilir mi?
- Geçiş: `dp[i][j] = dp[i-1][j] OR (j >= a_i AND dp[i-1][j-a_i])`
- Cevap: toplam tek ise `False`, değilse `dp[n][toplam/2]`
- Zaman `O(n·S)`, bellek `O(n·S)` (1B sürüm `O(S)`)

## Dosyalar
- `partition_equal_subset_sum.py` — çözüm (2B tablo + geri izleme + 1B sürüm)
- `partition_equal_subset_sum.gif` — `[1, 5, 11, 5]` örneği için adım adım animasyon
- `rapor.pdf` — açıklama raporu
- `make_gif.py`, `make_pdf.py` — GIF ve PDF üreticileri

## Çalıştırma
```
python3 partition_equal_subset_sum.py            # örnekler
python3 partition_equal_subset_sum.py 1 5 11 5   # kendi girdiniz
```
