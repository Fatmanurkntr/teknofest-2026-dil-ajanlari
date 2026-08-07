# TEKNOFEST 2026 — Yapay Zeka Dil Ajanları Yarışması — Senaryo 1

Kamu Evrak ve Yazışma Süreçleri için Çok Ajanlı Akıllı Destek Sistemi.
Demo kurum profili: Örenli İlçe Kaymakamlığı (kurgusal).

## Klasör Yapısı ve Pipeline Karşılığı

| Klasör | Hangi Faz 0 pipeline'ı | Durum |
|---|---|---|
| `schemas/` | Pipeline 1 — Arayüz Şeması | Başlanmadı |
| `templates/`, `validators/`, `tests/` | Pipeline 2 — Format Motoru | 🔧 Devam ediyor |
| `data/raw/mevzuat/` | Pipeline 3 — Mevzuat Korpusu Toplama | Başlanmadı |
| `data/config/` | Pipeline 4 — Kurum Config | Başlanmadı |
| `docs/` | Ortak dokümantasyon | — |
| `data/processed/` | Faz 1 (mevzuat işleme) | İleride |
| `data/sentetik/` | Faz 2 (sentetik veri üretimi) | İleride |
| `docker/` | Faz 1 (altyapı) | İleride |

## Faz 0 Tracker

| # | Pipeline | Durum |
|---|---|---|
| 1 | Arayüz Şeması (JSON Sözleşmesi) | Başlanmadı |
| 2 | Format Motoru | 🔧 Devam ediyor |
| 3 | Mevzuat Korpusu Toplama | Başlanmadı |
| 4 | Kurum Config (Kaymakamlık) | Başlanmadı |

## Lisans

Açık kaynak lisansı (Apache 2.0 / MIT — ekip kararı burada belirtilecek)
TEKNOFEST şartnamesi madde 7 gereği zorunludur.
