from turtle import width
from xml.dom.minidom import Identified
import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

window = pygame.display.set_mode((900,500))
pygame.display.set_caption("My game")
black = (0,0,0)
white = (255,255,255)
width = 900
height = 500
Border = pygame.Rect(900//2-5, 0,10, 500)
spacesgip_width, spaceship_height = 55,40
spaceship_red_png = pygame.image.load(os.path.join("spaceship_red.png"))
spaceship_red= pygame.transform.rotate(pygame.transform.scale(spaceship_red_png,(spacesgip_width, spaceship_height)),270)
spaceship_yellow_png = pygame.image.load(os.path.join("spaceship_yellow.png"))
spaceship_yellow= pygame.transform.rotate(pygame.transform.scale(spaceship_yellow_png,(spacesgip_width, spaceship_height)),90)
background = pygame.transform.scale(pygame.image.load(os.path.join("space.png")), (width, height))
FPS = 60
Bullet_vel =7
Max_bullets = 5
vel=5
Health_font = pygame.font.SysFont( "Arial",30, True)
winner_font = pygame.font.SysFont("Comicsans", 100, True)
red_hit = pygame.USEREVENT +1
yellow_hit = pygame.USEREVENT +2

Bullet_hit_sound = pygame.mixer.Sound(os.path.join("Game_hit.mp3") )
Bullet_fire_sound = pygame.mixer.Sound(os.path.join("Game_bullet.mp3"))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health ):
  window.blit(background, (0,0))
  pygame.draw.rect(window, white, Border)

  red_health_text = Health_font.render("Health: " + str(red_health), 1,(255,255,255))
  yellow_health_text= Health_font.render("Health: " + str(yellow_health), 1 , (255,255,255))
  window.blit(red_health_text, (width- red_health_text.get_width()-20,10))
  window.blit(yellow_health_text, (20,10))
  window.blit(spaceship_red, (red.x, red.y))
  window.blit(spaceship_yellow,(yellow.x, yellow.y))

  for bullet in red_bullets:
    pygame.draw.rect(window, (0,255,0), bullet)
  for bullet in yellow_bullets:
    pygame.draw.rect(window, (0,255,0), bullet)
  pygame.display.update()

def yellow_move (key,yellow):
    if key[pygame.K_LEFT] and yellow.x - vel > Border.x + Border.width:
      yellow.x -=vel
    if key[pygame.K_RIGHT] and yellow.x + vel + yellow.width < width :
      yellow.x +=vel
    if key[pygame.K_UP] and yellow.y - vel>0:
      yellow.y -= vel
    if key[pygame.K_DOWN] and yellow.y + vel + yellow.height< height -13:
      yellow.y +=vel

def red_move (key,red):
    if key[pygame.K_a] and red.x -vel>0:
      red.x -=vel
    if key[pygame.K_d] and red.x +vel+ red.width < Border.x:
      red.x +=vel
    if key[pygame.K_w] and red.y -vel >0:
      red.y -= vel
    if key[pygame.K_s] and red.y +vel +red.height < 500 -13:
      red.y +=vel

def bullets_collision(yellow_bullets, red_bullets, yellow, red):
  for bullet in yellow_bullets:
    bullet.x -= Bullet_vel
    if red.colliderect(bullet):
      pygame.event.post(pygame.event.Event(red_hit))
      yellow_bullets.remove(bullet)
    elif bullet.x < 0:
      yellow_bullets.remove(bullet)
    
  for bullet in red_bullets:
    bullet.x += Bullet_vel
    if yellow.colliderect(bullet):
      pygame.event.post(pygame.event.Event(yellow_hit))
      red_bullets.remove(bullet)
    elif bullet.x > width:
      red_bullets.remove(bullet)

def draw_winner(text):
  draw_text =winner_font.render(text,1, white)
  window.blit(draw_text, (width //2 - draw_text.get_width()//2, height//2 - draw_text.get_height()//2))
  pygame.display.update()
  pygame.time.delay(1000)
def main():
  red= pygame.Rect(100,300,spacesgip_width,spaceship_height)
  yellow = pygame.Rect(700,300,spacesgip_width,spaceship_height)
  yellow_bullets =[]
  red_bullets =[]
  red_health =10
  yellow_health = 10
  Clock= pygame.time.Clock()
  run = True
  while run:
    Clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LCTRL and len(red_bullets) < Max_bullets:
          bullet = pygame.Rect(red.x + red.width, red.y+ red.height//2- 2, 30, 5)
          red_bullets.append(bullet)
          Bullet_fire_sound.play()

        if event.key == pygame.K_RCTRL and len(yellow_bullets) < Max_bullets:  
          bullet= pygame.Rect(yellow.x, yellow.y + yellow.height//2 -2, 30,5)
          yellow_bullets.append(bullet)
          Bullet_fire_sound.play()
      if event.type == red_hit:
        yellow_health -=1
        Bullet_hit_sound.play()
      if event.type == yellow_hit:
        red_health -=1
        Bullet_hit_sound.play()

    winner_text = ""
    if red_health <=0:
      winner_text = "yellow wins!"
    if yellow_health <=0:
      winner_text = "red wins!"
    if winner_text != "":
      draw_winner(winner_text)
      break

    key = pygame.key.get_pressed()
    yellow_move (key, yellow)
    red_move (key,red)
    draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    bullets_collision(yellow_bullets, red_bullets, yellow, red)

  main()

if __name__ == "__main__":
  main()