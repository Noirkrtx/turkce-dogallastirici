#!/usr/bin/env python3
"""dil_denetim.py: Türkçe metinde yapay zeka ve çeviri kokan kalıpları bulur.

Kural dosyası: ../references/kurallar.json (bu dosyaya göre göreli yol).

Kullanım:
    python3 dil_denetim.py metin.txt            # dosyadan
    echo "metin" | python3 dil_denetim.py       # stdin'den
    python3 dil_denetim.py metin.txt --json     # makine okur çıktı
    python3 dil_denetim.py metin.txt --esik 80  # puan < 80 ise çıkış kodu 1
    python3 dil_denetim.py metin.txt --tur uzun # uzun yazı (Article) modu
    python3 dil_denetim.py metin.txt --kip rapor # kip: post (varsayılan, eski
        davranış) | rapor | ogretici | akademik | sesli | telgraf
    python3 dil_denetim.py tez.txt --kip akademik --bolum bulgular

Bağımlılık yok (saf Python 3.8+). Rehber: references/kip-matrisi.md ve kurallar.json (kip seviyeleri).

Seviyeler:
    HATA  (-10) yayından önce düzelt (sahibin açık kuralı ya da kesin AI izi)
    UYARI (-4)  büyük ihtimalle düzelt; tek başına değil, kümelenince güçlü
    BILGI (-1)  bak, karar ver (meşru kullanımı olabilir)
Aynı kural en çok 3 kez puan düşürür; rapor hepsini listeler.

Betik bir yardımcıdır, hakem değil: sıfır uyarı metnin doğal olduğunu
kanıtlamaz. Son test, metni sesli okumak (bkz. rehber §1).
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import unicodedata
from dataclasses import dataclass, asdict

AGIRLIK = {"HATA": 10, "UYARI": 4, "BILGI": 1}
KURAL_TAVAN = 3  # bir kural en çok kaç kez puan düşürür

# ---------------------------------------------------------------- yardımcılar


def tr_kucuk(s: str) -> str:
    return s.replace("I", "ı").replace("İ", "i").lower()


def kelimeler(s: str) -> list[str]:
    return re.findall(r"[0-9A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîû'’]+", s)


@dataclass
class Bulgu:
    satir: int
    seviye: str
    kural: str
    mesaj: str
    alinti: str


@dataclass
class Cumle:
    metin: str
    satir: int
    paragraf: int


def cumlelere_bol(metin: str) -> list[Cumle]:
    """Paragraf (boş satır) ve satır sonu da sınır sayılır: postlarda her
    satır çoğu zaman ayrı bir cümledir."""
    cumleler: list[Cumle] = []
    paragraf = 0
    onceki_bos = True
    for i, satir in enumerate(metin.splitlines(), 1):
        if not satir.strip():
            onceki_bos = True
            continue
        if onceki_bos:
            paragraf += 1
            onceki_bos = False
        # ? ve ! ile biten parçaları da ayır; "..." / "…" tek sınır
        parcalar = re.split(r"(?<=[.!?…])\s+(?=\S)", satir.strip())
        for p in parcalar:
            p = p.strip()
            if p and kelimeler(p):
                cumleler.append(Cumle(p, i, paragraf))
    return cumleler


def kisalt(s: str, n: int = 70) -> str:
    s = s.strip()
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------------------------------------------------------------- kelime listeleri
# (desen, seviye, öneri). Desenler küçük harfe çevrilmiş metinde aranır.
AI_IFADELER: list[tuple[str, str, str]] = [
    # önem şişirme / jenerik değerlendirme
    (r"önemli bir rol", "UYARI", "neyi, nasıl etkilediğini somut söyle"),
    (r"kritik (bir )?öneme? sahip", "UYARI", "neden kritik, tek somut gerekçe yaz"),
    (r"\bkritik\b", "BILGI", "çoğu zaman 'önemli' ya da hiçbir şey yeter"),
    (r"büyük önem taşı", "UYARI", "önemini örnekle göster"),
    (r"göz ardı edilme(meli|memeli)", "UYARI", "kim, neyi atlamasın? etken yaz"),
    (r"derinlemesine", "UYARI", "'ayrıntılı' ya da sil"),
    (r"\bbu bağlamda\b", "UYARI", "sil; bağı cümlenin kendisi kursun"),
    (r"\bsöz konusu\b", "UYARI", "'bu', 'o' ya da adıyla an"),
    (r"\bsonuç olarak\b", "UYARI", "kapanış özeti yazma; son fikirle bitir"),
    (r"\bkısacası\b", "UYARI", "özet cümleyi sil"),
    (r"\bözetle\b", "UYARI", "özet cümleyi sil"),
    (r"büyük ölçüde", "BILGI", "'çoğu', 'epey' ya da sayı"),
    (r"dikkat çekici", "UYARI", "neyin şaşırttığını söyle"),
    (r"\boldukça\b", "BILGI", "'epey', 'baya' ya da sil"),
    (r"\bkapsamlı\b", "UYARI", "kaç sayfa / kaç madde, onu yaz"),
    (r"\bbütüncül\b", "UYARI", "sil ya da somutla"),
    (r"\bvazgeçilmez\b", "UYARI", "abartı; sil"),
    (r"\bhayati (önem|bir)", "UYARI", "abartı; sil"),
    (r"ışık tut", "UYARI", "'anlatıyor', 'gösteriyor'"),
    (r"altını çiz", "UYARI", "'diyor', 'vurguluyor' bile fazla; doğrudan aktar"),
    (r"\bele al(ıyor|acağ|ın|mak|dı)", "BILGI", "'anlatıyor', 'bakıyor'"),
    (r"olanak tanı", "UYARI", "'-ebiliyorsun'"),
    (r"imkan(ı)? sun|imkân(ı)? sun", "UYARI", "'-ebiliyorsun'"),
    (r"önem arz", "HATA", "bürokratik; 'önemli' bile gerekmez"),
    (r"değer kat", "UYARI", "neyi kolaylaştırdığını yaz"),
    (r"katkı sağla|katkıda bulun", "UYARI", "neye yaradığını yaz"),
    (r"gerçekleştir(il|di|mek|en)", "BILGI", "'yaptı', 'oldu'"),
    (r"potansiyel(ini)? (ortaya|açığa)", "UYARI", "sil"),
    (r"etkili bir şekilde|etkin bir şekilde", "UYARI", "sil"),
    (r"(kelimenin )?tam anlamıyla", "UYARI", "sil"),
    (r"her zamankinden daha", "UYARI", "kıyas noktası ver ya da sil"),
    (r"giderek (artan|önem)", "UYARI", "ne zamandan beri, ne kadar?"),
    (r"^günümüzde\b|\bgünümüzde,", "UYARI", "klişe girizgah; doğrudan başla"),
    (r"hızla (gelişen|değişen) dünya", "HATA", "klişe girizgah"),
    # çeviri kokusu
    (r"oyun değiştiri?ci|oyunun kurallarını", "HATA", "çeviri kalıbı (game changer)"),
    (r"günün sonunda", "HATA", "çeviri kalıbı (at the end of the day)"),
    (r"ezber boz", "UYARI", "reklam dili"),
    (r"bir sonraki seviye", "HATA", "çeviri kalıbı (next level)"),
    (r"dinamik dünyası", "HATA", "çeviri kalıbı (dynamic world of)"),
    (r"yolculuğ(u|una|unda)\b", "BILGI", "mecaz 'yolculuk' ise sil"),
    (r"derin(e)? dal", "HATA", "çeviri kalıbı (deep dive / delve)"),
    (r"masaya yatır", "BILGI", "klişe; 'baktım', 'inceledim'"),
    (r"\bunutmayın\b|\bunutma ki\b", "UYARI", "öğüt tonu; sil"),
    (r"hadi başlayalım|haydi başlayalım|gelin (birlikte )?bakalım", "HATA", "anons cümlesi; doğrudan başla"),
    (r"bu (yazıda|paylaşımda|flood'da|thread'de)", "UYARI", "yol haritası anonsu"),
    # sohbet / asistan artıkları
    (r"umarım (yardımcı|faydalı) olur", "HATA", "asistan artığı"),
    (r"\belbette\b|\btabii ki\b", "BILGI", "asistan açılışı mı? bak"),
    (r"harika bir soru", "HATA", "asistan artığı"),
    (r"yalnız değilsin", "HATA", "terapist modu"),
    # sahte samimiyet / vurgu anonsu
    (r"dürüst olmak gerekirse", "UYARI", "doğrudan söyle"),
    (r"gerçek şu ki|işin aslı şu", "UYARI", "doğrudan söyle"),
    (r"\basıl (mesele|soru|önemli olan)", "UYARI", "etiketi vuruştan sonra koy ya da sil"),
    (r"işte (tam da )?bu yüzden", "UYARI", "vurgu anonsu"),
    (r"(sadece|yalnızca) .{1,40}? değil,? (aynı zamanda|ayrıca)", "HATA", "'sadece X değil, Y' kalıbı"),
    (r"\bbir (araç|ürün|kitap|şey) değil,", "UYARI", "'X değil, Y' kalıbı"),
    # edilgen / bürokratik
    (r"gerekmektedir|gerekmekte\b", "HATA", "'lazım', 'gerek'"),
    (r"(ıl|il|ul|ül|n)malıdır|(ıl|il|ul|ül|n)melidir", "UYARI", "edilgen öğüt; kim yapsın?"),
    (r"söylenebilir|denilebilir|ifade edilebilir", "UYARI", "kaçamak edilgen; 'bence' de"),
    (r"(çerçevesinde|doğrultusunda|kapsamında|noktasında)", "BILGI", "bürokratik ek; yığılmışsa sil"),
]

# sayaçla bakılanlar: (desen, eşik_bilgi, eşik_uyarı, açıklama)
SAYAC_IFADELER = [
    (r"\baslında\b", 1, 2, "'aslında' tik halinde"),
    (r"\bpeki\b", 1, 2, "'peki' ile soru açma kalıbı"),
    (r"\bayrıca\b", 1, 2, "ekleme bağlacı yığılması"),
    (r"\bise\b", 3, 5, "'ise' karşıtlık yığılması"),
]

BAGLAC_ACILIS = ("ayrıca", "bununla birlikte", "öte yandan", "bunun yanı sıra",
                 "dolayısıyla", "buna ek olarak", "ek olarak", "üstelik", "dahası",
                 "sonuç olarak", "kısacası", "bu bağlamda", "nitekim")

# şapka: gerekli olanlar (anlam ayırt eder, TDK) ayrı seviyede
SAPKA_GEREKLI = {"hâlâ": "hala (babanın kız kardeşi)", "kâr": "kar (yağış)",
                 "hâl": "hal (pazar yeri)", "âdet": "adet (sayı)",
                 "âlem": "alem (bayrak)", "âşık": "aşık (kemik)",
                 "şûra": "şura (orası)", "âdem": "adem (yokluk)"}

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F02F"
    "\U0001F0A0-\U0001F0FF\U0001F100-\U0001F1FF\U0001F200-\U0001F2FF"
    "\u2B50\u2B55\u203C\u2049\u27B0]"
)
KALIN_RE = re.compile("[\U0001D400-\U0001D7FF]")
URL_RE = re.compile(r"https?://\S+|www\.\S+")

# ---------------------------------------------------------------- denetimler


def _eski_bulgular(metin: str, tur: str = "post") -> tuple[list[Bulgu], dict]:
    """Eski (post) kural seti. Bu fonksiyonun gövdesi geriye uyumluluk için
    değiştirilmez; kip davranışı denetle_kip() içinde üstüne kurulur."""
    bulgular: list[Bulgu] = []
    satirlar = metin.splitlines()
    cumleler = cumlelere_bol(metin)

    def ekle(satir, seviye, kural, mesaj, alinti=""):
        bulgular.append(Bulgu(satir, seviye, kural, mesaj, kisalt(alinti)))

    # --- satır bazlı desenler
    for no, ham in enumerate(satirlar, 1):
        if not ham.strip():
            continue
        satir = URL_RE.sub(" URL ", ham)
        kucuk = tr_kucuk(satir)

        # 1. iki nokta
        for m in re.finditer(r":", satir):
            once, sonra = satir[: m.start()], satir[m.end():]
            if re.search(r"\d$", once) and re.match(r"\d", sonra):
                continue  # saat, oran: 14:30, 1:2
            bas = tr_kucuk(once.strip())
            if bas in ("kaynak", "kaynaklar", "not", "kaynak ve not"):
                ekle(no, "BILGI", "iki-nokta",
                     "'Kaynak:' satırı kabul; yine de 'kaynak →' ya da düz satır daha doğal", ham)
                continue
            kalan = sonra.strip()
            if re.search(r"\b(şu|şöyle|basit|belli|net|ortada|açık|sorun|soru|mesele|cevap|fark|sır)\s*$",
                         tr_kucuk(once.strip())):
                ekle(no, "HATA", "iki-nokta-tanitim",
                     "'... şu: / basit: / mesele şu:' anons kalıbı; etiketi at, iddiayı düz söyle", ham)
            elif not kalan:
                ekle(no, "UYARI", "iki-nokta",
                     "satır sonu ':' (başlık + liste kalıbı); cümleyle bağla", ham)
            elif len(kelimeler(kalan)) <= 8 and not re.search(r"[,;]", kalan):
                ekle(no, "HATA", "iki-nokta-tanitim",
                     "':' ile tanıtım/vuruş kalıbı (sahibin yasağı); cümleyi düz kur", ham)
            else:
                ekle(no, "UYARI", "iki-nokta",
                     "':' + açıklama; postta genelde gereksiz, virgül ya da yeni cümle", ham)

        # 2. tireler
        if "—" in satir:
            ekle(no, "HATA", "em-dash", "uzun tire (—); virgül, nokta ya da parantez kullan", ham)
        if "–" in satir:
            ekle(no, "HATA", "en-dash", "orta tire (–); aralıkta '-' kullan, cümlede virgül", ham)
        if re.search(r"\s-\s", satir) and not re.match(r"\s*-\s", satir):
            ekle(no, "UYARI", "tire-ara", "boşluklu tire ara söz olarak; virgül ya da parantez", ham)

        # 3. şapkalı harfler
        for k in re.findall(r"\w*[âîûÂÎÛ]\w*", satir):
            kk = tr_kucuk(k)
            kok = next((g for g in SAPKA_GEREKLI if kk.startswith(g)), None)
            if kok:
                ekle(no, "BILGI", "sapka-gerekli",
                     f"'{k}' anlam ayırt eder ({SAPKA_GEREKLI[kok]}); kalabilir, tutarlı ol", ham)
            elif kk.startswith("zekâ") or kk.startswith("zekâ"):
                ekle(no, "HATA", "sapka-zeka", f"'{k}' → şapkasız 'zeka' (sahibin kuralı)", ham)
            else:
                ekle(no, "UYARI", "sapka",
                     f"'{k}' → şapkasız yaz ({unicodedata.normalize('NFKD', k).encode('ascii','ignore').decode() or k})", ham)

        # 4. -mektedir / -maktadır ve -dır yığını
        for m in re.finditer(r"\w+m[ae]kt[ae]d[ıi]r(l[ae]r)?\b", kucuk):
            ekle(no, "HATA", "mektedir", f"'{m.group(0)}' resmi yazı kipi; '-iyor' ya da geniş zaman", ham)
        for m in re.finditer(r"\w+m[ıiuü]şt[ıiuü]r(l[ae]r)?\b", kucuk):
            ekle(no, "UYARI", "mistir", f"'{m.group(0)}' kesinlik/resmiyet eki; postta '-di' ya da '-miş' yeter", ham)

        # 5. AI ifadeleri
        for desen, seviye, oneri in AI_IFADELER:
            for m in re.finditer(desen, kucuk):
                ekle(no, seviye, "ai-ifade", f"'{m.group(0)}' → {oneri}", ham)

        # 8. kalın Unicode
        if KALIN_RE.search(satir):
            ekle(no, "HATA", "kalin-unicode", "Unicode kalın harf (bu hesapta yok; arama ve ekran okuyucu bozulur)", ham)

        # noktalı virgül
        if satir.count(";") >= 1:
            ekle(no, "BILGI", "noktali-virgul", "';' postta seyrek; çoğu zaman nokta ya da virgül", ham)

        # 6. üçlü virgül listesi (X, Y ve Z / X, Y, Z)
        for c in re.split(r"(?<=[.!?…:])\s+", satir):
            parcalar = [p.strip() for p in re.split(r",|\sve\s|\sile\s", c) if p.strip()]
            if c.count(",") >= 2 and len(kelimeler(c)) <= 4:
                ekle(no, "UYARI", "kesik-parca",
                     "virgülle doğranmış kısa parça (yapay vuruculuk); düz cümle kur", c)
                continue
            if c.count(",") >= 1 and len(parcalar) >= 3:
                kisa = [p for p in parcalar[-3:] if 1 <= len(kelimeler(p)) <= 3]
                if len(kisa) == 3 and (c.count(",") >= 2 or re.search(r",[^,]+\sve\s", c)):
                    ekle(no, "UYARI", "uclu-liste",
                         "üçlü sıralama; ikiye indir, birini aç ya da sıralamayı boz", c)

    # --- metin geneli sayaçlar
    kucuk_tum = tr_kucuk(URL_RE.sub(" ", metin))
    for desen, e_bilgi, e_uyari, aciklama in SAYAC_IFADELER:
        n = len(re.findall(desen, kucuk_tum))
        if n >= e_uyari:
            ekle(0, "UYARI", "tekrar", f"{aciklama}: {n} kez")
        elif n >= e_bilgi and desen in (r"\bpeki\b",):
            ekle(0, "BILGI", "tekrar", f"{aciklama}: {n} kez")

    emojiler = EMOJI_RE.findall(metin)
    if len(emojiler) > 3:
        ekle(0, "HATA", "emoji", f"{len(emojiler)} emoji (en çok 1)")
    elif len(emojiler) > 1:
        ekle(0, "UYARI", "emoji", f"{len(emojiler)} emoji (en çok 1)")

    # --- cümle bazlı denetimler
    uz = [len(kelimeler(c.metin)) for c in cumleler]

    # 7. soru + hemen cevap
    for a, b in zip(cumleler, cumleler[1:]):
        if a.metin.rstrip().endswith("?") and a.paragraf == b.paragraf \
                and not b.metin.rstrip().endswith("?") and len(kelimeler(b.metin)) <= 7:
            ekle(a.satir, "UYARI", "soru-cevap",
                 "soru sorup hemen kısa cevap veriyor; doğrudan söyle ya da soruyu açık bırak",
                 a.metin + " " + b.metin)

    # bağlaçla açılış
    for c in cumleler:
        kc = tr_kucuk(c.metin)
        for b in BAGLAC_ACILIS:
            if kc.startswith(b + " ") or kc.startswith(b + ","):
                ekle(c.satir, "UYARI", "baglac-acilis", f"cümle '{b}' ile açılıyor; bağlaçsız bağla", c.metin)

    # açılış tekrarı
    ilkler: dict[str, list[int]] = {}
    for c in cumleler:
        k = kelimeler(c.metin)
        if k:
            ilkler.setdefault(tr_kucuk(k[0]), []).append(c.satir)
    for kel, nolar in ilkler.items():
        if len(nolar) >= 3 and len(nolar) >= len(cumleler) / 4:
            ekle(nolar[0], "UYARI", "acilis-tekrar",
                 f"{len(nolar)} cümle '{kel}' ile açılıyor (satır {', '.join(map(str, nolar))})")

    # cümle sonu kafiyesi: aynı ekle biten yüklemler (-acağım, -maktadır, -iyor...)
    sonlar: dict[str, list[int]] = {}
    for c in cumleler:
        k = kelimeler(c.metin)
        if k and len(k[-1]) >= 5:
            sonlar.setdefault(tr_kucuk(k[-1])[-5:], []).append(c.satir)
    for ek, nolar in sonlar.items():
        if len(nolar) >= 3 and len(nolar) >= len(cumleler) / 3:
            ekle(nolar[0], "UYARI", "son-kafiye",
                 f"{len(nolar)} cümle '-{ek}' ile bitiyor (satır {', '.join(map(str, nolar))}); "
                 "birini isim cümlesi, soru ya da devrik yap")

    # kesik cümle yığını (3+ art arda ≤4 kelime)
    seri = 0
    for i, n in enumerate(uz):
        seri = seri + 1 if n <= 4 else 0
        if seri == 3:
            ekle(cumleler[i].satir, "UYARI", "kesik-yigin",
                 "art arda 3+ çok kısa cümle (yapay vuruculuk); bazılarını virgülle bağla",
                 cumleler[i].metin)

    # 10. cümle uzunluğu tekdüzeliği
    istat = {}
    if len(uz) >= 4:
        ort = statistics.mean(uz)
        sd = statistics.pstdev(uz)
        cv = sd / ort if ort else 0
        istat = {"cumle": len(uz), "ort_kelime": round(ort, 1), "std": round(sd, 1), "cv": round(cv, 2)}
        if cv < 0.30:
            ekle(0, "UYARI", "tekduze-ritim",
                 f"cümle uzunlukları çok benzer (ort {ort:.1f}, std {sd:.1f}, cv {cv:.2f}); bir kısa bir uzun ekle")
        elif cv < 0.40:
            ekle(0, "BILGI", "tekduze-ritim", f"ritim biraz düz (cv {cv:.2f})")
        if tur == "post" and ort > 18:
            ekle(0, "UYARI", "uzun-cumle", f"ortalama cümle {ort:.1f} kelime; post için uzun (hedef 6-14)")
    elif uz:
        istat = {"cumle": len(uz), "ort_kelime": round(statistics.mean(uz), 1)}

    # 11. paragraf sonu vurucu cümle
    paragraflar: dict[int, list[Cumle]] = {}
    for c in cumleler:
        paragraflar.setdefault(c.paragraf, []).append(c)
    cok_cumleli = [p for p in paragraflar.values() if len(p) >= 2]
    vurucu = []
    for p in cok_cumleli:
        son = len(kelimeler(p[-1].metin))
        digerleri = [len(kelimeler(c.metin)) for c in p[:-1]]
        if son <= 6 and son <= 0.6 * statistics.mean(digerleri):
            vurucu.append(p[-1])
    if len(cok_cumleli) >= 2 and len(vurucu) >= 2 and len(vurucu) >= len(cok_cumleli) / 2:
        for c in vurucu:
            ekle(c.satir, "UYARI", "vurucu-kapanis",
                 "paragraf kısa vurucu cümleyle kapanıyor (kalıp tekrarı)", c.metin)

    # sayılı listeler / madde imleri (postta)
    madde = [i for i, s in enumerate(satirlar, 1) if re.match(r"\s*([-•*▪]|\d+[.)])\s+", s)]
    if tur == "post" and len(madde) >= 3:
        ekle(madde[0], "BILGI", "madde-liste", f"{len(madde)} madde satırı; postta düz cümle daha doğal (Denedim adımları hariç)")

    # okunabilirlik (Ateşman 1997)
    hece = sum(len(re.findall(r"[aeıioöuüâîû]", tr_kucuk(w))) for c in cumleler for w in kelimeler(c.metin))
    kel_say = sum(uz)
    if kel_say and cumleler:
        atesman = 198.825 - 40.175 * (hece / kel_say) - 2.610 * (kel_say / len(cumleler))
        istat["atesman"] = round(min(100.0, max(0.0, atesman)), 1)
        if tur == "post" and atesman < 50:
            ekle(0, "BILGI", "okunabilirlik", f"Ateşman {atesman:.0f} (zor); post için 70+ hedefle")

    return bulgular, istat


def _puanla(bulgular: list[Bulgu]) -> int:
    sayac: dict[str, int] = {}
    ceza = 0
    for b in bulgular:
        anahtar = b.kural
        sayac[anahtar] = sayac.get(anahtar, 0) + 1
        if sayac[anahtar] <= KURAL_TAVAN:
            ceza += AGIRLIK[b.seviye]
    return max(0, 100 - ceza)


def denetle(metin: str, tur: str = "post") -> dict:
    """Eski arayüz: post kipi (varsayılan). Çıktı biçimi ve puanı değişmez;
    yalnız TDK yazım ve alan sözlüğü HATA'ları eklenir (bkz. denetle_kip)."""
    return denetle_kip(metin, "post", tur=tur)



