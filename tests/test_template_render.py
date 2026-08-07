"""
tests/test_template_render.py
──────────────────────────────────────────────────────────────────────────────
Şablon Render Doğrulama Testleri

Bu dosya "girdi doğru mu?" değil, "çıktı doğru mu?" sorusunu yanıtlar:
Jinja2 şablonları GERÇEKTEN render edilir, üretilen metin üzerinde:
  1. Anahtar ifadelerin kaç kez geçtiği kontrol edilir (tam sayı eşleşmesi).
  2. Belge bölümlerinin render edilmiş metinde doğru sırada geldiği
     kontrol edilir (alan sırası: Sayı→Tarih→Konu→Muhatap→İlgi→
     Metin→İmza→Ek→Dağıtım→İletişim).

Çalıştırmak için:
    pytest tests/test_template_render.py -v
"""

import pytest
from jinja2 import UndefinedError

from renderers.template_renderer import (
    get_env,
    render_cevap_yazisi,
    render_tekit_yazisi,
    render_ust_yazi,
)


# ──────────────────────────────────────────────────────────────────────────────
# Jinja2 ortamı — templates/ klasörünü yükle
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def jinja_env():
    """
    Merkezi Jinja2 Environment'ı döndürür.

    Fixture doğrudan renderers.template_renderer.get_env() kullanır;
    böylece test ortamı ve üretim kodu (Ajan 6) aynı StrictUndefined
    konfigürasyonını paylaşır.  Testlerdeki jinja_env bağımsız bir
    Environment oluştursa, yapılandırmalar arasında kayıp oluşabilir.
    """
    return get_env()


# ──────────────────────────────────────────────────────────────────────────────
# Yardımcı fonksiyonlar
# ──────────────────────────────────────────────────────────────────────────────

def ifade_sayisi(metin: str, ifade: str) -> int:
    """Verilen ifadenin metinde kaç kez geçtiğini döndürür."""
    return metin.count(ifade)


def alan_sirasi_dogru_mu(metin: str, alanlar: list[str]) -> tuple[bool, str]:
    """
    Verilen alanların (alt diziler) render çıktısında sırayla
    (her birinin bir öncekinden SONRA) geçtiğini doğrular.

    Returns:
        (gecerli: bool, hata_mesaji: str)
    """
    pozisyon = 0
    for alan in alanlar:
        idx = metin.find(alan, pozisyon)
        if idx == -1:
            return False, (
                f"'{alan}' metinde bulunamadı "
                f"(arama pozisyonu {pozisyon}'dan itibaren)."
            )
        pozisyon = idx + len(alan)
    return True, ""


# ──────────────────────────────────────────────────────────────────────────────
# Ortak test verileri
# ──────────────────────────────────────────────────────────────────────────────

_ORTAK_CONTEXT = dict(
    tc_baslik={
        "idare_adi": "ÇEVRE VE ŞEHİRCİLİK BAKANLIĞI",
        "birim_adi": "Bilgi İşlem Dairesi Başkanlığı",
    },
    sayi="E-67915368-903.07.02-4752",
    tarih="07.08.2026",
    muhatap={"tur": "kurum", "isim": "ÇALIŞMA VE SOSYAL GÜVENLİK BAKANLIĞINA"},
    muhatap_turu="kurum_ust",
    imza={
        "ad_soyad": "Mehmet YILMAZ",
        "unvan": "Daire Başkanı",
        "yetki_turu": "normal",
    },
    iletisim={"adres": "Ankara 06100", "irtibat": "Ayşe KAYA", "telefon": "312 555 00 00"},
)

_ILGI = [
    {
        "tarih": "01.07.2026",
        "sayi": "E-67915368-903.07.02-1000",
        "aciklama": "yazı",
    }
]


# ──────────────────────────────────────────────────────────────────────────────
# 1. ust_yazi.jinja2
# ──────────────────────────────────────────────────────────────────────────────

