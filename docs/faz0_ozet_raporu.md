# Faz 0 Kapanış Özet Raporu

**Proje:** TEKNOFEST 2026 Yapay Zeka Dil Ajanları Yarışması — Senaryo 1  
**Kapsam:** Kamu Evrak ve Yazışma Süreçleri için Çok Ajanlı Akıllı Destek Sistemi  
**Demo Kurum:** Örenli İlçe Kaymakamlığı (kurgusal)  
**Tarih:** 2026-08-10  
**Durum:** Faz 0 kapalı — 4 pipeline tamamlandı, test edildi, çapraz doğrulandı.

---

## 1. Ne İnşa Edildi

### Pipeline 1 — Arayüz Şeması (JSON Sözleşmesi)

**Sorumlu klasör:** `schemas/`

**Çıktı dosyaları:**

| Dosya | İçerik |
|---|---|
| `schemas/evrak_state_schema.py` | 306 satır — `EvrakState` Pydantic v2 modeli ve 7 alt-model |
| `schemas/README.md` | Alan sahiplik matrisi, hardcode etmeme ilkesi, çapraz kontrol sonuçları |
| `schemas/test_evrak_state_schema.py` | 10 test |

**Şemadaki modeller:**

- `PipelineAsama` (11 değerli enum) — akış geçiş durumları
- `KaynakTuru` (2 değer) — kural tabanlı / LLM tabanlı
- `HitlKarar` (3 değer) — HITL karar sonuçları
- `MuhatapHiyerarsi` (5 değer) — hiyerarşi/kapanış ifadesi seçimi
- `Muhatap` — şablon render parametresi
- `CikarilanAlanlar` — OCR/çıkarım düğümü çıktısı
- `MevzuatEslesme` — RAG düğümü tek eşleşme birimi
- `YonlendirmeKarari` — kural motoru kararı
- `DogrulamaSonucu` — doğrulama düğümü çıktısı (Pydantic, serializable)
- `AuditKaydi` — her düğüm geçişinde yazılan denetim kaydı
- `EvrakState` — tüm düğümlerin paylaştığı tek state nesnesi

**Test sayısı:** 10 (dosya: `schemas/test_evrak_state_schema.py`)

**Önemli tasarım kararları:**