# ================================================================ kipler
# Kip katmanı (turkce-dogallastirici). Seviyeler references/kurallar.json'da.

import os  # noqa: E402

KIPLER = ("post", "rapor", "ogretici", "akademik", "sesli", "telgraf")
KIP_ESIK = {"post": 85, "rapor": 80, "ogretici": 75, "sesli": 85, "telgraf": 85, "akademik": None}
KIP_ORT_UST = {"rapor": 16, "ogretici": 20, "akademik": 20, "sesli": 16}
_SIRA = {"BILGI": 1, "UYARI": 2, "HATA": 3}

_KURAL_YOLLARI = [
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "references", "kurallar.json"),
]
_KURALLAR = None


def kurallar() -> dict:
    global _KURALLAR
    if _KURALLAR is None:
        for yol in _KURAL_YOLLARI:
            if os.path.exists(yol):
                with open(yol, encoding="utf-8") as f:
                    _KURALLAR = json.load(f)
                break
        else:
            raise SystemExit("kurallar.json bulunamadı (references/)")
    return _KURALLAR


def tr_kucuk_nfc(s: str) -> str:
    return tr_kucuk(unicodedata.normalize("NFC", s))


# ---- maske: denetim dışı bölgeler (alıntı, URL, DOI, atıf, şablon, kod, kaynakça)
_SABLON_ETIKET = re.compile(
    r"(?i)\b(Sonuç / köprü|Sor / bekle|Şimdi söyle|Hedef|Süre|Sonuç|Kaynak(?:lar)?|Not|Kısa sonuç|"
    r"Senden istenen|Tam rapor|Dayanak|Bağlantı|Konu|Sayaç|Kaldığı yer|Donanım|İzleme|Gerekçe)\s*:")
