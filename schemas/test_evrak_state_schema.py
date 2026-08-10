"""
schemas/test_evrak_state_schema.py
──────────────────────────────────────────────────────────────────────────────
Pipeline 1 — Arayüz Şeması Test Paketi

Kapsam:
  - Gecerli EvrakState ornegi olusturulabiliyor mu
  - Zorunlu alan (evrak_id) eksikse hata veriyor mu
  - muhatap_turu gecersiz bir degerle hata veriyor mu
  - evrak_turu'na rastgele string verilebiliyor mu (hata VERMEMELI)
  - alanlar.ek_alanlar'a onceden tanimsiz anahtar eklenebiliyor mu
  - JSON serializasyon (model_dump_json) calisiyor mu
"""

from __future__ import annotations

import json
from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.evrak_state_schema import (
    AuditKaydi,
    CikarilanAlanlar,
    DogrulamaSonucu,
    EvrakState,
    HitlKarar,
    KaynakTuru,
    MevzuatEslesme,
    Muhatap,
    MuhatapHiyerarsi,
    PipelineAsama,
    YonlendirmeKarari,
)


# ──────────────────────────────────────────────────────────────────────────────
# Yardimci Fabrika
# ──────────────────────────────────────────────────────────────────────────────


def minimal_state(**kwargs) -> EvrakState:
    """Gecerli, minimal bir EvrakState ornegi olusturur."""
    defaults = {
        "evrak_id": "TEST-001",
        "olusturulma_zamani": datetime(2026, 8, 10, 11, 0, 0),
    }
    defaults.update(kwargs)
    return EvrakState(**defaults)


# ──────────────────────────────────────────────────────────────────────────────
# Test 1: Gecerli Ornek Olusturma
# ──────────────────────────────────────────────────────────────────────────────


def test_gecerli_evrak_state_olusturulabilir():
    """Tam dolu, gecerli bir EvrakState ornegi beklenen degerlerle olusturulabilmelidir."""
    state = EvrakState(
        evrak_id="EVR-2026-0042",
        kurum_profili_id="kaymakamlik_v1",
        olusturulma_zamani=datetime(2026, 8, 10, 9, 30, 0),
        pipeline_asamasi=PipelineAsama.GIRIS,
        ham_metin="Sayın Kaymakam, ...",
        ocr_guven_skoru=0.97,
        kaynak_format="pdf",
        evrak_turu="dilekce",
        evrak_turu_guven=0.91,
        alanlar=CikarilanAlanlar(
            gonderen_adi="Ahmet YILMAZ",
            tarih="10.08.2026",
            konu="Tapu Islemi",
            ek_alanlar={"ozel_alan": "ozel_deger"},
        ),
        mevzuat_eslesmeleri=[
            MevzuatEslesme(
                madde_no="Madde 5",
                kaynak_dokuman="657 Sayili Kanun",
                ozet="Devlet memurlarinin gorev tanimlari",
                benzerlik_skoru=0.88,
                kaynak_dogrulandi=True,
            )
        ],
        yazi_turu="cevap_yazisi",
        yazi_turu_kaynagi=KaynakTuru.KURAL,
        yonlendirme=YonlendirmeKarari(
            onerilen_birim_id="yazi_isleri",
            guven_skoru=0.95,
            kaynak=KaynakTuru.KURAL,
            gerekce="Kural tabanlı eslesme.",
        ),
        muhatap=Muhatap(tur="gercek_kisi", isim="Ahmet YILMAZ"),
        muhatap_turu=MuhatapHiyerarsi.GERCEK_KISI,
        taslak_metin="T.C. KAYMAKAMLIK ...",
        sablon_id="cevap_yazisi",
        dogrulama=DogrulamaSonucu(
            format_kurallarina_uygun=True,
            kaynaklar_dogrulandi=True,
            guven_skoru=0.99,
            llm_self_check_calisti=True,
            sorunlar=[],
        ),
        hitl_karari=HitlKarar.ONAYLANDI,
        hitl_kullanici="fatima.kantar",
        hitl_notu="Onaylandi, imzaya hazir.",
        hitl_zamani=datetime(2026, 8, 10, 10, 0, 0),
        audit_log=[
            AuditKaydi(
                dugum_adi="ocr_dugumu",
                zaman=datetime(2026, 8, 10, 9, 31, 0),
                girdi_ozeti="PDF dosyasi",
                cikti_ozeti="ham_metin cikarildi",
                llm_cagrisi_yapildi=False,
                sure_ms=120,
            )
        ],
    )

    assert state.evrak_id == "EVR-2026-0042"
    assert state.pipeline_asamasi == PipelineAsama.GIRIS.value  # use_enum_values=True
    assert state.ocr_guven_skoru == 0.97
    assert state.muhatap.tur == "gercek_kisi"
    assert state.muhatap_turu == MuhatapHiyerarsi.GERCEK_KISI.value
    assert len(state.mevzuat_eslesmeleri) == 1
    assert state.dogrulama.format_kurallarina_uygun is True