class TestUstYaziRender:

    @pytest.fixture
    def render(self, jinja_env):
        tmpl = jinja_env.get_template("ust_yazi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "konu": "Personel Hareketleri Hakkında",
            "metin_paragraflari": [
                "İlgili yazışmalar hakkında bilgi sunulmaktadır."
            ],
            "kapalis_ifadesi": "arz ederim.",
        }
        return tmpl.render(**ctx)

    # ── Alan varlığı ────────────────────────────────────────────────────────

    def test_tc_baslik_var(self, render):
        assert "T.C." in render

    def test_idare_adi_buyuk_harf(self, render):
        assert "ÇEVRE VE ŞEHİRCİLİK BAKANLIĞI" in render

    def test_sayi_var(self, render):
        assert "Sayı: E-67915368-903.07.02-4752" in render

    def test_tarih_var(self, render):
        assert "Tarih: 07.08.2026" in render

    def test_konu_var(self, render):
        assert "Konu: Personel Hareketleri Hakkında" in render

    def test_konu_noktalama_yok(self, render):
        # Konu satırı nokta ile bitmemeli
        for satir in render.splitlines():
            if satir.strip().startswith("Konu:"):
                assert not satir.rstrip().endswith("."), (
                    f"Konu satırı nokta ile bitti: '{satir}'"
                )

    def test_muhatap_buyuk_harf(self, render):
        assert "ÇALIŞMA VE SOSYAL GÜVENLİK BAKANLIĞINA" in render

    def test_kapanis_arz(self, render):
        assert "arz ederim." in render

    def test_imza_ad_soyad(self, render):
        assert "Mehmet YILMAZ" in render

    def test_imza_unvan(self, render):
        assert "Daire Başkanı" in render

    def test_ek_konulmadi(self, render):
        assert "Ek konulmadı." in render

    def test_iletisim_var(self, render):
        assert "Ankara 06100" in render
        assert "Ayşe KAYA" in render

    # ── "arz ederim." tam olarak 1 kez geçmeli ──────────────────────────────

    def test_arz_tam_1_kez(self, render):
        sayi = ifade_sayisi(render, "arz ederim.")
        assert sayi == 1, (
            f"'arz ederim.' {sayi} kez geçti, tam 1 kez geçmeli.\n"
            f"--- RENDER ---\n{render}"
        )

    # ── Alan sırası ──────────────────────────────────────────────────────────

    def test_alan_sirasi(self, render):
        gecerli, mesaj = alan_sirasi_dogru_mu(render, [
            "Sayı:",
            "Tarih:",
            "Konu:",
            "ÇALIŞMA VE SOSYAL GÜVENLİK BAKANLIĞINA",  # Muhatap
            "İlgili yazışmalar",                          # Metin
            "arz ederim.",                                # Kapanış
            "Mehmet YILMAZ",                              # İmza
            "Ek konulmadı.",                              # Ek
            "Ankara 06100",                               # İletişim
        ])
        assert gecerli, f"Alan sırası hatalı: {mesaj}\n--- RENDER ---\n{render}"

    # ── İlgi bloğu opsiyonel: ilgi verilmediğinde "İlgi:" olmamalı ───────────

    def test_ilgi_yok_ise_satirda_gozukmesin(self, jinja_env):
        tmpl = jinja_env.get_template("ust_yazi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "konu": "Test Konusu",
            "metin_paragraflari": ["Test metni."],
            "kapalis_ifadesi": "arz ederim.",
        }
        render = tmpl.render(**ctx)
        for satir in render.splitlines():
            assert not satir.strip().startswith("İlgi:"), (
                f"İlgi verilmediğinde 'İlgi:' satırı render edilmemeli: '{satir}'"
            )

    def test_ilgi_varsa_gozukur(self, jinja_env):
        tmpl = jinja_env.get_template("ust_yazi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "konu": "Test Konusu",
            "ilgi": _ILGI,
            "metin_paragraflari": ["Test metni."],
            "kapalis_ifadesi": "arz ederim.",
        }
        render = tmpl.render(**ctx)
        assert "İlgi:" in render, "İlgi verildiğinde render'da görünmeli."
        assert "tarihli ve" in render
        assert "sayılı" in render

    # ── Gerçek kişi muhatabında "Sayın" öneki ───────────────────────────────

    def test_gercek_kisi_sayin_oneki(self, jinja_env):
        tmpl = jinja_env.get_template("ust_yazi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "muhatap": {"tur": "gercek_kisi", "isim": "Ahmet YILMAZ"},
            "muhatap_turu": "gercek_kisi",
            "konu": "Test Konusu",
            "metin_paragraflari": ["Test metni."],
            "kapalis_ifadesi": "Saygılarımla.",
        }
        render = tmpl.render(**ctx)
        assert "Sayın Ahmet YILMAZ" in render

    # ── Çoklu muhatap: "DAĞITIM YERLERİNE" ──────────────────────────────────

    def test_dagitim_muhatap(self, jinja_env):
        tmpl = jinja_env.get_template("ust_yazi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "muhatap": {"tur": "dagitim", "isim": ""},
            "muhatap_turu": "kurum_karisik",
            "konu": "Test Konusu",
            "metin_paragraflari": ["Test metni."],
            "kapalis_ifadesi": "arz ve rica ederim.",
        }
        render = tmpl.render(**ctx)
        assert "DAĞITIM YERLERİNE" in render