_KAYNAKCA_BASLIK = re.compile(r"^\s*(#+\s*)?\**\s*(kaynaklar|kaynakça|referanslar|references)\s*\**\s*:?\s*$", re.I)
MASKELER = [
    (re.compile(r"```.*?```", re.S), " xkodx "),
    (re.compile(r"`[^`\n]+`"), " xkodx "),
    (re.compile(r"https?://\S+|www\.\S+"), " xurlx "),
    (re.compile(r"\bdoi:\s*\S+|\b10\.\d{4,}/\S+", re.I), " xdoix "),
    (re.compile(r"\bPMID:?\s*\d+|\barXiv:\s*\d{4}\.\d{4,5}", re.I), " xpmidx "),
    (re.compile(r"\{\{[^}]*\}\}"), " xyerx "),
    (re.compile(r"\[(TIK|BEKLE|SOR[^\]]*|AUTHOR TO INSERT|CITATION NEEDED|ÖLÇÜM|[A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?: [a-zçğıöşü]+){0,3})\]"), " xyerx "),
    (re.compile(r"</?dfn>"), ""),
    (re.compile(r"«[^»\n]*»"), " xalintix "),
    (re.compile(r"“[^”\n]{0,400}”"), " xalintix "),
    (re.compile(r"\"[^\"\n]{0,400}\""), " xalintix "),
    (re.compile(r"\s?\[\d+(?:[,\-–]\s?\d+)*\]"), ""),
    (re.compile(r"\s?\((?:\d+(?:\s?[,\-–]\s?\d+)*)\)"), ""),
    (re.compile(r"\s?\([A-ZÇĞİÖŞÜ][^()\n]{0,60}?,\s?\d{4}[a-z]?\)"), ""),
    (re.compile(r"^MEDIA:.*$", re.M), ""),
]


