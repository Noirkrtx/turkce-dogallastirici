#!/usr/bin/env python3
"""okunurluk.py: Türkçe okunabilirlik ölçüleri (yalnız BİLGİ, puan düşürmez).

Kullanım:
    python3 okunurluk.py metin.txt [--kip post|rapor|ogretici|akademik|sesli|telgraf] [--json]

Ölçüler:
    Ateşman 1997: 198,825 - 40,175 x (hece/kelime) - 2,610 x (kelime/cümle)
        (formül ikincil kaynaktan; references/literatur.md L11)
    Bezirci-Yılmaz 2010 (YOD): kök( OKS x (H3x0,84 + H4x1,5 + H5x3,5 + H6x26,25) )
        OKS: cümle başına kelime; Hn: cümle başına n heceli kelime (H6: 6+)
        (references/literatur.md L12, Eşitlik 9)

Kip aralıkları references/kip-matrisi.md "Okunurluk kalibrasyonu" bölümünden
gelir; kapı değildir, yalnız raporlanır. 50 kelimenin altında raporlanmaz.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import unicodedata

UNLU = "aeıioöuüâîû"

# Projenin kendi metinlerinden ölçülen çeyrekler arası aralık (evals/kalibrasyon.json).
# Yalnız bilgi: "bu kipteki metinlerimizin ortası" demektir, hedef değildir.
KIP_ARALIK = {
    "post": {"atesman": (61.6, 71.9), "yod": (8.9, 12.8)},  # n=51
    "rapor": {"atesman": (81.1, 89.7), "yod": (6.6, 9.5)},  # n=11
    "ogretici": {"atesman": (77.1, 87.6), "yod": (7.2, 9.9)},  # n=35
    "akademik": {"atesman": (13.4, 37.1), "yod": (25.1, 37.2)},  # n=161
    "sesli": {"atesman": (84.8, 93.7), "yod": (4.5, 7.2)},  # n=5
    "telgraf": {"atesman": None, "yod": None},
}


def tr_kucuk(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    return s.replace("I", "ı").replace("İ", "i").lower()


def kelimeler(s: str) -> list[str]:
    return re.findall(r"[0-9A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîû'’]+", s)


def hece(kelime: str) -> int:
    n = len(re.findall(f"[{UNLU}]", tr_kucuk(kelime)))
    return max(1, n) if re.search(r"[A-Za-zÇĞİÖŞÜçğıöşü]", kelime) else 1


def cumleler(metin: str) -> list[str]:
    """Satır ve cümle sonu sınırdır; 4 kelimeden kısa satırlar (başlık, etiket,
    madde başı) ölçüye girmez: yoksa şablonlu metin yapay olarak kolay görünür."""
    out = []
    for satir in metin.splitlines():
        satir = satir.strip()
        if not satir or len(kelimeler(satir)) < 4:
            continue
        for p in re.split(r"(?<=[.!?…])\s+(?=\S)", satir):
            if kelimeler(p):
                out.append(p)
    return out


def olc(metin: str, kip: str = "post") -> dict:
    cs = cumleler(metin)
    kel = [w for c in cs for w in kelimeler(c)]
    n_c, n_k = len(cs), len(kel)
    if not n_c or not n_k:
        return {"kelime": n_k, "cumle": n_c}
    heceler = [hece(w) for w in kel]
    atesman = 198.825 - 40.175 * (sum(heceler) / n_k) - 2.610 * (n_k / n_c)
    oks = n_k / n_c
    h = lambda k: sum(1 for x in heceler if x == k) / n_c  # noqa: E731
    h6 = sum(1 for x in heceler if x >= 6) / n_c
    yod = math.sqrt(oks * (h(3) * 0.84 + h(4) * 1.5 + h(5) * 3.5 + h6 * 26.25))
    sonuc = {
        "kelime": n_k, "cumle": n_c,
        "hece_kelime": round(sum(heceler) / n_k, 2),
        "kelime_cumle": round(oks, 1),
        "atesman": round(atesman, 1),
        "bezirci_yilmaz": round(yod, 1),
    }
    if n_k < 50:
        sonuc["not"] = "50 kelimenin altında: ölçü güvenilmez, raporlanmaz"
        return sonuc
    ar = KIP_ARALIK.get(kip) or {}
    if ar.get("atesman"):
        lo, hi = ar["atesman"]
        yer = "altında" if atesman < lo else "üstünde" if atesman > hi else "içinde"
        sonuc["kip_karsilastirma"] = (
            f"Ateşman {atesman:.0f}: {kip} metinlerimizin çeyrek aralığının "
            f"({lo:.0f}-{hi:.0f}) {yer} (bilgi, kapı değil)")
    return sonuc


def main() -> int:
    ap = argparse.ArgumentParser(description="Ateşman + Bezirci-Yılmaz okunabilirlik")
    ap.add_argument("dosya", nargs="?")
    ap.add_argument("--kip", default="post", choices=list(KIP_ARALIK))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    metin = open(a.dosya, encoding="utf-8").read() if a.dosya else sys.stdin.read()
    s = olc(metin, a.kip)
    if a.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
    else:
        print(", ".join(f"{k}={v}" for k, v in s.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