# ──────────────────────────────────────────────────────────────────────────────
# 2. cevap_yazisi.jinja2
# ──────────────────────────────────────────────────────────────────────────────

class TestCevapYazisiRender:

    @pytest.fixture
    def render(self, jinja_env):
        tmpl = jinja_env.get_template("cevap_yazisi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "konu": "Bilgi Talebi Cevabı",
            "ilgi": _ILGI,
            "yanit_turu": "bilgi_goruş_talebi",
            "metin_paragraflari": [
                "İlgili yazınız incelenmiş olup cevabımız aşağıda sunulmaktadır."
            ],
            "kapalis_ifadesi": "arz ederim.",
        }
        return tmpl.render(**ctx)

    # ── İlgi bloğu her zaman mevcut olmalı ──────────────────────────────────

    def test_ilgi_zorunlu_gozukur(self, render):
        assert "İlgi:" in render, "Cevap yazısında ilgi her zaman render edilmeli."
        assert "tarihli ve" in render
        assert "sayılı" in render

    # ── Alan sırası ──────────────────────────────────────────────────────────

    def test_alan_sirasi(self, render):
        gecerli, mesaj = alan_sirasi_dogru_mu(render, [
            "Sayı:",
            "Tarih:",
            "Konu:",
            "ÇALIŞMA VE SOSYAL GÜVENLİK BAKANLIĞINA",
            "İlgi:",
            "İlgili yazınız incelenmiş",
            "arz ederim.",
            "Mehmet YILMAZ",
            "Ek konulmadı.",
            "Ankara 06100",
        ])
        assert gecerli, f"Alan sırası hatalı: {mesaj}\n--- RENDER ---\n{render}"

    # ── "arz ederim." tam olarak 1 kez ──────────────────────────────────────

    def test_arz_tam_1_kez(self, render):
        sayi = ifade_sayisi(render, "arz ederim.")
        assert sayi == 1, (
            f"'arz ederim.' {sayi} kez geçti, tam 1 kez geçmeli.\n"
            f"--- RENDER ---\n{render}"
        )

    # ── yanıt_turu iç metadata alandır; render çıktısına yansımaz ───────────
    # yanit_turu şablonda {# ... #} yorumu içinde yer alır → Jinja2 çıktıya
    # koymaz. Bu testte iç alanın doğru kapanışa yol açtığı doğrulanır.

    def test_yanit_turu_icin_kapalis_render(self, jinja_env):
        """bilgi_goruş_talebi türünde kurum_ust -> 'arz ederim.' render edilmeli."""
        tmpl = jinja_env.get_template("cevap_yazisi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "konu": "Bilgi Talebi Cevabı",
            "ilgi": _ILGI,
            "yanit_turu": "bilgi_goruş_talebi",
            "metin_paragraflari": ["Cevap metni."],
            "kapalis_ifadesi": "arz ederim.",
        }
        render = tmpl.render(**ctx)
        assert "arz ederim." in render, (
            "bilgi_goruş_talebi / kurum_ust -> 'arz ederim.' render edilmeli."
        )
        # yanit_turu iç metadata; render çıktısında bulunmamalı
        assert "yanit_turu=" not in render, (
            "yanit_turu iç metadata alandır; render çıktısına yansımamalı."
        )

    # ── Ek yoksa "Ek konulmadı." ─────────────────────────────────────────────

    def test_ek_konulmadi(self, render):
        assert "Ek konulmadı." in render

    # ── Ek varsa ek adı render edilir ────────────────────────────────────────

    def test_ek_varsa_render(self, jinja_env):
        tmpl = jinja_env.get_template("cevap_yazisi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "konu": "Cevap Testi",
            "ilgi": _ILGI,
            "yanit_turu": "belge_talebi",
            "metin_paragraflari": ["Cevap metni."],
            "kapalis_ifadesi": "arz ederim.",
            "ekler": [{"ad": "Rapor", "bilgi": "2 sayfa"}],
        }
        render = tmpl.render(**ctx)
        assert "Ek: Rapor (2 sayfa)" in render

    # ── Dağıtım bloğu ─────────────────────────────────────────────────────────

    def test_dagitim_render(self, jinja_env):
        tmpl = jinja_env.get_template("cevap_yazisi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "konu": "Cevap Testi",
            "ilgi": _ILGI,
            "yanit_turu": "belge_talebi",
            "metin_paragraflari": ["Cevap metni."],
            "kapalis_ifadesi": "arz ederim.",
            "dagitim": {"geregi": ["İl Müdürlüğüne"], "bilgi": ["Genel Müdürlüğe"]},
        }
        render = tmpl.render(**ctx)
        assert "Gereği:" in render
        assert "Bilgi:" in render
        assert "İl Müdürlüğüne" in render
        assert "Genel Müdürlüğe" in render