def maskele(metin: str) -> str:
    satirlar = metin.splitlines()
    for i, s in enumerate(satirlar):
        if _KAYNAKCA_BASLIK.match(s):
            satirlar = satirlar[:i]
            break
    m = "\n".join(satirlar)
    for desen, yerine in MASKELER:
        m = desen.sub(yerine, m)
    return m


_KISALTMA_NOKTA = {"dr", "prof", "doç", "uzm", "vb", "vs", "ör", "örn", "bkz", "s", "no", "yy", "st", "dk", "sa", "yrd"}


def cumle_satirlari(metin: str) -> str:
    """Paragraf içi cümleleri ayrı satıra alır (boş satırlar = paragraf korunur)."""
    out = []
    for satir in metin.splitlines():
        if not satir.strip():
            out.append("")
            continue
        parcalar, bas = [], 0
        for m in re.finditer(r"[.!?…]+[\"”’)]?\s+(?=[\"“(\[]?[A-ZÇĞİÖŞÜ0-9])", satir):
            onceki = re.findall(r"[\wçğıöşüÇĞİÖŞÜ]+$", satir[bas:m.start()])
            tok = tr_kucuk(onceki[0]) if onceki else ""
            if tok in _KISALTMA_NOKTA or re.fullmatch(r"\d+", tok) or re.fullmatch(r"[a-zçğıöşü]", tok):
                continue
            parcalar.append(satir[bas:m.end()].strip())
            bas = m.end()
        parcalar.append(satir[bas:].strip())
        out.extend(p for p in parcalar if p)
    return "\n".join(out)


