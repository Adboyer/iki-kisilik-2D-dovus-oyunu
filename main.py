# -*- coding: utf-8 -*-
"""
Created on Sat May 11 23:07:15 2024

@author: AdemTrks
"""

import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#oyun penceresi oluşturma
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dövüş Oyunu")


#kare hızını ayarla
clock = pygame.time.Clock()
FPS = 60

baslangic_zamani = pygame.time.get_ticks() // 1000  # saniye cinsinden başlangıç zamanı
toplam_sure=90
 
#renkleri tanımla
KIRMIZI = (255, 0, 0)
YESIL = (0, 255, 0)
SARI = (255, 255, 0)
BEYAZ = (255, 255, 255)
TURUNCU=(255,150,0)
    

#oyun değişkenlerini tanımlayın
intro_count = 3 #baslama saniyesi
last_count_update = pygame.time.get_ticks() #son sayım guncellemesi
score = [0, 0]#oyuncu scores. [P1, P2]
round_over = False #tur bitti mi
ROUND_OVER_COOLDOWN = 2000 #bekleme süresinin sonunda 

#dövüşçü değişkenlerini tanımla
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#müzik ve sesleri yükle
pygame.mixer.music.load("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/ses/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/ses/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/ses/magic.wav")
magic_fx.set_volume(0.75)

#arka plan resmini yükle
bg_image = pygame.image.load("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/resim/background/background.jpg").convert_alpha()

#model sayfalarını yükle
warrior_sheet = pygame.image.load("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/resim/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/resim/wizard/Sprites/wizard.png").convert_alpha()

#Zafer resmini yükle
victory_img = pygame.image.load("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/resim/icons/victory.png").convert_alpha()

#her animasyondaki adım sayısını tanımlayın
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#yazı tipini tanımla
count_font = pygame.font.Font("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/fonts/turok.ttf", 80)
score_font = pygame.font.Font("C:/Users/AdemTrks/OneDrive/Masaüstü/oyun_programlama/fonts/turok.ttf", 30)

#metin çizme işlevi
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#arka plan çizme işlevi
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#Savaşçı sağlık çubuklarını çizme işlevi
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, BEYAZ, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, BEYAZ, (x, y, 400, 30))
  if health>=75:
      pygame.draw.rect(screen, YESIL, (x, y, 400 * ratio, 30))
  if health>=50 and health<=75:
      pygame.draw.rect(screen, SARI, (x, y, 400 * ratio, 30))
  if health>=25 and health<=50:
      pygame.draw.rect(screen, TURUNCU, (x, y, 400 * ratio, 30))
  if health>=0 and health<=25:
      pygame.draw.rect(screen, KIRMIZI, (x, y, 400 * ratio, 30))
      
#iki savaşçı örneği yarat
fighter_1 = Fighter(1, 270, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


def draw_start_screen():
    #screen.fill((0, 0, 0))  # Ekranı siyahla temizle
    draw_bg()
    draw_text("BASLAMAK ICIN TUSA BASINIZ", score_font, BEYAZ,320,280)  # Başlama mesajını çiz
    pygame.display.update()  # Ekranı güncelle
    
show_start_screen = True

#oyun döngüsü
run = True
while run:
    
  clock.tick(FPS)
 
  if show_start_screen:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                show_start_screen = False  # Başlangıç ekranını gizle
  
  else:
      #arka plan çizmek
      draw_bg()

      #oyuncu istatistiklerini göster
      draw_health_bar(fighter_1.health, 20, 20)
      draw_health_bar(fighter_2.health, 580, 20)
      draw_text("P1: " + str(score[0]), score_font, KIRMIZI, 20, 60)
      draw_text("P2: " + str(score[1]), score_font, KIRMIZI, 580, 60)
      
      suanki_zaman = pygame.time.get_ticks() // 1000  # saniye cinsinden geçen zaman
      gecen_sure = suanki_zaman - baslangic_zamani
      kalan_sure = max(0, toplam_sure - gecen_sure)
      font = pygame.font.SysFont(None, 55)
      text = font.render(str(kalan_sure) , True, (0, 0, 0))
      screen.blit(text, (SCREEN_WIDTH / 2 -20, 20))
      
      if kalan_sure==0:
          fontt = pygame.font.SysFont(None, 100)
          text = fontt.render('Game Over', True, (0, 0, 0))
          screen.blit(text, (300, SCREEN_HEIGHT/2 -100))
          pygame.time.delay(3000) 
          show_start_screen = True
          toplam_sure=63
          score = [0, 0]#oyuncu scores. [P1, P2]
          show_start_screen=True
          continue
       
          
      #geri sayım başlıyor
      if intro_count <= 0:
        #move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
      else:
        #ekran sayımı zamanlayıcısı
        draw_text(str(intro_count), count_font, KIRMIZI, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #güncelleme sayımı zamanlayıcısı
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
          intro_count -= 1
          last_count_update = pygame.time.get_ticks()
      
      #savaşçıları güncelle
      fighter_1.update()
      fighter_2.update()

      #savaşçıları çiz
      fighter_1.draw(screen)
      fighter_2.draw(screen)

      #Oyuncu yenilgisini kontrol et
      if round_over == False:
        if fighter_1.alive == False:
          score[1] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
          score[0] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
      else:
        #zafer resmini göster
        screen.blit(victory_img, (300, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
          round_over = False
          intro_count = 3
          fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
          fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

      #olay işleyicisi
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False


      #güncelleme ekranı
      pygame.display.update()
  

#pygame'den çık
pygame.quit()
exit()
