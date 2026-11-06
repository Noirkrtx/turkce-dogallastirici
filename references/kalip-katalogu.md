# Kalıp kataloğu

Her kalıp: **Tanı** (kodun ya da okurun neye baktığı) · **Örnek** (bizim metinlerimizden ya da kurulmuş; repo örneği değil) · **Düzeltme** · **Dokunma** (meşru kullanım) · **Kip / Şiddet** (ayrıntı `kurallar.json`) · **Dayanak** (K-xx: literatür ilke kodu, L-xx: `literatur.md`, TDK-xx: `tdk.md`, D-xx: `ornek-duzeltmeler.md`).

Kural kodu (`dil_denetim.py` çıktısındaki köşeli parantez) → kalıp kimliği. Değişiklik özetinde kimlik yazılır: "KAT-22: 'tasarlanmış olup' bölündü".

Toplam 60 kalıp (KAT-74…78 dış sözlükten eklendi). KAT-74 öncesi kip başına açık kalıp sayısı: post 27, rapor 46, ogretici 44, akademik 41, sesli 47, telgraf 13.

## KAT-01 · İki nokta ile tanıtım / vuruş
- **Kod:** `iki-nokta-tanitim, iki-nokta`
- **Tanı:** Satır '... şu:', '... bir sayfa:' ile bitip kısa bir ad ya da vuruşla tamamlanıyor.
- **Örnek:** "Her sabah bir dil bilgisi kuralı: Günün Kuralı." (V01)
- **Düzeltme:** "Her sabah bir dil bilgisi kuralını Günün Kuralı adıyla yazacağım."
- **Dokunma:** Şablon etiketleri (Sonuç:, Hedef:, Şimdi söyle:, Süre:, Kaynak:, Sayaç:), saat ve oran (14:30, 1:2), akademikte liste/tanım girişi.
- **Kip / Şiddet:** post HATA (tanıtım) / UYARI; rapor UYARI; öğretici UYARI/BİLGİ; akademik kapalı; sesli UYARI
- **Dayanak:** D1, 03a, TDK N2 (TDK'ye göre doğru, üslup kararı)

## KAT-02 · Uzun ve orta tire
- **Kod:** `em-dash, en-dash`
- **Tanı:** Metinde U+2014 ya da U+2013 var.
- **Örnek:** ham raporda "aylık ~€3–6 ek" aralığı orta tireyle (U+2013) yazılmış (V05).
- **Düzeltme:** Aralıkta kısa çizgi (5-7), cümlede virgül, nokta ya da parantez.
- **Dokunma:** Alıntı, İngilizce künye ve kod bloğu (maskelenir).
- **Kip / Şiddet:** bütün kiplerde HATA
- **Dayanak:** proje kararı, TDK Ç3, STY-06

## KAT-03 · Boşluklu tire ara söz
- **Kod:** `tire-ara`
- **Tanı:** ' - ' ile açılan ara söz.
- **Örnek:** "sonuç - bence - yanlış"
- **Düzeltme:** Virgül ya da parantez.
- **Dokunma:** Satır başı madde imi.
- **Kip / Şiddet:** bütün kiplerde UYARI
- **Dayanak:** TDK Ç4

## KAT-04 · Şapka
- **Kod:** `sapka, sapka-zeka, sapka-gerekli`
- **Tanı:** â, î, û içeren kelime.
- **Örnek:** "Yapay zekâ araçlarını deniyorum"
- **Düzeltme:** Bütün kiplerde şapkasız: 'zeka', 'kağıt', 'dahil' (KAT-66).
- **Dokunma:** Anlam ayıranlar (hâlâ, kâr, âdet) yalnız BİLGİ.
- **Kip / Şiddet:** bütün kiplerde HATA (zekâ) / UYARI (diğerleri); telgraf kapalı
- **Dayanak:** D1, 03 §8

## KAT-05 · -mektedir / -maktadır
- **Kod:** `mektedir`
- **Tanı:** Yüklem '-mektedir' ile bitiyor.
- **Örnek:** "Bu durum sorun yaratmaktadır."
- **Düzeltme:** Post/sesli: '-iyor' ya da geniş zaman. Rapor/öğretici: seyrelt.
- **Dokunma:** Akademikte yerleşik bilgi ve yorum ('düşündürmektedir'), yalnız yığılma KAT-64.
- **Kip / Şiddet:** post HATA; rapor UYARI; öğretici UYARI; akademik kapalı (KAT-64); sesli HATA
- **Dayanak:** Ç1, akademik yazım rehberi USL-05/08

## KAT-06 · -mıştır kesinlik eki
- **Kod:** `mistir`
- **Tanı:** Yüklem '-mıştır' ile bitiyor.
- **Örnek:** "Çalışma tamamlanmıştır."
- **Düzeltme:** Post: '-di' ya da '-miş'.
- **Dokunma:** Akademik Giriş/Tartışma (Başer: Türkçe norm); Yöntem/Bulgular için KAT-67.
- **Kip / Şiddet:** post UYARI; rapor UYARI; öğretici BİLGİ; akademik kapalı; sesli UYARI
- **Dayanak:** K-13, L08

## KAT-07 · Önem şişirme ve jenerik değerlendirme
- **Kod:** `ai-ifade`
- **Tanı:** 'önemli bir rol', 'büyük önem taşır', 'kapsamlı', 'vazgeçilmez', 'ışık tutar'.
- **Örnek:** "... sürücü basıncın yakından izlenmesi büyük önem taşır." (V06 temel çıktısı)
- **Düzeltme:** Neyi nasıl etkilediğini somut söyle ya da sil; somut fiil kaynakta yoksa uydurma.
- **Dokunma:** 'kritik hasta/stenoz/bakım', 'kilit' terim; 'anlamlı' istatistik terimi.
- **Kip / Şiddet:** post kalıba göre HATA/UYARI/BİLGİ; diğer kiplerde en çok UYARI; akademikte 'kritik/kapsamında' BİLGİ
- **Dayanak:** dil_denetim eski liste, SOZ-01/03

## KAT-08 · "X değil, Y" ve "sadece X değil, aynı zamanda Y"
- **Kod:** `ai-ifade`
- **Tanı:** Olumsuzla kurulan karşıtlıkla vurgu.
- **Örnek:** "Bu bir araç değil, bir yaklaşım."
- **Düzeltme:** İddiayı düz söyle: "Bu bir yaklaşım."
- **Dokunma:** Gerçek düzeltme ('ARR değil RRR raporlanmış'); 'yalnızca X değil, Y de' (Alpay doğru buluyor).
- **Kip / Şiddet:** post HATA; rapor/öğretici/sesli UYARI; akademik BİLGİ
- **Dayanak:** K-15 (06 düzeltmesi), 03a

## KAT-09 · Edilgen öğüt ve kaçamak edilgen
- **Kod:** `ai-ifade`
- **Tanı:** 'yapılmalıdır', 'söylenebilir', 'denilebilir'.
- **Örnek:** "Bu konuda dikkatli olunmalıdır."
- **Düzeltme:** Kim yapsın, söyle; post/rapor 'bence'.
- **Dokunma:** Akademik Sonuç bölümünde öneri ('ihtiyatla yorumlanmalıdır') BİLGİ.
- **Kip / Şiddet:** post UYARI; akademikte '-malıdır' BİLGİ
- **Dayanak:** K-09, USL-05

## KAT-10 · Soru sorup hemen cevaplamak
- **Kod:** `soru-cevap`
- **Tanı:** Soru cümlesinin ardından aynı paragrafta ≤7 kelimelik cevap.
- **Örnek:** "Ne kaybedersin? Çok şey."
- **Düzeltme:** Doğrudan söyle ya da soruyu açık bırak.
- **Dokunma:** Öğretici soru (cevap sonraki paragrafta), sesli [SOR]/[BEKLE].
- **Kip / Şiddet:** post/rapor/akademik UYARI; öğretici ve sesli kapalı
- **Dayanak:** 03b, sunum kuralları

## KAT-11 · Cümle başı bağlaç yığını
- **Kod:** `baglac-acilis`
- **Tanı:** Cümle 'Ayrıca', 'Öte yandan', 'Bununla birlikte', 'Dolayısıyla' ile açılıyor.
- **Örnek:** "Ayrıca bu yaklaşım ... Öte yandan ..."
- **Düzeltme:** Bağlaçsız bağla ya da önceki cümleye kat.
- **Dokunma:** Öğretici ve akademikte gerçek ilişkiyi adlandıran bağlaç (STY-07).
- **Kip / Şiddet:** post/rapor/sesli UYARI; öğretici ve akademik kapalı (KAT-30)
- **Dayanak:** K-01, L01

## KAT-12 · Açılış tekrarı ve cümle sonu kafiyesi
- **Kod:** `acilis-tekrar, son-kafiye`
- **Tanı:** 3+ cümle aynı kelimeyle açılıyor ya da aynı ekle bitiyor.
- **Örnek:** "Bu ... Bu ... Bu ..."
- **Düzeltme:** Birini isim cümlesi, soru ya da birleşik cümle yap.
- **Dokunma:** Akademikte '-mektedir' bitişleri (kapalı), terim tekrarı (STY-32).
- **Kip / Şiddet:** post/rapor/sesli UYARI; öğretici BİLGİ; akademik BİLGİ/kapalı
- **Dayanak:** dil_denetim, 03a

## KAT-13 · Kesik cümle yığını ve kesik parça
- **Kod:** `kesik-yigin, kesik-parca`
- **Tanı:** Art arda 3+ çok kısa cümle; virgülle doğranmış ≤4 kelimelik parça.
- **Örnek:** "Bazen, kısa, satranç." (V01)
- **Düzeltme:** "Arada kısa satranç notları da olur."
- **Dokunma:** Telgraf not, slayt iskeleti.
- **Kip / Şiddet:** post/rapor/sesli UYARI; öğretici UYARI/BİLGİ; akademik ve telgraf kapalı
- **Dayanak:** 03a

## KAT-14 · Tekdüze ritim
- **Kod:** `tekduze-ritim`
- **Tanı:** Cümle uzunluğunun değişim katsayısı <0,30 (UYARI), <0,40 (BİLGİ).
- **Örnek:** Hepsi 9-11 kelimelik beş cümle.
- **Düzeltme:** Bir kısa, bir uzun; birleştir ya da böl.
- **Dokunma:** Akademikte kapalı (STY-30: ritim yapay değiştirilmez).
- **Kip / Şiddet:** post/rapor/öğretici/sesli UYARI-BİLGİ; akademik kapalı
- **Dayanak:** K-23, L17

## KAT-15 · Paragraf sonu vurucu kapanış ve vecize
- **Kod:** `vurucu-kapanis`
- **Tanı:** Paragrafların çoğu kısa, özlü bir cümleyle bitiyor.
- **Örnek:** "... İşte fark bu."
- **Düzeltme:** Son fikirle bitir, ders çıkarma.
- **Dokunma:** Öğretici bölüm sonu özet ve köprü; akademik Sonuç bölümü.
- **Kip / Şiddet:** post HATA ilkesi (kod UYARI); rapor UYARI; öğretici BİLGİ; akademik kapalı
- **Dayanak:** K-31, D12

## KAT-16 · Üçlü sıralama
- **Kod:** `uclu-liste`
- **Tanı:** Kısa üç öğeli sıralama ('X, Y ve Z').
- **Örnek:** "okuduğumu, denediğimi, öğrendiğimi"
- **Düzeltme:** İkiye indir, birini aç, sıralamayı boz; bilgi taşıyan öğeyi silme.
- **Dokunma:** Gerçekten üç öğe olan sayım (tezde üç belirteç).
- **Kip / Şiddet:** post/rapor/sesli UYARI; öğretici ve akademik BİLGİ
- **Dayanak:** 03a, STY-07

## KAT-17 · Noktalı virgül
- **Kod:** `noktali-virgul`
- **Tanı:** Satırda ';'.
- **Örnek:** "Lisans açık; kurulum root ile uzaktan çekilen betikle." (V05)
- **Düzeltme:** Nokta ya da virgül.
- **Dokunma:** Akademikte ondalık virgüllü sayı listesi ('4,2 (3,1-5,8); 3,9 ...').
- **Kip / Şiddet:** post BİLGİ; rapor ve sesli UYARI; öğretici BİLGİ; akademik kapalı
- **Dayanak:** K-03, L01

## KAT-18 · Emoji ve Unicode kalın
- **Kod:** `emoji, kalin-unicode`
- **Tanı:** 1'den fazla emoji; 𝐤𝐚𝐥ı𝐧 harf.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** En çok 1 emoji; kalın yok.
- **Dokunma:** Hesabın kendi üslup kararı Unicode kalını onaylıyorsa (hesaba bağlı).
- **Kip / Şiddet:** post UYARI/HATA; rapor BİLGİ
- **Dayanak:** post üslup kuralları

## KAT-19 · Kelime tiki ve sayaç
- **Kod:** `tekrar`
- **Tanı:** 'aslında', 'ayrıca', 'peki', 'ise' yığılması.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** Tekrarı at.
- **Dokunma:** Tek kullanım.
- **Kip / Şiddet:** post/rapor/sesli UYARI; öğretici/akademik BİLGİ
- **Dayanak:** dil_denetim

## KAT-20 · -e sahip olmak
- **Kod:** `cev-sahip`
- **Tanı:** Niteleme için '-e sahip' ('yüksek özgüllüğe sahip test').
- **Örnek:** "bu boşluğu doldurma potansiyeline sahip olup" (V07a)
- **Düzeltme:** "bu boşluğu doldurabilir" ya da '-li / -i olan'.
- **Dokunma:** Somut mülkiyet ('eve sahip'), duygu ('sahip olmaktan gurur').
- **Kip / Şiddet:** post kapalı; diğer kiplerde UYARI
- **Dayanak:** K-14, L09 (Y sınıfı: aday)

## KAT-21 · 'tarafından' yığılması
- **Kod:** `cev-tarafindan`
- **Tanı:** Metinde 3+ 'tarafından'.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** Özneyi öne al; bir tanesi meşru.
- **Dokunma:** Resmî tek kullanım.
- **Kip / Şiddet:** BİLGİ
- **Dayanak:** CEV-03

## KAT-22 · -mekte olup / -miş olup
- **Kod:** `cev-olup`
- **Tanı:** Fiil + 'olup' ile ekleme zinciri.
- **Örnek:** "tasarlanmış olup ... içermemektedir" (V07a)
- **Düzeltme:** "tasarlanmıştır ve ... içermemektedir" ya da cümleyi böl.
- **Dokunma:** İsim + 'olup' ('0,0167 olup').
- **Kip / Şiddet:** post kapalı; diğer kiplerde UYARI
- **Dayanak:** SOZ-04, akademik yazım rehberi CEV

## KAT-23 · Belirsiz 'bir' yığılması
- **Kod:** `cev-bir-yigini`
- **Tanı:** Aynı cümlede 3+ 'bir'.
- **Örnek:** "bir kısmı ... bir grup ... bir şemsiye terim"
- **Düzeltme:** Deyime ve birleşik fiile eklenen 'bir'i at.
- **Dokunma:** 'anlamlı bir artış'ta 'anlamlı' terimdir, değişmez.
- **Kip / Şiddet:** BİLGİ
- **Dayanak:** K-17, L10

## KAT-24 · '... bir şekilde' zarfı
- **Kod:** `cev-bir-sekilde`
- **Tanı:** 'dikkatli bir şekilde', 'kritik bir şekilde'.
- **Örnek:** "etkinlikleri dikkatli bir şekilde planlamasını" (V07b)
- **Düzeltme:** "dikkatle planlamasını"
- **Dokunma:** Tek kelimelik zarfı olmayan ifade.
- **Kip / Şiddet:** post kapalı; diğer kiplerde UYARI
- **Dayanak:** CEV, humanizer #8

## KAT-25 · Gereksiz iyelik zamiri
- **Kod:** `cev-iyelik-zamir`
- **Tanı:** 'bizim çalışmamız', 'sizin öğrenciniz'.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** Zamiri at.
- **Dokunma:** Vurgu ya da karşıtlık.
- **Kip / Şiddet:** BİLGİ
- **Dayanak:** CEV-04

## KAT-26 · Zincirleme sıfat-fiil
- **Kod:** `cev-digi-zinciri`
- **Tanı:** Aynı cümlede 3+ '-dığı/-diği'.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** Böl.
- **Dokunma:** Tanım cümlesi.
- **Kip / Şiddet:** sesli UYARI; diğer BİLGİ
- **Dayanak:** K-20, L19

## KAT-27 · 'mevcut'
- **Kod:** `cev-mevcut`
- **Tanı:** 'mevcut' = 'var / eldeki'.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** 'var', 'eldeki'.
- **Dokunma:** Akademik 'mevcut örneklem' (kapalı).
- **Kip / Şiddet:** rapor/öğretici/sesli BİLGİ
- **Dayanak:** CEV

## KAT-28 · 'olarak' yığılması
- **Kod:** `cev-olarak-yigini`
- **Tanı:** Aynı cümlede 2+ 'olarak'.
- **Örnek:** "değersizliği olarak değil ... çerçevesinde"
- **Düzeltme:** Birini at.
- **Dokunma:** 'tedavi olarak', 'profilaksi olarak'.
- **Kip / Şiddet:** BİLGİ
- **Dayanak:** SOZ-04

## KAT-30 · 'Öncelikle' / 'Sonuç olarak' açılışı
- **Kod:** `yap-oncelikle`
- **Tanı:** Cümle bu kalıplarla açılıyor.
- **Örnek:** "Öncelikle şunu belirtmek gerekir..."
- **Düzeltme:** Sil.
- **Dokunma:** Akademik Sonuç bölümü özeti.
- **Kip / Şiddet:** rapor/sesli UYARI; öğretici/akademik BİLGİ
- **Dayanak:** K-01, L01 (06)

## KAT-31 · -arak/-erek zinciri
- **Kod:** `yap-arak-zinciri`
- **Tanı:** Aynı cümlede 2+ zarf-fiil ('olarak' hariç).
- **Örnek:** "vurgulayarak, ortaya koyarak"
- **Düzeltme:** Böl ya da çekimli yüklem + bağlaç; '-ip'e kaçma.
- **Dokunma:** Tek zarf-fiil.
- **Kip / Şiddet:** sesli UYARI; diğer BİLGİ
- **Dayanak:** K-02, L01

## KAT-32 · 'Bu durum / Bu da / Bu sayede' açılışı
- **Kod:** `yap-bu-durum`
- **Tanı:** Cümle öncülü belirsiz gösterme ile açılıyor.
- **Örnek:** "Bu durum, öğretmenin ... gerektirir" (V07b)
- **Düzeltme:** Öncülü adıyla an ya da 'Bu nedenle'.
- **Dokunma:** Öncülü tek ve açıksa.
- **Kip / Şiddet:** rapor/öğretici/sesli UYARI; akademik BİLGİ
- **Dayanak:** SOZ-05

## KAT-33 · 'Sonuç' ile başlayan cümle
- **Kod:** `yap-sonuc-acilis`
- **Tanı:** Cümle 'Sonuç' sözcüğüyle başlıyor.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** Yalnız bilgi.
- **Dokunma:** Şablon etiketi 'Sonuç:'.
- **Kip / Şiddet:** BİLGİ
- **Dayanak:** L01 (yazar: konuya bağlı)

## KAT-34 · Sıra sözüyle numaralama
- **Kod:** `yap-sira-sozu`
- **Tanı:** 'İlk olarak ... İkinci olarak ... Son olarak'.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** Numaralamayı kaldır, ilişkiyi bağlaçla kur.
- **Dokunma:** Sesli kipte sınıfta adım sayma (ölçülü).
- **Kip / Şiddet:** rapor/öğretici/akademik UYARI; sesli kapalı
- **Dayanak:** D23, STY-05

## KAT-35 · Cümle uzunluğu kip hedefi dışında
- **Kod:** `yap-uzun-ort, yap-kisa-ort, uzun-cumle`
- **Tanı:** Ortalama: post >18, rapor >16, öğretici >20 ya da <12, akademik >20, sesli >16.
- **Örnek:** V06 ilk turda ort. 11,6 (aşırı bölünmüş)
- **Düzeltme:** Böl ya da bağlaçla birleştir.
- **Dokunma:** Tıbbi terim yoğun cümle.
- **Kip / Şiddet:** BİLGİ (sesli UYARI)
- **Dayanak:** K-24 (ev varsayılanı)

## KAT-40 · 've/veya/yahut' öncesi virgül
- **Kod:** `tdk-ve-virgul`
- **Tanı:** ', ve ' / ', veya ' / ', yahut '.
- **Örnek:** "Raporu okudum, ve yeni bir ölçüm istedim."
- **Düzeltme:** Virgülü sil.
- **Dokunma:** 'ya da' (TDK listesinde yok). Ara sözün kapanış virgülü şüphesinde model okur ama kural HATA kalır (proje kararı).
- **Kip / Şiddet:** bütün kiplerde HATA
- **Dayanak:** TDK-V1

## KAT-41 · 'hem ..., hem' virgülü
- **Kod:** `tdk-hem-hem`
- **Tanı:** Tekrarlı bağlaç arasında virgül.
- **Örnek:** "Hem gider, hem ağlar."
- **Düzeltme:** Virgülü sil.
- **Dokunma:** istisna tanımlanmadı
- **Kip / Şiddet:** UYARI
- **Dayanak:** TDK-V2

## KAT-42 · Sayı yazımı
- **Kod:** `tdk-yuzde, tdk-sira-kesme, tdk-rakamla-baslama`
- **Tanı:** '25%', '% 25', '8.'inci', cümle rakamla başlıyor.
- **Örnek:** "45 öğrenci dahil edildi."
- **Düzeltme:** '%25', '8.' ya da '8'inci', 'Çalışmaya 45 öğrenci alındı.'
- **Dokunma:** Numaralı başlık ('1. Giriş'), madde.
- **Kip / Şiddet:** yüzde/sıra HATA; rakamla başlama rapor/akademik UYARI
- **Dayanak:** TDK-S2, S6, S8

## KAT-43 · Ondalık nokta
- **Kod:** `tdk-ondalik-nokta`
- **Tanı:** 'p<0.05', 'OR 1.41'.
- **Örnek:** "(%95 GA 1.52-3.83)" (V07d temel çıktısı)
- **Düzeltme:** Ondalık virgül: '1,29'.
- **Dokunma:** Sürüm (2.1.317, GPT-5.2), saat (17.30), bölüm/tablo no (Tablo 2.1), İngilizce künye.
- **Kip / Şiddet:** post kapalı; diğer UYARI
- **Dayanak:** TDK-S3, V10

## KAT-44 · Bitişik/ayrı yazım
- **Kod:** `tdk-yada, tdk-belirsizlik-bitisik, tdk-bir-takim, tdk-sey-bitisik, tdk-isbirligi, tdk-ki-bitisik, tdk-oysa-ki`
- **Tanı:** yada, bir çok, hiç bir, herşey, işbirliği, demekki.
- **Örnek:** "herşeyi düz metin gibi okuyor" (V10)
- **Düzeltme:** ya da, birçok, hiçbir, her şey, iş birliği, demek ki.
- **Dokunma:** kullanıcının ham mesajı ve alıntı (KORU); 'bir takım kurduk' (sayı + ad).
- **Kip / Şiddet:** HATA ('bir takım' UYARI, 'oysa ki' BİLGİ)
- **Dayanak:** TDK-B1, B3, B4, B7, B8, B12

## KAT-45 · Kesme işareti
- **Kod:** `tdk-tirnak-kesme, tdk-kurum-kesme, tdk-ayrac-kesme`
- **Tanı:** Tırnaktan sonra kesme; kurum adına kesme; ayraçtan sonra ek.
- **Örnek:** "Türk Dil Kurumu'nun"
- **Düzeltme:** "Türk Dil Kurumunun"
- **Dokunma:** Yabancı kurum/proje adı ('ARDS Network'ün'), unvan ('Başkanı'na').
- **Kip / Şiddet:** HATA
- **Dayanak:** TDK-T3, K2, K8

## KAT-46 · İki nokta / dört nokta
- **Kod:** `tdk-uc-nokta`
- **Tanı:** '..' ya da '....'.
- **Örnek:** "Ali...."
- **Düzeltme:** '...'
- **Dokunma:** '?..', '!..' (TDK doğru).
- **Kip / Şiddet:** UYARI
- **Dayanak:** TDK-N4 (06 düzeltmesi)

## KAT-47 · Belirsiz sayı
- **Kod:** `tdk-belirsiz-sayi`
- **Tanı:** '1,500' gibi binlik mi ondalık mı belli olmayan sayı.
- **Örnek:** "Raporda 1,500 hasta yazıyor" (V12)
- **Düzeltme:** Dokunma; raporda not düş.
- **Dokunma:** Baştaki sıfır (0,350) ondalıktır.
- **Kip / Şiddet:** BİLGİ (post kapalı)
- **Dayanak:** NOK-03, 05 §3

## KAT-50 · Alan sözlüğü
- **Kod:** `alan-betik, alan-on-baski, alan-respiratuvar, alan-olasilik-orani, alan-gaz`
- **Tanı:** 'betik', 'ön baskı', 'respiratuvar', 'olasılık oranı', kan gazı anlamında tek başına 'gaz'.
- **Örnek:** "uzaktan çekilen betikle" (V05)
- **Düzeltme:** 'kod', 'preprint', 'solunumsal', 'odds ratio (OR)', 'bu kan gazında'.
- **Dokunma:** kullanıcının kelimeyi andığı meta cümle (V10); fizik anlamında 'gaz değişimi'; öğretici okuma metninde 'gaz' (D22).
- **Kip / Şiddet:** betik/ön baskı HATA; diğerleri UYARI/BİLGİ
- **Dayanak:** D13, D15, D20, D24

## KAT-60 · 'çalışmamızda / kliniğimizde'
- **Kod:** `aka-iyelik-calisma`
- **Tanı:** Akademikte birinci çoğul iyelik.
- **Örnek:** "Çalışmamızda yüksek okuma kaygısının" (V07e temel çıktısı)
- **Düzeltme:** 'Bu çalışmada'.
- **Dokunma:** istisna tanımlanmadı
- **Kip / Şiddet:** akademik UYARI
- **Dayanak:** D24

## KAT-61 · Kaçınma yığılması
- **Kod:** `aka-kacinma-yigini`
- **Tanı:** 'olabileceği düşünülebilir', 'muhtemelen olabilir'.
- **Örnek:** "yararlı olabileceği düşünülebilir bir sinyaldir" (V13)
- **Düzeltme:** Tek kaçınma: 'yararlı olabileceğini düşündüren'. Sıfıra indirme.
- **Dokunma:** Tek kaçınma.
- **Kip / Şiddet:** akademik HATA; diğer UYARI
- **Dayanak:** K-26, STY-13

## KAT-62 · Öznesiz yorum edilgeni
- **Kod:** `aka-oznesiz-yorum`
- **Tanı:** '... olduğu düşünülmektedir'.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** 'Bu bulgu, X'i düşündürmektedir' (USL-05).
- **Dokunma:** istisna tanımlanmadı
- **Kip / Şiddet:** akademik UYARI
- **Dayanak:** akademik yazım rehberi USL-05

## KAT-63 · İstatistik yazım tuzakları
- **Kod:** `aka-p-sifir, aka-anlamliliga-yaklasti`
- **Tanı:** 'p=0,000', 'anlamlılığa yaklaştı'.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** 'p<0,001'; p değerini ver, 'anlamlı değil' de.
- **Dokunma:** istisna tanımlanmadı
- **Kip / Şiddet:** HATA / UYARI
- **Dayanak:** akademik yazım rehberi

## KAT-64 · -mektedir yoğunluğu
- **Kod:** `aka-mektedir-yogunluk`
- **Tanı:** Yüklemlerin yarısından çoğu '-mektedir'.
- **Örnek:** V07e Tartışma paragrafı (5/7 yüklem '-mektedir')
- **Düzeltme:** Bulgu cümlelerini '-mış/-dı', yerleşik bilgiyi '-mektedir' bırak.
- **Dokunma:** Yerleşik bilgi, yorum.
- **Kip / Şiddet:** akademik UYARI
- **Dayanak:** Ç1, YAPI-03

## KAT-65 · Promosyon ve öncelik iddiası
- **Kod:** `aka-ilk-kez`
- **Tanı:** 'ilk kez', 'benzersiz', 'çığır açan'.
- **Örnek:** "Ancak bu çığır açan vizyon" (V11 temel çıktısı)
- **Düzeltme:** Kanıtla sınırla ya da sil.
- **Dokunma:** Kanıtlı öncelik (literatür taramasıyla).
- **Kip / Şiddet:** akademik UYARI; diğer BİLGİ
- **Dayanak:** akademik yazım rehberi ABR

## KAT-66 · Akademik şapka (kaldırıldı)
- **Kod:** `aka-sapka` (bütün kiplerde kapalı)
- **Karar:** Tez dahil hiçbir metinde şapka kullanılmaz. Şapkalı yazım her kipte `sapka` / `sapka-zeka` kuralına düşer ('dâhil' → 'dahil', 'zekâ' → 'zeka').
- **Uzun/orta çizgi:** tezde de yok; aralıklar kısa çizgiyle ("%95 GA 1,42-3,76", "2024-2026").

## KAT-67 · Yöntem/Bulgular'da -mıştır
- **Kod:** `aka-mistir-bolum`
- **Tanı:** --bolum yontem|bulgular iken '-mıştır'.
- **Örnek:** "tasarlanmıştır" (V07c)
- **Düzeltme:** Proje kuralı: '-dı/-ldı'. **Raporlanır, toplu dönüştürülmez**: tez sahibinin kararı (Başer: Türkçe norm).
- **Dokunma:** Giriş, Tartışma.
- **Kip / Şiddet:** akademik UYARI (yalnız --bolum ile)
- **Dayanak:** D24, K-13

## KAT-70 · Okunuşu yazılmamış kısaltma ve birim
- **Kod:** `ses-kisaltma, ses-birim`
- **Tanı:** Sesli metinde 'EKG', 'mmHg', 'PaCO2'.
- **Örnek:** "Verilen göl örneğinin pH’ı 7,9 korunur" (V08)
- **Düzeltme:** Okunuş tablosuyla yaz: 'pe ha yedi virgül dokuz'.
- **Dokunma:** Okunuşu yerleşik kısaltma (tabloda ilk okunuş kısaltmanın kendisi değilse yaz).
- **Kip / Şiddet:** sesli UYARI
- **Dayanak:** K-30, D5

## KAT-71 · Okunmayan işaret
- **Kod:** `ses-parantez, ses-egik-cizgi, ses-simge`
- **Tanı:** Parantez, '/', ≥, %, → .
- **Örnek:** "Sor / bekle: ... KT geri hesabıyla"
- **Düzeltme:** Tam cümleye aç.
- **Dokunma:** Şablon etiketi.
- **Kip / Şiddet:** sesli UYARI
- **Dayanak:** K-30

## KAT-72 · İç not sızıntısı
- **Kod:** `ses-ic-not, ses-banka-vaka`
- **Tanı:** Dosya adı, v2, §, 'denetim', 'aktarım', 'prova ölçülmedi', 'Vaka 23'.
- **Örnek:** "Taslak ilk4 aktarım denetimi bitti; tam45dk/prova/Linux açık." (V08)
- **Düzeltme:** Sil; vaka ders içi sırayla ('birinci vaka'). Silinenleri koru.py --muaf ile kaydet.
- **Dokunma:** istisna tanımlanmadı
- **Kip / Şiddet:** sesli HATA
- **Dayanak:** D19, sunum kuralları

## KAT-73 · Nefessiz cümle
- **Kod:** `ses-uzun-cumle`
- **Tanı:** Sesli metinde 25+ kelimelik cümle.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** Böl; yeni bilgiyi yüklemin hemen önüne koy (K-27).
- **Dokunma:** istisna tanımlanmadı
- **Kip / Şiddet:** sesli UYARI
- **Dayanak:** K-29, L14

## KAT-74 · Süslü abartı (AI sözlüğü)
- **Kod:** `ai-abarti-sus`
- **Tanı:** 'yadsınamaz', 'adeta', 'geniş bir yelpaze', 'dönüm noktası', 'kilometre taşı', 'kilit rol', 'kalbinde yer alan', '... kanıtıdır', 'gözler önüne serer', 'zahmetsizce', 'titizlikle', 'kilidini aç'.
- **Örnek:** "Günümüzde yapay zekanın etkisi yadsınamaz." (V14)
- **Düzeltme:** Sil ya da somut olguyla değiştir.
- **Dokunma:** 'mozaik' bilerek listede yok (mozaik trizomi, V15).
- **Kip / Şiddet:** post/rapor/öğretici/sesli UYARI; akademik BİLGİ; telgraf kapalı
- **Dayanak:** yucezerey/turkish-anti-ai-skill sözlüğü (MIT), proje kararı

## KAT-75 · Söylem anonsu ve bürokratik bağ
- **Kod:** `ai-soylem-anons, ai-burokratik-bag`
- **Tanı:** 'unutulmamalıdır ki', 'belirtmek gerekir ki', 'son tahlilde', 'mesele şu ki', 'uzmanlar belirtiyor ki', 'araştırmalar göstermektedir ki'; 'bu doğrultuda', 'bu çerçevede', 'bahsi geçen'.
- **Örnek:** "Unutulmamalıdır ki her model hata yapar." (V14)
- **Düzeltme:** Anonsu sil, söyleneni doğrudan söyle; otoriteyi adıyla kaynakla.
- **Dokunma:** Akademik metin (V15); 'bu noktada' bilerek listede yok.
- **Kip / Şiddet:** post/rapor/sesli UYARI; öğretici UYARI/BİLGİ; akademik ve telgraf kapalı
- **Dayanak:** yucezerey sözlüğü, proje kararı

## KAT-76 · Pazarlama çevirisi ve gizli negatif paralellik
- **Kod:** `ai-pazarlama-ceviri, ai-negatif-paralel`
- **Tanı:** 'sinerji', 'paradigma değişimi', 'proaktif', 'bir üst seviyeye', 'hepsi bir arada', 'istifade et'; 'yalnızca X olmakla kalmayıp', 'mesele X değil,'.
- **Örnek:** "Uygulama yalnızca hızlı olmakla kalmayıp güvenli de." (V14)
- **Düzeltme:** Somut faydayı düz cümleyle yaz; olumsuz yarıyı at.
- **Dokunma:** Gerçek düzeltme (KAT-08).
- **Kip / Şiddet:** post/rapor/öğretici/sesli UYARI; akademik BİLGİ
- **Dayanak:** yucezerey sözlüğü, proje kararı

## KAT-77 · Cümle başında gereksiz kişi zamiri
- **Kod:** `yap-zamir-acilis`
- **Tanı:** Cümle 'Ben'/'Biz' ile açılıyor, yüklem kişiyi zaten gösteriyor.
- **Örnek:** (henüz bizim metinlerimizden örnek yok)
- **Düzeltme:** Zamiri düşür.
- **Dokunma:** Vurgu/karşıtlık ('Ben bu özelliği henüz denemedim'); bu yüzden post ve sesli kipte kapalı.
- **Kip / Şiddet:** rapor/öğretici BİLGİ; post, sesli, akademik kapalı
- **Dayanak:** yucezerey sentaks rehberi, geriye uyum testi

## KAT-78 · Başlıkta Title Case
- **Kod:** `yap-baslik-title-case`
- **Tanı:** Markdown başlığında bağlaç büyük ('Kurulum Ve Kullanım').
- **Örnek:** "## Kurulum Ve Kullanım"
- **Düzeltme:** Bağlaçları küçük yaz ya da tümce düzeni kullan.
- **Dokunma:** Özel ad.
- **Kip / Şiddet:** UYARI; sesli kapalı
- **Dayanak:** TDK, yucezerey notu

## Model okuması (kodla ölçülmeyenler)

- **Konu izi (post):** "Bunu bir insan kendi hayatında yazar mıydı, yoksa bir ajanın görev raporu mu?" İkincisiyse konu değişir (D10).
- **Uydurma ayrıntı:** "denedim, kullanıyorum, en sevdiğim" kayıt yoksa yazılmaz (03b §6).
- **Jenerik örnek:** beyaz yaka ofis örneği (D6).
- **Terim Türkçeleştirme:** agent → ajan, context → bağlam, summary → özet kullanıcının ham metninde yapılmaz (D26). V03 temel çıktısı bu yüzden kalıyor; kod ölçütü yakalamıyor.
- **Olgu hatası:** fark edilir, düzeltilmez, raporlanır ('1,37 kat artırıyordu').
- **Eşanlamlı ikame:** yöntem değildir (K-04, DAMAGE); yapı değişir.