def _etiket_muaf(metin: str) -> str:
    return _SABLON_ETIKET.sub(lambda m: m.group(1) + " ·", metin)


# ---- özel kurallar
_ISTAT_ONCESI = {"or", "rr", "hr", "auc", "ga", "ci", "nnt", "nnh", "lr", "p", "arr", "rrr", "sd", "ss"}


def _ondalik_nokta(cumle: str):
    for m in re.finditer(r"(?<![\d.])(\d+)\.(\d{1,2})(?![\d.])", cumle):
        once = cumle[: m.start()]
        onceki = re.findall(r"([^\s(]+)\s*[<>=≤≥]?\s*$", once)
        tok = onceki[0] if onceki else ""
        if re.search(r"[A-Za-zçğıöşü]-?$", once[-1:] if once else ""):
            continue  # GPT-5.2, v1.5
        if re.match(r"['’]", cumle[m.end():m.end() + 1]) and len(m.group(1)) == 2:
            continue  # 17.30'da saat
        if len(m.group(1)) == 2 and len(m.group(2)) == 2 and int(m.group(1)) < 24 and int(m.group(2)) < 60 \
                and tr_kucuk(tok.strip("<>=")) not in _ISTAT_ONCESI:
            continue  # 08.30 saat
        tk = tr_kucuk(tok.strip("<>=≤≥(:"))
        if re.match(r"(tablo|şekil|bölüm|ek|madde|kısım|başlık)", tk):
            continue
        if tok[:1].isupper() and tk not in _ISTAT_ONCESI and not tok.isupper():
            continue  # Opus 4.7, Claude 1.0 gibi ürün sürümü
        yield m.group(0)


