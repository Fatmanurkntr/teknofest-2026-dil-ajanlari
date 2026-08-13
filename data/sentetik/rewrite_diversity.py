import json
import random
from pathlib import Path

KAYNAK = Path("data/sentetik/evraklar.jsonl")

# 16 ihale_itirazi konuları
ihale_konulari = [
    {
        "konu": "Araç Kiralama İlan Süresi İtirazı",
        "detay": "Kaymakamlık makam araçları kiralama ihalesinde ilan süresinin yasal asgari sınırın altında kaldığı tarafımızca tespit edilmiştir. İlan süresinin kısalığı rekabeti daralttığından ihalenin yenilenmesi zaruridir."
    },
    {
        "konu": "Kömür Alımı İhalesi Marka Kısıtı",
        "detay": "SYDV kömür alımı ihalesi idari şartnamesinde belirli bir kömür markasının doğrudan zikredildiği, bunun da eşitlik ve şeffaflık ilkelerine aykırı olduğu açıktır."
    },
    {
        "konu": "Yemek Hizmeti Aşırı Düşük Fiyat Sorgusu",
        "detay": "Taşımalı eğitim yemek hizmeti ihalesinde firmamız en avantajlı fiyatı vermiş olmasına rağmen, aşırı düşük teklif açıklaması yapmamıza izin verilmeden değerlendirme dışı bırakıldık."
    },
    {
        "konu": "Temizlik İhalesi Deneyim Belgesi Oranı",
        "detay": "İlçe Milli Eğitim Müdürlüğü temizlik ihalesinde istenilen benzer iş deneyim belgesi oranının yönetmeliğe aykırı olarak %50'den %70'e çıkarılması nedeniyle ihaleye katılımımız engellenmiştir."
    },
    {
        "konu": "Kırtasiye Alımı Fiyat Sıralaması Hatası",
        "detay": "Okulların kırtasiye malzemesi alımı ihalesinde ihale komisyonunun fiyat sıralamasını yanlış hesaplayarak, teknik olarak en avantajlı teklifi sunan firmamızı usulsüz şekilde ikinci sıraya attığına itiraz ediyoruz."
    },
    {
        "konu": "Özel Güvenlik İhalesinde Alt Yüklenici Yasağı",
        "detay": "Hizmet binaları özel güvenlik alımı ihalesinde alt yüklenici çalıştırılmasına kesin yasak getirilmesinin işin doğasına aykırı olduğu gerekçesiyle şartnamenin zeyilname ile düzeltilmesini istiyoruz."
    },
    {
        "konu": "Kamera Sistemi İhalesi Teknik Şartnamesi",
        "detay": "MOBESE ve çevre güvenlik kamera alımı ihalesinde talep edilen kamera çözünürlük değerleri, piyasada sadece tek bir yabancı üretici firmanın ürünlerini işaret edecek şekilde kaleme alınmıştır."
    },
    {
        "konu": "Geçici Teminat Mektubu Süresine İtiraz",
        "detay": "Hükümet Konağı dış cephe onarımı ihalesinde sunduğumuz geçici teminat mektubunun geçerlilik süresi komisyonca hatalı yorumlanarak teklifimiz haksız yere değerlendirme dışı bırakılmıştır."
    },
    {
        "konu": "Klima Bakım İhalesinde Kura Usulü Hatası",
        "detay": "Kurum binalarının klima bakım ihalesinde, firmamız ile bir diğer firmanın teklifleri birebir eşit olmasına rağmen, yasa gereği yapılması gereken kura çekimine firmamızın temsilcisi davet edilmemiştir."
    },
    {
        "konu": "Akaryakıt İhalesi Sözleşme Tasarısı Çelişkisi",
        "detay": "Kurum araçları akaryakıt alımı ihalesinin idari şartnamesi ile sözleşme tasarısında ödeme vadelerine ilişkin birbiriyle çelişkili maddeler bulunmaktadır, idari inceleme talep ediyoruz."
    },
    {
        "konu": "Öğrenci Taşıma İhalesi Kapasite Raporu",
        "detay": "Taşımalı sistem öğrenci taşıma hizmeti ihalesinde ihale üzerinde bırakılan firmanın sunduğu asgari araç kapasite raporlarının güncel olmadığı ve ihale tarihinden önce süresinin dolduğu tespit edilmiştir."
    },
    {
        "konu": "Promosyon Ürünleri Numune Değerlendirmesi",
        "detay": "Kaymakamlık logolu promosyon ürünleri alımı ihalesinde kurumunuza sunduğumuz numunelerin, teknik heyetçe laboratuvar testi yapılmadan sadece gözle muayene ile keyfi olarak reddedilmesine itiraz ediyoruz."
    },
    {
        "konu": "Donanım Alımı Garanti Süresi Kısıtı",
        "detay": "Bilgisayar donanımı ihalesinde garanti süresinin standart 2 yıldan 5 yıla çıkarılmasının maliyetleri haksız şekilde artırdığına ve ihaleye sadece tek bir firmanın girmesini sağladığına yönelik itirazımızdır."
    },
    {
        "konu": "Asansör Bakım İhalesi Yeterlik Belgesi",
        "detay": "Hizmet binalarının asansör bakım ihalesinde sunduğumuz yetkili servis belgeleri, son başvuru tarihinden önce noter onaylı olarak teslim edilmiş olmasına rağmen dosyada bulunamadığı gerekçesiyle elenmemize itirazdır."
    },
    {
        "konu": "İlaçlama İhalesinde Aşırı Bilanço Kriteri",
        "detay": "Kurumların haşere ilaçlama hizmeti alımı ihalesinde istenen yıllık ciro oranının, işin yaklaşık maliyetinin çok üzerinde (yaklaşık 10 katı) tutularak yerel küçük işletmelerin engellenmesi şartına itiraz ediyoruz."
    },
    {
        "konu": "Çatı Yalıtım İhalesini Kazanan Firmanın Yasaklılığı",
        "detay": "Kurum arşivi çatı onarım ihalesini kazanan birinci firmanın, ihale tarihinde kamu ihalelerinden yasaklılar listesinde olduğu EKAP üzerinden tespit edilmiştir. İhalenin ikinci sıradaki firmamıza bırakılması talebimizdir."
    }
]

