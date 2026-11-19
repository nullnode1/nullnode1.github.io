# FreeBSD için ES8336 Tiger Lake Ses Sürücüsü

*19 Kasım 2026*

## Giriş

Merhabalar! Ben **Görkem**. Günlük hayatımda **Fedora Linux** kullanan birisiyim. Normalde pek oyun oynamam. Genellikle bilgisayarımla uğraşmayı, yeni şeyler denemeyi ve sistemi kurcalamayı severim.

Geçenlerde **FreeBSD** kullanmaya karar verdim. Aslında daha önce de denemiştim. O zamanlar FreeBSD 14.2 sürümünü bilgisayarıma temiz kurulum yaparak yüklemiştim.

Fakat kurmaz olaydım!

**Wi-Fi** o kadar yavaş çalışıyordu ki sinirden laptopu paramparça edecektim. Neyse, bir şekilde sistemi kurdum. Masaüstü ortamı olarak da o zamanlar **KDE Plasma** kullanmayı tercih etmiştim.

Sistem açıldığında her şey gözle görülür şekilde garip çalışıyordu. Ses sürücüleri çalışmıyor, Bluetooth almış başını gidiyor, ekran kartı sürücüsü bile ağlıyordu.

Ekrandaki yırtılmalar da cabası! Sanki 60 Hz ekranda Valorant'ı 100 FPS oynuyormuşum gibi sürekli görüntü yırtılması yaşıyordum.

Kısacası, pek de güzel bir deneyim değildi.

## Fedora'ya Geri Dönüş

O dönem yaşadığım sorunlardan dolayı tekrar **Fedora'ya** dönmüştüm.

Fedora öyle bir sistem ki benim bilgisayarımda varsayılan olarak **Windows'tan bile kat kat daha iyi** çalışıyordu.

Bilgisayarımın üreticisi **Casper**. Kullandığım modelde bazı donanımların Windows tarafında özel OEM sürücülerine ve yapılandırmalarına ihtiyacı var. Ancak Windows'ta yaşadığım bir ses sorunu vardı.

Bilgisayar açıldıktan yaklaşık 5 saniye sonra ses kartı kendiliğinden kapanıyordu. Ses gidiyor, bir daha da gelmiyordu.

Öyle bir rezillik!

Fakat **Fedora'da** durum tamamen farklıydı. Sistemi kurduğum anda **Wi-Fi, ses, ekran kartı** ve diğer donanımlar herhangi bir ek uğraş gerektirmeden çalışıyordu.

Windows'tan Fedora'ya ilk geçtiğimde ciddi anlamda şaşırmıştım.

Yaklaşık **2-3 yıl Fedora kullandım** ve gayet memnundum. Windows'u gram aratmıyordu.

Tabii bu süre içerisinde yalnızca Fedora kullanmadım. Birçok farklı **Linux dağıtımını** kendi bilgisayarımda kurup denedim.

Her dağıtımın kendine göre güzel özellikleri var.

Mesela **CachyOS**, Arch Linux tabanlı olmasına rağmen benim denemelerimde oldukça hızlı ve kararlı çalışıyordu. **Ubuntu** ise kullanım kolaylığı, sadeliği ve Debian tabanından gelen geniş paket ekosistemi sayesinde güzel bir alternatifti.

Ancak şöyle bir sorun vardı:

**Bilgisayarımın ses kartı, Fedora dışında denediğim dağıtımların çoğunda düzgün çalışmıyordu.**

Aslında Linux çekirdeği ses donanımımı tanıyordu. Yani donanım tamamen desteksiz değildi. Sorun daha çok ses kartının nasıl yapılandırıldığıyla ilgiliydi.

Bilgisayar açılırken hoparlörü düzgün şekilde etkinleştirmek yerine doğrudan **headphones**, yani kulaklık çıkışına geçiyordu. Bu nedenle laptopun kendi hoparlörlerinden ses alamıyordum.

Ben de o dönem yapay zekâdan yardım alarak yapılandırma dosyalarını düzenliyor ve ses kartını çalışır hâle getiriyordum.

Şimdiyse Fedora'da hazır gelen **`sof-essx8336`** ile ilgili yapılandırmalardan yararlanarak diğer Linux dağıtımlarında da bu sorunu çözebiliyorum.

Yani Linux tarafında ses sorununu bir şekilde halletmiştim.

Ama asıl macera daha yeni başlıyordu.

## FreeBSD 15.1 ile Yeniden Tanışma

