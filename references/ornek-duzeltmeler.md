# Örnek düzeltmeler

Gerçek kullanımda okurların verdiği geri bildirimlerden çıkarılmış, genel geçer dil kuralları. Kişi, tarih ve mesaj metni bilerek yok; yalnız kural ve gerekçe var. Kod (D1, D2, ...) katalogda ve `kurallar.json`'da `kaynak` alanında geçer. Yeni bir düzeltme geldiğinde bu tabloya satır olarak eklenir (öğrenen sözlük).

| # | Okurun itirazı (özet) | Kural | Kip | Katalog |
|---|---|---|---|---|
| D1 | Tanıtım iki noktası ve "zekâ" şapkası yapay duruyor | ":" ile tanıtım/vuruş yok; "zeka" şapkasız; kart içi metin ciddi kalabilir | post (şapka rapora da) | KAT-01, KAT-04 |
| D2 | Ham araştırma metni okunmuyor | ham araştırma notu okuma metni olarak verilmez | rapor | - |
| D3 | "Cümle yığını" | bağlamsız, birbirine bağlanmayan cümle yığını iz | rapor, öğretici | KAT-35 |
| D4 | Okur orta düzey İngilizce biliyor | okuma metni Türkçe; çeviri kokusu bu kipte ağır | öğretici | KAT-20…28 |
| D5 | Seslendirmede yabancı kelime kayıyor | yabancı kelime TTS'te kayıyor: okunuşla yaz ya da azalt | sesli | KAT-70 |
| D6 | Örnek herkese uymuyor | jenerik ofis örneği iz | post | model okuması |
| D7 | Ne yapay ne aşırı basit olsun | iç jargon yok, aşırı basitlik yok; terim kalır | post, öğretici | koruma 4 |
| D8 | Seste vurgu yok | sesli metinde yeni bilgi yüklem önüne, durak | sesli | KAT-73, K-27 |
| D9 | Tekdüzelik dinlemeyi zorlaştırıyor | tekdüze ritim sesli metinde daha ağır | sesli | KAT-14 |
| D10 | Konu ilgi çekmez | konu izi: ajanın iç süreci konu olarak AI gibi okunur | post | model okuması |
| D11 | Kullanıcı ham fikir veriyor | kullanıcının cümleleri korunur, yazım düzelir, yorumlanan belirsiz ifade söylenir | post (yanıt) | koruma 9, V03 |
| D12 | Açılıştaki referansa sonda dönmek gereksiz | açılış referansına sonda dönmek "biliyoruz gösterisi" | post | KAT-15 |
| D13 | "betik" az bilinen bir kelime | **"betik" değil "kod"** | bütün kipler | KAT-50 |
| D14 | arXiv'de yayımlanan çalışma preprint'tir | yerleşik terim: preprint | - | KAT-50 |
| D15 | "ön baskı" yapay duruyor | **"preprint"**; literatür postunda ayrıntı ilk yanıta | post | KAT-50, V02 |
| D16 | Cümleler bağlam kurmuyor | öğretici: temel önce, cümleler bağlaçla, terim ilk kullanımda tanımlı | öğretici | KAT-35 |
| D17 | Sadeleştirme istenmiyor | anlaşılırlık sadeleştirme değildir | tümü | koruma 3 |
| D18 | İçerik azaltılmasın | doğallaştırıcı içerik azaltmaz, terim sadeleştirmez | tümü | koruma 3, 4 |
| D19 | Anlatıcı notu okunduğunda konuşma gibi olsun | anlatıcı notu = konuşma metni, birinci tekil, sınıfa hitap | sesli | KAT-72, V08 |
| D20 | Tıbbi Türkçede "kan gazı" tek başına "gaz" denmez | kan gazı anlamında tek başına "gaz" yok | sesli, slayt | KAT-50 |
| D21 | Verilen örnek her yerde kullanılmasın | örnek ifade sabit kalıba çevrilmez | genel | model okuması |
| D22 | Okuma metni slayt değildir | slayt dil kuralları okuma metnine zorla uygulanmaz | öğretici | KAT-50 ('gaz' öğreticide BİLGİ) |
| D23 | "Birinci, ikinci, üçüncü" sıralaması AI gibi | sıra sözüyle numaralama yok | akademik, genel | KAT-34 |
| D24 | Akademik yazım kararları | OR/LR Türkçeleştirilmez; "bu çalışmada"; Yöntem/Bulgular "-dı/-ldı" tercih edilir (raporlanır, toplu dönüştürülmez) | akademik | KAT-60, KAT-67, KAT-50 |
| D25 | Yazarın kendi dili öğrenilsin | ses kartı: kişinin kendi yazısından ölçü al | genel | - |
| D26 | İngilizce terim geçince terimi bırak, cümleyi Türkçe kur | terim korunur, söz dizimi Türkçe | tümü | koruma 4, V03 |

## Ses kartı (kişinin kendi yazısından ölçü almak)

Kullanıcı kendi yazısından örnek verdiyse ölçü odur. Alınacak: kısa satır, bir düşünce bir satır; konuşma sözleri ("vallahi, resmen, mesela, bakalım"); kanaat + temkin ("ihtiyatlı olmakta fayda var"); doğrudanlık; karışık İngilizce terim (context, design, validasyon). Alınmayacak: yazım hataları, "birşey/herşey", büyük harf tutarsızlığı. Doğallık pürüz eklemekle değil ritim, kanaat ve somutlukla kurulur.

## Proje kararları

- "ve" öncesi virgül TDK gereği bütün kiplerde HATA (sıralı cümlelerde de).
- Sesli kip okunuş tablosu `sesli-okunus.md`'dedir; koru.py sesli kipte onu kullanır.
- Okunabilirlik eşikleri projenin kendi metinlerinden kalibre edildi; yalnız BİLGİ, puan düşürmez (`kip-matrisi.md`).