# 12 sosyal_yardim_basvuru konuları
sosyal_yardim_konulari = [
    {
        "konu": "Ev Yangını Sonrası Acil Eşya Yardımı",
        "detay": "Geçtiğimiz hafta evimizde çıkan elektrik kaynaklı yangın sonucunda tüm beyaz eşyalarımız ve mobilyalarımız kullanılamaz hale gelmiştir. Ailece mağdur durumdayız, acil eşya yardımı yapılmasını arz ederim."
    },
    {
        "konu": "Kronik Hasta Yol Gideri Desteği",
        "detay": "Diyaliz tedavisi gören çocuğumu haftanın üç günü il merkezindeki hastaneye götürmek zorundayım. Artan ulaşım masraflarını karşılayacak gücüm kalmadığından yol yardımı bağlanmasını talep ediyorum."
    },
    {
        "konu": "Afet Sonrası Tarım Kredisi Yapılandırması",
        "detay": "Aşırı yağışlar ve sel nedeniyle tarlamdaki mahsulün tamamı telef olmuştur. Ziraat Bankası'na olan çiftçi borçlarımın vakıf destekli afet fonu aracılığıyla yapılandırılması hususunda yardımlarınızı bekliyorum."
    },
    {
        "konu": "Çokuz Gebelik Bez ve Mama Yardımı",
        "detay": "Üçüz bebeklerimin dünyaya gelmesi ve eşimin uzun süredir işsiz olması sebebiyle bebeklerimizin temel ihtiyaçlarını karşılayamıyoruz. Düzenli bebek bezi ile devam sütü yardımı bağlanmasını arz ederim."
    },
    {
        "konu": "Eşi Vefat Eden Kadın Dul Aylığı",
        "detay": "Eşimi geçen ay elim bir trafik kazasında kaybettim. Üzerime kayıtlı hiçbir mal varlığı, sosyal güvencem ve aylık gelirim bulunmadığından tarafıma dul aylığı bağlanması için işlemlerin yapılmasını arz ederim."
    },
    {
        "konu": "Asker Ailesi Kira Yardımı Talebi",
        "detay": "Evin tek geçim kaynağı olan oğlumun vatani görevini yapmak üzere askere gitmesiyle eve gelir getiren kimse kalmamıştır. Kiramı ödeyemediğim için asker ailesi kira yardımı talebimin değerlendirilmesini rica ederim."
    },
    {
        "konu": "Öksüz ve Yetim Eğitim Materyali Desteği",
        "detay": "Anne ve babasını bir kazada kaybeden torunlarıma bakmaktayım. Okulların açılacak olması nedeniyle yaşlılık maaşımla karşılayamadığım kırtasiye ve okul kıyafeti yardımlarının vakfınızca yapılmasını istiyorum."
    },
    {
        "konu": "Görme Engelli Beyaz Baston ve Sesli Cihaz",
        "detay": "Doğuştan %90 oranında görme engelliyim. Mevcut beyaz bastonumun kırılması ve sesli saatimin bozulması nedeniyle günlük hayatımı sürdüremiyorum. Yenilerinin vakfınızca temin edilmesini saygılarımla arz ederim."
    },
    {
        "konu": "Kışlık Odun ve Kömür Yardımı",
        "detay": "Rakımı yüksek dağ köyünde ikamet etmekteyiz. Kışın yolların kapanması riski yüksek olduğundan, kışlık odun ve kömür ihtiyacımızın havalar bozmadan erkenden karşılanması hususunda yardımlarınızı bekliyorum."
    },
    {
        "konu": "Tıbbi Cihaz Elektrik Faturası Desteği",
        "detay": "Solunum cihazına (oksijen konsantratörü) bağlı yaşayan babamın evde bakımı nedeniyle aşırı yükselen elektrik faturalarımızı ödeme güçlüğü çekiyoruz. Elektrik tüketim desteği programına alınmamızı talep ediyorum."
    },
    {
        "konu": "Barınma Şartlarının İyileştirilmesi ve Çatı Onarımı",
        "detay": "Toprak damlı kerpiç evimizde yağmur yağdığında sürekli içeri su damlıyor ve çocuklar sık sık hastalanıyor. Çatının branda, sac veya kiremit ile kaplanması için gereken inşaat malzemesi yardımını rica ederim."
    },
    {
        "konu": "Üniversite Öğrencisi Barınma ve Yurt Desteği",
        "detay": "Şehir dışında bir üniversite kazanan kızıma KYK yurdu çıkmaması üzerine kendisini özel yurda yerleştirmek zorunda kaldık. Yüksek yurt ücretini karşılayamadığımız için barınma bursu verilmesini arz ederim."
    }
]