# ──────────────────────────────────────────────────────────────────────────────
# 3. tekit_yazisi.jinja2  — en kritik render testleri
# ──────────────────────────────────────────────────────────────────────────────

class TestTekitYazisiRender:

    @pytest.fixture
    def render(self, jinja_env):
        tmpl = jinja_env.get_template("tekit_yazisi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "ilgi": _ILGI,
            "gun": 10,
        }
        return tmpl.render(**ctx)

    # ── "tekiden rica ederim" TAM OLARAK 1 KEZ geçmeli ──────────────────────
    # Bu test Sorun 1 (çift kapanış buğu) için yazılmıştır. §7 bloğu
    # kaldırılmadan önce bu test BAŞARISIZ olurdu.

    def test_tekiden_rica_ederim_tam_1_kez(self, render):
        sayi = ifade_sayisi(render, "tekiden rica ederim")
        assert sayi == 1, (
            f"'tekiden rica ederim' {sayi} kez geçti, tam 1 kez geçmeli.\n"
            f"--- RENDER ---\n{render}"
        )

    # ── Konu daima "Tekit Yazısı" ────────────────────────────────────────────

    def test_konu_sabit_tekit(self, render):
        assert "Konu: Tekit Yazısı" in render

    # ── "Konu: Tekit Yazısı" tam olarak 1 kez geçmeli ───────────────────────

    def test_konu_tekit_tam_1_kez(self, render):
        sayi = ifade_sayisi(render, "Konu: Tekit Yazısı")
        assert sayi == 1, (
            f"'Konu: Tekit Yazısı' {sayi} kez geçti, tam 1 kez geçmeli."
        )

    # ── İlgi bloğu var ───────────────────────────────────────────────────────

    def test_ilgi_render(self, render):
        assert "İlgi:" in render
        assert "tarihli ve" in render
        assert "sayılı" in render

    # ── gun parametresi metne yansıyor ───────────────────────────────────────

    def test_gun_metinde(self, render):
        assert "10 gün içinde" in render

    # ── Alan sırası ──────────────────────────────────────────────────────────

    def test_alan_sirasi(self, render):
        gecerli, mesaj = alan_sirasi_dogru_mu(render, [
            "Sayı:",
            "Tarih:",
            "Konu: Tekit Yazısı",
            "ÇALIŞMA VE SOSYAL GÜVENLİK BAKANLIĞINA",
            "İlgi:",
            "tekiden rica ederim",
            "Mehmet YILMAZ",
            "Ek konulmadı.",
            "Ankara 06100",
        ])
        assert gecerli, f"Alan sırası hatalı: {mesaj}\n--- RENDER ---\n{render}"

    # ── metin_ek opsiyonel eklendiğinde render edilir ─────────────────────────

    def test_metin_ek_render(self, jinja_env):
        tmpl = jinja_env.get_template("tekit_yazisi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "ilgi": _ILGI,
            "gun": 7,
            "metin_ek": "Konu acildir.",
        }
        render = tmpl.render(**ctx)
        assert "Konu acildir." in render
        # "tekiden rica ederim" hâlâ yalnızca 1 kez geçmeli
        sayi = ifade_sayisi(render, "tekiden rica ederim")
        assert sayi == 1, (
            f"metin_ek ile birlikte 'tekiden rica ederim' {sayi} kez geçti, "
            f"tam 1 kez geçmeli.\n--- RENDER ---\n{render}"
        )

    # ── metin_ek olmadığında kalıp metni temiz render ─────────────────────────

    def test_gun_farkli_degerler(self, jinja_env):
        """gun değeri her çağrıda değiştirilebilmeli (varsayılan yok)."""
        tmpl = jinja_env.get_template("tekit_yazisi.jinja2")
        for gun_degeri in [3, 7, 15, 30]:
            ctx = {**_ORTAK_CONTEXT, "ilgi": _ILGI, "gun": gun_degeri}
            render = tmpl.render(**ctx)
            assert f"{gun_degeri} gün içinde" in render, (
                f"gun={gun_degeri} için '{gun_degeri} gün içinde' metinde bulunamadı."
            )

    # ── Yetki devri render ────────────────────────────────────────────────────

    def test_yetki_devri_render(self, jinja_env):
        tmpl = jinja_env.get_template("tekit_yazisi.jinja2")
        ctx = {
            **_ORTAK_CONTEXT,
            "imza": {
                "ad_soyad": "Ali KAYA",
                "unvan": "Şube Müdürü",
                "yetki_turu": "yetki_devri",
                "vekil_makam": "Daire Başkanı",
            },
            "ilgi": _ILGI,
            "gun": 5,
        }
        render = tmpl.render(**ctx)
        assert "Ali KAYA" in render
        assert "Daire Başkanı a." in render

    # ── StrictUndefined: gun eksikse Jinja2 hata fırlatmalı ──────────────────

    def test_gun_eksikse_hata(self, jinja_env):
        """gun parametresi zorunludur; eksik geçilirse UndefinedError beklenir."""
        from jinja2 import UndefinedError
        tmpl = jinja_env.get_template("tekit_yazisi.jinja2")
        ctx = {**_ORTAK_CONTEXT, "ilgi": _ILGI}
        # gun anahtarı yok
        with pytest.raises(UndefinedError):
            tmpl.render(**ctx)


