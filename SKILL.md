---
name: turkce-dogallastirici
description: "Türkçe metni doğallaştırır: kipe göre (post, rapor, öğretici, akademik, sesli, telgraf) yapay zeka ve çeviri izini temizler; sayıyı, birimi, terimi, atfı ve temkini kodla korur. Kullanıcı 'doğal yaz', 'AI gibi duruyor', 'çeviri gibi', 'insanlaştır', 'dil denetimi' dediğinde ya da Türkçe metin teslim edilmeden önce kullan. İngilizce metin, kod ve kaynakça için kullanma."
license: MIT
metadata:
  version: "0.1.0"
  author: "NOIR (@noirkrtx)"
  tags: "türkçe, doğallaştırma, ai-izi, tdk, akademik-yazım, sesli-metin"
---

# Türkçe doğallaştırıcı

Türkçe metni kipine göre (post, rapor, öğretici, akademik, sesli, telgraf) AI ve çeviri izinden temizler; sayıyı, birimi, terimi, temkini, atıfı ve şablon işaretini kodla korur. Yöntem yapıyı değiştirmektir, eşanlamlı ikame değil. Saf Python, bağımlılık yok (eval koşturucu PyYAML ister).

## When to Use

- Açık istek: "doğal yaz", "AI gibi duruyor", "çeviri gibi", "insanlaştır", "AI izini temizle", "dil denetimi", "humanize" ve metin Türkçe.
- Akış içi, teslimden önce: sosyal medya postu (`--kip post`), rapor ve okuma metni (`--kip rapor` / `ogretici`), sunum anlatıcı notu ve TTS metni (`--kip sesli`), Türkçe tez/makale dil okuması (`--kip akademik`, yalnız denetim ve işaretli kalıplar).
- **Kullanma:** İngilizce metin (İngilizce bir humanizer kullan), kod, tablo hücresi, künye/kaynakça, alıntı, yasal madde, kullanıcının kendi mesajı (istenmedikçe). Vaka notu ve slayt iskeleti yalnız `telgraf` (yazım/noktalama).

## Kipler (ayrıntı `references/kip-matrisi.md`)

| Kip | Ne | Kod eşiği |
|---|---|---|
| `post` | sosyal medya postu, yanıt; uzun yazı için `--tur uzun` | HATA 0, puan ≥85 (varsayılan) |
| `rapor` | mesajla teslim edilen rapor, okuma sürümü, haftalık özet | HATA 0, puan ≥80 |
| `ogretici` | okuma/çalışma/ders hazırlık metni | HATA 0, puan ≥75 |
| `akademik` | Türkçe tez, makale | yalnız HATA 0 (puan yok, STY-30) |
| `sesli` | anlatıcı notu, canlı kart, TTS metni | HATA 0, puan ≥85 |
| `telgraf` | vaka notu, slayt iskeleti, liste | HATA 0, kelime ±%5 |

Kip çağıran iş akışından gelir; doğrudan istekte metinden çıkar, en yakın kipi seç ve raporda söyle.

## Değişmez kurallar (`references/koruma-kurallari.md`)

1. İddia gücü değişmez: temkin her önermede kalır (kaçınma yığılması teke iner, sıfıra inmez), öneri gücü ve kılavuz sınıfı aynen.
2. Sayı birimiyle ve terimiyle; doz-birim-yol, µ/m, RR/OR/HR/NNT/GA/p bayt bayt; göreli risk "X kat artırdı"ya çevrilmez; belirsiz sayıya ("1,500") dokunulmaz.
3. Bilgi eklenmez, çıkarılmaz; kaynakta olmayan özne ("biz"), neden, sıra, deneyim yok. Sadeleştirme yok (D17, D18).
4. Terim, özel ad, kısaltma, sürüm, alıntı, atıf (önermesiyle), URL/DOI/PMID, şablon işareti ([TIK], [SOR: …], {{…}}, «», <dfn>, [Kurum adı]) korunur.
5. Kip dışına çıkılmaz. Olgu hatası düzeltilmez, raporlanır. Zaten doğalsa dokunulmaz.
6. Uzun/orta tire yok; "betik" değil "kod"; "ön baskı" değil "preprint".

## How to Run