Yaklaşık 1-2 hafta önce biraz canım sıkıldı. Ne yapsam diye düşünürken aklıma tekrar **FreeBSD** geldi.

Yeni sürümlerini araştırmaya başladım. Özellikle **FreeBSD 15.1** sürümünde dizüstü bilgisayar uyumluluğuyla ilgili çalışmaların ilerlediğini ve FreeBSD Vakfının bu konuya daha fazla önem vermeye başladığını gördüm.

Bunun üzerine kendi kendime dedim ki:

**"Acaba bu sefer bilgisayarımda nasıl çalışacak?"**

Akşamına `FreeBSD-15.1-RELEASE-amd64-memstick.img` dosyasını indirip bilgisayarıma kurulum yaptım.

Kurulum ekranının tasarımı eski olmasına rağmen oldukça anlaşılırdı. Hatta kurulum aracına birkaç yeni özellik de eklemişler. Bu da hoşuma gitti.

Tabii kurulumdan sonra varsayılan olarak grafiksel bir masaüstüyle karşılaşmıyorsunuz. Bu normal çünkü FreeBSD, Linux dağıtımlarının çoğundan farklı olarak masaüstü ortamını kullanıcıya seçtiren bir yapıya sahip.

Ayrıca FreeBSD, masaüstünde de kullanılabilmesine rağmen uzun yıllardır özellikle sunucu ve sistem yönetimi alanlarında güçlü bir yere sahip.

Yine de günlük kullanımda oldukça hafif ve hızlı çalışabiliyor.

**FreeBSD Vakfı** da dizüstü bilgisayar deneyimini iyileştirmek için çalışmalar yürütüyor.

Merak edenler için:

[FreeBSD Laptop Testing and Integration Project](https://www.freebsd.org/status/report-2026-01-2026-03/laptop-integration/)

Neyse, sistemi kurdum.

Oturum yöneticisi olarak hafif olması nedeniyle **LightDM** kullanmayı tercih ettim.

Görüntüleme sistemi içinse **X11** seçtim. Aslında FreeBSD üzerinde Wayland kullanmak da mümkün. Fakat bazı masaüstü ortamlarında ve donanımlarda uyumluluk sorunları yaşanabildiğinden, kendi bilgisayarımda daha sorunsuz olacağını düşündüğüm X11 ile devam etmeye karar verdim.

Masaüstü ortamı olarak da **XFCE4** seçtim.

Amacım basitti: Hafif, hızlı, sade ve günlük kullanımda beni uğraştırmayacak bir sistem kurmak.

Birkaç ayar yaptıktan sonra XFCE4'ü istediğim kıvama getirdim ve masaüstümü tamamladım.

Sonuç gerçekten hoşuma gitti!

## Peki, Donanımlar Çalışıyor mu?

Şimdi gelelim FreeBSD 15.1 kurduktan sonra bilgisayarımda nelerin çalışıp nelerin çalışmadığına.

**Ekran Kartı**

Bilgisayarımda **Intel Iris Xe (Tiger Lake GT2)** grafik birimi bulunuyor.

Ekran kartı sürücüsü gayet güzel çalışıyor. **OpenGL, Vulkan** ve diğer grafik özelliklerinde yaptığım denemelerde ciddi bir sorunla karşılaşmadım.

Önceki FreeBSD deneyimime göre oldukça iyi durumdaydı.

**Pil Yönetimi**

Pil yönetimi çalışıyor gibi görünüyor. Açıkçası çok fazla kurcalamadım.

Ancak pil durumunu algılama, şarj kablosunu takıp çıkarınca durumun değişmesi ve temel güç yönetimi özellikleri çalışıyordu.

Uyku modu ve pil tasarrufu gibi konularda ise daha kapsamlı testler yapmadım.

**Ekran Parlaklığı**

Ekran parlaklığını değiştirebiliyorum. Yani donanım tarafında bu özellik çalışıyor.

Ancak parlaklığı daha rahat yönetebilmek için kendime küçük bir arayüz yazdım.

Sonuç olarak parlaklık sorunum yok.

**Bluetooth**

Bluetooth'u henüz test etmedim.

Açıkçası günlük hayatımda çok fazla kullanmadığım için şimdilik öncelik vermedim. Dolayısıyla çalışıp çalışmadığı konusunda kesin bir şey söyleyemiyorum.

**USB**

USB aygıtları ilk başta biraz garip davranıyordu.

Sistem USB belleği algılıyordu ama dosyalarına doğrudan erişemiyordum. Aslında sorun USB sürücüsünden ziyade dosya sisteminin bağlanmasıyla ilgiliydi.

Küçük bir yapılandırma yaptıktan sonra bu sorunu da çözdüm.

**Mikrofon**

Kullandığım USB mikrofon çalışıyordu.

Ancak burada önemli bir ayrıntı var: USB mikrofon ayrı bir ses aygıtı olarak çalıştığından, laptopun dahili ES8336 ses donanımıyla aynı sürücüye ihtiyaç duymuyor.

**Ses Sürücüleri**

Aha! Geldik keyfimin içine eden asıl meseleye.

Bilgisayarımda **Intel Tiger Lake-LP Smart Sound Technology** ses denetleyicisi ve **Everest ES8336** ses kodeği bulunuyor.

Linux tarafında bu donanımın çalışması için **SOF (Sound Open Firmware)** altyapısı ve uygun ses sürücülerinden yararlanılıyor.

Fakat tahmin edin bakalım sorun ne?

**FreeBSD'de benim donanımım için hazır ve sorunsuz çalışan bir Intel SOF/ES8336 ses çözümü yoktu!**

SOF, yalnızca basit bir ses sürücüsünden ibaret değil. İçerisinde firmware, donanımla iletişim, ses işleme ve farklı bileşenlerin bir arada çalışmasını sağlayan oldukça kapsamlı bir altyapı bulunuyor.

Dolayısıyla Linux'taki sürücüyü alıp FreeBSD'ye kopyalayarak çalıştırmak mümkün değil.

FreeBSD'nin kendi çekirdek mimarisi ve ses altyapısıyla uyumlu bir çözüm gerekiyor.

Yıllardır FreeBSD forumlarında ve çeşitli topluluk platformlarında Intel SOF desteği hakkında sorular soruluyor. Özellikle bazı dizüstü bilgisayarlarda dahili hoparlörlerin çalışmaması sıkça gündeme geliyor.

Ben de birkaç gün önce **FreeBSD'nin resmî forumunda** bir konu açmıştım.

[FreeBSD için Intel SOF desteği planlanıyor mu? Tiger Lake ses sorunumu nasıl çözebilirim?](https://forums.freebsd.org/threads/any-plans-to-bring-intel-sof-audio-support-to-freebsd-tiger-lake-laptops.104378/post-783386)

Forumdaki kişiler sağ olsun, konuyla ilgilendiler ve yardımcı olmaya çalıştılar.

Ancak benim donanımım için doğrudan kullanabileceğim hazır bir çözüm bulunmadığını öğrendim.

İşte bu mesele birkaç gün boyunca kafamı kurcaladı.

## Kendi Ses Sürücümü Yazmaya Karar Verdim

Şöyle düşündüm:

FreeBSD ve Linux birbirinden farklı sistemler olsa da ikisi de Unix benzeri işletim sistemleri dünyasında yer alıyor.

FreeBSD kendi çekirdeği, kullanıcı alanı araçları ve sistem bileşenleriyle bütün bir işletim sistemi olarak geliştiriliyor. Linux ise teknik olarak bir çekirdek ve bu çekirdeği kullanan çeşitli işletim sistemi dağıtımları bulunuyor.

Her ikisinin de donanımla iletişim kurma yöntemleri ve sürücü mimarileri birbirinden farklı.

Üstelik araştırdığım kaynaklardan, Intel SOF altyapısının Linux tarafında bile olgunlaşmasının uzun yıllar aldığını gördüm.

Bunun üzerine kendi kendime dedim ki:

**"Madem benim ses kartım çalışmıyor, o zaman neden kendim bir sürücü yazmayı denemiyorum?"**

Tabii burada küçük bir sorun vardı.

**Ben sıfırdan bir kernel sürücüsü yazacak kadar teknik bilgiye veya programlama deneyimine sahip değilim.**

Donanım sürücüsü yazmak, normal bir Python betiği veya masaüstü uygulaması geliştirmekten çok daha farklı.

Üstelik yanlış yapılan bir işlem sistemin çökmesine bile neden olabiliyor.

Bu yüzden projeyi **yapay zekâ yardımıyla** geliştirmeye karar verdim.

Amacım Linux'taki bütün SOF altyapısını FreeBSD'ye taşımak değildi. Öncelikle kendi bilgisayarımın donanımına özel, ses çıkışı sağlayabilecek deneysel bir sürücü geliştirmek istiyordum.

## Yapay Zekâ ile Geliştirme Süreci

Öncelikle Linux çekirdeğinde bulunan **`sof-essx8336`** sürücüsünün kaynak kodunu inceledim ve Fedora sistemimde çalışan ses yapılandırmalarını topladım.

Ardından elde ettiğim kaynak kodlarını, yapılandırma dosyalarını ve donanım bilgilerini **GPT-6.1 Sol (High Effort)** modeline verdim.

Modele yalnızca kaynak kodlarını vermekle kalmadım. Bilgisayarımın farklı işletim sistemlerinde nasıl davrandığını da tek tek anlattım.

Örneğin:

- Fedora üzerinde sesin nasıl çalıştığını,
- Diğer Linux dağıtımlarında neden sorun yaşadığımı,
- Windows tarafındaki ses problemini,
- FreeBSD'nin hangi donanımları algıladığını,
- Hoparlör ve kulaklık çıkışlarının nasıl davrandığını.

Böylece önce sorunun nerede olduğunu anlamaya çalıştık.

Model, bilgisayarımdan teknik bilgi toplamak için birkaç **Python** ve **Shell (`sh`)** betiği hazırladı.

Bu araçlarla sistem günlüklerini, ses aygıtlarının durumlarını, donanım bilgilerini ve sürücünün verdiği tepkileri incelemeye başladık.

Ardından deneme yanılma süreci başladı.

Ben bilgisayarımda testleri yapıyor, sonuçları modele iletiyor, model de elde ettiğimiz bilgilere göre kodu düzenliyordu.

Bazen bir değişiklik hiçbir işe yaramıyordu.

Bazen ses kartı algılanıyor ama hoparlörden ses gelmiyordu.

Bazen de bir sorunu çözdüğümüzü düşünürken başka bir sorun ortaya çıkıyordu.

Kısacası, epey uğraştık.

Ama yaklaşık **4 saatlik çalışmanın sonunda ilk sesi çıkarmayı başardık!**

Düşünün, FreeBSD'de günlerdir ses alamadığım hoparlörden sonunda ses geliyordu.

Tabii bu, sürücünün tamamlandığı anlamına gelmiyordu.

Daha yapılacak çok iş vardı.

## 11 Saatin Sonunda Çalışan Hoparlör

İlk sesi elde ettikten sonra sürücüyü geliştirmeye devam ettik.

Ses çıkışının daha kararlı çalışması, sistem açılırken sürücünün otomatik yüklenmesi ve çeşitli yapılandırmaların düzgün uygulanması için birçok düzenleme yaptık.

Hataları tespit etmek için tekrar tekrar günlük kayıtlarını inceledik.

Ardından yeni yamalar hazırladık, sistemi yeniden başlattık ve testleri tekrarladık.

Sonunda yaklaşık **11 saatlik çalışmanın ardından**, laptopun dahili hoparlörlerinden ses verebilen deneysel bir FreeBSD sürücüsü elde ettik.

Bu benim için gerçekten güzel bir gelişmeydi.

Ancak bir eksik vardı.

**Kablolu kulaklık desteği henüz düzgün çalışmıyordu.**

## Kulaklık Desteği: 6 Saatlik Yeni Macera

Bir gün sonra tekrar bilgisayarın başına geçtim.

Bu sefer hedefim **3,5 mm jak girişinden çalışan kablolu kulaklık desteğini** eklemekti.

Aslında bu aşama ilkine göre biraz daha kolay oldu.

Çünkü elimizde artık hoparlörlerden ses çıkarabilen çalışan bir temel vardı.

Bunun üzerine kulaklık algılama ve ses çıkışları arasında geçiş yapma özelliklerini eklemeye başladık.

İstediğim şey basitti:

**Kulaklığı taktığımda hoparlör otomatik kapansın, ses kulaklığa geçsin. Kulaklığı çıkardığımda ise ses tekrar hoparlörden gelsin.**

Normal bir bilgisayarda oldukça sıradan görünen bu özellik, kendi geliştirdiğimiz deneysel sürücüde ayrıca ele alınması gereken bir konuydu.

Yine testler yaptık.

Kulaklığı taktım, çıkardım, ses denemeleri yaptım, sistem günlüklerini inceledim.

Bazen kulaklık çalışıyor ama hoparlör kapanmıyordu.

Bazen hoparlör çalışıyor ama kulaklık algılanmıyordu.

Bu sorunları da adım adım çözmeye çalıştık.

Yaklaşık **6 saatlik ek çalışmanın ardından** kulaklık algılama ve otomatik ses çıkışı değiştirme özelliklerini çalıştırmayı başardık.

Yani toplamda yaklaşık **17-18 saatlik çalışma sonucunda**, kendi bilgisayarımda hem hoparlör hem de kablolu kulaklık çıkışını kullanabildiğim deneysel bir sürücü ortaya çıktı.

## ESSXSOF Projesini Neden Açık Kaynak Olarak Yayınladım?

Başlangıçta tek amacım kendi laptopumun ses sorununu çözmekti.

Ancak daha sonra şöyle düşündüm:

**"Benimle aynı veya benzer donanımı kullanan başka insanlar da bu sorunu yaşıyor olabilir."**

Bu yüzden ortaya çıkan projeyi yalnızca kendi bilgisayarımda tutmak istemedim.

Sürücüyü **ESSXSOF** adıyla GitHub üzerinde açık kaynak olarak yayınladım.

Projede yalnızca sürücünün kaynak kodları bulunmuyor. Kurulum betikleri, çeşitli yardımcı araçlar ve teknik dokümantasyonlar da yer alıyor.

Özellikle dokümantasyon kısmına önem vermeye çalıştım.

Çünkü bir geliştirici projeyi incelediğinde sürücünün nasıl çalıştığını, hangi donanım özelliklerinden yararlandığını ve hangi parçaların kendi sistemine özel olduğunu anlayabilsin istedim.

Bu belgeleri de yapay zekâ yardımıyla hazırladım.

Belgelerde donanım kayıtları, ses çıkışı yönetimi, kulaklık algılama, sistem başlangıcında sürücünün yüklenmesi ve geliştirme sırasında karşılaştığımız sorunlar gibi birçok teknik ayrıntı bulunuyor.

Böylece başka bir geliştirici isterse bu kaynakları inceleyerek kendi donanımına uygun bir uyarlama yapmayı deneyebilir.

Ayrıca günümüzde GPT veya Claude gibi modeller, karmaşık kaynak kodlarını incelemek ve açıklamak konusunda da yardımcı olabiliyor.

Dolayısıyla projeyle ilgilenen kişiler, yeterli teknik bilgiye sahip olmaları ve gerekli testleri dikkatli şekilde yapmaları koşuluyla bu araçlardan da yararlanabilirler.

Tabii burada önemli bir şeyi belirtmek istiyorum:

**ESSXSOF, bütün Intel SOF veya ES8336 donanımlarını destekleyen evrensel bir sürücü değil.**

Şu an için kendi **Casper Nirvana NB F500** bilgisayarım üzerinde geliştirdiğim ve test ettiğim, donanıma özel deneysel bir çalışma.

Dolayısıyla başka bir bilgisayarda doğrudan çalışacağının garantisi yok.

Ancak benzer donanımlar üzerinde çalışmak isteyen geliştiriciler için bir başlangıç noktası veya teknik kaynak olabilir.

Zaten projeyi yayınlamamın en önemli nedenlerinden biri de bu.

## Sonuç

Açıkçası bu işe başlarken kendi bilgisayarım için çalışan bir ses sürücüsü ortaya çıkarabileceğimi pek düşünmüyordum.

Sonuçta kernel sürücüsü geliştirme konusunda ciddi bir deneyimim yoktu.

Ama merak ettim, araştırdım, denedim ve yapay zekânın da yardımıyla bir şeyler ortaya çıkarmayı başardım.

Bu süreçte sürücülerin nasıl çalıştığı, donanımla nasıl iletişim kurulduğu ve küçük gibi görünen bir ses sorununun arkasında ne kadar karmaşık bir yapı olabildiği hakkında birçok yeni şey öğrendim.

Elbette bu proje kusursuz değil. Hâlâ deneysel ve geliştirmeye açık.

Ama en azından benim bilgisayarımda **FreeBSD 15.1 üzerinde hoparlör ve kablolu kulaklık artık çalışıyor.**

Başlangıçtaki hedefim de zaten buydu.

Kim bilir, belki ileride bu çalışma başka geliştiricilerin de işine yarar.

**Şimdilik benden bu kadar!**

Yazımı okuduğunuz için teşekkür ederim.

Projeye, kaynak kodlarına ve teknik dokümantasyona aşağıdaki GitHub bağlantısından ulaşabilirsiniz.

**GitHub:** [nullnode1/essxsof](https://github.com/nullnode1/essxsof)
