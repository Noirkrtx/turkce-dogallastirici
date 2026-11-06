# Koruma kuralları (değişmez)

Her yeniden yazımda önce bu liste uygulanır, sonra `scripts/koru.py --once girdi --sonra cikti --kip <kip>` ile kodla doğrulanır. HATA varsa metin teslim edilmez: düzelt, en çok 2 tur; yine HATA kalıyorsa farkı raporla.

| # | Kural | koru.py denetimi | Şiddet |
|---|---|---|---|
| 1 | **Anlam ve iddia gücü.** Temkin (olabilir, ilişkili, düşündürüyor, henüz, yaklaşık) her önermede en az bir kez kalır. Kaçınma yığılması teke iner, sıfıra inmez (K-26). Kanıt düzeyi yükseltilmez, öneri veriye atfedilmez. | `temkin`: önerme (cümle, `;`, `ve` ile ayrılan parça) başına varlık; '-abil' yalnız çekimli yüklemde sayılır ('taşıyabileceği bilgi' sayılmaz) | HATA |
| 2 | **Sayı ve birim** birlikte, yakın terimiyle korunur ("Pplat 26 cmH2O"). Belirsiz sayıya ("1,500") dokunulmaz, not düşülür. | `sayi-birim` (çoklu küme), `terim-sayi` (OR 2,3 / Ppeak 26 yer değişimi) | HATA; kaynakta olan değerin tekrarı UYARI |
| 2a | **Tıp:** doz-birim-yol birlikte ("0,1 mg/kg IV"), µ ile m karışmaz, süre ve aralık ("8 saatte bir", "ilk 6 saatte"), eşik işareti yönü (<, >, ≤, ≥). RR, OR, HR, ARR, RRR, NNT, NNH, LR, AUC, %95 GA alt-üst, p ve işareti, n/N bayt bayt. "Anlamlı" istatistik terimiyse eşanlamlıyla değişmez. Göreli risk mutlak riske ya da "X kat artırdı" anlatımına çevrilmez. | `sayi-birim` (birim dahil: µg/kg/dk ≠ mg/kg/dk), `karsilastirma`, `kisaltma`, `nedensel` | HATA |
| 2b | **Öneri gücü ve kılavuz sınıfı** aynen: önerilir / önerilebilir / önerilmez / "verilmesi düşünülebilir", Sınıf I/IIa/IIb/III, Düzey A/B/C, GRADE güçlü/zayıf. | `oneri-gucu` (çoklu küme) | HATA |
| 3 | **Bilgi ekleme/çıkarma yok.** Kaynakta olmayan özne ("biz"), neden, sıra, kıyas, deneyim eklenmez; bilgi taşıyan öğe silinmez. Sadeleştirme ve içerik azaltma yok (D17, D18). | `ozel-isim` (yeni ad UYARI), `nedensel`, `uzunluk`; ekleme sorusu model okumasında | HATA/UYARI |
| 4 | **Terim** korunur: preprint, odds ratio (OR), NT-proBNP, kan gazı, solunumsal, agent, context. "kritik hasta", "kritik stenoz", "kilit" bağlamında terimdir. | `kisaltma`; Türkçe karşılığa çevirme model okumasında (V03 kör noktası) | HATA |
| 5 | **Özel ad, kısaltma, sürüm:** "Claude Code 2.1.317", "ARDS Network'ün" (yabancı kurum adına TDK-K2 uygulanmaz). | `ozel-isim`, `kisaltma` | HATA |
| 6 | **Alıntı ve kaynak:** tırnak içi, künye, kaynakça, metin içi atıf ([12], (4,9), (Yazar, 2024)) ve bağlı olduğu önerme, URL, DOI, PMID, arXiv no, kod bloğu bayt bayt. Cümle bölünürse atıf önermesiyle gider. | `alinti`, `atif`, `atif-baglilik` | HATA (sesli kipte atıf okunmaz: UYARI) |
| 7 | **Şablon işaretleri:** [TIK], [SOR: …], [BEKLE], {{yer_tutucu}}, «», <dfn>, [AUTHOR TO INSERT], [Kurum adı], MEDIA:, "❓ Senden istenen". | `sablon` | HATA (sesli kipte [TIK]/[SOR] eklemek UYARI) |
| 8 | **Kip dışına çıkılmaz** (akademik konuşma diline, post akademiğe dönmez). | model okuması | - |
| 9 | **Dürüstlük:** "denedim, okudum" yalnız kayda dayanır; anekdot, duygu, sahne uydurulmaz. Kullanıcının ham cümlesi korunur, yorumlanan belirsiz ifade raporda söylenir (D11). | model okuması | - |
| 10 | **Kimlik:** metne yazarın kaynakta olmayan kimlik ayrıntısı (yer, kurum, meslek) eklenmez. | model okuması | - |
| 11 | **Olgu hatası** fark edilirse düzeltilmez, raporda not edilir ("riski 1,37 kat artırıyordu"). | model okuması | - |
| 12 | **Zaten doğalsa** küçük düzeltme ya da hiç. | `degisen_cumle` (eval) | - |

## Bilerek silinenler

İç not, dosya yolu, kart kimliği, kod adı ("KT", "Tablo B"), banka vaka numarası rapor ve sesli kipte çıkarılır. Bunlar `koru.py --muaf "KT,23"` ile verilir; koru.py kayıp listesinden düşer ve `muaf` alanında raporlar. Dosya yolu ve atıf numaraları sayı denetimine girmez.

## Sesli kip

`koru.py --kip sesli` iki metni `references/sesli-okunus.md` tablosuyla simgeye geri çevirir (okunuş → yazım, sayı sözü → rakam), sonra karşılaştırır. Tabloda olmayan okunuş değer kaybı olarak HATA verir; yeni okunuş önce tabloya eklenir. Kart içi adım numaraları ("0: ... 1: ...") sayı sayılmaz, [TIK] olur.

## Bilinen sınırlar

- Önerme hizalaması kök örtüşmesine (ilk 5 harf, ≥%30) dayanır; çok yeniden kurulmuş cümlede temkin karşılığı bulunamazsa UYARI verir, HATA değil.
- Olumsuzluk sayacı yalnız UYARI: "X değil, Y" kalıbını kaldırmak sayıyı meşru değiştirir.
- Terimin Türkçe karşılığına çevrilmesi (agent → ajan) kısaltma olmadığı için yakalanmaz.
