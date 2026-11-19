# FreeBSD ES8336 Tiger Lake Sürücsü

*19 Kasım 2026*

## Giriş
Merhabalar! Ben **Görkem**, günlük hayatımda **Fedora Linux** kullanan birisiyim. Normalde pek oyun oynamam. Genelde bilgisayarımla uğraşmayı ve onu kurcalamayı severim.
Geçenlerde **FreeBSD** kullanmaya karar verdim. Aslında önceden denemiştim. FreeBSD 14.2 sürümünü bilgisayarıma temiz kurulum yaparak kurmuştum. Fakat kurmaz olaydım, **Wi-Fi** o kadar yavaş çalışıyor ki sinirden laptopu param parça edecektim. Neyse, sistemi kurdum. Masaüstü ortamı olarak o zaman **KDE** seçmiş idim. Sistem açıldığında gözle fark edilir şekilde **garip** bir biçimde çalışıyor idi. Ses sürücüleri çalışmıyor, bluetooth almış başını gidiyor, ekran kartı sürücüsü bile ağlıyor idi. Ekrandaki yırtılmalar sanki 60Hz ekranda valoyu 100fps oynarmışcasına ekranda yırtılmalar vardı. 

O zaman **Fedora'ya** geri dönmüş idim. **Fedora** öyle bir sistem ki bilgisayarımda varsayılan olarak **Windows'tan** bile kat kat daha iyi çalışıyordu. Bilgisayarımın üreticisi **Casper** donanıma özel **OEM** sürücüler ürettiği için ve bu sürücüler **Windows'ta** şuanda düzgün çalışmadığı için ses kartı bilgisayar açıldıktan 5 saniye sonrasında otomatik kapanıyor idi. Öyle bir rezillik. Fakat **Fedora'da** bilgisayarımkurulduğu anda varsayılan olarak **Wi-Fi*, **Ses** ve daha nicesi her şey tek anlamıyla kusursuz bir şekilde çalışıyor idi. Bende zaten **Windows'tan** **Fedora'ya** geçtiğimde ciddi anlamda şaşırmıştım. Yaklaşık 2-3 yıl **Fedora** kullandım. Gayet memnun idim. **Windows'u* gram aratmıyor idi. Ben aynı zamanda sadece **Fedora** değil birden fazla **Linux** dağıtımını kendi bilgisayarımda denedim, kurdum, çalıştırdım. Her dağıtımın kendince güzel yanı var. Mesela **CahcyOS** Arch Linux tabanlı olmasına rağmen çok stabil ve çok hızlı, **Ubuntu** ise kolaylık sadelik ve paket genişliği açısından **Debian** tabanlı olduğu için çok güzel. Ancak şöyle bir sorun vardı. Bilgisayarımın ses kartı **Fedora** dışında hiçbir dağıtımda çalışmıyor idi. Ama teknik olarak destekliyor ve görüyor idi. Tek sorun konfigrasyon hatası. Bilgisayar açılırken ses kartımı başlatmak yerine direk **headphones** yani kulaklık moduna geçiyordu ve hoparlörden hiçbir ses gelmiyordu. Ben de **yapay-zeka** kullanaraktan o dönem konfigrasyonu düzeltip sistemde çalıştırılabilir hale getiriyordum. Şimdi ise **Fedora'da** otomatik hazır gelen **sof-essx8336** konfigrasyonlarını kopyalayıp her dağıtımda kullanıp sorunumu çözebiliyorum.

Yaklaşık 1-2 hafta önce birazcık canım sıkıldı. Sonrasında ise **FreeBSD**'nin yeni sürümleri çıktığını öğrendim. Yeni sürümde yani **15.1** sürümünde **Wi-Fi** vb. sorunların büyük ölçüde düzeltildiği ve laptop uyumluluk projesi olduğunu gördüm. Bende acaba bu sefer nasıl çalışır diye merak edip akşam **FreeBSD-15.1-RELEASE-amd64-memstick.img** dosyasını indirip bilgisayarıma kurulum yaptım. 