def _ozel_kurallar(kod: str, cumleler: list[str], kip: str, bolum: str | None):
    """(cumle_no, alinti, ek_mesaj) üretir."""
    if kod == "tdk-ondalik-nokta":
        for i, c in enumerate(cumleler, 1):
            for v in _ondalik_nokta(c):
                yield i, c, f"'{v}'"
    elif kod == "tdk-rakamla-baslama":
        for i, c in enumerate(cumleler, 1):
            if re.match(r"\d", c) and not re.match(r"\d+(\.\d+)*[.)]?\s+\S+(\s+\S+){0,7}$", c) \
                    and not re.match(r"\d+(\.\d+)*[.)]\s", c):
                yield i, c, ""
    elif kod == "cev-tarafindan":
        n = sum(len(re.findall(r"\btarafından\b", tr_kucuk_nfc(c))) for c in cumleler)
        if n >= 3:
            yield 0, "", f"{n} kez"
    elif kod == "cev-bir-yigini":
        for i, c in enumerate(cumleler, 1):
            n = len(re.findall(r"\bbir\b", tr_kucuk_nfc(c)))
            if n >= 3:
                yield i, c, f"{n} 'bir'"
    elif kod == "cev-digi-zinciri":
        for i, c in enumerate(cumleler, 1):
            n = len(re.findall(r"\b\w+(dığı|diği|duğu|düğü|tığı|tiği|tuğu|tüğü)\w*", tr_kucuk_nfc(c)))
            if n >= 3:
                yield i, c, f"{n} sıfat-fiil"
    elif kod == "cev-olarak-yigini":
        for i, c in enumerate(cumleler, 1):
            k = tr_kucuk_nfc(c)
            n = len(re.findall(r"\bolarak\b", k)) - len(re.findall(r"\b(tedavi|profilaksi|ilaç) olarak\b", k))
            if n >= 2:
                yield i, c, f"{n} 'olarak'"
    elif kod == "yap-oncelikle":
        kal = ("öncelikle", "sonuç olarak") if kip in ("ogretici", "akademik") else ("öncelikle",)
        for i, c in enumerate(cumleler, 1):
            k = tr_kucuk_nfc(c)
            if any(k.startswith(x + " ") or k.startswith(x + ",") for x in kal):
                yield i, c, ""
    elif kod == "yap-arak-zinciri":
        for i, c in enumerate(cumleler, 1):
            n = len([w for w in re.findall(r"\b\w+(?:arak|erek)\b", tr_kucuk_nfc(c)) if w != "olarak"])
            if n >= 2:
                yield i, c, f"{n} zarf-fiil"
    elif kod == "yap-bu-durum":
        for i, c in enumerate(cumleler, 1):
            if re.match(r"(bu durum|bu da |bu sayede)", tr_kucuk_nfc(c)):
                yield i, c, ""
    elif kod == "yap-sonuc-acilis":
        for i, c in enumerate(cumleler, 1):
            if re.match(r"sonu[çc]\w*\b(?! ·)", tr_kucuk_nfc(c)) and not re.match(r"sonuç olarak", tr_kucuk_nfc(c)):
                yield i, c, ""
    elif kod == "yap-sira-sozu":
        for i, c in enumerate(cumleler, 1):
            if re.match(r"(ilk olarak|ikinci olarak|üçüncü olarak|son olarak|birincisi|ikincisi|üçüncüsü)\b", tr_kucuk_nfc(c)):
                yield i, c, ""
    elif kod == "yap-uzun-ort":
        uz = [len(kelimeler(c)) for c in cumleler]
        ust = KIP_ORT_UST.get(kip)
        if ust and len(uz) >= 3 and statistics.mean(uz) > ust:
            yield 0, "", f"ortalama {statistics.mean(uz):.1f} kelime (hedef ≤{ust}, K-24)"
    elif kod == "yap-kisa-ort":
        uz = [len(kelimeler(c)) for c in cumleler]
        if len(uz) >= 4 and statistics.mean(uz) < 12:
            yield 0, "", f"ortalama {statistics.mean(uz):.1f} kelime (öğretici hedef 15-20, K-24)"
    elif kod == "aka-mektedir-yogunluk":
        sonlar = [bool(re.search(r"m[ae]kt[ae]d[ıi]r(l[ae]r)?[.!?]*$", tr_kucuk_nfc(c).rstrip())) for c in cumleler]
        if len(sonlar) >= 4 and sum(sonlar) / len(sonlar) > 0.5:
            yield 0, "", f"{sum(sonlar)}/{len(sonlar)} yüklem"
    elif kod == "aka-mistir-bolum":
        if bolum in ("yontem", "bulgular"):
            for i, c in enumerate(cumleler, 1):
                for m in re.finditer(r"\w+m[ıiuü]şt[ıiuü]r(l[ae]r)?\b", tr_kucuk_nfc(c)):
                    yield i, c, f"'{m.group(0)}'"
    elif kod == "ses-kisaltma":
        for i, c in enumerate(cumleler, 1):
            for w in re.findall(r"[0-9A-Za-zÇĞİÖŞÜçğıöşü₂]+", c):
                if sum(ch.isupper() for ch in w) >= 2 and not w.startswith("x"):
                    yield i, c, f"'{w}'"
    elif kod == "ses-uzun-cumle":
        for i, c in enumerate(cumleler, 1):
            if len(kelimeler(c)) > 25:
                yield i, c, f"{len(kelimeler(c))} kelime"


