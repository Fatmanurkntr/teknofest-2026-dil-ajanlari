"""
schemas/evrak_state_schema.py
──────────────────────────────────────────────────────────────────────────────
LangGraph Düğümleri Arası Paylaşılan State (Durum) Şeması
Pipeline 1 — Arayüz Şeması (JSON Sözleşmesi)

AMAÇ:
  6 düğümlü LangGraph akışındaki (OCR → Sınıf+Çıkarım → Mevzuat RAG →
  Kural Motoru → Taslaklama → Doğrulama) tüm düğümlerin okuyup yazacağı
  TEK durum nesnesini tanımlar.  Pydantic v2 ile doğrulama desteklidir.

KRİTİK TASARIM İLKESİ — HARDCODE ETMEME:
  `evrak_turu`, `yazi_turu` ve `YonlendirmeKarari.onerilen_birim_id`
  alanları kasıtlı olarak düz `str` bırakılmıştır.  Bu üç alanın
  gerçek değer kümesi, Pipeline 4 (Kurum Config, paralel branch'te
  geliştiriliyor) tarafından üretilen `kurum_profili.yaml` dosyasından
  gelecektir.  Enum/Literal ile sabitlenmesi, merge sonrasında farklı
  kurum profillerine geçişte şema dosyasının da değiştirilmesini
  zorunlu kılardı — bu mimari esnekliği yok eder.
  Detaylar için: schemas/README.md

BAĞIMLILIKLAR:
  - Pipeline 2 (Format Motoru): templates/*.jinja2 parametreleriyle
    uyumlu — muhatap / muhatap_turu alanları şablon başlıklarından
    türetilmiştir.
  - Pipeline 3 (Mevzuat Korpusu): henüz merge edilmemiş paralel
    branch'te geliştiriliyor.
  - Pipeline 4 (Kurum Config): henüz merge edilmemiş paralel
    branch'te geliştiriliyor.

MERGE NOTU:
  Pipeline 3/4 merge sonrasında evrak_turu, yazi_turu ve
  onerilen_birim_id değerlerinin kurum_profili.yaml ile tutarlılığını
  çapraz kontrol ediniz (bkz. schemas/README.md).
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ──────────────────────────────────────────────────────────────────────────────
# Enum Tanımları
# ──────────────────────────────────────────────────────────────────────────────


class PipelineAsama(str, Enum):
    """LangGraph akışındaki düğüm geçiş durumları."""

    GIRIS = "giris"
    OCR_TAMAMLANDI = "ocr_tamamlandi"
    SINIF_CIKARIM_TAMAMLANDI = "sinif_cikarim_tamamlandi"
    MEVZUAT_TAMAMLANDI = "mevzuat_tamamlandi"
    YAZI_TURU_YONLENDIRME_TAMAMLANDI = "yazi_turu_yonlendirme_tamamlandi"
    TASLAK_HAZIR = "taslak_hazir"
    DOGRULAMA_TAMAMLANDI = "dogrulama_tamamlandi"
    HITL_BEKLIYOR = "hitl_bekliyor"
    ONAYLANDI = "onaylandi"
    REDDEDILDI = "reddedildi"
    HATA = "hata"


class KaynakTuru(str, Enum):
    """Karar veya bilginin kaynağı: kural tabanlı mı, LLM tabanlı mı?"""

    KURAL = "kural_tabanli"
    LLM = "llm_tabanli"


class HitlKarar(str, Enum):
    """Human-in-the-Loop incelemesi sonucu."""

    ONAYLANDI = "onaylandi"
    DUZELTILDI = "duzeltildi"
    REDDEDILDI = "reddedildi"


class MuhatapHiyerarsi(str, Enum):
    """
    Yazinin muhatabinin hiyerarsik konumu.

    Bu enum hiyerasi kavrami temsil eder; deger kumesi kurum-bagimsizdir
    (yonetmelik kaynakli: Madde 16/12, ust_yazi.jinja2 baslik yorumu).
    Sablonlarda kapanis ifadesi (arz/rica) bu alana gore secilir.

    Degerler:
      kurum_alt     -> alt makama yazi -> "rica ederim."
      kurum_ust     -> ust makama yazi -> "arz ederim."
      kurum_ayni    -> ayni duzey makama yazi -> "arz ederim."
      kurum_karisik -> dagitimli (ust+alt karisik) -> "arz ve rica ederim."
      gercek_kisi   -> gercek kisiye yazi -> "Saygilarimla." (arz/rica KULLANILMAZ)
    """

    KURUM_ALT = "kurum_alt"
    KURUM_UST = "kurum_ust"
    KURUM_AYNI = "kurum_ayni"
    KURUM_KARISIK = "kurum_karisik"
    GERCEK_KISI = "gercek_kisi"


# ──────────────────────────────────────────────────────────────────────────────
# Alt-Modeller
# ──────────────────────────────────────────────────────────────────────────────


class Muhatap(BaseModel):
    """
    Yazinin muhatabı — sablon render katmanina (templates/*.jinja2)
    dogrudan aktarilir.

    tur:
      "kurum"       -> isim BUYUK HARF + yonelme eki (Madde 14)
      "gercek_kisi" -> "Sayin Ad SOYAD" (Madde 14)
      "dagitim"     -> "DAGITIM YERLERINE" (Madde 14)
    isim:
      Kurum veya kisi adi; tur=="dagitim" ise bu alan kullanilmaz.
    """

    tur: Literal["kurum", "gercek_kisi", "dagitim"]
    isim: str


class CikarilanAlanlar(BaseModel):
    """
    OCR + Siniflandirma dugumu tarafindan evraktan cikarilan yapilandirilmis
    alanlar.  Zorunlu olmayan alanlar None birakilabilir.
    """

    gonderen_adi: Optional[str] = None
    tarih: Optional[str] = None
    konu: Optional[str] = None
    talep_metni: Optional[str] = None
    referans_no: Optional[str] = None
    ek_alanlar: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Semada onceden tanimlanmamis ek alanlar icin serbest anahtar-deger deposu. "
            "Pipeline 3/4 kaynakli yeni alanlar merge oncesinde gecici olarak buraya yazilabilir."
        ),
    )


class MevzuatEslesme(BaseModel):
    """Mevzuat RAG dugumu tarafindan bulunan tek bir mevzuat maddesi eslesmes."""

    madde_no: str
    kaynak_dokuman: str
    ozet: str
    benzerlik_skoru: float = Field(ge=0.0, le=1.0)
    kaynak_dogrulandi: bool


class YonlendirmeKarari(BaseModel):
    """
    Kural Motoru dugumunun urettigi yonlendirme karari.

    onerilen_birim_id:
      Deger kumesi kurum_profili.yaml dosyasindan (Pipeline 4, ayri branch'te
      gelistiriliyor) gelir; burada sabitlenmez.  Enum/Literal yapilmamalidir.
    """

    onerilen_birim_id: str = Field(
        description=(
            "Deger kumesi kurum_profili.yaml dosyasindan (Pipeline 4, "
            "ayri branch'te gelistiriliyor) gelir; burada sabitlenmez."
        )
    )
    guven_skoru: float = Field(ge=0.0, le=1.0)
    kaynak: KaynakTuru
    gerekce: Optional[str] = None


class DogrulamaSonucu(BaseModel):
    """
    Dogrulama dugumu ciktisi.

    validators/format_validator.py icindeki DogrulamaSonucu (dataclass) ile
    kavramsal olarak ortusur; ancak bu model Pydantic tabanli olup state'e
    gomulmek icin tasarlanmistir.

    Fark:
      - format_validator.DogrulamaSonucu: validator'in ic donus turu (dataclass).
      - Bu model: tum dugumlerin okuyabilecegi serializable state alani.
    """

    format_kurallarina_uygun: bool
    kaynaklar_dogrulandi: bool
    guven_skoru: float = Field(ge=0.0, le=1.0)
    llm_self_check_calisti: bool = False
    sorunlar: list[str] = Field(default_factory=list)


class AuditKaydi(BaseModel):
    """Her dugum gecisinde olusturulan denetim kaydi."""

    dugum_adi: str
    zaman: datetime
    girdi_ozeti: str
    cikti_ozeti: str
    llm_cagrisi_yapildi: bool
    sure_ms: Optional[int] = None


# ──────────────────────────────────────────────────────────────────────────────
# Ana State Modeli
# ──────────────────────────────────────────────────────────────────────────────


class EvrakState(BaseModel):
    """
    LangGraph 6-dugumlu akisinda tum dugumlerin okuyup yazacagi
    paylasilan durum (state) nesnesi.

    Sahiplik matrisi icin: schemas/README.md

    HARDCODE ETMEME ILKESI:
      evrak_turu, yazi_turu ve yonlendirme.onerilen_birim_id alanlari
      kasitli olarak duz str birakilmistir; Enum/Literal yapilmamalidir.
      Ayrintilar: schemas/README.md ve bu modulun baslik docstring'i.
    """

    model_config = ConfigDict(use_enum_values=True)

    # -- Kimlik ve Meta --------------------------------------------------------
    evrak_id: str = Field(description="Evrakin benzersiz tanimlayicisi.")
    kurum_profili_id: str = Field(
        default="kaymakamlik_v1",
        description=(
            "Aktif kurum profilinin kimligi. "
            "Gercek profil verisi Pipeline 4 (kurum_profili.yaml) tarafindan yonetilir."
        ),
    )
    olusturulma_zamani: datetime
    pipeline_asamasi: PipelineAsama = PipelineAsama.GIRIS

    # -- OCR Dugumu Ciktilari --------------------------------------------------
    ham_metin: Optional[str] = None
    ocr_guven_skoru: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    kaynak_format: Optional[str] = None  # or. "pdf", "docx", "goruntu"

    # -- Siniflandirma + Cikarim Dugumu Ciktilari ------------------------------
    evrak_turu: Optional[str] = Field(
        default=None,
        description=(
            "Evrakin turu (or. 'dilekce', 'resmi_yazi', 'muhtira'). "
            "Deger kumesi kurum_profili.yaml dosyasindan (Pipeline 4, "
            "ayri branch'te gelistiriliyor) gelir; burada sabitlenmez."
        ),
    )
    evrak_turu_guven: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    alanlar: Optional[CikarilanAlanlar] = None
    eksik_alanlar: list[str] = Field(default_factory=list)

    # -- Mevzuat RAG Dugumu Ciktilari ------------------------------------------
    mevzuat_eslesmeleri: list[MevzuatEslesme] = Field(default_factory=list)

    # -- Kural Motoru / Yonlendirme Dugumu Ciktilari ---------------------------
    yazi_turu: Optional[str] = Field(
        default=None,
        description=(
            "Uretilecek cikti yazisinin turu (or. 'ust_yazi', 'cevap_yazisi', 'tekit_yazisi'). "
            "Deger kumesi kurum_profili.yaml dosyasindan (Pipeline 4, "
            "ayri branch'te gelistiriliyor) gelir; burada sabitlenmez."
        ),
    )
    yazi_turu_kaynagi: Optional[KaynakTuru] = None
    yonlendirme: Optional[YonlendirmeKarari] = None

    # -- Muhatap Bilgisi -------------------------------------------------------
    # templates/*.jinja2 sablonlarinin hem `muhatap` (dict) hem `muhatap_turu`
    # (hiyerarsi) parametrelerini beklediginden dolayi iki ayri alan tanimlanmistir.
    muhatap: Optional[Muhatap] = Field(
        default=None,
        description=(
            "Sablon render'ina aktarilacak muhatap bilgisi. "
            "templates/*.jinja2 baslik yorumlariyla uyumludur (Madde 14)."
        ),
    )
    muhatap_turu: Optional[MuhatapHiyerarsi] = Field(
        default=None,
        description=(
            "Muhatap hiyerarsisi; kapanis ifadesi (arz/rica) secimini belirler. "
            "Enum degerleri yonetmelik kaynaklidir (Madde 16/12) — kurum-bagimsiz."
        ),
    )

    # -- Taslaklama Dugumu Ciktilari -------------------------------------------
    taslak_metin: Optional[str] = None
    sablon_id: Optional[str] = None  # or. "ust_yazi", "cevap_yazisi"

    # -- Dogrulama Dugumu Ciktilari --------------------------------------------
    dogrulama: Optional[DogrulamaSonucu] = None

    # -- HITL (Human-in-the-Loop) Alanlari ------------------------------------
    hitl_karari: Optional[HitlKarar] = None
    hitl_kullanici: Optional[str] = None
    hitl_notu: Optional[str] = None
    hitl_zamani: Optional[datetime] = None

    # -- Denetim Kaydi --------------------------------------------------------
    audit_log: list[AuditKaydi] = Field(default_factory=list)