`$SKILL_DIR` bu dosyanın bulunduğu klasördür (kurulumda nereye kopyalandıysa). Kodlar kendi `references/` klasörünü göreli yolla bulur; hangi dizinden çağrıldığı fark etmez.

```bash
python3 "$SKILL_DIR/scripts/dil_denetim.py" taslak.txt --kip rapor            # tespit, kip seviyeleri
python3 "$SKILL_DIR/scripts/dil_denetim.py" tez.txt --kip akademik --bolum bulgular --json
python3 "$SKILL_DIR/scripts/koru.py" --once girdi.txt --sonra cikti.txt --kip sesli --muaf 'KT,23'
python3 "$SKILL_DIR/scripts/okunurluk.py" metin.txt --kip ogretici            # Ateşman + Bezirci-Yılmaz, yalnız bilgi
python3 "$SKILL_DIR/evals/calistir.py"                                        # eval vakaları (PyYAML gerekir)
```

## Procedure

1. **Kip ve okur.** Kip kodunu, okuru, çağıran iş akışını yaz. `telgraf` ise yalnız yazım/noktalama, 5'e atla. *Bitti:* kip raporun ilk satırında.
2. **Koruma listesi.** Metindeki sayı+birim+terim, kısaltma, özel ad, temkin sözleri, atıflar, alıntılar, şablon işaretleri. Bilerek silinecekleri (iç not, dosya yolu, kart kimliği, kod adı, banka vaka no) ayrı yaz. *Bitti:* `--muaf` listesi hazır.
3. **Tespit.** `dil_denetim.py --kip <kip> --json` + model okuması: "Bunu AI/çeviri yapan ne?" en çok 3 madde (yapı, konu, ses); postta konu testi ("bir insan kendi hayatında yazar mıydı?"). Yazım (TDK, alan) bulgularını üslup bulgularından ayrı listele. *Bitti:* her HATA/UYARI'nın KAT kimliği (`references/kalip-katalogu.md`) belli.
4. **Yeniden yaz.** Kullanıcı kendi yazısından örnek verdiyse cümle uzunluğu, bağlaç ve ton ölçüsü o örnektir (`references/ornek-duzeltmeler.md`, ses kartı). Sıra: önce sil (dolgu, anons, kapanış dersi, iç not) → sonra birleştir/böl (ritim, "-arak" zinciri, "-miş olup", yan cümle) → en son bağlaç. Eşanlamlı ikame yok. En az bir eleştiri turu (Self-Refine). Silme testi: yazarken eklediğin söylem parçacığını ('işte', 'zaten'), devrik cümleyi ya da bağlacı çıkar; anlamdan ve tondan bir şey eksilmiyorsa sil. **Akademik:** yalnız işaretli kalıplar (KAT-20…28, 40…47, 61…66); ritim kırma kapalı; "-mektedir", edilgen, "düşündürmektedir" meşru; KAT-67 ("-mıştır" Yöntem/Bulgular) raporlanır, toplu dönüştürülmez. **Sesli:** okunuşlar `references/sesli-okunus.md` tablosundan; birinci tekil, sınıfa hitap, [TIK]/[SOR]/[BEKLE]. *Bitti:* değişiklik özeti KAT kimlikleriyle.
5. **Koruma denetimi.** `koru.py --once --sonra --kip <kip> [--muaf ...]`. HATA varsa 4'e dön, en çok 2 tur; hâlâ HATA kalıyorsa metni teslim etme, farkı raporla. UYARI'ları (olumsuzluk, yeni ad, atıf bağlılığı) tek tek oku. *Bitti:* `KORUMA GEÇTİ`.
6. **Puan.** `dil_denetim.py --kip <kip>` kip eşiğini geçmeli (yukarıdaki tablo). Okunurluk yalnız bilgi. *Bitti:* HATA 0 ve eşik.
7. **Sesli okuma.** post ve sesli kipte zorunlu: cümle cümle nefes noktası, yüklemden uzak özne, okunmayan simge, yabancı kelime, yeni bilginin yüklem önünde olması. TTS denemesi isteğe bağlı. *Bitti:* takılan cümle yok ya da düzeltildi.
8. **Rapor.** Kip; değişiklik özeti (KAT kodlarıyla); korunanlar tamam/değil; silinenler (muaf); puan önce > sonra; Ateşman ve Bezirci-Yılmaz; olgu notu; yorumlanan belirsiz ifade. *Bitti:* rapor bu 8 başlığı taşıyor.

