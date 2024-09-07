import pygame
class Fighter():
    
    
    
#Sınıfın yapıcı metodudur ve bir Fighter nesnesi oluşturur.
#Parametrelerle gelen bilgileri kullanarak karakterin başlangıç durumunu ve özelliklerini ayarlar.
#Karakterin animasyonlarını yükler, başlangıç pozisyonunu ve boyutunu belirler, çeşitli durum bayraklarını (koşma, zıplama, saldırma vb.) ve saldırı sesini ayarlar.
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player  # Oyuncu numarasını saklar (1 veya 2 gibi)
        self.size = data[0]  # Karakterin boyutunu belirler
        self.image_scale = data[1]  # Karakterin ölçeklendirme faktörü
        self.offset = data[2]  # Karakterin görüntü ofseti (kayması)
        self.flip = flip  # Karakterin görüntüsünün yatayda çevrilip çevrilmeyeceğini belirler
        self.animation_list = self.load_images(sprite_sheet, animation_steps)  # Animasyonları yükler
        self.action = 0  # Mevcut eylemi belirtir (0: boştayken, 1: koşarken, 2: zıplarken, vb.)
        self.frame_index = 0  # Mevcut animasyon karesinin indeksini saklar
        self.image = self.animation_list[self.action][self.frame_index]  # Mevcut görüntüyü belirler
        self.update_time = pygame.time.get_ticks()  # Son güncelleme zamanını saklar
        self.rect = pygame.Rect((x, y, 80, 180))  # Karakterin dikdörtgenini oluşturur (konum ve boyut)
        self.vel_y = 0  # Dikey hızını saklar (zıplama ve yerçekimi için)
        self.running = False  # Koşma durumunu saklar
        self.jump = False  # Zıplama durumunu saklar
        self.attacking = False  # Saldırı durumunu saklar
        self.attack_type = 0  # Saldırı türünü belirler (0: saldırı yok, 1: saldırı 1, 2: saldırı 2)
        self.attack_cooldown = 0  # Saldırı bekleme süresini saklar
        self.attack_sound = sound  # Saldırı sesini saklar
        self.hit = False  # Karakterin vurulup vurulmadığını belirler
        self.health = 100  # Karakterin sağlık puanını saklar
        self.alive = True  # Karakterin hayatta olup olmadığını belirler







#Sprite sheet'ten animasyon karelerini çıkarır ve ölçeklendirir.
#Her animasyon adımı için bir dizi oluşturur ve bu diziyi animation_list adlı ana listeye ekler.
#Animasyon listelerini döndürerek karakterin animasyonlarını oluşturur.
  def load_images(self, sprite_sheet, animation_steps): # model sayfasından görselleri çıkarma
        animation_list = []  # Animasyon listesi oluşturuluyor
        for y, animation in enumerate(animation_steps):  # Her animasyon adımı için döngü
            temp_img_list = []  # Geçici resim listesi
            for x in range(animation):  # Her adımın kareleri için döngü
                # Sprite sheet'ten belirli bir kareyi çıkar
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                # Görüntüyü ölçeklendir ve geçici listeye ekle
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            # Geçici resim listesini animasyon listesine ekle
            animation_list.append(temp_img_list)
        return animation_list  # Animasyon listesini döndür






#Karakterin hareketini ve etkileşimlerini yönetir.
#Klavye girdilerini okuyarak karakterin hareketini, zıplamasını ve saldırmasını kontrol eder.
#Yerçekimini uygular, karakterin ekran sınırlarını aşmasını engeller ve diğer karakterle yüz yüze gelmesini sağlar.
#Saldırı bekleme süresini yönetir ve karakterin pozisyonunu günceller.
  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    
    key = pygame.key.get_pressed()#tuşlara basmak

    #yalnızca şu anda saldırmıyorsa diğer eylemleri gerçekleştirebilir
    if self.attacking == False and self.alive == True and round_over == False:
      #Oyuncu 1 kontrollerini kontrol edin
      if self.player == 1:
        #hareket
        if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_d]:
          dx = SPEED
          self.running = True
        #zıplamak
        if key[pygame.K_w] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #saldırı
        if key[pygame.K_r] or key[pygame.K_t]:
          self.attack(target)
          #Hangi saldırı türünün kullanıldığını belirleyin
          if key[pygame.K_r]:
            self.attack_type = 1
          if key[pygame.K_t]:
            self.attack_type = 2
        if key[pygame.K_q]:
          self.flip = True
        if key[pygame.K_e]:
            self.flip = False
        #saldırı


      #oyuncu 2 kontrollerini kontrol edin
      if self.player == 2:
        #hareket
        if key[pygame.K_LEFT]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT]:
          dx = SPEED
          self.running = True
        #zıplamak
        if key[pygame.K_UP] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #saldırı
        if key[pygame.K_KP1] or key[pygame.K_KP2]:
          self.attack(target)
          #Hangi saldırı türünün kullanıldığını belirleyin
          if key[pygame.K_KP1]:
            self.attack_type = 1
          if key[pygame.K_KP2]:
            self.attack_type = 2
        if key[pygame.K_KP4]:
           self.flip = True
        if key[pygame.K_KP5]:
             self.flip = False

    #yer çekimini uygula
    self.vel_y += GRAVITY
    dy += self.vel_y

    #oyuncunun ekranda kalmasını sağlayın
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #oyuncuların birbirleriyle yüzleşmesini sağlayın
    #if target.rect.centerx > self.rect.centerx:
     # self.flip = False
    #else:
     # self.flip = True

    #saldırı bekleme süresini uygula
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #Oyuncu pozisyonunu güncelle
    self.rect.x += dx
    self.rect.y += dy





