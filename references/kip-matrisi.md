# Kip matrisi

Kip işin başında belirlenir. Çağıran iş akışı verir (sosyal medya postu `post`, rapor/okuma metni `rapor`/`ogretici`, sunum notu `sesli`/`ogretici`); doğrudan istekte metinden çıkarılır ve raporda söylenir. Yanlış kip bütün seviyeleri kaydırır.

| Kip | Ne | Okur | Ses | Kod eşiği (`dil_denetim.py`) |
|---|---|---|---|---|
| `post` | sosyal medya postu, yanıt, uzun yazı tanıtımı (`--tur uzun`) | niş, meraklı | konuşma dili, birinci tekil | HATA 0, puan ≥85 (eski davranış, varsayılan) |
| `rapor` | mesajla teslim edilen rapor, okuma sürümü PDF metni, haftalık özet | işi isteyen kişi | doğrudan, sıcak, hüküm önde | puan ≥80, HATA 0 |
| `ogretici` | okuma/çalışma metni, ders hazırlık metni | öğrenen okur, öğrenciler | ders kitabı anlatıcısı, bağlaçlı | puan ≥75, HATA 0 |
| `akademik` | Türkçe tez, makale, özet | hakem, jüri | akademik yazım kuralları | **puan yok**, yalnız HATA 0 (STY-30) |
| `sesli` | anlatıcı notu, canlı kart konuşma satırı, TTS metni | dinleyen | konuşma metni, sınıfa hitap | puan ≥85, HATA 0 |
| `telgraf` | vaka notu, slayt iskeleti, tablo, madde listesi | çalışan | **yalnız yazım ve noktalama** | HATA 0, kelime ±%5 |

## Meşru (M) / iz (İ) özeti

| Özellik | post | rapor | ogretici | akademik | sesli |
|---|---|---|---|---|---|
| "...: Ad" tanıtım iki noktası | İ HATA | İ UYARI | İ UYARI | M | İ UYARI |
| Şablon etiketi ("Sonuç:", "Hedef:", "Sayaç:") | BİLGİ | M | M | M | M |
| Uzun/orta tire | HATA | HATA | HATA | HATA | HATA |
| -mektedir | HATA | UYARI | UYARI | **M** (yığılma UYARI, KAT-64) | HATA |
| -mıştır | UYARI | UYARI | BİLGİ | Yöntem/Bulgular UYARI (raporla, dönüştürme) | UYARI |
| Edilgen | yığılınca İ | BİLGİ | BİLGİ | **M** | kim yaptı belli olsun |
| Öznesiz yorum ("söylenebilir") | UYARI | UYARI | UYARI | UYARI | UYARI |
| Noktalı virgül | BİLGİ | UYARI | BİLGİ | M | UYARI |
| Şapka | yok (zekâ HATA) | yok | BİLGİ | **TDK zorunlu** | fark etmez |
| Birinci tekil | M | M | dar | İ ("bu çalışmada") | M |
| Cümle başı bağlaç | UYARI | UYARI | M | M ("Öncelikle/Sonuç olarak" BİLGİ) | UYARI |
| Sıra sözü numaralama | İ | UYARI | UYARI | UYARI (D23) | M (ölçülü) |
| Üçlü sıralama | UYARI | UYARI | BİLGİ | BİLGİ | UYARI |
| "X değil, Y" | HATA | UYARI | UYARI | BİLGİ | UYARI |
| Soru + hemen cevap | UYARI | UYARI | M | UYARI | M ([SOR]/[BEKLE]) |
| Kapanışta vecize | HATA ilkesi | UYARI | vecize UYARI, özet/köprü M | Sonuç bölümünde M | köprü cümlesi |
| Ritim kırma (cv) | açık | açık | açık | **kapalı** (STY-30) | açık, zorunlu |
| Eşanlamlı ile terim değiştirme | kapalı | kapalı | kapalı | kapalı | kapalı |
| Konuşma sözü ("yani", "mesela") | 1 tane | seyrek | yok | yok | doğal doz |
| Çeviri izi (KAT-20…28) | kapalı (eski davranış) | UYARI/BİLGİ | UYARI/BİLGİ | UYARI/BİLGİ | UYARI/BİLGİ |
| Cümle ortalaması (K-24, BİLGİ) | 6-14 | 10-16 | 15-20 | 12-20 | 8-16, >25 yok |

Post kipinde yeni kalıp aileleri (çeviri, yapısal, akademik, sesli) kapalıdır: mevcut post akışları aynı komutu çağırıyor, puanlar değişmesin diye. Post kipine yalnız kesin kurallar eklendi: TDK yazımı (KAT-40…46) ve alan sözlüğü (KAT-50). `--eski` bayrağı bunları da kapatır.

## Okunurluk kalibrasyonu (yalnız BİLGİ, puan düşürmez)

`scripts/okunurluk.py` Ateşman ve Bezirci-Yılmaz (YOD) hesaplar; `dil_denetim.py` post dışı kiplerde istatistiğe yazar. Aralıklar projenin kendi metinlerinin çeyrekleridir (Q1-Q3), hedef değil: "bu metin bizim o kipteki metinlerimizin ortasında mı" sorusuna cevap verir. Ölçüm `evals/kalibrasyon.json`, maskelenmiş metin, ≥50 kelime, 4 kelimeden kısa satırlar dışarıda.

| Kip | n | Ateşman Q1 / medyan / Q3 | YOD Q1 / medyan / Q3 | Kaynak |
|---|---|---|---|---|
| post | 51 | 61,6 / 65,9 / 71,9 | 8,9 / 10,8 / 12,8 | post taslakları (yanıtlar hariç) |
| rapor | 11 | 81,1 / 83,4 / 89,7 | 6,6 / 7,8 / 9,5 | mesajla teslim edilen raporlar |
| ogretici | 35 | 77,1 / 84,6 / 87,6 | 7,2 / 8,1 / 9,9 | okuma ve ders metinleri |
| akademik | 161 | 13,4 / 27,0 / 37,1 | 25,1 / 31,0 / 37,2 | akademik metin gövde paragrafları (yalnız ölçü; metin repoda yok) |
| sesli | 5 | 84,8 / 87,7 / 93,7 | 4,5 / 6,3 / 7,2 | konuşmacı kartları |

Sınırlar: rapor ve sesli örneklemi küçük; Şablonlu raporlar "·" ile bölünmüş kısa satırlar, konuşmacı kartları etiketli kısa satırlar olduğu için Ateşman yüksek çıkıyor (ölçü satır yapısına duyarlı). Terim yoğun metinde Ateşman düşük çıkar; terim sadeleştirilmez (D18). 02'deki ev varsayılanları (post 65+, rapor 55+, öğretici 50+, sesli 60+) bu ölçümle yalnız post için tutarlı.
