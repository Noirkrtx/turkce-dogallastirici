# TDK yazım katmanı (özet)

Kaynak: TDK Yazım Kuralları sayfaları (tdk.gov.tr; madde kodları aşağıdaki tabloda). TDK **doğru yazımı** belirler, **üslubu** belirlemez: bir işaret TDK'ye göre doğru olup bizim kipte iz sayılabilir (en açık örnek iki nokta). Rapor "yazım hatası" ile "üslup izi"ni ayrı listeler.

## Kodla denetlenenler (`kurallar.json`, aile TDK)

| Kod | Kural | Örnek doğru · yanlış | Şiddet | Yanlış pozitif / istisna |
|---|---|---|---|---|
| TDK-V1 | "ve, veya, yahut" öncesi ve sonrası virgül yok | "gördüm ve istedim" · "gördüm, ve istedim" | **HATA, bütün kipler** (proje kararı; sıralı cümlelerde de) | "ya da" listede yok; ara sözün kapanış virgülü şüphesi model okumasına not düşülür ama kural HATA kalır |
| TDK-V2 | hem ... hem arasında virgül yok | "Hem gider hem ağlar." | UYARI | |
| TDK-V4 | şart ekinden sonra virgül yok | "Biri gelecek olursa susuyorlardı." | kodda yok (model) | TDK'nin kendi örneği: "Köyde kim çaresiz kalırsa, kimin işi bozulursa..." (eş görevli öbekler) |
| TDK-S2 | yüzde işareti önde, bitişik | "%25" · "25%", "% 25" | HATA | |
| TDK-S3 | ondalık virgül | "15,2" · "15.2", "p<0.05" | UYARI (post kapalı) | sürüm (2.1.317, GPT-5.2), saat (17.30'da), Tablo/Şekil/bölüm no, İngilizce künye |
| TDK-S6 | sıra sayısında ikisi birden yok | "8." ya da "8'inci" · "8.'inci" | HATA | |
| TDK-S8 | cümle rakamla başlamaz | "Çalışmaya 45 öğrenci alındı." · "45 öğrenci alındı." | rapor/akademik UYARI | numaralı başlık ("1. Giriş"), madde |
| TDK-B1 | "ya da" ayrı | · "yada" | HATA | |
| TDK-B3 | bağlaç "ki" ayrı | "demek ki" · "demekki" | HATA | |
| TDK-B4 | kalıplaşmış "oysaki" bitişik | "oysaki" · "oysa ki" | BİLGİ | |
| TDK-B7 | belirsizlik sözleri bitişik | birçok, birkaç, hiçbir, herhangi | HATA; "bir takım" UYARI | "bir takım kurduk" (sayı + ad) doğru |
| TDK-B8 | "bir şey", "her şey" ayrı | · "herşey", "birşey" | HATA | kullanıcının ham mesajı ve alıntı KORU [sözlükten doğrulanmadı] |
| TDK-B12 | "iş birliği" ayrı | · "işbirliği" | HATA | |
| TDK-T3 | tırnaktan sonra gelen ek kesmesiz | "“Bit Palas”ını" · "“Bit Palas”'ını" | HATA | |
| TDK-K2 | kurum adına gelen ek kesmesiz | "Türk Dil Kurumunun" · "Kurumu'nun" | HATA | yabancı kurum/proje adı ("ARDS Network'ün"), unvan ("Başkanı'na"), belirli yönetmelik |
| TDK-K8 | ek ayraçtan önce | "Yunus Emre'nin (1240?-1320)" · ")'nin" | HATA | |
| TDK-N4 | üç nokta; iki ya da dört+ nokta yok | "Ali..." · "Ali....", "Ali.." | UYARI | "?..", "!.." doğru |
| TDK-Ç3 | uzun çizgi yalnız konuşma çizgisi | | **HATA, bütün kipler** (ev kuralı daha sıkı) | alıntı, İngilizce künye, kod maskelenir |
| NOK-03 | belirsiz sayı | "1,500" | BİLGİ: dokunma, not düş | baştaki sıfır (0,350) ondalık |

## Model okuması (kodlanmadı)

- **De/da bağlacı ayrı** ("Ayşe de geldi"), bulunma eki bitişik ("Türkiye'de"). Otomatik ayrım güvenilmez (bir denemede 25/25 aday bulunma ekiydi).
- **Soru eki ayrı** ("Verecek misin?"); "ilgili" gibi -mi ile biten sözcükler yanlış pozitif verir.
- **Kısaltmaya gelen ek okunuşa uyar:** "TDK'nin", "BT'de", "EKG'de", "GPT'ye"; "API'ye" (okunduğu gibi, metin içinde tek biçim).
- **İki noktadan sonra** cümle büyük harfle, sıralama küçük harfle başlar ("Üç bulgu vardı: ateş, öksürük ve hırıltı.").
- **Zarf-fiil ve virgül:** tek zarf-fiilden sonra virgül yok, art arda zarf-fiillerde var; ama "-arak" zinciri ayrıca iz (KAT-31).
- **Saat** noktayla: "17.30'da" (akademik/rapor zorunlu; post esnek).
- **Birleşik kelime:** ön yargı, yan etki, arka plan, alt grup ayrı; hissetmek, kaybolmak bitişik.

## Şapka (kipe bağlı)

- post, rapor: şapkasız ("yapay zeka", "kağıt", "hikaye"); "zekâ" HATA; anlam ayıranlar (hâlâ, kâr, âdet) BİLGİ.
- öğretici: şapkasız varsayılan, anlam ayıranlar serbest.
- akademik: **TDK zorunlu** ("dâhil", "hâlâ", "resmî", "yapay zekâ").
- sesli: yazım fark etmez; "hala/hâlâ" karışmasın.
