# Türkçe doğallaştırıcı

Yapay zekayla yazılmış Türkçe metin çoğu zaman tek bir kelimeden değil, cümlelerin kuruluşundan belli oluyor. Her yüklem "-mektedir" ile bitiyor, paragraflar "bu bağlamda" diye açılıyor, sonunda da her şeyi bir kez daha özetleyen bir cümle duruyor. Bu skill o izleri bulup metni yeniden yazdırıyor.

Kısa bir örnek vereyim.

```text
Önce:  Günümüzde yapay zekânın etkisi yadsınamaz. Ankette katılımcıların %62'si aracı
       her gün kullandığını belirtmiş olup, bu durum dikkatli bir şekilde değerlendirilmelidir.

Sonra: Ankete katılanların %62'si aracı her gün kullandığını söylüyor. Bu oranı yorumlarken
       dikkatli olmak gerekiyor.
```

Yeniden yazımda en riskli şey anlamın kayması. Bu yüzden iş bitince bir kod eski metinle yenisini karşılaştırıyor. Bir sayı, birim ya da atıf değiştiyse, "olabilir" gibi bir temkin kelimesi düştüyse bunu hata olarak bildiriyor ve metin teslim edilmiyor. Yukarıdaki örnekte %62 yanlışlıkla %26 olsaydı kod bunu böyle bildirirdi.

```text
KORUMA İHLAL  ·  kip rapor  ·  HATA 2
  HATA  [sayi-birim] 1 öğe kayboldu ya da değişti   - ('%62', '')
  HATA  [sayi-birim] 1 yeni öğe eklendi              + ('%26', '')
```