# ──────────────────────────────────────────────────────────────────────────────
# Test 2: Zorunlu Alan Eksik → ValidationError
# ──────────────────────────────────────────────────────────────────────────────


def test_evrak_id_eksikse_validation_error():
    """
    evrak_id zorunlu bir alan; eksik birakildiginda Pydantic ValidationError
    firlatmalidir.
    """
    with pytest.raises(ValidationError) as exc_info:
        EvrakState(olusturulma_zamani=datetime(2026, 8, 10, 11, 0, 0))

    # Hatanin evrak_id alanini isaret ettigini dogrula
    errors = exc_info.value.errors()
    alan_adlari = [e["loc"][0] for e in errors]
    assert "evrak_id" in alan_adlari


# ──────────────────────────────────────────────────────────────────────────────
# Test 3: muhatap_turu Gecersiz Deger → ValidationError
# ──────────────────────────────────────────────────────────────────────────────


def test_muhatap_turu_gecersiz_deger_hata_verir():
    """
    muhatap_turu alani MuhatapHiyerarsi enum'u ile kisitlidir.
    Enum'da olmayan bir deger ValidationError firlatmalidir.
    """
    with pytest.raises(ValidationError) as exc_info:
        minimal_state(muhatap_turu="TAMAMEN_YANLIS_DEGER")

    errors = exc_info.value.errors()
    alan_adlari = [e["loc"][0] for e in errors]
    assert "muhatap_turu" in alan_adlari


# ──────────────────────────────────────────────────────────────────────────────
# Test 4: evrak_turu Rastgele String → Hata VERMEMELI
# ──────────────────────────────────────────────────────────────────────────────


def test_evrak_turu_rastgele_string_kabul_edilir():
    """
    evrak_turu alani kasitli olarak duz str birakilmistir; Enum/Literal DEGILDIR.

    Neden hata vermemeli:
      Bu alanin gercek deger kumesi Pipeline 4 (Kurum Config, ayri branch'te
      gelistiriliyor) tarafindan uretilen kurum_profili.yaml dosyasindan gelir.
      Eger bu alan Enum/Literal yapilsaydi, farkli kurum profillerine geciste
      sema dosyasi da degistirilmek zorunda kalirdi — bu mimari esnek degil.
      Dolayisiyla herhangi bir string gecerlidir; deger kumesi dogrulamasi
      pipeline calisma zamaninda config katmaninda yapilir.
    """
    state = minimal_state(evrak_turu="gelecekte_tanimlanacak_tur")
    assert state.evrak_turu == "gelecekte_tanimlanacak_tur"

    state2 = minimal_state(evrak_turu="herhangi_bir_string_12345")
    assert state2.evrak_turu == "herhangi_bir_string_12345"


# ──────────────────────────────────────────────────────────────────────────────
# Test 5: ek_alanlar Serbest Anahtar-Deger
# ──────────────────────────────────────────────────────────────────────────────