def _yeni_bulgular(ham: str, maskeli: str, kip: str, bolum: str | None) -> list[Bulgu]:
    bulgular: list[Bulgu] = []
    cumleler = [c for c in cumle_satirlari(maskeli).splitlines() if c.strip() and kelimeler(c)]
    ham_satirlar = [c for c in cumle_satirlari(ham).splitlines() if c.strip()]
    for k in kurallar()["yeni"]:
        sev = k["seviye"].get(kip, "KAPALI")
        if sev == "KAPALI":
            continue
        mesaj = f"{k['aciklama']} → {k['oneri']} [{k['katalog']}]"
        desen = k["desen"]
        if desen == "OZEL":
            for no, alinti, ek in _ozel_kurallar(k["kod"], cumleler, kip, bolum):
                bulgular.append(Bulgu(no, sev, k["kod"], (ek + ": " if ek else "") + mesaj, kisalt(alinti)))
            continue
        kaynak, ham_mi = (ham_satirlar, True) if desen.startswith("HAM:") else (cumleler, False)
        rx = re.compile(desen[4:] if ham_mi else desen)
        for no, c in enumerate(kaynak, 1):
            for m in rx.finditer(c if ham_mi else tr_kucuk_nfc(c)):
                bulgular.append(Bulgu(no, sev, k["kod"], f"'{m.group(0)}': {mesaj}", kisalt(c)))
    return bulgular


def _uygula(eylem: str, seviye: str) -> str | None:
    if eylem == "=":
        return seviye
    if eylem == "KAPALI":
        return None
    if eylem.startswith("<"):
        tavan = eylem[1:]
        return seviye if _SIRA[seviye] <= _SIRA[tavan] else tavan
    return eylem