# ──────────────────────────────────────────────────────────────────────────────
# 4. Sayfa no render testi (tüm şablonlar)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("tmpl_adi,extra_ctx", [
    (
        "ust_yazi.jinja2",
        {"konu": "Test", "metin_paragraflari": ["Metin."], "kapalis_ifadesi": "arz ederim."},
    ),
    (
        "cevap_yazisi.jinja2",
        {
            "konu": "Test",
            "ilgi": _ILGI,
            "yanit_turu": "belge_talebi",
            "metin_paragraflari": ["Metin."],
            "kapalis_ifadesi": "arz ederim.",
        },
    ),
    (
        "tekit_yazisi.jinja2",
        {"ilgi": _ILGI, "gun": 5},
    ),
])
def test_sayfa_no_render(jinja_env, tmpl_adi, extra_ctx):
    """sayfa_no verildiğinde '1/2' formatında render edilmeli."""
    tmpl = jinja_env.get_template(tmpl_adi)
    ctx = {**_ORTAK_CONTEXT, **extra_ctx, "sayfa_no": "1/2"}
    render = tmpl.render(**ctx)
    assert "1/2" in render, (
        f"{tmpl_adi}: sayfa_no='1/2' render çıktısında bulunamadı."
    )


# ──────────────────────────────────────────────────────────────────────────────
# 5. T.C. başlık sırası — 3 şablonda da
# ──────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("tmpl_adi,extra_ctx", [
    (
        "ust_yazi.jinja2",
        {"konu": "Test", "metin_paragraflari": ["Metin."], "kapalis_ifadesi": "arz ederim."},
    ),
    (
        "cevap_yazisi.jinja2",
        {
            "konu": "Test",
            "ilgi": _ILGI,
            "yanit_turu": "belge_talebi",
            "metin_paragraflari": ["Metin."],
            "kapalis_ifadesi": "arz ederim.",
        },
    ),
    (
        "tekit_yazisi.jinja2",
        {"ilgi": _ILGI, "gun": 5},
    ),
])
def test_tc_baslik_sirasi(jinja_env, tmpl_adi, extra_ctx):
    """T.C. → idare adı → birim adı sırası her şablonda korunmalı."""
    tmpl = jinja_env.get_template(tmpl_adi)
    ctx = {**_ORTAK_CONTEXT, **extra_ctx}
    render = tmpl.render(**ctx)
    gecerli, mesaj = alan_sirasi_dogru_mu(render, [
        "T.C.",
        "\u00c7EVRE VE \u015eEH\u0130RC\u0130L\u0130K BAKANLI\u011eI",
        "Bilgi \u0130\u015flem Dairesi Ba\u015fkanl\u0131\u011f\u0131",
    ])
    assert gecerli, f"{tmpl_adi}: {mesaj}"