def test_ek_alanlar_onceden_tanimsiz_anahtar_kabul_edilir():
    """
    CikarilanAlanlar.ek_alanlar alani dict[str, str] turundedir.
    Semada onceden tanimlanmamis herhangi bir anahtar eklenebilmeli;
    ValidationError firlamamalidir.
    """
    alanlar = CikarilanAlanlar(
        ek_alanlar={
            "pipeline3_ozel_alan": "deger1",
            "basvuru_no": "2026/1234",
            "ilgili_mudurlu": "Plan ve Proje Mudurlugu",
        }
    )

    assert alanlar.ek_alanlar["pipeline3_ozel_alan"] == "deger1"
    assert alanlar.ek_alanlar["basvuru_no"] == "2026/1234"
    assert len(alanlar.ek_alanlar) == 3

    state = minimal_state(alanlar=alanlar)
    assert state.alanlar.ek_alanlar["ilgili_mudurlu"] == "Plan ve Proje Mudurlugu"


# ──────────────────────────────────────────────────────────────────────────────
# Test 6: JSON Serializasyon
# ──────────────────────────────────────────────────────────────────────────────


def test_model_dump_json_calisir():
    """
    EvrakState.model_dump_json() gecerli JSON uretmeli ve
    yeniden yukleme (model_validate_json) ile ayni veriye donmeli.
    """
    state = EvrakState(
        evrak_id="EVR-JSON-TEST",
        olusturulma_zamani=datetime(2026, 8, 10, 12, 0, 0),
        pipeline_asamasi=PipelineAsama.OCR_TAMAMLANDI,
        ham_metin="OCR sonrasi ham metin",
        ocr_guven_skoru=0.85,
        muhatap=Muhatap(tur="kurum", isim="Icisleri Bakanligi"),
        muhatap_turu=MuhatapHiyerarsi.KURUM_UST,
    )

    json_str = state.model_dump_json()
    assert isinstance(json_str, str)

    # Gecerli JSON mi?
    parsed = json.loads(json_str)
    assert parsed["evrak_id"] == "EVR-JSON-TEST"
    assert parsed["ham_metin"] == "OCR sonrasi ham metin"
    assert parsed["muhatap"]["tur"] == "kurum"
    assert parsed["muhatap_turu"] == "kurum_ust"

    # Geri yukleme
    restored = EvrakState.model_validate_json(json_str)
    assert restored.evrak_id == state.evrak_id
    assert restored.ocr_guven_skoru == state.ocr_guven_skoru
    assert restored.muhatap.isim == "Icisleri Bakanligi"


# ──────────────────────────────────────────────────────────────────────────────
# Test 7: Ek Gecerlilik Kontrolleri
# ──────────────────────────────────────────────────────────────────────────────


def test_guven_skoru_sinir_disi_hata_verir():
    """Guven skoru [0.0, 1.0] araliginin disina ciktiginda ValidationError olmali."""
    with pytest.raises(ValidationError):
        minimal_state(ocr_guven_skoru=1.5)

    with pytest.raises(ValidationError):
        minimal_state(ocr_guven_skoru=-0.1)


def test_varsayilan_degerler():
    """
    Zorunlu olmayan alanlar belirtilmediginde beklenen varsayilan degerleri almalidir.
    """
    state = minimal_state()
    assert state.kurum_profili_id == "kaymakamlik_v1"
    assert state.pipeline_asamasi == PipelineAsama.GIRIS.value
    assert state.ham_metin is None
    assert state.mevzuat_eslesmeleri == []
    assert state.eksik_alanlar == []
    assert state.audit_log == []
    assert state.dogrulama is None
    assert state.muhatap is None
    assert state.muhatap_turu is None


def test_muhatap_tur_gecersiz_literal_hata_verir():
    """
    Muhatap.tur alani Literal["kurum", "gercek_kisi", "dagitim"] ile kisitlidir.
    Baska bir deger ValidationError firlatmalidir.
    """
    with pytest.raises(ValidationError):
        Muhatap(tur="bilinmeyen_tur", isim="Test Kurumu")


def test_mevzuat_eslesme_benzerlik_sinir_kontrolu():
    """MevzuatEslesme.benzerlik_skoru [0.0, 1.0] araliginda olmalidir."""
    with pytest.raises(ValidationError):
        MevzuatEslesme(
            madde_no="Madde 1",
            kaynak_dokuman="Test",
            ozet="Test ozet",
            benzerlik_skoru=1.1,  # gecersiz: > 1.0
            kaynak_dogrulandi=True,
        )