- `evrak_turu`, `yazi_turu`, `YonlendirmeKarari.onerilen_birim_id` → düz `str`, Enum/Literal DEĞİL. Gerekçe: değer kümesi kuruma özel `kurum_profili.yaml`'dan gelir; şemaya sabitlenmesi farklı kurum profillerine geçişi kırar.
- `MuhatapHiyerarsi` enum'u → Enum YAPILDI. Gerekçe: hiyerarşi kavramı yönetmelik kaynaklı ve kurum-bağımsız (Madde 16/12).
- `DogrulamaSonucu` → Pydantic modeli (dataclass olan `validators/format_validator.py::DogrulamaSonucu`'dan ayrı), state'e JSON-serializable olarak gömülmek için.
- `CikarilanAlanlar.ek_alanlar: dict[str, str]` → önceden tanımlanmamış kurum-özel alanlar için serbest depo.

---

### Pipeline 2 — Format Motoru

**Sorumlu klasörler:** `templates/`, `validators/`, `renderers/`, `tests/`

**Çıktı dosyaları:**

| Dosya | İçerik |
|---|---|
| `templates/ust_yazi.jinja2` | 204 satır — üst yazı + bilgilendirme yazısı şablonu |
| `templates/cevap_yazisi.jinja2` | 172 satır — cevap yazısı şablonu |
| `templates/tekit_yazisi.jinja2` | 159 satır — tekit yazısı şablonu |
| `templates/README.md` | Kurulum, kullanım örnekleri, [TASARIM KARARI] tablosu |
| `validators/format_validator.py` | 740 satır — 12 kural fonksiyonu + `validate_format()` |
| `validators/__init__.py` | Paket tanımı |
| `renderers/template_renderer.py` | 150 satır — merkezi Jinja2 render modülü |
| `renderers/__init__.py` | Paket tanımı |
| `tests/test_format_validator.py` | 96 test |
| `tests/test_template_render.py` | 52 test |

**Test sayısı:** 148 (96 validator + 52 render)

**Validator kapsamı (12 kural fonksiyonu):**

`sayi_formati_dogru_mu` · `tarih_formati_dogru_mu` · `konu_formati_dogru_mu` · `muhatap_formati_dogru_mu` · `ilgi_formati_dogru_mu` · `arz_rica_dogru_mu` · `imza_blogu_dogru_mu` · `ek_listesi_dogru_mu` · `dagitim_listesi_dogru_mu` · `tekit_konu_dogru_mu` · `tekit_ilgi_zorunlu_mu` · `tekit_metin_kalibi_dogru_mu` + `cevap_ilgi_zorunlu_mu` + `kisaltma_aciklama_mevcut_mu` + `tc_baslik_dogru_mu` + `sayfa_no_formati_dogru_mu`

Kaynak: RG 10.06.2020/31151 (Resmî Yazışma Yönetmeliği, Madde 10–19, 31, 33, 34, 35) + Cumhurbaşkanlığı Kılavuzu (2022).

**Önemli tasarım kararları (6 [TASARIM KARARI]):**

| # | Konu | Karar | Gerekçe |
|---|---|---|---|
| 1 | Satır aralığı | 1.0 (tek satır) | Yönetmelik/kılavuzda sayısal değer yok |
| 2 | Ek/Dağıtım öncesi boşluk | 2 satır | "Uygun satır boşluğu" ifadesi sayısal değer içermiyor |
| 3 | Kısaltma kuralı kapsamı | Sadece kurumsal/özel isim (TBMM, KEP) | Genel↔kurumsal ayrımı yönetmelikte net değil |
| 4 | 9pt küçültme | MVP'de uygulanmaz | Somut eşik tanımlı değil, nadir kenar durum |
| 5 | Arz/rica (hiyerarşi belirsiz) | Varsayılan "arz ederim." | Güvenli taraf (kurum_ust davranışı) |
| 6 | Bilgilendirme yazısı şablonu | `ust_yazi.jinja2` kullanılır | Kılavuz Bölüm C: ayrı biçimsel şablon yoktur |

**Renderer güvenceleri (`renderers/template_renderer.py`):**

- `StrictUndefined` — merkezi singleton environment; tanımsız değişken sessizce boş string olmaz, `UndefinedError` fırlatır.
- `render_cevap_yazisi()` — render öncesi `ilgi` zorunluluk kontrolü ([TASARIM KARARI]).
- `render_tekit_yazisi()` — render öncesi `gun` + `ilgi` zorunluluk kontrolü (Madde 34).

---

### Pipeline 3 — Mevzuat Korpusu Toplama

**Sorumlu klasörler:** `data/raw/mevzuat/`, `docs/`

**Çıktı dosyaları:**

| Dosya | Boyut | Kaynak | Kullanım Amacı |
|---|---|---|---|
| `data/raw/mevzuat/resmi_yazisma_yonetmeligi.pdf` | 8.2 MB | mevzuat.gov.tr (RG 10.06.2020/31151) | Format Motoru — biçim kuralları |
| `data/raw/mevzuat/resmi_yazisma_kilavuzu.pdf` | 15.2 MB | tccb.gov.tr (2022 güncel sürüm) | Format Motoru — örnek şablonlar (Örnek 1-24) |
| `data/raw/mevzuat/3071_dilekce_hakki_kanunu.pdf` | 212 KB | mevzuat.gov.tr | Mevzuat RAG — dilekçe yasal dayanağı |
| `data/raw/mevzuat/4982_bilgi_edinme_kanunu.pdf` | 196 KB | mevzuat.gov.tr | Mevzuat RAG — bilgi edinme yasal dayanağı |
| `data/raw/mevzuat/5442_il_idaresi_kanunu.pdf` | 304 KB | mevzuat.gov.tr | Yönlendirme — kurum profili birim listesi dayanağı |
| `docs/kaynak_referanslari.md` | — | — | Kaynak belgesi (şartname md. 7 gereği) |

**Test sayısı:** 0 — Pipeline 3 veri toplama aşamasıdır; test kapsamı dışındadır (ham dosya bütünlüğü kontrol edilmemiştir).

**Önemli not:** İki kaynak değerlendirme sonrası reddedilmiştir:

- `24193939_Resmi_Yazışma_Kuralları.pdf` — DETSİS-öncesi sayı formatı içeriyor, Madde 11 ile çelişiyor.
- `669020121106121401.pdf` — metin içeriği taranamaz/boş.

---

### Pipeline 4 — Kurum Config

**Sorumlu klasör:** `data/config/`

**Çıktı dosyaları:**

| Dosya | Boyut |
|---|---|
| `data/config/kurum_profili_kaymakamlik.yaml` | 191 satır |

**YAML yapısı (4 ana bölüm):**

- `kurum` — kurum adı, türü, üst makam, yasal dayanak.
- `birimler` — 9 birim, her birinde `id`, `ad`, `aciklama`, `anahtar_kelimeler`.
- `evrak_turleri` — 6 evrak türü, her birinde `id`, `ad`, `aciklama`, `yasal_dayanak`, `tipik_hedef_birim`.
- `yazi_turleri` — 4 çıktı türü, her birinde `id`, `ad`, `kullanim_durumu`, `sablon` (şablon dosyası yolu).

**Test sayısı:** 0 — YAML doğruluğu çapraz kontrol yoluyla doğrulandı (bkz. Bölüm 3).

---

## 2. Mimari İlkeler — Fiilen Nasıl Uygulandı

### İlke 1: Hardcode Etmeme (Kurum-Bağımsız Çekirdek)

**İlke:** Çekirdek motor kurum-bağımsız çalışır; kurum-özel değer kümeleri ayrı config dosyasından enjekte edilir.

**Kodda nerede somutlaştı:**

| Alan | Dosya:Satır | Tip | Neden Enum Yapılmadı |
|---|---|---|---|
| `EvrakState.evrak_turu` | `schemas/evrak_state_schema.py:246` | `Optional[str]` | 6 evrak türü `kurum_profili.yaml / evrak_turleri[*].id`'den gelir |
| `EvrakState.yazi_turu` | `schemas/evrak_state_schema.py:262` | `Optional[str]` | 4 çıktı türü `kurum_profili.yaml / yazi_turleri[*].id`'den gelir |
| `YonlendirmeKarari.onerilen_birim_id` | `schemas/evrak_state_schema.py:166` | `str` | 9 birim ID'si `kurum_profili.yaml / birimler[*].id`'den gelir |

**Karşı örnek — Enum YAPILAN alanlar (gerekçeli):**

- `MuhatapHiyerarsi` (`schemas/evrak_state_schema.py:82`) → Enum YAPILDI. Gerekçe: 5 değer (kurum_alt, kurum_ust, kurum_ayni, kurum_karisik, gercek_kisi) yönetmelik kaynaklı (Madde 16/12) ve kurum-bağımsız; farklı kurumda da kapanış ifadesi mantığı değişmez.
- `Muhatap.tur` (`schemas/evrak_state_schema.py:123`) → `Literal["kurum", "gercek_kisi", "dagitim"]`. Gerekçe: muhatap türleri yönetmelik tanımlı (Madde 14), kurum-bağımsız.

### İlke 2: Şablon + Kod Hibrit (LLM'e Format Garantisi Bırakılmadı)

**İlke:** Resmî yazı formatı belirsiz LLM çıktısına değil, Jinja2 şablonlarına ve deterministik kural fonksiyonlarına teslim edildi.

**Kodda nerede somutlaştı:**

- **Şablonlar** (`templates/*.jinja2`) — Her yazı türü (üst yazı, cevap, tekit) için sabit yapısal şablon. LLM, metin paragraflarını üretir; format, şablon tarafından garanti edilir.
- **Kilitli alanlar** — `tekit_yazisi.jinja2`: `konu` alanı daima `"Tekit Yazısı"` (dışarıdan geçilemez, Madde 34); metin kalıbı `"tekiden rica ederim."` ile biter.
- **Merkezi renderer** (`renderers/template_renderer.py:53–57`) — `StrictUndefined` singleton; tanımsız değişken `UndefinedError` fırlatır, sessiz boşluk üretmez.
- **Pre-check kontrolü** (`renderers/template_renderer.py:101–107`, `132–146`) — `render_cevap_yazisi()` ve `render_tekit_yazisi()` render başlamadan zorunlu alan kontrolü yapar; LLM'in eksik context göndermesi durumu açıklayıcı `ValueError` ile engellenir.
- **Validator** (`validators/format_validator.py:586–739`) — `validate_format()`: sayı formatı regex, tarih format kontrolü, kapanış ifadesi hiyerarşi eşleştirmesi, imza formatı — hiçbiri LLM'e devredilmez.

### İlke 3: Çapraz Doğrulama Disiplini

**Yapılan kontroller (2026-08-10, merge sonrası):**

| # | Kontrol | Yöntem | Sonuç |
|---|---|---|---|
| a | `evrak_turu` ↔ `kurum_profili.yaml / evrak_turleri[*].id` | YAML okundu, id listesi çıkarıldı | ✅ 6 id tutarlı |
| b | `yazi_turu` ↔ `kurum_profili.yaml / yazi_turleri[*].id` + `sablon` alanı | YAML yapısı incelendi; yanlış `sablon_haritasi` ismi düzeltildi | ✅ 4 id + şablon yolları doğrulandı |
| c | `onerilen_birim_id` ↔ `kurum_profili.yaml / birimler[*].id` | YAML okundu | ✅ 9 id tutarlı |
| d | `MevzuatEslesme.kaynak_dokuman` ↔ `data/raw/mevzuat/` dosya adları | `docs/kaynak_referanslari.md` incelendi | ✅ Dosya adı tabanlı isimlendirme konvansiyonu önerildi |

Detaylar: `schemas/README.md — Pipeline 3/4 Çapraz Kontrol Sonuçları`

---

## 3. Pipeline'lar Arası Bağımlılık Haritası

```
Pipeline 3 (Mevzuat Korpusu)              Pipeline 4 (Kurum Config)
  data/raw/mevzuat/*.pdf                    data/config/kurum_profili_kaymakamlik.yaml
          │                                          │
          │ kaynak_dokuman isimlendirme               │ evrak_turleri[*].id
          │ konvansiyonu beslenir                     │   → EvrakState.evrak_turu (str)
          │                                          │
          ▼                                          │ yazi_turleri[*].id + .sablon
  EvrakState.mevzuat_eslesmeleri                     │   → EvrakState.yazi_turu (str)
  MevzuatEslesme.madde_no                           │   → Taslaklama düğümü şablon seçimi
  MevzuatEslesme.ozet                               │
  MevzuatEslesme.benzerlik_skoru                    │ birimler[*].id
                                                    │   → YonlendirmeKarari.onerilen_birim_id (str)
                                                    │
                                                    ▼
Pipeline 1 (Arayüz Şeması)         Pipeline 2 (Format Motoru)
  schemas/evrak_state_schema.py  ←──── templates/*.jinja2
                                         (muhatap + muhatap_turu parametreleri
                                          şablon başlık yorumlarından türetildi)
          │
          │ EvrakState.taslak_metin
          │   ← renderers/template_renderer.py
          │       ← validators/format_validator.py
          │
          ▼
  HITL onayı → nihai evrak çıktısı
```

**Kritik bağımlılıklar:**

- `EvrakState.muhatap` (tip: `Muhatap`) — `templates/*.jinja2` başlık yorumlarında `muhatap: dict { tur: "kurum"|"gercek_kisi"|"dagitim", isim: str }` şeklinde tanımlıdır. Şema bu yapıyla birebir uyumludur.
- `EvrakState.muhatap_turu` (tip: `MuhatapHiyerarsi`) — şablonlardaki 5 `muhatap_turu` string değeri (`kurum_alt`, `kurum_ust`, `kurum_ayni`, `kurum_karisik`, `gercek_kisi`) enum değerleriyle birebir örtüşür.
- `EvrakState.dogrulama` (tip: `DogrulamaSonucu`) — `validators/format_validator.py`'deki `DogrulamaSonucu` dataclass ile kavramsal olarak örtüşür; ancak state'e gömülmek için Pydantic modeli olarak ayrıca tanımlandı.
- `EvrakState.sablon_id` — `kurum_profili.yaml / yazi_turleri[*].id` değerlerinden biri olur; Taslaklama düğümü bu id ile `yazi_turleri[*].sablon` alanından şablon yolunu seçer.

---

## 4. Faz 0'da Yapılmayan, Faz 1+'a Bırakılan İşler

Aşağıdaki kalemler Faz 0 kapsamı dışındadır. Hiçbirinde henüz bir başlangıç yapılmamıştır.

### Ajan/LLM Mantığı — Henüz Başlanmadı

- **OCR düğümü:** Gerçek OCR entegrasyonu (Tesseract, Azure OCR vb.) yazılmadı. `EvrakState.ham_metin` alanı tanımlandı; onu dolduran kod yok.
- **Sınıflandırma + Çıkarım düğümü:** LLM çağrısı, `evrak_turu` tahmini ve `CikarilanAlanlar` doldurma mantığı yazılmadı.
- **Mevzuat RAG düğümü:** Embedding, vektör arama, `MevzuatEslesme` listesi üretme mantığı yazılmadı.
- **Kural Motoru / Yönlendirme düğümü:** `kurum_profili.yaml / birimler[*].anahtar_kelimeler` ile eşleştirme mantığı ve `YonlendirmeKarari` üretme yazılmadı.
- **Taslaklama düğümü:** Şablon seçimi + renderer çağrısı + HITL hazırlama mantığı yazılmadı.
- **Doğrulama düğümü:** `validate_format()` çağrısı, LLM self-check, `DogrulamaSonucu` doldurma mantığı yazılmadı.

### Orkestrasyon — Henüz Başlanmadı

- **LangGraph grafiği:** 6 düğümün bağlandığı, `EvrakState`'i taşıyan akış grafiği kurulmadı. `EvrakState` tanımlandı; onu kullanan graph yok.

### Veri İşleme — Henüz Başlanmadı

- **Mevzuat chunk/embedding:** `data/raw/mevzuat/` altındaki 5 PDF dosyası ham olarak toplandı. Chunking, embedding ve vektör veritabanına yükleme işlemi henüz yapılmadı.
- **`data/processed/`:** Boş.

### Altyapı — Henüz Başlanmadı

- **Docker:** `docker/` klasörü var, içi boş. Qdrant, PostgreSQL, uygulama container'ları tanımlanmadı.
- **Vektör veritabanı (Qdrant):** Kurulmadı, yapılandırılmadı.
- **İlişkisel veritabanı (PostgreSQL):** Kurulmadı, yapılandırılmadı.

### Arayüz — Henüz Başlanmadı

- **Demo arayüzü (Streamlit):** Kullanıcı arayüzü yazılmadı.

### Test Kapsamı Boşlukları

- Pipeline 3 (mevzuat PDF'leri) için ham dosya bütünlüğü testi yazılmadı.
- Pipeline 4 (YAML yapısı) için şema doğrulama testi yazılmadı.
- Entegrasyon testi (birden fazla düğümün birlikte çalışması) henüz yok.

---

## 5. Doğrulama Geçmişi

### Test Özeti

| Test Dosyası | Test Sayısı | Kapsam |
|---|---|---|
| `schemas/test_evrak_state_schema.py` | 10 | Pipeline 1 şema: geçerli örnek, zorunlu alan, muhatap_turu enum, evrak_turu serbest str, ek_alanlar, JSON serializasyon, güven skoru sınır kontrolleri |
| `tests/test_format_validator.py` | 96 | Pipeline 2 validator: 12 kural fonksiyonu için geçerli/hatalı senaryolar, `validate_format()` entegrasyon testleri, [TASARIM KARARI] işaretleme |
| `tests/test_template_render.py` | 52 | Pipeline 2 render: 3 şablon için gerçek Jinja2 render çıktısı doğrulaması, alan sırası kontrolü, renderer API güvenceleri |
| **Toplam** | **158** | **0 başarısız, 0 atlanan** |

Son çalışma: `2026-08-10 — 158 passed in 0.66s`

### Denetim Olayları

**Olay 1 — Merge Sırasında schemas/ Klasörünün Yanlışlıkla Silinmesi**

4 pipeline merge edilirken bir commit `schemas/` klasörünü sildi. Bu durum fark edildi, klasör elle geri eklenerek yeniden commit edildi:

```
fix: silinen evrak_state_schema dosyalari ve testleri geri getirildi
4 files changed, 697 insertions(+), 5 deletions(-)
create mode 100644 schemas/README.md
create mode 100644 schemas/evrak_state_schema.py
create mode 100644 schemas/test_evrak_state_schema.py
```

Bu olay kasıtlı olarak şeffaf biçimde dokümante edilmektedir. Sebep: merge geçmişindeki her anomalinin kayıt altına alınması, ilerideki hata ayıklama süreçlerinde değerli bağlam sağlar. Pipeline testlerinin hepsi başarıyla geçmiştir.

**Olay 2 — schemas/README.md'deki Yanlış `sablon_haritasi` Referansı**

Pipeline 1 yazılırken `kurum_profili.yaml` henüz görülemediğinden şema docstring'inde `sablon_haritasi` adlı bir yapı varsayılmıştı. Merge sonrası YAML gerçekten okunduğunda bu anahtarın var olmadığı, gerçek yapının `yazi_turleri[*].sablon` olduğu tespit edildi ve düzeltildi.

**Olay 3 — README.md Faz 0 Tracker Yanlış Durumu**

Pipeline 3 ve Pipeline 4 tamamlanmış olmasına rağmen README.md'de "Başlanmadı" yazıyordu. Faz 0 denetiminde tespit edilerek "✅ Tamamlandı" olarak güncellendi.

### Çözülmemiş Merge Çakışması Kontrolü

`git grep` ile tüm kaynak dosyalar tarandı: `<<<<<<<`, `=======`, `>>>>>>>` işaretleri bulunmadı. `.orig` veya `.bak` uzantılı dosya yok.

---

## 6. Sıradaki Adım — Faz 1 Önerisi

1. **Mevzuat işleme:** `data/raw/mevzuat/*.pdf` dosyalarını chunk'la, embed et, Qdrant'a yükle. Başlangıç noktası: `resmi_yazisma_yonetmeligi.pdf` ve kanun metinleri.
2. **LangGraph grafiğini kur:** `EvrakState`'i taşıyan 6 düğümlü akışı `langgraph` kütüphanesiyle oluştur. Başlangıç için stub düğümler (gerçek LLM çağrısı olmadan geçiş yapan) kullanılabilir.
3. **OCR + Sınıflandırma düğümü:** Ham metin → `evrak_turu` + `CikarilanAlanlar` pipeline'ını bir LLM (Gemini) ile yaz. `kurum_profili.yaml / evrak_turleri` konfigürasyonunu enjekte et.
4. **Mevzuat RAG düğümü:** Soru → embedding → Qdrant arama → `MevzuatEslesme` listesi pipeline'ı.
5. **Kural Motoru:** `birimler[*].anahtar_kelimeler` + mevzuat eşleşmesi → `YonlendirmeKarari` üretme mantığı.
6. **Taslaklama + Doğrulama düğümleri:** `render_*` fonksiyonları + `validate_format()` LangGraph düğümlerine sarıl.
7. **Docker altyapısı:** Qdrant, PostgreSQL ve uygulama container'larını tanımla.
8. **HITL arayüzü:** Taslaği insan onayına sunan minimal Streamlit ekranı.
9. **Entegrasyon testleri:** Birden fazla düğümü kapsayan uçtan uca test senaryoları.
