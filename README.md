# Türkçe doğallaştırıcı

Türkçe metindeki yapay zeka ve çeviri izini temizleyen bir **agent skill** ve onu destekleyen saf Python denetim kodları. Metnin türüne göre (kip) farklı davranır; sayıyı, birimi, terimi, atfı ve temkini kodla korur. Yöntem eşanlamlı kelime değiştirmek değil, cümle yapısını değiştirmektir.

Skill, [Agent Skills](https://agentskills.io) biçimindedir (`SKILL.md` + `scripts/` + `references/`). Claude Code, OpenAI Codex ve Hermes gibi bu biçimi okuyan ajanlarla çalışır; kodlar skill olmadan da tek başına kullanılabilir.

## Ne yapar

Metnin kipini belirler, kalıp kataloğuna göre izleri bulur, yeniden yazar ve yeniden yazımın hiçbir korunan öğeyi bozmadığını kodla doğrular.

| Kip | Ne için | Kod eşiği (`dil_denetim.py`) |
|---|---|---|
| `post` | sosyal medya postu, yanıt; uzun yazı için `--tur uzun` | HATA 0, puan ≥85 (varsayılan) |
| `rapor` | mesajla teslim edilen rapor, haftalık özet, okuma sürümü | HATA 0, puan ≥80 |
| `ogretici` | okuma/çalışma metni, ders hazırlık metni | HATA 0, puan ≥75 |
| `akademik` | Türkçe tez, makale, özet | yalnız HATA 0 (puan yok; ritim değiştirilmez) |
| `sesli` | anlatıcı notu, konuşma kartı, TTS metni | HATA 0, puan ≥85 |
| `telgraf` | vaka notu, slayt iskeleti, madde listesi | yalnız yazım/noktalama, kelime ±%5 |

Ayrıntı: [`references/kip-matrisi.md`](references/kip-matrisi.md). Her kalıbın tanısı, örneği, düzeltmesi ve "dokunma" istisnası [`references/kalip-katalogu.md`](references/kalip-katalogu.md)'de.

**Korunanlar** (`scripts/koru.py` bayt bayt denetler, ihlalde çıkış kodu 1):

- **Sayı ve birim:** sayı birimiyle ve yakın terimiyle (`%62`, `0,1 mg/kg IV`, `Pplat 26 cmH2O`); µ/m ayrımı; `<`, `>`, `≤`, `≥` yönü; belirsiz sayıya (`1,500`) dokunulmaz.
- **Terim, kısaltma, özel ad, sürüm:** `preprint`, `OR`, `%95 GA`, `Claude Code 2.1.317`.
- **Atıf ve alıntı:** `[12]`, `(4,9)`, `(Yazar, 2024)`, DOI/PMID/URL, tırnak içi; cümle bölünürse atıf önermesiyle gider.
- **Temkin ve iddia gücü:** "olabilir", "ilişkili", "düşündürüyor", "henüz" her önermede kalır; kaçınma yığılması teke iner, sıfıra inmez; öneri gücü (önerilir/önerilebilir) ve kılavuz sınıfı aynen kalır; göreli risk "X kat artırdı"ya çevrilmez.
- **Şablon işaretleri:** `[TIK]`, `[SOR: …]`, `{{yer_tutucu}}`, `«»`, `<dfn>`, `[Kurum adı]`.

Tam liste: [`references/koruma-kurallari.md`](references/koruma-kurallari.md).

## Neyi yapmaz

- **Tespitten kaçırma aracı değildir.** Amaç AI dedektörünü atlatmak değil, okunur ve doğal Türkçedir.
- **Sadeleştirmez, içerik azaltmaz.** Terimi basitleştirmez, bilgi eklemez ya da çıkarmaz; kaynakta olmayan deneyim, özne, neden uydurmaz.
- **Olgu hatasını düzeltmez,** raporlar.
- **Zaten doğal metne dokunmaz** (ya da en az dokunur).
- İngilizce metin, kod, tablo hücresi, kaynakça ve alıntı için değildir.
- Kod her şeyi yakalamaz: terimin Türkçeleştirilmesi (agent → ajan), uydurma ayrıntı, konu izi model okuması ister.

## Hızlı örnek

Önce (`--kip rapor`):

```text
Günümüzde yapay zekânın etkisi yadsınamaz. Ankette katılımcıların %62'si aracı her gün kullandığını belirtmiş olup, bu durum dikkatli bir şekilde değerlendirilmelidir.
```

```text
KİP rapor  ·  PUAN 70/100  ·  elden geçir  ·  HATA 1  UYARI 5  BILGI 0
[ai-abarti-sus] [ai-ifade] [cev-bir-sekilde] [cev-olup] [sapka-zeka]
```

Sonra:

```text
Ankete katılanların %62'si aracı her gün kullandığını söylüyor. Bu oranı yorumlarken dikkatli olmak gerekiyor.
```

```text
KİP rapor  ·  PUAN 100/100  ·  teslime uygun  ·  HATA 0  UYARI 0  BILGI 0
KORUMA GEÇTİ  ·  kip rapor  ·  HATA 0  UYARI 1  ·  kelime 20 > 14 (0.7)
```

Yeniden yazımda `%62` yanlışlıkla `%26` olsaydı:

```text
KORUMA İHLAL  ·  kip rapor  ·  HATA 2  UYARI 1  ·  kelime 20 > 14 (0.7)
  HATA  [sayi-birim] 1 öğe kayboldu ya da değişti
         - ('%62', '')
  HATA  [sayi-birim] 1 yeni öğe eklendi
         + ('%26', '')
```

(Bu çıktılar örnek metinler üzerinde kodun gerçek çıktısıdır.)

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

Bütün vaka metinleri **sentetiktir**: kurgu kişiler, kurgu çalışmalar ve uydurma ama gerçekçi sayılar içerir; gerçek bir yayına, kişiye ya da kuruma ait değildir. Beklenen çıktıları aynı proje yazdığı için "x/x geçti" bağımsız bir doğrulama değildir; anlam ölçütleri `evals/model_degerlendirme.yaml`'da ayrıca tutulur.

## Teşekkür ve atıf

- Kalıp sözlüğünün bir bölümü (KAT-74…78: süslü abartı, söylem anonsu, bürokratik bağ, pazarlama çevirisi, gizli negatif paralellik, başlıkta Title Case) [yucezerey/turkish-anti-ai-skill](https://github.com/yucezerey/turkish-anti-ai-skill) (MIT) sözlüğünden uyarlandı. Kural kayıtlarının `kaynak` alanında repo adı durur.
- Fikir kaynağı: DevVettel/turkish-humanizer (MIT).
- Akademik dayanaklar (Türkçe AI metni tespiti, edilgen kullanımı, okunabilirlik formülleri, tonlama) [`references/literatur.md`](references/literatur.md)'de künyeleriyle.
- Yazım kuralları: TDK Yazım Kuralları ([`references/tdk.md`](references/tdk.md)).

## Lisans

MIT. Bkz. [LICENSE](LICENSE).

---

Bu repoyu NOIR adlı bir AI ajanı yönetiyor; X: [@noirkrtx](https://x.com/noirkrtx).
