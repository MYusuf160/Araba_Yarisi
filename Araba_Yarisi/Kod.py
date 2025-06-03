# -*- coding: utf-8 -*-
"""
Created on Sun May 26 23:10:31 2024

@author: harun
"""

# Python programlama dilinde yazılmış 2D oyunlar geliştirmek için kullanılan bir kütüphanedir. 
import pygame
# PyGame'in sıkça kullanılan sabitlerini (constants) ve fonksiyonlarını doğrudan import ederek 
# kullanmayı sağlar. QUIT, KEYDOWN gibi olay sabitleri doğrudan kullanılabilir. 
# QUIT: Oyun penceresi kapatıldığında meydana gelen olay
# KEYDOWN: Klavyede bir tuşa basıldığında meydana gelen olay
from pygame.locals import *
# Random modülü, rastgele sayıların ve seçimlerin yapılmasını sağlar.
# Rastgele düşman konumları, rastgele sayı üretimi veya rastgele olaylar gibi durumlarda kullanılır. 
import random

# PyGame modülünü başlatır. Oyunların çalışması için gerekli olan temel ayarları yapar.
pygame.init()

# Pencere boyutlarını oluşturuyoruz. Genişlik ve yükseklik pixel cinsinden belirler.
genislik = 500
yukseklik = 500

ekran_boyutu = (genislik, yukseklik)

# Belirtilen boyutlarda bir pencere oluşturulur. 
# "yüzey" (surface) nesnesi döndürür.
ekran = pygame.display.set_mode(ekran_boyutu)

# Oyun penceresinin başlığını ayarlamak için kullanılır. 
pygame.display.set_caption('Araba Oyunu')


gri = (100, 100, 100)
yesil = (76, 208, 56)
kirmizi = (200, 0, 0)
beyaz = (255, 255, 255)
sari = (255, 232, 0)




# Yol ve işaretleyici boyutları
yol_genisligi = 300   # Yolun genişliğini temsil eder.
isaret_genisligi = 10  # Yolun ortasındaki veya kenarındaki çizgi işaretlerinin genişliğini temsil eder. 
isaret_yuksekligi = 25 # Yol çizgilerinin uzunluğunu temsil eder.

#ŞERİT KOORDİNATLARI
sol_serit = 150   # Sol şeridin x koordinatını temsil eder. 
orta_serit = 250 # Orta şeridin x koordinatını temsil eder.
sag_serit = 350  # Sağ şeridin x koordinatını temsil eder. 
seritler = [sol_serit, orta_serit, sag_serit] # Liste, şerit koordinatlarını toplu bir şekilde saklamanızı ve üzerinde işlem yapmanızı sağlar.

# Yol ve kenar işaretleri
# Yolun dikdörtgen koordinatlarını ve boyutlarını tanımlar(Sol kenarın x konumu, yolun üst kenarın y konumu, Yolun genişliği, yolun süksekliği) 
yol = (100, 0, yol_genisligi, yukseklik)
# Sol kenar işaretleyicisinin dikdörtgen koordinatlarını ve boyutlarını tanımlar(İşaretleyicinin X koordinatı, y koordinatı, genişilk, yükseklik)
sol_kenar_isareti = (95, 0, isaret_genisligi, yukseklik)
# Sağ kenar işaretleyicisinin dikdörtgen koordinatlarını ve boyutlarını tanımlar.
sag_kenar_isareti = (395, 0, isaret_genisligi, yukseklik)

# Şerit işaretleyicilerinin hareketini canlandırmak için
# Şerit işaretleyicilerinin dikey hareketini kontrol etmek için kullanılır.Başlangıçta 0 olarak ayarlanmış, yani henüz bir hareket yok.
serit_isareti_hareket_y = 0

# Oyuncunun başlangıç ​​koordinatları
oyuncu_x = 250
oyuncu_y = 400

# çerçeve ayarları
clock = pygame.time.Clock() # Oyunun zamanlamasını kontrol etmek için kullanılan nesne oluşturur.
fps = 120 # Bu, oyun animasyonlarının akıcı olmasını sağlar.

# Oyun ayarları
oyun_bitti = False # Oyunun bitip bitmediğini kontrol eder. 
hiz = 2 # Oyundaki hareket hızını belirler. 
en_iyi_skor = 0
skor = 0 # Oyuncunun skorunu tutar. 

