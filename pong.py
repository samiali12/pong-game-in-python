import pygame 
import random

def move_ball():

    global b, ball_xspeed, ball_yspeed, player_score,opponent_score , score_timer
    
    b.x += ball_xspeed
    b.y += ball_yspeed

    if b.top <= 0 or b.bottom >= SCREEN_HEIGHT-10:
        ball_yspeed *= - 1

    if b.left <= 0:
        opponent_score +=1
        pygame.mixer.Sound.play(sound)

        score_timer = pygame.time.get_ticks()
        ball_restart()

    if b.right >= SCREEN_WIDTH:
        player_score += 1
        pygame.mixer.Sound.play(sound)
        score_timer = pygame.time.get_ticks()
        ball_restart()

    if b.colliderect(player) or b.colliderect(opponent):
        ball_xspeed *= -1
        pygame.mixer.Sound.play(score_sound)

def player_move():

    if player.top <= 16:
        player.top = 16

    if player.bottom >= SCREEN_HEIGHT-20:
        player.bottom = SCREEN_HEIGHT-20

def opponent_move():

    if opponent.top < b.y:
        opponent.top += opponenet_speed

    if opponent.bottom > b.y:
        opponent.bottom -= opponenet_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom -= opponenet_speed

def ball_restart():

    global ball_xspeed, ball_yspeed, score_timer

    current_time = pygame.time.get_ticks()
    b.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    
    if (current_time - score_timer)  < 2100:
        ball_xspeed , ball_yspeed = 0 , 0

    else:  
        ball_yspeed = 7 * random.choice((1,-1))
        ball_xspeed = 7 * random.choice((1,-1))
        score_timer = 0



pygame.init() # INITIALIZE THE MODULES OF PYGAME
pygame.mixer.pre_init(44100,-16,2,512)


# game color 
BLACK = (  0,   0,   0)
WHITE = ( 255, 255, 255)
BLUE =  (  0,   0,  255)
GREEN = (  0,  255,  0)
RED =   ( 255,  0,   0)

# screen height and width 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

FPS = 30 # frame rate per second 

# game player and ball variable 
ball_xspeed = 7
ball_yspeed = 7
player_speed = 0
opponenet_speed = 6

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # SET SCREEN WIDTH AND HEIGHT
pygame.display.set_caption("Pong Game") # Set the screen caption of our game video

clock = pygame.time.Clock()

b = pygame.draw.rect(screen, (211,211,211),[SCREEN_WIDTH//2,SCREEN_HEIGHT//2,20,20] )
player = pygame.draw.rect(screen, BLUE,[0,SCREEN_HEIGHT//2,20,100] )
opponent = pygame.draw.rect(screen, BLUE,[SCREEN_WIDTH-20,(SCREEN_HEIGHT)//2, 20,100] )

net = pygame.draw.line(screen, WHITE, [SCREEN_WIDTH//2,5], [SCREEN_WIDTH//2, SCREEN_HEIGHT-10], 2)
        
# game text 
player_score = 0
opponent_score = 0

font = pygame.font.Font(r"SourceSansPro-Regular.ttf",30)
game_end_font = pygame.font.Font(r"SourceSansPro-Regular.ttf",20)

# score timer
score_timer = None

# game sound effect

sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

game_end = False

while not game_end:

    for event in pygame.event.get():

        if event.type  == pygame.QUIT:
            
            game_end = True 

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_speed += 7

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_speed -= 7
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_speed -= 7

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_speed += 7

            if event.key == pygame.K_RETURN:
                ball_yspeed = 7 * random.choice((1,-1))
                ball_xspeed = 7 * random.choice((1,-1))
                player_score = 0
                opponent_score = 0
        
        

    if score_timer:
        ball_restart()
    

    player.top += player_speed

    screen.fill(BLACK)

    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, BLUE, opponent)
    pygame.draw.rect(screen, WHITE, net )
    pygame.draw.ellipse(screen, WHITE, b)
    
    move_ball()
    
    player_move()
    opponent_move()

    if player_score >= 1 and opponent_score < 11:
        player_score_text = font.render(f"Player Won",False,BLUE)
        screen.blit(player_score_text, ((SCREEN_WIDTH//3)//2,100))
        ball_xspeed , ball_yspeed = 0, 0

        player = pygame.draw.rect(screen, BLUE,[0,SCREEN_HEIGHT//2,20,100] )
        opponent = pygame.draw.rect(screen, BLUE,[SCREEN_WIDTH-20,(SCREEN_HEIGHT)//2, 20,100] )

        # check if user want play again
        game_end_message = game_end_font.render(f"Press Enter to play again",False,WHITE)
        screen.blit(game_end_message, ((SCREEN_WIDTH//3)//2-30,200))
        


    if opponent_score >= 11 and player_score < 11:
        opponent_score_text = font.render(f"Opponent Won",False,RED)
        screen.blit(opponent_score_text, ((SCREEN_WIDTH-(SCREEN_WIDTH//2))+((SCREEN_WIDTH)//2)//2-90,100))
        ball_xspeed , ball_yspeed = 0, 0

        game_end_message = game_end_font.render(f"Press Enter to play again",False,WHITE)
        screen.blit(game_end_message, ((SCREEN_WIDTH-(SCREEN_WIDTH//2))+((SCREEN_WIDTH)//2)//2-90,200))

        player = pygame.draw.rect(screen, BLUE,[0,SCREEN_HEIGHT//2,20,100] )
        opponent = pygame.draw.rect(screen, BLUE,[SCREEN_WIDTH-20,(SCREEN_HEIGHT)//2, 20,100] )

    player_score_text = font.render(f"{player_score}",False,BLUE)
    screen.blit(player_score_text, ((SCREEN_WIDTH//2)//2,30))
    opponent_text = font.render(f"{opponent_score}",False,RED)
    screen.blit(opponent_text, ((SCREEN_WIDTH-(SCREEN_WIDTH//2))+((SCREEN_WIDTH)//2)//2,30))

    pygame.display.update()
    clock.tick(60)