# ────────────────────────────────────────────────────────────────────────────────
# Renderer API Testleri
# Bu sınıf "jinja_env fixture'ında StrictUndefined tanımlı" varsayımının
# ötesine geçer: render_* fonksiyonlarının uyguladığı ön-kontrolleri test eder.
# ────────────────────────────────────────────────────────────────────────────────

class TestRendererApi:
    """render_* fonksiyonlarının StrictUndefined ve ön-kontrol güvencelerini test eder."""

    _TEKIT_CTX = {
        **_ORTAK_CONTEXT,
        "ilgi": _ILGI,
        "gun": 7,
    }
    _UST_CTX = {
        **_ORTAK_CONTEXT,
        "konu": "Test Konusu",
        "metin_paragraflari": ["Metin."],
        "kapalis_ifadesi": "arz ederim.",
    }
    _CEVAP_CTX = {
        **_ORTAK_CONTEXT,
        "konu": "Cevap Testi",
        "ilgi": _ILGI,
        "yanit_turu": "belge_talebi",
        "metin_paragraflari": ["Metin."],
        "kapalis_ifadesi": "arz ederim.",
    }

    # ── render_ust_yazi ───────────────────────────────────────────────────────────────

    def test_render_ust_yazi_str_doner(self):
        """render_ust_yazi başarılı çağrıda str dönmelidir."""
        sonuc = render_ust_yazi(self._UST_CTX)
        assert isinstance(sonuc, str)
        assert "T.C." in sonuc

    def test_render_ust_yazi_eksik_alan_undefined_error(self):
        """
        Zorunlu alan eksikse UndefinedError fırlatılmalıdır.
        StrictUndefined merkezi renderer'dan geldiğinden, çağrıcı
        herhangi bir ayar yapmak zorunda kalmaz.
        """
        eksik_ctx = {k: v for k, v in self._UST_CTX.items() if k != "sayi"}
        with pytest.raises(UndefinedError):
            render_ust_yazi(eksik_ctx)

    # ── render_cevap_yazisi ─────────────────────────────────────────────────────────

    def test_render_cevap_yazisi_gecerli(self):
        """Geçerli context ile render_cevap_yazisi str dönmelidir."""
        sonuc = render_cevap_yazisi(self._CEVAP_CTX)
        assert isinstance(sonuc, str)
        assert "\u0130lgi:" in sonuc

    def test_render_cevap_yazisi_ilgi_yok_value_error(self):
        """
        [TASARIM KARARI] ilgi eksikse ValueError fırlatılmalıdır.
        render_cevap_yazisi bu kontrolü Jinja2'nin render öncesinde
        yapar; Ajan 6 UndefinedError yerine açıklayıcı mesaj alır.
        """
        eksik_ctx = {k: v for k, v in self._CEVAP_CTX.items() if k != "ilgi"}
        with pytest.raises(ValueError, match="ilgi"):
            render_cevap_yazisi(eksik_ctx)

    def test_render_cevap_yazisi_ilgi_bos_liste_value_error(self):
        """ilgi boş liste geçildiğinde de ValueError fırlatılmalıdır."""
        bos_ilgi_ctx = {**self._CEVAP_CTX, "ilgi": []}
        with pytest.raises(ValueError, match="ilgi"):
            render_cevap_yazisi(bos_ilgi_ctx)

    # ── render_tekit_yazisi ─────────────────────────────────────────────────────────

    def test_render_tekit_yazisi_gecerli(self):
        """Geçerli context ile render_tekit_yazisi str dönmelidir."""
        sonuc = render_tekit_yazisi(self._TEKIT_CTX)
        assert isinstance(sonuc, str)
        assert "tekiden rica ederim" in sonuc

    def test_render_tekit_gun_eksik_value_error(self):
        """
        gun eksikse ValueError fırlatılmalıdır.
        UndefinedError'a göre açıklayıcı bir mesaj içermelidir.
        Ajan 6 bu sayede hangi parametreyi neden eklemesi gerektiğini
        anlar.
        """
        eksik_ctx = {k: v for k, v in self._TEKIT_CTX.items() if k != "gun"}
        with pytest.raises(ValueError, match="gun"):
            render_tekit_yazisi(eksik_ctx)

    def test_render_tekit_gun_none_value_error(self):
        """gun=None geçildiğinde de ValueError fırlatılmalıdır."""
        none_ctx = {**self._TEKIT_CTX, "gun": None}
        with pytest.raises(ValueError, match="gun"):
            render_tekit_yazisi(none_ctx)

    def test_render_tekit_ilgi_yok_value_error(self):
        """ilgi eksikse ValueError fırlatılmalıdır (Madde 34)."""
        eksik_ctx = {k: v for k, v in self._TEKIT_CTX.items() if k != "ilgi"}
        with pytest.raises(ValueError, match="ilgi"):
            render_tekit_yazisi(eksik_ctx)

    def test_render_tekit_gun_farkli_degerlerle_calisir(self):
        """Farklı gun değerleri render_tekit_yazisi ile doğru render edilmeli."""
        for gun in [3, 7, 14, 30]:
            ctx = {**self._TEKIT_CTX, "gun": gun}
            sonuc = render_tekit_yazisi(ctx)
            assert f"{gun} gün içinde" in sonuc, (
                f"gun={gun} için '{gun} gün içinde' render çıktısında bulunamadı."
            )

    def test_renderer_ve_fixture_ayni_env(self):
        """
        get_env()'in döndürdüğü environment StrictUndefined kullanmalıdır.
        Bu test, test ortamı ile üretim renderer'ının aynı konfigürasyonu
        paylaştığını güvence altına alır.

        Not: env.undefined, Jinja2'de bir sınıf nesnesidir (instance değil);
        bu yüzden 'is' karşılaştırması kullanılır.
        """
        from renderers.template_renderer import get_env
        from jinja2 import StrictUndefined
        env = get_env()
        assert env.undefined is StrictUndefined, (
            "Renderer env'i StrictUndefined kullanmıyor! "
            f"Gerçek değer: {env.undefined}"
        )