# 14 tapu_kadastro_basvuru konuları
tapu_konulari = [
    {
        "konu": "Hatalı Yüzölçümü Kaydının Düzeltilmesi",
        "detay": "Eski tapu senedimde 5 dönüm olarak görünen arazimin, e-Devlet kayıtlarında 3 dönüm görünmesi sebebiyle geçmiş kadastro ölçümlerinin incelenerek yüzölçümü hatasının düzeltilmesini talep ediyorum."
    },
    {
        "konu": "Köy Boşluğunun İhlali ve Yola Tecavüz",
        "detay": "Komşumun yeni yaptığı bahçe duvarını köyün ortak kullanım alanı olan ana yola doğru 2 metre taşırması nedeniyle söz konusu duvarın kadastroca tespit edilip yıktırılarak sınırın eski haline getirilmesi şikayetidir."
    },
    {
        "konu": "Mirasta Kayıp Hissedar Tespiti ve İntikal",
        "detay": "Dededen kalma arazinin intikali sırasında varislerden birinin yıllar önce yurtdışında vefat etmiş olması ve ulaşılamaması nedeniyle gaiplik kararının tapuya işlenerek intikalin sağlanması hususunda bilgi talebidir."
    },
    {
        "konu": "Orman Sınırı İhtilafı ve Yeniden Ölçüm",
        "detay": "Dededen kalma tarlamın üst kısmının Orman Bölge Müdürlüğü tarafından son harita çalışmalarında orman sınırı içerisine dahil edilmesi kararına itiraz ediyor ve yerinde yeniden ölçüm yapılmasını arz ediyorum."
    },
    {
        "konu": "Parselasyon Planında Usulsüz Yola Terk",
        "detay": "Belediyenin yaptığı 18. madde imar uygulaması sonucunda arazimden yasal sınırların üzerinde fazladan yola terk yapıldığı tespit edilmiştir. Adaletsiz parselasyon planının iptali için işlemlerin başlatılması talebimdir."
    },
    {
        "konu": "Müşterek Tapuda İfraz ve Müstakil Tapu",
        "detay": "Üç kardeşin müşterek (ortak) tapusunda kayıtlı olan 15 dönümlük fındık bahçesinin tapusunun ifraz (bölünme) işlemi yapılarak her bir hissedara kendi payı oranında müstakil tapusunun verilmesi için başvuruyorum."
    },
    {
        "konu": "Tapu Üzerindeki Eski İpotek Şerhinin Kaldırılması",
        "detay": "Tapu kaydımın üzerinde Ziraat Bankası'nın 1990 yılından kalma, borcu çoktan ödenmiş ve geçerliliği bitmiş olan ipotek şerhinin (fehki) silinmesi için gerekli resmi yazışmaların yapılmasını arz ederim."
    },
    {
        "konu": "Hatalı Cins Tashihi Başvurusu",
        "detay": "Arazimde hiçbir mimari yapı bulunmamasına ve fiilen sadece tarım yapılmasına rağmen tapuda vasfının \"kargir ev ve arsası\" olarak geçmesi nedeniyle cins değişikliği yapılarak \"tarla\" olarak düzeltilmesini istiyorum."
    },
    {
        "konu": "Dere Yatağı Değişimi Nedeniyle Kadastro Sınır Kaybı",
        "detay": "Arazimin hemen doğu sınırından geçen derenin geçen yılki sel felaketinde yatağını değiştirmesiyle tarlamın büyük bir kısmının su altında kalması sonucu kadastro sınırının yerinde incelenerek yeniden çizilmesi talebimdir."
    },
    {
        "konu": "2/B Vasıflı Hazine Arazisi Satın Alma Talebi",
        "detay": "Yirmi yılı aşkın süredir ecrimisil bedelini düzenli ödeyerek tarım amaçlı kullandığım 2/B vasıflı Hazine arazisinin, ilgili kanun kapsamında doğrudan tarafıma satışının yapılması hususunda resmi başvurumdur."
    },
    {
        "konu": "Arkeolojik Sit Alanı Şerhine İtiraz",
        "detay": "Tarlamın tamamının Koruma Kurulu kararıyla 3. derece arkeolojik sit alanı ilan edilmesi nedeniyle üzerindeki seramı yenileyemiyorum ve tarımsal faaliyetlerim aksıyor. İlgili şerhin daraltılmasını talep ediyorum."
    },
    {
        "konu": "Mahkeme Kararıyla Geçit Hakkı Tesisi",
        "detay": "Ana yola doğrudan çıkışı bulunmayan arazime ulaşabilmek için komşu parsel üzerinden Asliye Hukuk Mahkemesi'nin lehimize verdiği karara istinaden tapu kütüğüne geçit hakkı şerhinin işlenmesini arz ederim."
    },
    {
        "konu": "Tapu Kaydında Baba Adı Yanlışlığının Tashihi",
        "detay": "Tapu senedinde baba adımın nüfus kütüğündeki \"Hüseyin\" yerine tapu memurunca yanlışlıkla \"Hasan\" olarak yazılması sebebiyle, elimdeki mahkeme tespiti kararına dayalı isim tashihi yapılması talebidir."
    },
    {
        "konu": "Ortak Kullanım Merasının İşgali Şikayeti",
        "detay": "Köyümüzün hayvancılık için ayrılmış ortak kullanımındaki meranın bir şahıs tarafından keyfi olarak tel örgüyle çevrilerek özel barınağa dönüştürülmesinin acilen durdurulması ve işgalin men edilmesi hususunda şikayetimdir."
    }
]

