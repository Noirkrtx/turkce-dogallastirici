# Sesli kip okunuş tablosu

Sesli kipte (anlatıcı notu, canlı kart konuşma satırı, TTS okuma metni) sayı, simge, birim ve kısaltma bilerek açılır. Bu tablo iki iş görür:

1. Yeniden yazarken hangi okunuşun kullanılacağını söyler (ilk okunuş önerilen, diğerleri kabul edilen).
2. `scripts/koru.py --kip sesli` iki metni karşılaştırmadan önce okunuşları bu tabloyla simgeye geri çevirir. **Tabloda olmayan dönüşüm koruma HATA'sı verir** (değer ya da terim kaybolmuş sayılır). Yeni bir okunuş gerekiyorsa önce buraya satır ekle.

Kurallar (tablonun dışında, kodda):

- **`#` işareti:** okunuşta sayının yeri ("kilogram başına # miligram" = "kilogram başına sıfır virgül bir miligram"). Türkçe söyleyişte birim sayının iki yanına bölünebildiği için gerekli.
- **Sayı:** rakamla yazılmış sayı yazıyla okunur: `12` → "on iki", `1.500` → "bin beş yüz". Sesli metinde rakam bırakmak da serbest (TTS okur), ama aynı metinde tek biçim.
- **Ondalık:** tam kısım + "virgül" + ondalık kısım. Ondalık kısım ya bütün sayı olarak ("7,25" → "yedi virgül yirmi beş") ya da baştaki sıfırlar tek tek okunarak ("0,002" → "sıfır virgül sıfır sıfır iki") yazılır. İkisi de geri çevrilir.
- **Yüzde:** `%95` → "yüzde doksan beş". İşaret önde olduğu gibi okunuş da önde.
- **Aralık:** `1,4-3,8` → "bir virgül dört ile üç virgül sekiz arası". Kısa çizgi okunmaz, "ile" söylenir.
- **Karşılaştırma işaretinin yönü korunur:** `p<0,001` "pe değeri sıfır virgül sıfır sıfır birden küçük" olarak da yazılabilir; koru.py yönü `<`, `>`, `≤`, `≥` çiftinde denetler, "=" yalnız okunuş farkıdır.
- **Atıf işareti** ([12], (4,9)) sesli metinde okunmaz; koru.py sesli kipte atıf kaybını HATA değil UYARI sayar, atıf konuşmacı notunun kaynak satırında kalmalıdır.
- **Tek başına "bir"** sayı sayılmaz (belirsizlik sözcüğü); yalnız "virgül", birim ya da "yüzde" ile birlikteyse sayıdır.

## Tablo

| yazım | okunuşlar (; ile ayrılır, ilki önerilen) | tür |
|---|---|---|
| mmHg | milimetre cıva; milimetre civa | birim |
| cmH₂O | santimetre su; santimetre su basıncı | birim |
| cmH2O | santimetre su; santimetre su basıncı | birim |
| mL/kg | kilogram başına # mililitre; kilo başına # mililitre; kilogram başına mililitre | birim |
| mg/kg | kilogram başına # miligram; kilo başına # miligram; kilogram başına miligram; kilo başına miligram | birim |
| µg/kg/dk | kilogram başına dakikada # mikrogram; dakikada kilogram başına # mikrogram; kilo başına dakikada # mikrogram; kilogram başına dakikada mikrogram | birim |

| mEq/L | litrede # miliekivalan; litre başına # miliekivalan; litrede miliekivalan | birim |
| mmol/L | litrede # milimol; litrede milimol | birim |
| mg | miligram | birim |
| µg | mikrogram | birim |
| mcg | mikrogram | birim |
| mL | mililitre | birim |
| kg | kilogram | birim |
| dk | dakika | birim |
| sn | saniye | birim |
| ms | milisaniye | birim |
| IU | ünite; uluslararası ünite | birim |
| % | yüzde | simge |
| ≥ | büyük ya da eşit; büyük eşit; en az | simge |
| ≤ | küçük ya da eşit; küçük eşit; en çok | simge |
| < | küçüktür | simge |
| > | büyüktür | simge |
| ± | artı eksi | simge |
| P/F | pe bölü ef; pe bölü ef oranı | kısaltma |
| pH | pe ha | kısaltma |
| CO2 | karbondioksit; ce o iki | kısaltma |
| pCO₂ | pe ce o iki; karbondioksit kısmi basıncı | kısaltma |
| PaCO2 | pe a ce o iki; arteriyel karbondioksit basıncı | kısaltma |
| PaO2 | pe a o iki; arteriyel oksijen basıncı | kısaltma |
| HCO₃ | bikarbonat; ha ce o üç | kısaltma |
| SpO2 | oksijen satürasyonu; es pe o iki | kısaltma |
| FiO2 | fi o iki; solunan oksijen oranı | kısaltma |
| PEEP | pip; ekspirasyon sonu pozitif basınç | kısaltma |
| Pplat | plato basıncı; pe plat | kısaltma |
| Ppeak | tepe basıncı; pe pik | kısaltma |
| OR | odds oranı; o er | kısaltma |
| RR | göreli risk; rölatif risk; er er | kısaltma |
| HR | hazard oranı; tehlike oranı | kısaltma |
| NNT | tedavi edilmesi gereken hasta sayısı; en en te | kısaltma |
| NNH | zarar görmesi beklenen hasta sayısı; en en ha | kısaltma |
| AUC | eğri altındaki alan; a u ce | kısaltma |
| GA | güven aralığı | kısaltma |
| p | pe değeri | kısaltma |
| IV | damar yoluyla; damardan; i ve | kısaltma |
| IM | kas içine; i me | kısaltma |
| PO | ağızdan; pe o | kısaltma |
| EKG | e ka ge; elektrokardiyografi | kısaltma |
| BT | be te; bilgisayarlı tomografi | kısaltma |
| MR | em er; manyetik rezonans | kısaltma |
| ARDS | ards; a er de es | kısaltma |
| QTc | düzeltilmiş QT; ku te ce | kısaltma |
| GRACE | greys; greys skoru | kısaltma |
| Sınıf I | sınıf bir | öneri sınıfı |
| Sınıf IIa | sınıf iki a | öneri sınıfı |
| Sınıf IIb | sınıf iki be | öneri sınıfı |
| Sınıf III | sınıf üç | öneri sınıfı |
| Düzey A | düzey a | kanıt düzeyi |
| Düzey B | düzey be | kanıt düzeyi |
| Düzey C | düzey ce | kanıt düzeyi |

Not: "pip" (PEEP) ve "greys" (GRACE) İngilizce okunuşun Türkçe yazımıdır; alanda yerleşik söyleyiş farklı olabilir, ilk TTS denemesinde dinlenmeli (D5: yabancı kelime kayması).