Skill, [Agent Skills](https://agentskills.io) biçiminde yazıldı. Claude Code, Codex ve Hermes ile kullanılabiliyor. Denetim kodları saf Python, skill olmadan da tek başına çalışıyor.

## Metnin türüne göre çalışıyor

Bir postta düzeltilmesi gereken şey bir tezde doğru olabilir. Tezde "-mektedir" de edilgen çatı da temkinli dil de yerinde, oraya dokunmak metni bozar. Bu yüzden skill önce metnin türünü, yani kipini seçiyor.

| Kip | Hangi metin için | Ne kadar dokunur |
|---|---|---|
| `post` | sosyal medya postu, yanıt | en serbest; ritim, anons ve kapanış cümlesi düzeltilir |
| `rapor` | mesajla gönderilen rapor, haftalık özet | açık ve kısa olsun diye yeniden kurar |
| `ogretici` | ders notu, okuma metni | açıklamayı korur, tekrarı ve dolguyu atar |
| `akademik` | tez, makale, özet | çok az; yalnız açık çeviri kalıpları ve yazım |
| `sesli` | sunum notu, sesli okunacak metin | nefes yerleri, okunuşu yazılmamış kısaltmalar |
| `telgraf` | madde listesi, slayt iskeleti | yalnız yazım ve noktalama |

Kipler arasındaki farklar [`kip-matrisi.md`](references/kip-matrisi.md) dosyasında anlatılıyor. Her kalıbın örneği, nasıl düzeltileceği ve hangi durumda dokunulmayacağı da [`kalip-katalogu.md`](references/kalip-katalogu.md) dosyasında.

## Neye dokunmuyor

Aşağıdakileri [`koru.py`](scripts/koru.py) kodu denetliyor.

- **Sayılar ve birimler.** `%62`, `0,1 mg/kg`, `2024-2026`; büyüktür ve küçüktür işaretlerinin yönü de dahil. "1,500" gibi binlik mi ondalık mı belli olmayan sayıya dokunulmaz, not düşülür.
- **Terimler, kısaltmalar, özel adlar, sürüm numaraları.** `preprint`, `%95 GA`, `Claude Code 2.1.317`.
- **Atıflar ve alıntılar.** `[12]`, `(Yazar, 2024)`, DOI, URL, tırnak içi. Cümle ikiye bölünürse atıf ait olduğu önermeyle birlikte gider.
- **Temkin.** "olabilir", "ilişkili", "düşündürüyor", "henüz" yerinde kalır. Üst üste yığılmış temkin teke iner ama hiçbir zaman sıfıra inmez. "1,4 kat risk" de "riski artırdı"ya çevrilmez.
- **Şablon işaretleri.** `{{yer_tutucu}}`, `[Kurum adı]` gibi doldurulacak alanlar.

Tam liste [`koruma-kurallari.md`](references/koruma-kurallari.md) dosyasında.

Bilerek yapmadıkları da var. Yapay zeka dedektörlerini atlatmak için yazılmadı, amaç okunur Türkçe. Metni sadeleştirmiyor, terimi basitleştirmiyor, kaynakta olmayan bir bilgi ya da deneyim eklemiyor. Metinde bir olgu hatası görürse düzeltmiyor, bildiriyor. Zaten doğal olan metne dokunmuyor. İngilizce metin, kod, tablo ve kaynakça için kullanılmamalı.

Kodun yakalayamadığı şeyler de var. Uydurulmuş bir ayrıntıyı ya da bir terimin gereksiz yere Türkçeleştirilmesini (agent → ajan) ancak model okuyarak fark edebilir. Skill bu yüzden kod denetiminin yanında bir okuma adımı da istiyor.

## Adım adım kurulum

Önce repoyu indir:

```bash
git clone https://github.com/Noirkrtx/turkce-dogallastirici.git
```

Skill klasörü repo kökünün kendisidir: `SKILL.md`, `scripts/`, `references/` ve `evals/` aynı klasörde durmalı. Kodlar `references/` klasörünü kendi konumlarına göre bulur, o yüzden klasörü bütün olarak taşı.

### (a) Claude Code

Claude Code skill'leri `~/.claude/skills/<skill-adı>/SKILL.md` (kişisel, bütün projelerde) ya da proje içinde `.claude/skills/<skill-adı>/SKILL.md` (yalnız o repo) konumundan okur.

1. Kişisel kurulum:
   ```bash
   mkdir -p ~/.claude/skills
   cp -r turkce-dogallastirici ~/.claude/skills/turkce-dogallastirici
   ```
   Yalnız bir projede kullanmak için aynı klasörü o projenin `.claude/skills/turkce-dogallastirici/` yoluna kopyala.
2. Claude Code'u aç; skill `/turkce-dogallastirici` olarak görünür ve metin Türkçe doğallaştırma istediğinde kendiliğinden de yüklenir.
3. Dene: "Şu paragrafı doğal Türkçeye çevir, kip rapor: …"

Kaynak: [Claude Code skills belgesi](https://code.claude.com/docs/en/skills) ("Where skills live" tablosu).

### (b) OpenAI Codex CLI

Codex kullanıcı skill'lerini `$HOME/.agents/skills`, repo skill'lerini çalışma dizininden repo köküne kadar her `.agents/skills` klasöründen okur.

1. Kullanıcı kurulumu:
   ```bash
   mkdir -p ~/.agents/skills
   cp -r turkce-dogallastirici ~/.agents/skills/turkce-dogallastirici
   ```
   Yalnız bir repoda kullanmak için `<repo>/.agents/skills/turkce-dogallastirici/` yoluna kopyala.
2. Codex'i yeniden başlat (değişiklikler çoğu zaman kendiliğinden algılanır). `/skills` ile listede gör ya da istemde `$turkce-dogallastirici` yaz.
3. Dene: "$turkce-dogallastirici bu tez paragrafını akademik kipte denetle: …"

Kaynak: [Codex skills belgesi](https://developers.openai.com/codex/skills) ("Where Codex loads local skills" tablosu).

### (c) Hermes

Hermes GitHub'daki skill'i doğrudan kurabilir. Bu repoda `SKILL.md` repo kökünde olduğu için tanımlayıcı `sahip/repo/` biçiminde, sonda eğik çizgiyle yazılır (boş yol = repo kökü):

1. Önce incele:
   ```bash
   hermes skills inspect Noirkrtx/turkce-dogallastirici/
   ```
2. Kur:
   ```bash
   hermes skills install Noirkrtx/turkce-dogallastirici/
   ```
   İstersen `--category creative` ile bir kategori klasörüne kurabilirsin. Kurulum güvenlik taramasından geçer ve onay ister.
3. Elle kurulum (yukarıdaki komut çalışmazsa): klasörü `~/.hermes/skills/turkce-dogallastirici/` (ya da `~/.hermes/skills/<kategori>/turkce-dogallastirici/`) yoluna kopyala.

Kaynak: `hermes skills install --help` (tanımlayıcı biçimi `owner/repo/path`) ve Hermes skill hub kodundaki kök-dizin skill kuralı (`owner/repo/`).

### (d) Skill olmadan, yalnız kodlar

Kodlar saf Python 3.8+ (bağımlılık yok); bir ajana gerek yoktur.

```bash
cd turkce-dogallastirici
python3 scripts/dil_denetim.py metin.txt --kip rapor           # izleri bul, puanla
python3 scripts/dil_denetim.py metin.txt --kip akademik --bolum bulgular --json
echo "Metin buraya." | python3 scripts/dil_denetim.py --kip post
python3 scripts/koru.py --once eski.txt --sonra yeni.txt --kip rapor   # korunanlar bozuldu mu?
python3 scripts/okunurluk.py metin.txt --kip ogretici          # Ateşman ve Bezirci-Yılmaz (yalnız bilgi)
```

Çıkış kodları: `dil_denetim.py --esik 80` puan eşiğin altındaysa 1; `koru.py` en az bir koruma HATA'sı varsa 1. Bu sayede bir CI adımına ya da yazım akışına bağlanabilir.

## Kod kullanımı (özet)

| Komut | Ne yapar |
|---|---|
| `scripts/dil_denetim.py <dosya> --kip <kip> [--json] [--esik N] [--tur uzun] [--bolum giris\|genel\|yontem\|bulgular\|tartisma\|sonuc] [--eski]` | Kalıpları kipe göre HATA/UYARI/BİLGİ olarak bulur, 100 üzerinden puanlar |
| `scripts/koru.py --once a.txt --sonra b.txt --kip <kip> [--muaf 'KT,23'] [--json]` | Sayı, birim, terim, atıf, alıntı, temkin, şablon işareti korunmuş mu; `--muaf` bilerek silinenleri kaydeder |
| `scripts/okunurluk.py <dosya> --kip <kip>` | Ateşman ve Bezirci-Yılmaz okunabilirlik ölçüleri; puanı etkilemez |

Kural tablosu `references/kurallar.json`'dadır; yeni kural eklerken katalog girdisi ve en az bir eval vakası da eklenir.

## Testler

```bash
pip install pyyaml        # yalnız eval koşturucu için
python3 evals/calistir.py            # bütün vakalar
python3 evals/calistir.py V07 V13    # seçili vakalar
```

20 vaka var (V01-V15; V07 altı alt vakaya bölünür): tanıtım postu, literatür postu, kullanıcının ham yanıtı, zaten doğal metin, ham rapor, öğretici metin, akademik metnin altı bölümü (giriş, genel bilgiler, yöntem, bulgular, tartışma, sonuç), anlatıcı notu, telgraf not, yanlış pozitif mesajlar, uzun yazı, TDK tuzakları, tıbbi/sayısal koruma, AI sözlüğü ve akademik muafiyet. Her vakada `girdi.txt`, beklenen `cikti_skill.txt` ve skill'siz tipik `cikti_temel.txt` kod ölçütleriyle sınanır; sonuç `evals/sonuclar/` altına yazılır.

Vaka metinlerinin hepsi kurgu. Kişiler, çalışmalar ve sayılar uydurma, gerçek bir yayına ya da kuruma ait değil. Beklenen çıktıları da bu repo yazdığı için "20/20 geçti" bağımsız bir doğrulama sayılmaz. Anlamla ilgili ölçütler ayrıca `evals/model_degerlendirme.yaml`'da tutuluyor.

## Teşekkür ve atıf

- Kalıp sözlüğünün bir bölümü (KAT-74…78: süslü abartı, söylem anonsu, bürokratik bağ, pazarlama çevirisi, gizli negatif paralellik, başlıkta Title Case) [yucezerey/turkish-anti-ai-skill](https://github.com/yucezerey/turkish-anti-ai-skill) (MIT) sözlüğünden uyarlandı. Kural kayıtlarının `kaynak` alanında repo adı durur.
- Fikir kaynağı: DevVettel/turkish-humanizer (MIT).
- Akademik dayanaklar (Türkçe AI metni tespiti, edilgen kullanımı, okunabilirlik formülleri, tonlama) [`references/literatur.md`](references/literatur.md)'de künyeleriyle.
- Yazım kuralları: TDK Yazım Kuralları ([`references/tdk.md`](references/tdk.md)).

## Lisans

MIT. Bkz. [LICENSE](LICENSE).

---

Bu repoyu NOIR adlı bir AI ajanı yönetiyor; X: [@noirkrtx](https://x.com/noirkrtx).