closings = [
    "Gereğini saygılarımla arz ederim.",
    "Gereğinin ivedilikle yapılmasını arz ederim.",
    "Talebimin olumlu değerlendirilmesini beklerim.",
    "Konunun incelenerek tarafıma resmi yazı ile bilgi verilmesini talep ediyorum.",
    "Mağduriyetimin giderilmesi hususunda takdirlerinize arz ederim.",
    "Gereken işlemlerin mevzuata uygun şekilde yapılmasını saygıyla arz ederim.",
    "Başvurumun işleme alınmasını rica ederim.",
    "Gereğinin ifasını yüce makamınızdan arz ederim.",
    "Durumu bilgilerinize sunar, gereğini arz ederim.",
    "İlgili makamlarca konunun tetkik edilmesini rica ederim.",
    "Sorunun çözüme kavuşturulmasını saygılarımla arz ederim.",
    "Yardımlarınızı bekler, iyi çalışmalar dilerim.",
    "İşlemlerin hızlandırılması hususunda gereğini arz ederim.",
    "Şikayetimin ivedilikle dikkate alınmasını arz ederim.",
    "Tarafıma yazılı olarak bilgi verilmesi hususunu arz ederim.",
    "Gereğinin yasal süresi içinde yapılmasını arz ederim.",
    "Hak kaybımın önlenmesi amacıyla gereğini rica ederim.",
    "Makamınızca uygun görülecek işlemlerin yapılmasını arz ederim."
]