Kurulum ekranının tasarımı eski olmasına rağmen gayet anlaşılır bir şekilde kurulumu yaptım. Kurulum betiğine birkaç yenilik eklemişler. O da hoşuma gitti. Tabi **grafiksel arayüz yok** bu normal çünkü **FreeBSD masaüstü odaklı değil, sunucu odaklı bir işletim sistemi.** Şuanda amacı dışında kullanım yapıyorum ama buna rağmen çok hafif ve hızlı bir sistem. **FreeBSD** vakfıda şuan bunun farkında ki artık laptop projesini başlatmış durumdalar: [FreeBSD Laptop Projesi](https://www.freebsd.org/status/report-2026-01-2026-03/laptop-integration/)

Neyse, sistemi kurdum. Oturum yöneticisi için hız ve hafiflik odaklı olan **LightDM**'yi seçtim. Görüntü sunucusu için ise ne yazık ki **Wayland** desteği hala deneysel ve hala buglar bulunduğu için daha eski ama kaliteli olan **X11** görüntü sunucusunu seçtim.

Sistem ağır olmasın, görüntü net ve hızlı olsun diye de **Masaüstü ortamı olarak **XFCE4** seçtim. Birkaç ayar yaptıktan sonra **XFCE4'ü** istediğim kıvama getirdim ve masaüstümü kurdum.

Şimdi ise sistemimde şuan nelerin çalışıp çalışmadığına gelelim.

**Ekran Kartı** yani **İntel Iris XE TGL2** sürücüleri çok güzel bir şekilde çalışıyor. **Vulkan**, **OpenGL** vb. grafik işleyicileride çok güzel bir şekilde çalışıyor. 

**Pil Yönetimi** çalışıyor olarak gördüm, çok kurcalamadım pil tasarufu, uyku modu, pilden çıkmasını ve pile takılmasını algılama vb. çalışıyor. 

**Görüntü** sürücüleri çalışıyor yani ekran parlaklığı yönetimi vb. sorunsuz çalışıyor **ama onu yönetmek için özel küçük bir arayüz yazdım ama teknik olarak çalışıyor.** 

**Bluetooth** sürücülerini henüz denemedim şuanda çalışıyor mu emin değilim ama kullanmıyorum.

**USB** sürücüleri ise USB vb. okuma başta çalıştı ama sadece usb nin bağlı olup olmadığını görüyor idi, içine erişemiyor idi. Küçük bir ayarla hemen onu düzelttik yoksa varsayılan olarak sürücüler var, çalışıyor.

**Mikrofon** sürücüsü çalışıyor çünkü Laptopun mikrofonu ses kartına bağlı değil, USB üzerinden çalışmakta.

**Ses Sürücüleri** aha, keyfimin içine eden şeyde tam bu idi. Bende bir **Intel Tiger Lake-LP Smart Sound Technology** ses yongası var. Ama... bu ses yongasının çalışması için **SOF (Sound Open Firmware)** desteğine ihtiyacı var. Ve tahmin edin bakalım sorun ne? **FreeBSD** için resmi bir **SOF** sürücüsü yok! bunun nedeni ise **SOF** projesinin çok kapsamlı ve büyük bir proje olması ve geliştirici ekibin şuanda bu desteği arka plana alıp sunucular için optimizasyon yamaları vb. ile uğraşması.

Yıllardır **FreeBSD**'nin forumlarında, topluluk platformlarında bu desteğin ne zaman geleceği, hoparlörün çalışmadığı vb. bir sürü şikayet ve sitem bulunmaktadır. Ben de birkaç gün öncesinde **FreeBSD**'nin resmi **Forum** sayfasında bir konu açmıştım. 

Açtığım konu şu şekilde idi: [FreeBSD için SOF desteği vb. getirmeyi düşünüyor musunuz? Ve bilgisayarımdaki ses sorununu nasıl çözerim?](https://forums.freebsd.org/threads/any-plans-to-bring-intel-sof-audio-support-to-freebsd-tiger-lake-laptops.104378/post-783386)

Forumdaki kişiler sağolsun ilgi gösterdiler yardımcı olmaya çalıştılar ama ne yazık ki **SOF** desteği olmadığı için şuan bunun mümkün olmadığını öğrendim.

Bu konu iki gündür kafamı karıştırdı. Yani **FreeBSD** direk **UNIX** tabanlı bütün bir işletim sistemi. **LINUX** ise **UNIX**'in çalışma mantığını kopyalayarak yapılmış alternatif açık kaynak kodlu bir işletim sistemi idi. Ama araştırdığım bazı kaynaklara göre zaten **SOF** sürücüsünün **LINUX** için stabil ve çalışır bir hal alması yıllar sürmüş. 

Bende dedim madem ses kartım çalışmıyor, bende **LINUX**'ta halihazırda bulunan ses sürücüsünü **sadece kendi yonga setim için yazmaya karar verdim.** Ama bir sorunum vardı çünkü ben bir **DRIVER** yazacak kadar teknik bilgi ve programlama dili bilgisine sahip değilim. Bu sebepten ötürü bu projeyi **yapay-zeka** ile yapmaya karar verdim. Öncelikle, internetten **LINUX** için yapılmış `sof-essx8336` sürücüsünün kaynak kodunu edinip kendi **Fedora** sisteminden edindiğim konfigrasyon dosyalarını **GPT 6.1 Sol, High Effort**'a atarak sesin öncelikle diğer linux dağıtımlarında ne gibi tepki verdiği, **Fedora'da** nasıl çalıştığı ve **Windows'ta** sesin ne gibi tepkiler verdiğini teker teker ona anlattım. 

Öncelikle model, yapılandırma için benim kendi bilgisayarımdan **LOG** toplayan birkaç **python** ve **sh** tabanlı tool yazdı. AI ile teker teker sistemde ses kanallarının nasıl çalıştığı, adreslerin nerede olduğunu bulma vb. baya bi deneme yanılma ile **ilk sesi 4 saatin sonunda** çıkarabildik. Sonrasında ise üstüne yamalar, düzenlemeler, sistem başlayınca boot olma vb. toplam 11 saatte sadece hoparlörden ses çıkaran basit bir sürücü yazabildik.

1 Gün sonra da **JAK** yani kablolu kulaklık desteği için uğraşmaya başladım. Aslında bu daha kolay oldu. Çünkü elimizde halihazırda bu donanım için çalışan bir speaker sürücüsü var. Ben bunun üstüne jak kulaklığı tak çıkar, ses testi, jak girince sış hoparlörü kapat vb. bunun üzerinde yine deneme yanılma ile **GPT** ile yaptık. 6 Saat daha çalıştıktan sonra toplam 17-18 saatte artık çalışan deneysel bir sürücü elde ettik. Bende benle benzer yonga kullanan veya benzer sisteme sahip olan insanlar için işe yarayabileceğini düşünerek açık kaynak kodlu bir şekilde tüm sürücüyü yayınladım. Aynı zamanda **GPT** tarafınan birkaç dökümantasyon hazırladım. Bu dökümantasyonlarda sürücünün nasıl çalıştığı vb. herşey yazıyor. Yani bu sürücüyü kendi bilgisayarına uyarlamak isteyen bir geliştirici bu notlara bakarak kendisi uyarlayabilir. Eğer hiçbir şey bilmiyor ise notları **GPT** veya **Claude** gibi muhakeme yeteneği güçlü olan güncel modellere kaynak kodunu vererek kendi bilgisayarına uyarlama girişiminde bulunabilir.

Şuanlık bu kadar. Yazımı okuduğunuz için teşekkür ederim. Aşağıdaki linkten projeye ulaşabilirsiniz.

Github: [https://github.com/nullnode1/essxsof](https://github.com/nullnode1/essxsof)