def denetle_kip(metin: str, kip: str = "post", tur: str = "post", bolum: str | None = None,
                eski: bool = False) -> dict:
    metin = unicodedata.normalize("NFC", metin) if kip != "post" else metin
    if kip == "post":
        # Eski davranış aynen + kesin yazım (TDK) ve alan sözlüğü kuralları.
        bulgular, istat = _eski_bulgular(metin, tur)
        if not eski:
            bulgular += _yeni_bulgular(metin, maskele(metin), "post", None)
        puan = _puanla(bulgular)
        karar = "yayına uygun" if puan >= 85 else "elden geçir" if puan >= 70 else "yeniden yaz"
        bulgular.sort(key=lambda b: (b.satir, -AGIRLIK[b.seviye]))
        return {"puan": puan, "karar": karar, "istatistik": istat,
                "sayim": {s: sum(1 for b in bulgular if b.seviye == s) for s in AGIRLIK},
                "bulgular": [asdict(b) for b in bulgular]}

    maskeli = _etiket_muaf(maskele(metin))
    hazir = cumle_satirlari(maskeli)
    eski, istat = _eski_bulgular(hazir, "kip")
    harita = kurallar()["eski"]
    bulgular: list[Bulgu] = []
    for b in eski:
        eylem = harita.get(b.kural, {}).get(kip, "=")
        if b.kural == "ai-ifade" and kip == "akademik" and re.search(r"sonuç olarak|kritik|gerçekleştir|kapsamında|çerçevesinde|doğrultusunda|malıdır|melidir", b.mesaj):
            eylem = "BILGI"
        yeni_sev = _uygula(eylem, b.seviye)
        if yeni_sev:
            b.seviye = yeni_sev
            bulgular.append(b)
    bulgular += _yeni_bulgular(metin, maskeli, kip, bolum)

    # okunurluk: yalnız bilgi, puan düşürmez
    try:
        sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
        import okunurluk  # type: ignore
        ok = okunurluk.olc(maskeli, kip)
        for a in ("atesman", "bezirci_yilmaz", "kip_karsilastirma", "not"):
            if a in ok:
                istat["okunurluk_" + a if a != "atesman" else "atesman"] = ok[a]
    except Exception as e:  # pragma: no cover
        istat["okunurluk_hata"] = str(e)
    cs = [c for c in hazir.splitlines() if c.strip() and kelimeler(c)]
    if cs:
        istat["virgul_cumle"] = round(sum(c.count(",") for c in cs) / len(cs), 2)
        istat["uzun25_orani"] = round(sum(1 for c in cs if len(kelimeler(c)) > 25) / len(cs), 2)

    sayim = {s: sum(1 for b in bulgular if b.seviye == s) for s in AGIRLIK}
    esik = KIP_ESIK[kip]
    if kip == "akademik":
        puan, karar = None, ("HATA yok" if sayim["HATA"] == 0 else "HATA'ları düzelt") + " (akademik kipte puan yok, STY-30)"
    else:
        puan = _puanla(bulgular)
        karar = ("teslime uygun" if puan >= esik and sayim["HATA"] == 0 else
                 "elden geçir" if puan >= esik - 15 else "yeniden yaz")
    bulgular.sort(key=lambda b: (b.satir, -AGIRLIK[b.seviye]))
    return {"kip": kip, "puan": puan, "karar": karar, "esik": esik, "istatistik": istat,
            "sayim": sayim, "bulgular": [asdict(b) for b in bulgular]}


def yazdir(sonuc: dict) -> None:
    kip = sonuc.get("kip", "post")
    puan = "yok" if sonuc["puan"] is None else f"{sonuc['puan']}/100"
    bas = f"PUAN {puan}" if kip == "post" else f"KİP {kip}  ·  PUAN {puan}"
    print(f"{bas}  ·  {sonuc['karar']}  ·  "
          f"HATA {sonuc['sayim']['HATA']}  UYARI {sonuc['sayim']['UYARI']}  BILGI {sonuc['sayim']['BILGI']}")
    if sonuc["istatistik"]:
        print("istatistik: " + ", ".join(f"{k}={v}" for k, v in sonuc["istatistik"].items()))
    print("-" * 72)
    birim = "satır" if kip == "post" else "cümle"
    for b in sonuc["bulgular"]:
        yer = f"{birim} {b['satir']:>2}" if b["satir"] else "genel   "
        print(f"{yer}  {b['seviye']:<5}  [{b['kural']}] {b['mesaj']}")
        if b["alinti"]:
            print(f"           » {b['alinti']}")
    if not sonuc["bulgular"]:
        print("Bulgu yok. Yine de sesli oku.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Türkçe metin için AI/çeviri kalıp denetimi (kipli)")
    ap.add_argument("dosya", nargs="?", help="metin dosyası (yoksa stdin)")
    ap.add_argument("--json", action="store_true", help="JSON çıktı")
    ap.add_argument("--esik", type=int, default=None,
                    help="bu puanın altında çıkış kodu 1 (post varsayılanı 70; diğer kiplerde kip eşiği)")
    ap.add_argument("--tur", choices=["post", "uzun"], default="post",
                    help="post (varsayılan) ya da uzun yazı/Article: uzun cümle ve madde uyarıları gevşer")
    ap.add_argument("--kip", choices=list(KIPLER), default="post",
                    help="post (varsayılan, eski davranış) | rapor | ogretici | akademik | sesli | telgraf")
    ap.add_argument("--eski", action="store_true",
                    help="yalnız post: 4 Kasım 2026 öncesi kural seti (TDK ve alan sözlüğü yok)")
    ap.add_argument("--bolum", choices=["giris", "genel", "yontem", "bulgular", "tartisma", "sonuc"],
                    help="akademik kipte tez bölümü (yontem/bulgular: '-mıştır' UYARI)")
    a = ap.parse_args()
    if a.dosya:
        with open(a.dosya, encoding="utf-8") as f:
            metin = f.read()
    else:
        metin = sys.stdin.read()
    if "\\n" in metin and metin.strip().count("\n") == 0:
        metin = metin.replace("\\n", "\n")  # tek satırda literal \n verilmişse
    sonuc = denetle_kip(metin, a.kip, tur=a.tur, bolum=a.bolum, eski=a.eski)
    if a.json:
        print(json.dumps(sonuc, ensure_ascii=False, indent=2))
    else:
        yazdir(sonuc)
    if a.kip == "akademik":
        return 0 if sonuc["sayim"]["HATA"] == 0 else 1
    esik = a.esik if a.esik is not None else (70 if a.kip == "post" else KIP_ESIK[a.kip])
    return 0 if sonuc["puan"] >= esik else 1


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # `| head` ile sessiz çık
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