#animasyon güncellemelerini yönetin
#Karakterin mevcut durumunu ve animasyonlarını günceller.
#Karakterin sağlık durumu, vurulma durumu, saldırı durumu, zıplama ve koşma gibi eylemleri kontrol eder ve buna göre animasyonları ayarlar.
#Animasyon karesini ve güncelleme zamanını yönetir.
#Animasyonun bitip bitmediğini kontrol eder ve gerekli durum bayraklarını sıfırlar.
  def update(self):
    #oyuncunun hangi eylemi gerçekleştirdiğini kontrol edin
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:ölüm
    elif self.hit == True:
      self.update_action(5)#5:vurmak
    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(3)#3:saldırı1
      elif self.attack_type == 2:
        self.update_action(4)#4:saldırı2
    elif self.jump == True:
      self.update_action(2)#2:zıplamak
    elif self.running == True:
      self.update_action(1)#1:koşmak
    else:
      self.update_action(0)#0:Boşta

    animation_cooldown = 50
    #resmi güncelle
    self.image = self.animation_list[self.action][self.frame_index]
    
    #son güncellemeden bu yana yeterli zaman geçip geçmediğini kontrol edin
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
      
      
    #animasyonun bitip bitmediğini kontrol edin
    if self.frame_index >= len(self.animation_list[self.action]):
      #eğer oyuncu öldüyse animasyonu sonlandırın
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #bir saldırının gerçekleştirilip gerçekleştirilmediğini kontrol edin
        if self.action == 3 or self.action == 4:
          self.attacking = False
          self.attack_cooldown = 20
        #hasar alınıp alınmadığını kontrol edin
        if self.action == 5:
          self.hit = False
          #Oyuncu bir saldırının ortasındaysa saldırı durdurulur
          self.attacking = False
          self.attack_cooldown = 20
  
 

       
#Karakterin saldırı gerçekleştirmesini sağlar.
#Saldırı bekleme süresi 0 ise saldırı durumunu aktif hale getirir ve saldırı sesini oynatır.
#Saldırı dikdörtgenini oluşturur ve bu dikdörtgenin hedefle çakışıp çakışmadığını kontrol eder.
#Çakışma durumunda hedefin sağlığını azaltır ve hedefin vurulma durumunu aktif hale getirir.
  def attack(self, target):
    if self.attack_cooldown == 0:  # Saldırı bekleme süresi 0 ise saldırıya izin ver
        # Saldırıyı gerçekleştir
        self.attacking = True  # Saldırı durumunu aktif hale getir
        self.attack_sound.play()  # Saldırı sesini oynat
        # Saldırı dikdörtgenini oluştur
        attacking_rect = pygame.Rect(
            self.rect.centerx - (2 * self.rect.width * self.flip),  # Saldırı yönüne göre merkezden ofset
            self.rect.y,  # Karakterin dikey konumu
            2 * self.rect.width,  # Saldırı dikdörtgeninin genişliği (karakterin genişliğinin 2 katı)
            self.rect.height  # Saldırı dikdörtgeninin yüksekliği
        )
        # Saldırı dikdörtgeninin hedefle çakışıp çakışmadığını kontrol edin
        if attacking_rect.colliderect(target.rect):
            target.health -= 10  # Hedefin sağlığını 10 azalt
            target.hit = True  # Hedefin vurulma durumunu aktif hale getir




#Karakterin mevcut eylemini değiştirir.
#Yeni eylem mevcut olandan farklıysa animasyonu sıfırlar ve son güncelleme zamanını yeniler.
#Bu sayede eylem değişikliğinde animasyonun doğru bir şekilde sıfırlanmasını sağlar            
  def update_action(self, new_action):
    # Yeni eylemin öncekinden farklı olup olmadığını kontrol edin
    if new_action != self.action:
        self.action = new_action  # Yeni eylemi ayarla
        # Animasyon ayarlarını güncelle
        self.frame_index = 0  # Animasyonun ilk karesine geri dön
        self.update_time = pygame.time.get_ticks()  # Son güncelleme zamanını şimdiki zaman olarak ayarla



#Karakterin görüntüsünü ekrana çizer.
#Görüntüyü yatayda çevirir (flip) ve doğru konumda ekrana yerleştirir.
#Karakterin ekrandaki görünümünü sağlar.
  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
    
    
    
    
    
    
    