## Pitfalls

- **Post kipi bilerek dar.** Post kipinde yeni çeviri/yapı aileleri kapalı, yalnız TDK yazımı, alan sözlüğü ve AI sözlüğü (KAT-74…76, UYARI) açık; mevcut post akışlarının puanı değişmesin diye. Yeni bir kuralı post'ta açmadan önce eski post örneklerini `--eski` bayrağıyla ve bayraksız denetleyip farkı tek tek oku; postta meşru kullanımı vuruyorsa (ör. vurgu için cümle başı 'Ben', KAT-77) kuralı post ve sesli kipte KAPALI yap. `--eski` tamamen eski kural setini verir.
- **Sözlük kalıbını alan terimiyle çakıştırma.** Dış sözlükteki 'mozaik' gibi süs kelimeleri tıpta terimdir (mozaik trizomi): kalıba alma ya da V15 gibi yanlış pozitif vakasıyla koru. Akademik kipte bürokratik bağlar ('bu doğrultuda', 'bahsi geçen', 'belirtmek gerekir ki') KAPALI, süs kelimeleri yalnız BİLGİ.
- **Kip yanlışsa her seviye kayar.** Akademik metni `post` ile denetlemek "-mektedir" için HATA yağdırır.
- **Sesli kipte koru.py tabloya bağlı.** Tabloda olmayan okunuş (ör. "pip" yerine "pe e e pe") değer kaybı sayılır; önce tabloya satır ekle.
- **Silinen iç notu `--muaf` ile ver**, yoksa koru.py sayı/ad kaybı diye HATA verir (doğru davranış: bilerek silindiği kayda geçmeli).
- **Kod sessiz diye metin doğal değildir.** Terimin Türkçeleştirilmesi (agent → ajan), uydurma deneyim, konu izi, olgu düzeltmesi kodla yakalanmaz; model okuması şart.
- **Meta kullanım da işaretlenir.** "betik kelimesini çok kullanıyorsun" gibi kelimeyi anan cümlede de `alan-betik` çıkar; kullanıcının ham mesajına dokunulmaz (V10).
- **Ateşman satır yapısına duyarlı:** şablonlu rapor ve konuşmacı kartı yapay olarak kolay görünür; kapı olarak kullanma.

## Verification

- `python3 evals/calistir.py` → bütün vakalar skill için "geçti". Sonuç dosyası `evals/sonuclar/<tarih>.json` ve `<tarih>-tablo.md` (git dışı).
- Vakalardaki girdi ve çıktılar sentetiktir; `cikti_skill.txt` beklenen çıktı, `cikti_temel.txt` skill'siz tipik çıktı örneğidir. Kendi beklenen çıktısını kendi aracıyla puanlayan "x/x geçti" raporu bağımsız test sayılmaz; anlam ölçütleri `evals/model_degerlendirme.yaml`'da ayrıca tutulur.
- **Dış Türkçe humanizer reposu karşılaştırması:** kodunu çalıştırmadan önce içe aktarımlarını (ağ/subprocess) kontrol et; repoyu geçici bir klasöre klonla. Sözlüğündeki Türkçe kalıpları literal grep'le değil, her birini tek cümleye koyup `dil_denetim.py --kip rapor --json` ile sına (regex aileleri literal aramada yanlış "yok" verir); yakalanmayanları listele. Tersine kendi `evals/` girdilerini (özellikle V04 zaten doğal, V10 yanlış pozitif, V07 akademik) onların tespit koduyla tara. Mutlak yasak listelerini ve sabit ritim eşiklerini (CoV) doğrudan alma; akademik kipteki meşru bağlaçlarla ("öte yandan", "söz konusu") çakışır. Alınacak kalıp post/rapor kipinde UYARI, akademikte muaf.
- Yeni kural eklerken: `references/kurallar.json` + `kalip-katalogu.md` girdisi + en az bir eval vakası (doğru ve yanlış pozitif).

Fikir kaynakları: DevVettel/turkish-humanizer (MIT) ve yucezerey/turkish-anti-ai-skill (MIT; KAT-74…78 kalıp sözlüğü). Akademik dayanaklar `references/literatur.md`.
