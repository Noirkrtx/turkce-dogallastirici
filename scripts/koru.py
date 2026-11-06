#!/usr/bin/env python3
"""koru.py: yeniden yazımın korunması gerekenleri bozup bozmadığını denetler.

Kullanım:
    python3 koru.py --once a.txt --sonra b.txt [--kip rapor] [--json]

Çıkış kodu 1: en az bir HATA (koruma ihlali). UYARI'lar model okumasına gider.

Denetimler (references/koruma-kurallari.md):
    sayi-birim     sayı + birim çoklu kümesi (µ/m ayrımı, ondalık, yüzde dahil)
    terim-sayi     kısaltma/istatistik terimi + sayı çiftleri (Ppeak 26 / Pplat 26 yer değişimi)
    karsilastirma  <, >, ≤, ≥ işaretinin yönü ve sayısı
    kisaltma       kısaltma kümesi (kaybolan HATA, eklenen UYARI)
    ozel-isim      büyük harfli özel adlar (kaybolan HATA, eklenen UYARI)
    alinti         tırnak ve «» içerikleri bayt bayt
    atif           [12], (4,9), (Yazar, 2024), PMID, DOI, URL; atıfın önermesiyle kalması
    sablon         [TIK], [SOR: ...], [BEKLE], {{...}}, <dfn>, [Kurum adı], MEDIA:
    oneri-gucu     önerilir/önerilebilir/önerilmez, Sınıf I-III, Düzey A-C
    temkin         girdide temkinli her önerme çıktıda en az bir temkin sözü taşır
    olumsuzluk     olumsuzluk sayısı farkı (UYARI, model okuması)
    nedensel       yeni nedensellik dili (akademik HATA, diğer UYARI)
    uzunluk        kelime oranı (telgraf ±%5, öğretici +%10 UYARI)

Sesli kipte iki metin önce references/sesli-okunus.md tablosuyla simgeye
geri çevrilir (okunuş → yazım, sayı sözcükleri → rakam); tabloda olmayan
dönüşüm sayı/terim kaybı olarak HATA verir.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter

BURA = os.path.dirname(os.path.realpath(__file__))
TABLO = os.path.join(BURA, "..", "references", "sesli-okunus.md")


def tr_kucuk(s: str) -> str:
    return unicodedata.normalize("NFC", s).replace("I", "ı").replace("İ", "i").lower()


def kelimeler(s: str) -> list[str]:
    return re.findall(r"[0-9A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîûµ₂₃'’]+", s)


def cumleler(metin: str) -> list[str]:
    out = []
    for satir in metin.splitlines():
        satir = satir.strip()
        if not satir:
            continue
        bas = 0
        for m in re.finditer(r"[.!?…]+[\"”’)]?\s+(?=[\"“(\[]?[A-ZÇĞİÖŞÜ])", satir):
            onceki = re.findall(r"[\wçğıöşü]+$", satir[bas:m.start()])
            if onceki and tr_kucuk(onceki[0]) in {"dr", "prof", "doç", "vb", "ör", "örn", "bkz", "vs"}:
                continue
            out.append(satir[bas:m.end()].strip())
            bas = m.end()
        if satir[bas:].strip():
            out.append(satir[bas:].strip())
    return out


# ---------------------------------------------------------------- sesli normalizasyon
SAYI = {"sıfır": 0, "bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6, "yedi": 7,
        "sekiz": 8, "dokuz": 9, "on": 10, "yirmi": 20, "otuz": 30, "kırk": 40, "elli": 50,
        "altmış": 60, "yetmiş": 70, "seksen": 80, "doksan": 90, "yüz": 100, "bin": 1000, "milyon": 10 ** 6}
EKLER = ("", "'", "’", "ın", "in", "un", "ün", "nın", "nin", "nun", "nün", "a", "e", "ya", "ye", "na", "ne",
         "da", "de", "ta", "te", "dan", "den", "tan", "ten", "ndan", "nden", "lık", "lik", "luk", "lük",
         "ı", "i", "u", "ü", "yı", "yi", "yu", "yü", "nı", "ni", "nu", "nü", "inci", "ıncı", "uncu", "üncü",
         "la", "le", "yla", "yle", "ar", "er", "şar", "şer")


def _sayi_sozu(tok: str):
    t = tr_kucuk(tok).replace("'", "").replace("’", "")
    for kok in sorted(SAYI, key=len, reverse=True):
        if t.startswith(kok) and t[len(kok):] in EKLER:
            return kok, t[len(kok):]
    return None


def _deger(koks: list[str]) -> int:
    toplam, ara = 0, 0
    for k in koks:
        v = SAYI[k]
        if v == 100:
            ara = (ara or 1) * 100
        elif v >= 1000:
            toplam += (ara or 1) * v
            ara = 0
        else:
            ara += v
    return toplam + ara


_SOZ = "(?:" + "|".join(sorted(list(SAYI) + ["virgül"], key=len, reverse=True)) + ")"
_EK = "(?:['’]?(?:" + "|".join(sorted([e for e in EKLER if e and e not in ("'", "’")], key=len, reverse=True)) + "))?"
_KOSU = re.compile(rf"(?<![\wçğıöşü])({_SOZ}{_EK}(?:\s+{_SOZ}{_EK})*)(?![\wçğıöşü])", re.I)


def sayi_sozlerini_cevir(metin: str) -> str:
    """Sayı sözü koşularını rakama çevirir: 'sıfır virgül sıfır sıfır iki' → '0,002'."""
    def cevir(m):
        kelimeler_ = m.group(1).split()
        if all(tr_kucuk(w) == "virgül" for w in kelimeler_):
            return m.group(0)
        cozum = [_sayi_sozu(w) or ("virgül", "") for w in kelimeler_]
        if len(cozum) == 1 and cozum[0][0] in ("bir", "on", "yüz", "bin", "altı") and \
                cozum[0][1] not in ("inci", "ıncı", "uncu", "üncü"):
            once = m.string[max(0, m.start() - 8):m.start()]
            sonra = tr_kucuk(m.string[m.end():m.end() + 12])
            if not (re.search(r"[%<>≤≥]\s*$|yüzde\s*$", once) or
                    re.match(r"\s*(virgül|mg|µg|ml|kg|dk|saat|gün|kez|kat|mili|mikro|kilo|gram|litre|dakika|santim|yaş)", sonra)):
                return m.group(0)
        ek = cozum[-1][1]
        if "virgül" in [c[0] for c in cozum]:
            i = [c[0] for c in cozum].index("virgül")
            tam, ond = [c[0] for c in cozum[:i]], [c[0] for c in cozum[i + 1:]]
            if not tam or not ond:
                return m.group(0)
            ond_s = "".join(str(SAYI[x]) for x in ond) if all(SAYI[x] < 10 for x in ond) else str(_deger(ond))
            deger = f"{_deger(tam)},{ond_s}"
        else:
            deger = str(_deger([c[0] for c in cozum]))
        return deger + (f"'{ek}" if ek else "")
    return _KOSU.sub(cevir, metin)


def koru_sayi_sozu(w: str) -> bool:
    return _sayi_sozu(w) is not None


def okunus_tablosu() -> list[tuple[str, str]]:
    ciftler = []
    if not os.path.exists(TABLO):
        return ciftler
    bolum = False
    for satir in open(TABLO, encoding="utf-8"):
        if satir.startswith("## Tablo"):
            bolum = True
            continue
        if not bolum or not satir.startswith("|") or satir.startswith("|---") or "yazım" in satir:
            continue
        hucre = [h.strip() for h in satir.strip().strip("|").split("|")]
        if len(hucre) >= 2:
            for ok in hucre[1].split(";"):
                if ok.strip():
                    ciftler.append((ok.strip(), hucre[0]))
    ciftler.sort(key=lambda c: len(c[0]), reverse=True)
    return ciftler


NUMW = (r"(?:sıfır|bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|otuz|kırk|elli|altmış|yetmiş|"
        r"seksen|doksan|yüz|bin|milyon|virgül)")
NUM = rf"((?:{NUMW}\s+)*{NUMW}|\d+(?:[.,]\d+)*)"


def sesli_normalle(metin: str) -> str:
    """Okunuş → yazım. Sıra: '#' (sayı yerli) kalıplar, sayı sözü içeren okunuşlar,
    sayı sözleri, kalan okunuşlar. Her iki metne de uygulanır."""
    m = unicodedata.normalize("NFC", metin)
    tablo = okunus_tablosu()
    sayili = re.compile(rf"(?<![\wçğıöşü]){_SOZ}(?![\wçğıöşü])", re.I)

    def duz(m, ok, yazim):
        rx = r"(?<![\wçğıöşü])" + re.escape(ok) + r"([a-zçğıöşü]{0,5})(?![\wçğıöşü])"
        if yazim == "%":
            return re.sub(rx + r"\s+", "% ", m, flags=re.I)
        if yazim in ("<", ">", "≤", "≥", "±"):
            return re.sub(rx, yazim + " ", m, flags=re.I)
        return re.sub(rx, lambda g: yazim + (f"'{g.group(1)}" if g.group(1) else ""), m, flags=re.I)

    for ok, yazim in [c for c in tablo if "#" in c[0]]:
        bas, son = (re.escape(x.strip()) for x in ok.split("#"))
        rx = rf"(?<![\wçğıöşü]){bas}\s+{NUM}\s+{son}([a-zçğıöşü]{{0,5}})(?![\wçğıöşü])"
        m = re.sub(rx, lambda g: f"{g.group(1)} {yazim}" + (f"'{g.group(2)}" if g.group(2) else ""), m, flags=re.I)
    for ok, yazim in [c for c in tablo if "#" not in c[0] and (sayili.search(c[0]) or c[1] == "%")]:
        m = duz(m, ok, yazim)
    m = sayi_sozlerini_cevir(m)
    for ok, yazim in [c for c in tablo if "#" not in c[0] and not sayili.search(c[0]) and c[1] != "%"]:
        m = duz(m, ok, yazim)
    m = re.sub(r"%\s+(\d)", r"%\1", m)
    m = re.sub(r"(\d)\s+ile\s+(\d[\d,]*)\s+arası\w*", r"\1-\2", m)
    m = re.sub(r"(?<![\wçğıöşü])([A-Za-z/₂₃0-9]{2,}) \1(?![\wçğıöşü])", r"\1", m)  # 'odds oranı OR' → 'OR'
    return m


# ---------------------------------------------------------------- çıkarıcılar
BIRIM = (r"µg/kg/dk|mcg/kg/dk|mg/kg/saat|mg/kg|mL/kg|mEq/L|mmol/L|mmHg|cmH₂O|cmH2O|µg|mcg|mg|mL|kg|IU|"
         r"dk|sn|ms|saat|gün|hafta|ay|yıl|kat|derece|mm|cm|L|g|U|bpm")
SAYI_RX = re.compile(r"(?<![A-Za-zÇĞİÖŞÜçğıöşü\d])(?:(?<=[\s(;:/])[-−]|^[-−])?%?\d+(?:[.,]\d+)*")


def _sayi_kanon(s: str) -> str:
    s = s.replace("−", "-")
    if re.fullmatch(r"-?%?\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    return s


def sayi_birim(metin: str) -> Counter:
    c = Counter()
    for m in SAYI_RX.finditer(metin):
        sonra = metin[m.end():m.end() + 14]
        b = re.match(r"\s?(" + BIRIM + r")(?![A-Za-zçğıöşü])", sonra)
        c[(_sayi_kanon(m.group(0)), b.group(1) if b else "")] += 1
    return c


KISALTMA_RX = re.compile(r"(?<![\wçğıöşü])([A-Za-zÇĞİÖŞÜçğıöşüµ₂₃/-]*[A-ZÇĞİÖŞÜ][A-Za-zÇĞİÖŞÜçğıöşü₂₃0-9/-]*?[A-ZÇĞİÖŞÜ0-9₂₃][A-Za-z0-9₂₃/-]*)")


def kisaltmalar(metin: str) -> Counter:
    c = Counter()
    for m in KISALTMA_RX.finditer(metin):
        w = re.split(r"['’]", m.group(1))[0].strip("-/")
        if sum(ch.isupper() for ch in w) >= 2 or re.search(r"[A-ZÇĞİÖŞÜ].*\d|\d.*[A-ZÇĞİÖŞÜ]", w):
            c[w] += 1
    return c


TERIM_ATLA = {"ve", "ile", "için", "başına", "olarak", "da", "de", "en", "çok", "az", "yaklaşık"}


def terim_sayi(metin: str) -> Counter:
    """Sayıdan önceki 4 kelime içinde en yakın büyük harfli terim + sayı."""
    c = Counter()
    for m in SAYI_RX.finditer(metin):
        pencere = re.split(r"[,;.:()\[\]]", metin[max(0, m.start() - 60):m.start()])[-1]
        once = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü₂₃][\w₂₃/-]*", pencere)[-4:]
        terim = next((t for t in reversed(once) if re.search(r"[A-ZÇĞİÖŞÜ]", t) and len(t) <= 12
                      and tr_kucuk(t) not in TERIM_ATLA), None)
        if terim:
            c[(re.split(r"['’]", terim)[0], _sayi_kanon(m.group(0)))] += 1
    return c


def karsilastirma(metin: str) -> Counter:
    return Counter((m.group(1), _sayi_kanon(m.group(2)))
                   for m in re.finditer(r"([<>≤≥])\s*(%?\d+(?:[.,]\d+)*)", metin))


def ozel_isimler(metin: str, yalniz_ic: bool) -> Counter:
    c = Counter()
    for cm in cumleler(metin):
        ws = list(re.finditer(r"[A-ZÇĞİÖŞÜ][a-zçğıöşüâîû]+(?:['’][a-zçğıöşü]+)?", cm))
        for i, m in enumerate(ws):
            if yalniz_ic and (m.start() == len(cm) - len(cm.lstrip("\"“(«*[ ")) or
                              re.search(r"[:·•)]\s*$", cm[:m.start()])):
                continue
            c[re.split(r"['’]", m.group(0))[0]] += 1
    return c


ALINTI_RX = re.compile(r"«([^»\n]*)»|“([^”\n]*)”|\"([^\"\n]*)\"")
ATIF_RX = re.compile(r"\[\d+(?:[,\-–]\s?\d+)*\]|\((?:\d+(?:\s?[,\-–]\s?\d+)*)\)|\([A-ZÇĞİÖŞÜ][^()\n]{0,60}?,\s?\d{4}[a-z]?\)"
                     r"|\bPMID:?\s*\d+|\bdoi:\s*\S+|\b10\.\d{4,}/\S+|https?://\S+|\barXiv:\s*\S+", re.I)
SABLON_RX = re.compile(r"\[TIK\]|\[BEKLE\]|\[SOR:[^\]]*\]|\{\{[^}]*\}\}|</?dfn>|«|»|\[AUTHOR TO INSERT\]|"
                       r"\[CITATION NEEDED\]|\[[A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?: [a-zçğıöşü]+){0,3}\]|^MEDIA:.*$|❓ Senden istenen", re.M)
ONERI_RX = re.compile(r"\b(önerilir|önerilebilir|önerilmez|önerilmektedir|önerilmemektedir|kontrendikedir|"
                      r"güçlü öneri|zayıf öneri|sınıf\s+(?:iii|iib|iia|ii|i|iv)\b|düzey\s+[abc]\b|grade)", re.I)
TEMKIN_RX = re.compile(r"\w*(abil|ebil)\w*|\bolası\w*|\bmuhtemel\w*|\byaklaşık\b|\bhenüz\b|\bilişkili\w*|"
                       r"\bdüşündür\w*|\bişaret ed\w*|\bişaret eder\w*|\bgörün\w*|\beğilim\w*|"
                       r"\bihtiyat\w*|\bbelki\b|\bgaliba\b|\bşüphe\w*|\bsanırım\b|\bdoğrulanma\w*|\bsınırlı\b|\btartışmalı\w*", re.I)
OLUMSUZ_RX = re.compile(r"\bdeğil\w*|\byok\w*|\bhiç\w*|\w+m[ae]m[ae]kt[ae]\w*|\w{2,}m[ae](?:d[ıiuü]|z\b|z[ıi]|m[ıiuü]ş|l[ıi]|y[ae]c[ae]k|y[ae]n|s[ıi]n|d[ıi]ğ)\w*|\w+m[ıiuü]yor\w*", re.I)
NEDEN_RX = re.compile(r"\bneden ol\w*|\byol aç\w*|\bnedeniyle\b|\bsonucunda\b|\betkisiyle\b|\bsağla(dı|r|mış)\w*|"
                      r"\bönle(di|r|miş)\w*|\bazalt(tı|ır|mış)\w*|\bartır(dı|ır|mış)\w*|\bkat artır\w*", re.I)


TEMKIN_SOZ_RX = re.compile(TEMKIN_RX.pattern.replace(r"\w*(abil|ebil)\w*|", ""), re.I)


def temkinli(c: str) -> bool:
    """'-abil/-ebil' yalnız çekimli yüklemde ('olabilir', 'düşünülebilir') temkin sayılır;
    'taşıyabileceği bilgi' gibi sıfat-fiil içindeki -abil ana iddiayı yumuşatmaz."""
    if TEMKIN_SOZ_RX.search(c):
        return True
    return bool(re.search(r"\w*(abil|ebil)(ir|mekte|miş|di|ecekt|iyor|mesi|mesine)\w*", tr_kucuk(c)))


def _kok_kumesi(s: str) -> set:
    return {tr_kucuk(w)[:5] for w in kelimeler(s) if len(w) >= 4 and not w.isdigit()}


def _ortusme(a: str, b: str) -> float:
    x, y = _kok_kumesi(a), _kok_kumesi(b)
    return len(x & y) / max(1, min(len(x), len(y)))


def oneri_gucu(metin: str) -> Counter:
    c = Counter(tr_kucuk(re.sub(r"\s+", " ", m.group(0))) for m in ONERI_RX.finditer(metin))
    # "düşünülebilir" yalnız öneri kalıbında (verilmesi/kullanımı düşünülebilir) sayılır
    for m in re.finditer(r"(\w+)\s+düşünülebilir", metin):
        if re.search(r"(mesi|ması|ımı|imi|umu|ümü|ılması|ilmesi)$", tr_kucuk(m.group(1))):
            c["düşünülebilir (öneri)"] += 1
    return c


# ---------------------------------------------------------------- ana denetim
DOSYA_RX = re.compile(r"[\w./-]*/[\w.-]+\.(?:md|py|txt|json|pdf|html|pptx|docx)\b")


def karsilastir(once: str, sonra: str, kip: str = "rapor", muaf: list[str] | None = None) -> dict:
    """muaf: bilerek silinen öğeler (iç not, dosya yolu, kod adı); kayıp listesinden düşülür ve raporlanır."""
    muaf = [m for m in (muaf or []) if m]
    once = unicodedata.normalize("NFC", once)
    sonra = unicodedata.normalize("NFC", sonra)
    o_k, s_k = (sesli_normalle(once), sesli_normalle(sonra)) if kip == "sesli" else (once, sonra)
    ihlaller = []

    def ekle(seviye, denetim, mesaj, eksik=None, fazla=None):
        ihlaller.append({"seviye": seviye, "denetim": denetim, "mesaj": mesaj,
                         "eksik": [str(x) for x in (eksik or [])], "fazla": [str(x) for x in (fazla or [])]})

    def kume_fark(ad, a: Counter, b: Counter, sev_eksik="HATA", sev_fazla="HATA"):
        eksik, fazla = list((a - b).elements()), list((b - a).elements())
        if muaf:
            eksik = [e for e in eksik if not any(m == (e[0] if isinstance(e, tuple) else e) or
                                                 (isinstance(e, tuple) and m in e) for m in muaf)]
        if eksik:
            ekle(sev_eksik, ad, f"{len(eksik)} öğe kayboldu ya da değişti", eksik=eksik)
        if fazla:
            ekle(sev_fazla, ad, f"{len(fazla)} yeni öğe eklendi", fazla=fazla)

    o_n, s_n = (DOSYA_RX.sub(" ", ATIF_RX.sub(" ", x)) for x in (o_k, s_k))  # atıf ve dosya yolu sayı değildir
    if kip == "sesli":  # kart içi kare/adım numarası ('0: yalnız pH. 1: ...') [TIK] olur, sayı değildir
        o_n, s_n = (re.sub(r"(?<![\d,.])\b\d{1,2}:\s", " ", x) for x in (o_n, s_n))
    sb_o, sb_s = sayi_birim(o_n), sayi_birim(s_n)
    kume_fark("sayi-birim", sb_o, sb_s, "HATA", "HATA")
    # kaynakta aynı değer zaten varsa fazlası yeni bilgi değil, tekrar: UYARI'ya indir
    for i in ihlaller:
        if i["denetim"] == "sayi-birim" and i["fazla"]:
            yeni_deger = [f for f, (sy, br) in zip(i["fazla"], (sb_s - sb_o).elements()) if (sy, br) not in sb_o]
            if not yeni_deger:
                i["seviye"], i["mesaj"] = "UYARI", "kaynakta olan değer tekrarlanmış (yeni sayı yok)"
    a, b = terim_sayi(o_n), terim_sayi(s_n)
    istat = re.compile(r"^(OR|RR|HR|ARR|RRR|NNT|NNH|LR|AUC|GA|CI|p|P|SS|SD|n|N)$|[A-Z].*[A-Z]|\d")
    a_ist = Counter({k: v for k, v in a.items() if istat.search(k[0])})
    b_ist = Counter({k: v for k, v in b.items() if istat.search(k[0])})
    eksik = list((a_ist - b_ist).elements())
    # terim metinde başka yerde aynı sayıyla duruyorsa (cümle yeniden kurulmuş) affet
    eksik = [e for e in eksik if not re.search(re.escape(e[0]) + r"[^.\n]{0,60}?" + re.escape(e[1]).replace(",", "[,.]"), s_k)
             and e[0] not in muaf and e[1] not in muaf]
    if eksik:
        ekle("HATA", "terim-sayi", "terim + sayı eşleşmesi bozuldu (değer yer değiştirmiş olabilir)", eksik=eksik)
    kume_fark("karsilastirma", karsilastirma(o_n), karsilastirma(s_n))
    o_s, s_s = SABLON_RX.sub(" ", o_k), SABLON_RX.sub(" ", s_k)
    kume_fark("kisaltma", kisaltmalar(o_s), kisaltmalar(s_s), "HATA", "UYARI")
    once_s, sonra_s = SABLON_RX.sub(" ", once), SABLON_RX.sub(" ", sonra)
    oi, si_hepsi = ozel_isimler(once_s, True), ozel_isimler(sonra_s, False)
    kayip = [w for w in oi if w not in si_hepsi and w not in s_k and w not in muaf]
    if kayip:
        ekle("HATA", "ozel-isim", "özel ad kayboldu", eksik=kayip)
    yeni = [w for w in ozel_isimler(sonra_s, True) if w not in ozel_isimler(once_s, False) and w not in o_k
            and not koru_sayi_sozu(w)]
    if yeni:
        ekle("UYARI", "ozel-isim", "yeni özel ad (kaynakta yok mu?)", fazla=yeni)
    kume_fark("alinti", Counter("".join(g) for g in ALINTI_RX.findall(once)),
              Counter("".join(g) for g in ALINTI_RX.findall(sonra)))
    atif_sev = "UYARI" if kip == "sesli" else "HATA"
    kume_fark("atif", Counter(ATIF_RX.findall(once)), Counter(ATIF_RX.findall(sonra)), atif_sev, atif_sev)
    # atıf önermesiyle kalıyor mu
    s_cs = cumleler(sonra)
    for c in cumleler(once):
        for at in ATIF_RX.findall(c):
            hedef = [x for x in s_cs if at in x]
            if hedef and max(_ortusme(c, h) for h in hedef) < 0.25:
                ekle("UYARI", "atif-baglilik", f"'{at}' dayandığı önermeden ayrılmış olabilir", eksik=[c[:80]])
    kume_fark("sablon", Counter(SABLON_RX.findall(once)), Counter(SABLON_RX.findall(sonra)),
              "HATA", "UYARI" if kip == "sesli" else "HATA")  # sesli: [TIK]/[SOR] eklemek meşru
    kume_fark("oneri-gucu", oneri_gucu(o_k), oneri_gucu(s_k))
    # temkin: önerme başına varlık
    def onermeler(t):
        return [p.strip() for c in cumleler(t) for p in re.split(r";|\s+ve\s+|,\s*(?:ancak|ama|fakat|oysa)\s+", c)
                if len(kelimeler(p)) >= 3]
    s_cs_n = onermeler(s_k)
    for c in onermeler(o_k):
        if not temkinli(c):
            continue
        es = [x for x in s_cs_n if _ortusme(c, x) >= 0.3]
        if not es:
            ekle("UYARI", "temkin", "temkinli önermenin karşılığı bulunamadı (silinmiş ya da çok değişmiş)", eksik=[c[:90]])
        elif not any(temkinli(x) for x in es):
            ekle("HATA", "temkin", "temkinli önerme çıktıda kesinleşmiş", eksik=[c[:90]])
    no, ns = len(OLUMSUZ_RX.findall(once)), len(OLUMSUZ_RX.findall(sonra))
    if no != ns:
        ekle("UYARI", "olumsuzluk", f"olumsuzluk sayısı {no} > {ns}; anlam tersine döndü mü (model okuması)?")
    nn, nsn = len(NEDEN_RX.findall(once)), len(NEDEN_RX.findall(sonra))
    if nsn > nn:
        ekle("HATA" if kip == "akademik" else "UYARI", "nedensel", f"nedensellik dili arttı ({nn} > {nsn})")
    ko, ks = len(kelimeler(once)), len(kelimeler(sonra))
    oran = ks / ko if ko else 1.0
    if kip == "telgraf" and abs(oran - 1) > 0.05:
        ekle("UYARI", "uzunluk", f"kelime oranı {oran:.2f} (telgraf ±%5)")
    if kip == "ogretici" and oran > 1.10:
        ekle("UYARI", "uzunluk", f"kelime oranı {oran:.2f} (öğretici en çok +%10; içerik eklenmiş olabilir)")
    hata = sum(1 for i in ihlaller if i["seviye"] == "HATA")
    return {"kip": kip, "hata": hata, "uyari": sum(1 for i in ihlaller if i["seviye"] == "UYARI"),
            "kelime_once": ko, "kelime_sonra": ks, "kelime_oran": round(oran, 3),
            "muaf": muaf, "gecti": hata == 0, "ihlaller": ihlaller}


def main() -> int:
    ap = argparse.ArgumentParser(description="Yeniden yazım koruma denetimi")
    ap.add_argument("--once", required=True)
    ap.add_argument("--sonra", required=True)
    ap.add_argument("--kip", default="rapor", choices=["post", "rapor", "ogretici", "akademik", "sesli", "telgraf"])
    ap.add_argument("--muaf", default="", help="bilerek silinenler, virgülle: 'KT,23' (raporda listelenir)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    s = karsilastir(open(a.once, encoding="utf-8").read(), open(a.sonra, encoding="utf-8").read(), a.kip,
                    [m.strip() for m in a.muaf.split(",")])
    if a.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
    else:
        print(f"KORUMA {'GEÇTİ' if s['gecti'] else 'İHLAL'}  ·  kip {s['kip']}  ·  HATA {s['hata']}  UYARI {s['uyari']}"
              f"  ·  kelime {s['kelime_once']} > {s['kelime_sonra']} ({s['kelime_oran']})")
        for i in s["ihlaller"]:
            print(f"  {i['seviye']:<5} [{i['denetim']}] {i['mesaj']}")
            for e in i["eksik"]:
                print(f"         - {e}")
            for f in i["fazla"]:
                print(f"         + {f}")
    return 0 if s["gecti"] else 1


if __name__ == "__main__":
    sys.exit(main())