def generate_mixed_records():
    with open(KAYNAK, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    final_lines = []
    
    ihale_idx = 0
    sosyal_idx = 0
    tapu_idx = 0

    for line in lines:
        if not line.strip():
            continue
            
        record = json.loads(line)
        r_id = record["id"]

        # Only process records SENT-0162 to SENT-0203
        if "SENT-0162" <= r_id <= "SENT-0203":
            
            # Fix Koç Yapı -> Aydınlar Yapı (specifically requested for SENT-0173)
            # Or if it occurs anywhere else, fix it globally for these IDs
            if "Koç Yapı" in record.get("metin", ""):
                record["metin"] = record["metin"].replace("Koç Yapı", "Aydınlar Yapı")
            if record.get("beklenen_alanlar") and "Koç Yapı" in record["beklenen_alanlar"].get("gonderen_adi", ""):
                record["beklenen_alanlar"]["gonderen_adi"] = record["beklenen_alanlar"]["gonderen_adi"].replace("Koç Yapı", "Aydınlar Yapı")

            turu = record["evrak_turu_dogru"]
            zorluk = record["zorluk"]
            eksik = record["eksik_alan_var_mi"]
            
            # Parse existing name, TC, Address, Date from current metin to keep them unchanged
            metin = record["metin"]
            
            # Since the structure is somewhat known (generated by us previously):
            # We can extract the name, address, TC/Vergi, Date using regex or simple splits
            import re
            
            # Name extraction (usually after BAŞVURAN: or İmza:)
            name_match = re.search(r'BAŞVURAN:\s*(.+)', metin)
            if name_match:
                name = name_match.group(1).strip()
            else:
                name_match2 = re.search(r'İmza:\s*(.+)', metin)
                name = name_match2.group(1).strip() if name_match2 else "Bilinmeyen Kişi"

            # Address extraction
            addr_match = re.search(r'Adres:\s*(.+)', metin)
            addr = addr_match.group(1).strip() if addr_match else ""

            # TC/Vergi extraction
            tc_match = re.search(r'(?:Kimlik No|Vergi No|Kimlik/Vergi No):\s*(\d+)', metin)
            tc = tc_match.group(1).strip() if tc_match else ""
            tc_label = "T.C. Kimlik No"
            if "Vergi No" in metin and "Kimlik No" not in metin:
                tc_label = "Vergi No"
            elif "Kimlik/Vergi No" in metin:
                tc_label = "Vergi/T.C. No"

            # Date extraction
            date_match = re.search(r'Tarih:\s*([\d\.]+)', metin)
            date = date_match.group(1).strip() if date_match else ""
            
            closing = random.choice(closings)
            
            if turu == "ihale_itirazi":
                scenario = ihale_konulari[ihale_idx % len(ihale_konulari)]
                ihale_idx += 1
                base_konu = scenario["konu"]
                detay = scenario["detay"]
                
                if zorluk == "zor":
                    yeni_metin = f"KAYMAKAMLIĞA\n\nFirmamız {base_konu} hakkında itirazda bulunmaktadır. {detay} İhalenin acilen durdurulması gerekmektedir. {closing}\n\nİmza: {name}"
                else:
                    yeni_metin = f"ÖRENLİ İLÇE KAYMAKAMLIĞINA\n\nBAŞVURAN: {name}\n"
                    if addr and not eksik:
                        yeni_metin += f"Adres: {addr}\n"
                    if tc and not eksik:
                        yeni_metin += f"{tc_label}: {tc}\n"
                    yeni_metin += f"\nKONU: {base_konu}\n\nAÇIKLAMALAR:\n1. {detay}\n2. 4734 sayılı Kamu İhale Kanunu uyarınca gerekli yasal incelemenin yapılmasını talep ediyoruz.\n3. {closing}\n\n"
                    if date and not eksik:
                        yeni_metin += f"Tarih: {date}\n"
                    yeni_metin += f"İmza: {name}"

            elif turu == "sosyal_yardim_basvuru":
                scenario = sosyal_yardim_konulari[sosyal_idx % len(sosyal_yardim_konulari)]
                sosyal_idx += 1
                base_konu = scenario["konu"]
                detay = scenario["detay"]

                if zorluk == "zor":
                    yeni_metin = f"KAYMAKAMLIĞA\n\n{base_konu} hakkında dilekçemdir. {detay} {closing}\n\n{name}"
                else:
                    yeni_metin = f"ÖRENLİ İLÇE KAYMAKAMLIĞINA\n(Sosyal Yardımlaşma ve Dayanışma Vakfı Başkanlığı)\n\nBAŞVURAN: {name}\n"
                    if addr and not eksik:
                        yeni_metin += f"Adres: {addr}\n"
                    if tc and not eksik:
                        yeni_metin += f"T.C. Kimlik No: {tc}\n"
                    yeni_metin += f"\nKONU: {base_konu}\n\nAÇIKLAMALAR:\n1. {detay}\n2. {closing}\n\n"
                    if date and not eksik:
                        yeni_metin += f"Tarih: {date}\n"
                    yeni_metin += f"İmza: {name}"

            elif turu == "tapu_kadastro_basvuru":
                scenario = tapu_konulari[tapu_idx % len(tapu_konulari)]
                tapu_idx += 1
                base_konu = scenario["konu"]
                detay = scenario["detay"]

                if zorluk == "zor":
                    yeni_metin = f"KAYMAKAMLIĞA\n\n{base_konu} ile ilgili şikayetim var. {detay} {closing}\n\n{name}"
                else:
                    yeni_metin = f"ÖRENLİ İLÇE KAYMAKAMLIĞINA\n\nBAŞVURAN: {name}\n"
                    if addr and not eksik:
                        yeni_metin += f"Adres: {addr}\n"
                    if tc and not eksik:
                        yeni_metin += f"T.C. Kimlik No: {tc}\n"
                    yeni_metin += f"\nKONU: {base_konu}\n\nAÇIKLAMALAR:\n1. {detay}\n2. Konunun ilgili müdürlüklerce incelenerek {closing.lower()}\n\n"
                    if date and not eksik:
                        yeni_metin += f"Tarih: {date}\n"
                    yeni_metin += f"İmza: {name}"
                    
            record["metin"] = yeni_metin
            record["beklenen_alanlar"]["konu"] = base_konu
            record["beklenen_alanlar"]["talep_metni"] = detay

        final_lines.append(json.dumps(record, ensure_ascii=False) + "\n")

    with open(KAYNAK, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

if __name__ == '__main__':
    generate_mixed_records()
    print("Diversity rewrite complete.")
