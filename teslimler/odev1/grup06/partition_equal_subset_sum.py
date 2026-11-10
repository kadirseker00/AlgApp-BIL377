"""
Partition Equal Subset Sum (Eşit Toplamlı Alt Küme Bölmesi) — Dinamik Programlama

Problem: Pozitif tam sayılardan oluşan bir dizi verildiğinde, dizinin
toplamları eşit olan iki alt kümeye bölünüp bölünemeyeceğini belirle.

DP durumu:
    dp[i][j] = True  <=>  ilk i elemandan bazıları seçilerek toplam j elde edilebilir
Başlangıç:
    dp[i][0] = True (boş küme), dp[0][j>0] = False
Geçiş:
    dp[i][j] = dp[i-1][j]                         (i. elemanı alma)
            OR (j >= a_i AND dp[i-1][j - a_i])    (i. elemanı al)
Cevap:
    toplam tek ise False, değilse dp[n][toplam/2]

Çalıştırma:
    python3 partition_equal_subset_sum.py              # örnekleri çalıştırır
    python3 partition_equal_subset_sum.py 1 5 11 5     # kendi girdiniz
"""
import sys


def can_partition_table(nums):
    """2B DP tablosunu kurar. (sonuç, tablo, hedef) döndürür."""
    total = sum(nums)
    if total % 2 == 1:
        return False, None, None
    target = total // 2
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True
    for i in range(1, n + 1):
        a = nums[i - 1]
        for j in range(1, target + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= a and dp[i - 1][j - a]:
                dp[i][j] = True
    return dp[n][target], dp, target


def reconstruct(nums, dp, target):
    """Tablodan geriye giderek toplamı target olan alt kümeyi bulur."""
    subset, j = [], target
    for i in range(len(nums), 0, -1):
        if not dp[i - 1][j]:          # i. eleman olmadan j yapılamıyorsa, o eleman seçilmiştir
            subset.append(nums[i - 1])
            j -= nums[i - 1]
    return subset[::-1]


def can_partition_1d(nums):
    """Bellek optimizasyonlu sürüm: O(hedef) bellek."""
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target
    for a in nums:
        for j in range(target, a - 1, -1):  # sağdan sola: her eleman en fazla bir kez
            dp[j] = dp[j] or dp[j - a]
    return dp[target]


def print_table(nums, dp, target):
    header = "        j: " + " ".join(f"{j:>2}" for j in range(target + 1))
    print(header)
    for i in range(len(dp)):
        label = "{}" if i == 0 else f"a{i}={nums[i-1]}"
        row = " ".join(" T" if v else " F" for v in dp[i])
        print(f"{label:>10} {row}")


def solve(nums):
    print(f"Girdi: {nums}   toplam = {sum(nums)}")
    ok, dp, target = can_partition_table(nums)
    assert ok == can_partition_1d(nums)
    if dp is None:
        print("Toplam tek sayı -> eşit bölme imkânsız.\nÇıktı: False\n")
        return ok
    print(f"Hedef = toplam / 2 = {target}")
    print_table(nums, dp, target)
    if ok:
        s1 = reconstruct(nums, dp, target)
        s2 = list(nums)
        for x in s1:
            s2.remove(x)
        print(f"Bölme: {s1} (toplam {sum(s1)})  |  {s2} (toplam {sum(s2)})")
    print(f"Çıktı: {ok}\n")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve([int(x) for x in sys.argv[1:]])
    else:
        for example in ([1, 5, 11, 5], [2, 2, 3, 5], [1, 2, 3, 5]):
            solve(example)