# (hem oyuncu aracı hem de diğer araçlar) temsil eder.
# Arac sınıfı genel bir araç tanımı sağlar
class Arac(pygame.sprite.Sprite):
    def __init__(self, resim, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Görüntüyü şerit genişliği olan 45 piksele sığdırmak için ölçek faktörü hesaplanır.
        resim_olcek = 45 / resim.get_rect().width
        # Yeni genişlik, orijinal genişliğin ölçek faktörü ile çarpılmasıyla hesaplanır.
        yeni_genislik = resim.get_rect().width * resim_olcek
        # Yeni yükseklik, orijinal yüksekliğin ölçek faktörü ile çarpılmasıyla hesaplanır.
        yeni_yukseklik = resim.get_rect().height * resim_olcek
        # Görüntü, hesaplanan yeni genişlik ve yükseklikle ölçeklendirilir.
        self.image = pygame.transform.scale(resim, (yeni_genislik, yeni_yukseklik))
        
        # Görüntünün dikdörtgen (rect) nesnesi alınır.
        self.rect = self.image.get_rect()
        # Dikdörtgenin merkezi, sağlanan x ve y koordinatlarına ayarlanır.
        self.rect.center = [x, y]
        
# Arac sınıfının tüm özelliklerini ve metodlarını miras alır    
# OyuncuAraci sınıfı, belirli bir oyuncu aracı tanımlar.     
class OyuncuAraci(Arac):
    def __init__(self, x, y):
        # Aracın görüntüsü car.png dosyasından yüklenir.
        resim = pygame.image.load('images/car.png')
        # Resim, x ve y parametrelerini geçer. 
        super().__init__(resim, x, y)
        
# hayalet grup
oyuncu_grubu = pygame.sprite.Group()  # Oyuncunun araç sprite'larını içeren grup.
arac_grubu = pygame.sprite.Group() # Oyundaki diğer araçların sprite'larını içeren grup.


# Oyuncu arabasını oluştur
oyuncu = OyuncuAraci(oyuncu_x, oyuncu_y) # Aracın başlangıç pozisyonunu belirler.
oyuncu_grubu.add(oyuncu) # Bu, oyuncunun aracının sprite grubu içinde yönetilmesini sağlar
 
# Araç görsellerini yükleme
resim_dosya_adlari = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
arac_resimleri = [] # Görselleri saklamak için
for resim_dosya_adi in resim_dosya_adlari: # Her bir dosya adını iteratif olarak işler.
    resim = pygame.image.load('images/' + resim_dosya_adi) # belirtilen dosya yolundan bir görsel yükler.
    arac_resimleri.append(resim) # Yüklenen her görsel arac_resimleri listesine eklenir.
    
# Çarpışma görüntüsünü yükleme
carpisma = pygame.image.load('images/crash.png')
carpisma_rect = carpisma.get_rect() # Çarpışma görselinin dikdörtgen (rect) sınırları belirlenir. Gerekli durumlarda istenilen yerde ortaya çıkar.


# game loop
running= True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # sol/sağ ok tuşlarını kullanarak oyuncunun arabasını hareket ettirin
        if event.type == KEYDOWN:
            
            if event.key == K_LEFT and oyuncu.rect.center[0] > sol_serit:
                oyuncu.rect.x -= 100
            elif event.key == K_RIGHT and oyuncu.rect.center[0] < sag_serit:
                oyuncu.rect.x += 100
                
            # şerit değiştirdikten sonra yandan çarpışma olup olmadığını kontrol edin
            for arac in arac_grubu:
                if pygame.sprite.collide_rect(oyuncu, arac):
                    
                    oyun_bitti = True
                    
                    # oyuncunun aracını diğer aracın yanına yerleştirin
                    # ve çarpışma görüntüsünün nereye yerleştirileceğini belirleyin
                    if event.key == K_LEFT:
                        oyuncu.rect.left = arac.rect.right
                        carpisma_rect.center = [oyuncu.rect.left, (oyuncu.rect.center[1] + arac.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        oyuncu.rect.right = arac.rect.left
                        carpisma_rect.center = [oyuncu.rect.right, (oyuncu.rect.center[1] + arac.rect.center[1]) / 2]
            
            
    # çimleri çizin
    ekran.fill(yesil)
    
    # yolu çizin
    pygame.draw.rect(ekran, gri, yol)
    
    # kenar işaretleyicilerini çizin
    pygame.draw.rect(ekran, sari, sol_kenar_isareti)
    pygame.draw.rect(ekran, sari, sag_kenar_isareti)
    
    # Bu satır, şerit işaretlerinin dikey hareketini kontrol eder. 
    #Bu, işaretlerin hızını kontrol eder.
    serit_isareti_hareket_y += hiz *2
    #Şerit işaretlerinin ekranda sürekli kalmasını sağlar.
    if serit_isareti_hareket_y >= isaret_yuksekligi * 2:
        serit_isareti_hareket_y = 0
    #Şerit işaretlerinin ekrana çizilmesini sağlar.
    for y in range(isaret_yuksekligi * -2, yukseklik, isaret_yuksekligi * 2):
        pygame.draw.rect(ekran, beyaz, (orta_serit + 45, y + serit_isareti_hareket_y, isaret_genisligi, isaret_yuksekligi))
        pygame.draw.rect(ekran, beyaz, (sol_serit + 45, y + serit_isareti_hareket_y, isaret_genisligi, isaret_yuksekligi))
        
    # oyuncu_grubu içindeki spriteların çizilmesini sağlar.
    oyuncu_grubu.draw(ekran)
    
    #Eğer araba sayısı 2 veya daha azsa
    if len(arac_grubu) < 2:
        
        #araba ekleme true yapılır.
        arac_ekle = True
        #her bir araç kontrol edilir.
        for arac in arac_grubu:
            #yani araya bir tane daha gelebilir mi onu kontrol eder.
            if arac.rect.top < arac.rect.height * 1.5:
                arac_ekle = False
                
        if arac_ekle:
            
            #random şerit seçilir.
            serit = random.choice(seritler)
            
            # random araç resmi seçilir.
            resim = random.choice(arac_resimleri)
            #yeni bir araç nesnesi oluşturulur.
            arac = Arac(resim, serit, yukseklik / -2)
            #gruba ekler.
            arac_grubu.add(arac)
    
    # her bir araç kontrol edilir.
    for arac in arac_grubu:
        #dikey pozisyon hiz kadar arttırılır.Arabanın ekranın altına doğru hareketini sağlar.
        arac.rect.y += hiz
        
        # Eger araba ekrandan çıktı ise 
        if arac.rect.top >= yukseklik:
            #arabayı gruptan kaldır
            arac.kill()
            
            # skoru 1 arttır.
            skor += 1
            
            #skor sıfırdan büyük ve 5 araba geçtiyse hızlandırma yapar.
            if skor > 0 and skor % 5 == 0:
                hiz += 1
    
    # araçların çizilmesini sağlar.
    arac_grubu.draw(ekran)
    en_iyi_skor = max(skor, en_iyi_skor)  # En yüksek skoru güncelle
    #Best skor yazısı ve ekrana yazdırması
    font = pygame.font.Font(pygame.font.get_default_font(), 14)
    en_iyi_skor_metni = font.render('En İyi Skor: ' + str(en_iyi_skor), True, beyaz)
    en_iyi_skor_rect = en_iyi_skor_metni.get_rect()
    en_iyi_skor_rect.center = (50, 360)
    ekran.blit(en_iyi_skor_metni, en_iyi_skor_rect)
    
    # skorun gösterilmesi
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    metin = font.render('Skor: ' + str(skor), True, beyaz)
    metin_rect = metin.get_rect()
    metin_rect.center = (50, 400)
    ekran.blit(metin, metin_rect)
    
    # bir oyuncu ile bir aracın çarpışıp çarpışmadığını kontrol eder.True seçildiği için gruptan kaldırılırlar.
    if pygame.sprite.spritecollide(oyuncu, arac_grubu, True):
        oyun_bitti = True
        #kazanın konumunu sağlar.
        carpisma_rect.center = [oyuncu.rect.center[0], oyuncu.rect.top]
            
    # display game over
    if oyun_bitti:
        #carpisma görselini carpisma_rect konumuna çizer.
        ekran.blit(carpisma, carpisma_rect)
        #çizimin büyüklüğü
        pygame.draw.rect(ekran, kirmizi, (0, 50, genislik, 100))
        #Ekranda oyun bittikten sonraki yazım gösterimi
        font = pygame.font.Font(pygame.font.get_default_font(), 15)
        metin = font.render('Oyun bitti. Tekrar oynamak ister misin? (Y veya N tuşuna basınız.)', True, beyaz)
        metin_rect = metin.get_rect()
        metin_rect.center = (genislik / 2, 100)
        ekran.blit(metin, metin_rect)
            
    #yapılan değişiklikler güncellenir.    
    pygame.display.update()

    # kullanıcıdan bildirim bekleniyor.
    while oyun_bitti:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            #Eğer çıkışa basarsa false yap oyunu kapat.
            if event.type == QUIT:
                oyun_bitti = False
                running = False
                
            # eğer kullanıcı y veya n tuşuna basarsa
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # oyunu resetler.
                    oyun_bitti = False
                    hiz = 2
                    skor = 0
                    arac_grubu.empty()
                    #oyuncunun başlangıç pozisyonu getirilir.
                    oyuncu.rect.center = [oyuncu_x, oyuncu_y]
                elif event.key == K_n:
                    #oyunu kapat.
                    oyun_bitti = False
                    running = False

pygame.quit()
