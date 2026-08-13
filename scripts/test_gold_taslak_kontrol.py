import pytest
from scripts.gold_taslak_kontrol import parse_taslak_metni
from validators.format_validator import validate_format

def test_gecerli_taslak_metni():
    gecerli_metin = """
T.C.
ÇEVRE VE ŞEHİRCİLİK BAKANLIĞI
Bilgi İşlem Dairesi Başkanlığı

Sayı: E-67915368-903.07.02-4752
Tarih: 07.08.2026
Konu: Personel Hareketleri Hakkında

ÇALIŞMA VE SOSYAL GÜVENLİK BAKANLIĞINA

İlgili yazışmalar hakkında bilgi sunulmaktadır.

arz ederim.

Mehmet YILMAZ
Daire Başkanı

Ek: Rapor (1 Sayfa)
"""
    taslak = parse_taslak_metni(gecerli_metin)
    sonuc = validate_format(taslak, "ust_yazi")
    
    assert sonuc.gecerli is True
    assert len(sonuc.hatalar) == 0

def test_hatali_taslak_metni():
    # Hatalı: Konu noktalama ile bitiyor, sayi formati hatali, kapaliş yok
    hatali_metin = """
T.C.
Çevre Ve Şehircilik Bakanlığı
Bilgi İşlem

Sayı: 1234
Tarih: 45.08.2026
Konu: Personel Hareketleri Hakkında.

ÇALIŞMA VE SOSYAL GÜVENLİK BAKANLIĞINA

İlgili yazışmalar hakkında bilgi sunulmaktadır.

Mehmet YILMAZ
Daire Başkanı
"""
    taslak = parse_taslak_metni(hatali_metin)
    sonuc = validate_format(taslak, "ust_yazi")
    
    assert sonuc.gecerli is False
    hatalar = [h.kural_kodu for h in sonuc.hatalar]
    
    assert "SAYI_FORMAT" in hatalar
    assert "TARIH_FORMAT" in hatalar
    assert "KONU_FORMAT" in hatalar
    assert "IMZA_BLOKU" in hatalar
    assert "TC_BASLIK" in hatalar

def test_tarih_etiketi_olmadan_tarih_ayristirma():
    # Sadece tarih değeri (Tarih: etiketi olmadan)
    metin = """
T.C.
ÖRENLİ İLÇE KAYMAKAMLIĞI
Yazı İşleri Müdürlüğü

Sayı: E-12345678-121.02-014                                      03.08.2026
Konu: Nüfus Cüzdanı Kayıp Bildirimi

                              ÖRENLİ İLÇE NÜFUS MÜDÜRLÜĞÜNE

İlgi: 02.08.2026 tarihli ve 2026/1284 sayılı dilekçe.

Bilgilerinize arz ederim.

                                    Ahmet YALÇIN
                                    Kaymakam a.
                                    Yazı İşleri Müdürü
"""
    taslak = parse_taslak_metni(metin)
    assert taslak.get("tarih") == "03.08.2026", "Tarih etiketsiz format doğru ayrıştırılamadı"

def test_kucuk_harfli_cumle_ici_kapanis_ayristirma():
    # Kapanış ifadesi küçük harfle ve cümle içinde ("Durum bilgilerinize sunulur.")
    metin = """
T.C.
ÖRENLİ İLÇE KAYMAKAMLIĞI
Yazı İşleri Müdürlüğü

Sayı: E-12345678-121.02-014                                      03.08.2026
Konu: Nüfus Cüzdanı Kayıp Bildirimi

                              Sayın Ahmet YALÇIN

Durum bilgilerinize sunulur.

                                    Mehmet YILMAZ
                                    Kaymakam a.
                                    Yazı İşleri Müdürü
"""
    taslak = parse_taslak_metni(metin)
    assert taslak.get("kapalis_ifadesi") == "Bilgilerinize sunulur.", "Küçük harfli kapanış ifadesi doğru ayrılamadı"
    # imza bloğunun da bulunduğunu teyit et
    assert taslak.get("imza", {}).get("ad_soyad") == "Mehmet YILMAZ"
