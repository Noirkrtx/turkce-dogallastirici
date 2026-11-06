#!/usr/bin/env python3
"""Eval koşturucu: her vakada skill çıktısı ve skill'siz temel çıktı kod ölçütleriyle sınanır.

Kullanım:
    python3 evals/calistir.py                 # bütün vakalar
    python3 evals/calistir.py V07a V13        # seçili vakalar

Her vaka klasörü: girdi.txt, vaka.yaml, cikti_skill.txt, cikti_temel.txt
(V13: cikti_skill_<kip>.txt / cikti_temel_<kip>.txt). Model ölçütleri
(anlam) evals/model_degerlendirme.yaml'dan okunur; kodla ölçülmez.
Çıktı: evals/sonuclar/<tarih>.json ve <tarih>-tablo.md (git dışı). Çıkış kodu 1:
skill çıktısında başarısız vaka var.
Bağımlılık: PyYAML (pip install pyyaml).
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

import yaml

B = Path(__file__).resolve().parent
sys.path.insert(0, str(B.parent / "scripts"))
import dil_denetim as dd  # noqa: E402
import koru  # noqa: E402


def oku(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def denetle(metin, kip, tur="post", bolum=None):
    return dd.denetle_kip(metin, kip, tur=tur, bolum=bolum)


def kokler(s):
    return {koru.tr_kucuk(w)[:5] for w in koru.kelimeler(s) if len(w) >= 4}


def cumle_seti(s):
    return [c.strip() for c in koru.cumleler(s)]


def olc(vk: dict, girdi: str, cikti: str, kip: str) -> dict:
    k = vk.get("kod", {})
    tur, bolum = vk.get("tur", "post"), vk.get("bolum")
    ayrac = k.get("ayrac")
    ana = cikti.split(ayrac)[0] if ayrac and ayrac in cikti else cikti
    tum = cikti.replace(ayrac, "") if ayrac else cikti
    r = denetle(ana, kip, tur, bolum)
    sonuc = {"dil_puan": r["puan"], "dil_sayim": r["sayim"],
             "dil_kurallar": sorted({b["kural"] for b in r["bulgular"] if b["seviye"] in ("HATA", "UYARI")}),
             "olcutler": {}}
    O = sonuc["olcutler"]
    if k.get("koru"):
        kr = koru.karsilastir(girdi, tum, k.get("koru_kip", kip), k.get("muaf"))
        sonuc["koru"] = {"hata": kr["hata"], "uyari": kr["uyari"], "kelime_oran": kr["kelime_oran"],
                         "ihlaller": [f"{i['seviye']} {i['denetim']}: {i['eksik'][:3]}{i['fazla'][:3]}" for i in kr["ihlaller"]]}
        O["koru_hata_0"] = kr["hata"] == 0
    if "hata_max" in k:
        O["dil_hata_max"] = r["sayim"]["HATA"] <= k["hata_max"]
    if "puan_min" in k and r["puan"] is not None:
        O["dil_puan_min"] = r["puan"] >= k["puan_min"]
    if "yasak_kurallar" in k:
        bulunan = []
        for y in k["yasak_kurallar"]:
            kod, _, alt = y.partition(":")
            bulunan += [kod + (":" + alt if alt else "") for b in r["bulgular"] if b["kural"] == kod and (not alt or alt in b["mesaj"])]
        O["yasak_kural_yok"] = not bulunan
        if bulunan:
            sonuc["yasak_bulunan"] = sorted(set(bulunan))
    if "kelime_oran" in k:
        oran = len(koru.kelimeler(tum)) / max(1, len(koru.kelimeler(girdi)))
        O["kelime_oran"] = k["kelime_oran"][0] <= oran <= k["kelime_oran"][1]
        sonuc["kelime_oran"] = round(oran, 3)
    if "ort_kelime" in k:
        ort = r["istatistik"].get("ort_kelime")
        O["ort_kelime"] = ort is not None and k["ort_kelime"][0] <= ort <= k["ort_kelime"][1]
        sonuc["ort_kelime"] = ort
    if "karakter_max" in k:
        O["karakter_max"] = len(cikti.strip()) <= k["karakter_max"]
        sonuc["karakter"] = len(cikti.strip())
    if "ortusme_min" in k:
        ck = kokler(cikti)
        ort = [len(kokler(x) & ck) / max(1, len(kokler(x))) for x in k["ortusme_ref"]]
        sonuc["ortusme"] = [round(x, 2) for x in ort]
        O["ortusme_min"] = sum(ort) / len(ort) >= k["ortusme_min"]
    if "degisen_cumle_max" in k:
        g = set(cumle_seti(girdi))
        n = sum(1 for c in cumle_seti(cikti) if c not in g)
        sonuc["degisen_cumle"] = n
        O["degisen_cumle_max"] = n <= k["degisen_cumle_max"]
    if k.get("puan_dusmez"):
        O["puan_dusmez"] = (r["puan"] or 0) >= (denetle(girdi, kip, tur, bolum)["puan"] or 0)
    if k.get("ayni_olmali"):
        O["degisiklik_yok"] = cikti.strip() == girdi.strip()
    if "ana_sayi_max" in k:
        n = len(re.findall(r"\d+(?:[.,]\d+)?", ana))
        sonuc["ana_sayi"] = n
        O["ana_sayi_max"] = n <= k["ana_sayi_max"]
    if "ilk_cumle_icerir" in k:
        O["hukum_once"] = k["ilk_cumle_icerir"] in "\n".join(cikti.splitlines()[:2])
    if k.get("ritim_degismez"):
        O["cumle_sayisi_ayni"] = len(cumle_seti(cikti)) == len(cumle_seti(girdi))
    sonuc["gecti"] = all(O.values())
    return sonuc


def vaka_kos(d: Path, model: dict) -> dict:
    vk = yaml.safe_load(oku(d / "vaka.yaml"))
    girdi = oku(d / "girdi.txt")
    k = vk.get("kod", {})
    kayit = {"vaka": d.name, "kip": vk.get("kip"), "beklenen": vk.get("beklenen"), "kaynak": vk.get("kaynak")}
    # tespit testi (girdi üzerinde)
    if "girdide_bulunmali" in k:
        kip = k.get("girdide_bulunmali_kip", vk.get("kip") if vk.get("kip") in dd.KIPLER else "rapor")
        r = denetle(girdi, kip, vk.get("tur", "post"), vk.get("bolum"))
        kurallar = {b["kural"] for b in r["bulgular"]}
        eksik = [x for x in k["girdide_bulunmali"] if x not in kurallar]
        kayit["tespit"] = {"kip": kip, "beklenen": k["girdide_bulunmali"], "kacan": eksik, "gecti": not eksik}
    if k.get("yalniz_tespit"):
        satirlar = [s for s in girdi.splitlines() if s.strip()]
        ai, yazim = [], []
        for s in satirlar:
            for b in denetle(s, vk["kip"])["bulgular"]:
                hedef = yazim if any(b["kural"].startswith(p) for p in k["yazim_aileleri"]) else ai
                hedef.append(f"{b['seviye']} {b['kural']}: {b['alinti'][:50]}")
        ai_hata = [x for x in ai if x.startswith("HATA")]
        kayit["tespit"] = {"mesaj": len(satirlar), "ai_hata": ai_hata, "ai_diger": ai, "yazim": yazim,
                           "gecti": len(ai_hata) <= k["ai_hata_max"]}
        kayit["gecti_skill"] = kayit["tespit"]["gecti"]
        return kayit
    if "kipler" in vk:  # V12: tuzaklar her kipte
        tz = {}
        for kip in vk["kipler"]:
            r = denetle(girdi, kip)
            tz[kip] = [f"{b['seviye']} {b['kural']}" for b in r["bulgular"] if b["seviye"] == "HATA"]
        kayit["tuzak_hatalari"] = tz
        kayit["tuzak_gecti"] = all(len(v) <= k["tuzak_hata_max"] for v in tz.values())
    kosular = k.get("alt_kosular") or [{"kip": vk.get("kip") if vk.get("kip") in dd.KIPLER else k.get("koru_kip", "rapor")}]
    for kosu in kosular:
        kip = kosu["kip"]
        ek = f"_{kip}" if k.get("alt_kosular") else ""
        for tur_ad in ("skill", "temel"):
            c = oku(d / f"cikti_{tur_ad}{ek}.txt")
            if not c:
                continue
            kayit[f"{tur_ad}{ek}"] = olc(vk, girdi, c, kip)
    skill_anahtarlar = [a for a in kayit if a.startswith("skill")]
    kayit["gecti_skill"] = all(kayit[a]["gecti"] for a in skill_anahtarlar) and kayit.get("tuzak_gecti", True) \
        and kayit.get("tespit", {}).get("gecti", True)
    temel_anahtarlar = [a for a in kayit if a.startswith("temel")]
    kayit["gecti_temel"] = all(kayit[a]["gecti"] for a in temel_anahtarlar) if temel_anahtarlar else None
    if d.name in model:
        kayit["model"] = model[d.name]
    return kayit


def main(secili: list[str]) -> int:
    model = yaml.safe_load(oku(B / "model_degerlendirme.yaml")) or {}
    vakalar = sorted(p for p in B.iterdir() if p.is_dir() and re.match(r"V\d", p.name))
    if secili:
        vakalar = [v for v in vakalar if any(v.name.startswith(s) for s in secili)]
    sonuc = [vaka_kos(v, model) for v in vakalar]
    tarih = datetime.date.today().isoformat()
    (B / "sonuclar").mkdir(exist_ok=True)
    dosya = B / "sonuclar" / f"{tarih}.json"
    json.dump({"tarih": tarih, "vakalar": sonuc},
              dosya.open("w", encoding="utf-8"), ensure_ascii=False, indent=1)
    satirlar = ["| Vaka | Kip | Skill | Temel | Skill: dil puanı / HATA / koru HATA | Temel: dil puanı / HATA / koru HATA | Not |",
                "|---|---|---|---|---|---|---|"]
    for s in sonuc:
        def ozet(on):
            parca = [v for a, v in s.items() if a.startswith(on) and isinstance(v, dict)]
            return "; ".join(f"{p['dil_puan'] if p['dil_puan'] is not None else 'yok'} / {p['dil_sayim']['HATA']} / "
                             f"{p.get('koru', {}).get('hata', '-')}" for p in parca) or "-"
        notlar = []
        for a, v in s.items():
            if isinstance(v, dict) and "olcutler" in v:
                kalan = [o for o, ok in v["olcutler"].items() if not ok]
                if kalan:
                    notlar.append(f"{a}: {', '.join(kalan)}")
        if "tespit" in s and not s["tespit"]["gecti"]:
            notlar.append(f"tespit kaçan: {s['tespit'].get('kacan') or s['tespit'].get('ai_hata')}")
        if "tuzak_gecti" in s:
            notlar.append("tuzaklar " + ("temiz" if s["tuzak_gecti"] else "YANLIŞ POZİTİF"))
        g = lambda x: "-" if x is None else ("geçti" if x else "KALDI")  # noqa: E731
        satirlar.append(f"| {s['vaka']} | {s['kip']} | {g(s['gecti_skill'])} | {g(s.get('gecti_temel'))} | {ozet('skill')} | {ozet('temel')} | {'; '.join(notlar)} |")
    gecen = sum(1 for s in sonuc if s["gecti_skill"])
    satirlar.append(f"\nSkill çıktısı: {gecen}/{len(sonuc)} vaka geçti.")
    (B / "sonuclar" / f"{tarih}-tablo.md").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    print("\n".join(satirlar))
    print(f"\nyazıldı: {dosya}")
    return 0 if all(s["gecti_skill"] for s in sonuc) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
