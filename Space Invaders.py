from pygame_functions import *
import pygame
import time
import random
import sqlite3

#create a database
conn = sqlite3.connect("Highscore_Database.db")

#create a cursor
c = conn.cursor()

#create a table to store the highscores
c.execute("create table if not exists highscore_table (Player_Name text, Score int)")

#function to insert data into the database
def insert_data(player_name , score): 
    with conn:
        c.execute("insert into highscore_table values(?,?)",(player_name , score))

#function to retrive data from the database
def get_data(): 
    c.execute("select * from highscore_table order by score desc limit 10")
    return c.fetchall()


#set the screensize 
screenSize(800,600)

#create a window
window  = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders by moveForward")

#load a background image
background = pygame.image.load("background.png")
#display the background image on the window
window.blit(background,(0,0))

#display heading
heading_font = pygame.font.SysFont("cooperblack",64)
heading_text = heading_font.render("SPACE INVADERS",True, (255, 255, 255)) 
window.blit(heading_text, (120,120))

#display tag
tag_font = pygame.font.SysFont("cooperblack",24)
tag_text = tag_font.render("By moveForward",False, (255, 92, 51)) 
window.blit(tag_text, (500,200))

#input player name
input_field = makeTextBox(250,330,320,0,"Enter player name", 15, 34)
#def makeTextBox(xpos, ypos, width, case=0, startingText="Please type here", maxLength=0, fontSize=22):
showTextBox(input_field)
player_name = textBoxInput(input_field)
#if player gives an empty input
if player_name == "":
    player_name = "Guest"

#background sound
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1) #-1 will play the music in an infinite loop

#create spaceship
spaceship_image = pygame.image.load("spaceship.png")
spaceship_xcor = 370
spaceship_ycor = 480
spaceship_xcor_change = 0 #horizontal animation of spaceship
spaceship_ycor_change = 0 #vertical animation of spaceship

#create a bullet
bullet_image = pygame.image.load("bullet.png")
bullet_xcor = spaceship_xcor
bullet_ycor = spaceship_ycor
bullet_ycor_change = 10 #vertical animation of the bullet
bullet_state = "ready"  #current state of the bullet

#create lists to store and track aliens
alien_list = []        #list to store the aliens
alien_xcor = []        #list to store X-coordinate of aliens
alien_ycor = []        #list to store Y-coordinate of aliens
alien_xcor_change = [] #list to store horizontal animation of aliens
alien_ycor_change = [] #list to store vertical animation of aliens
number_of_aliens = 8  #total number of aliens in the game
alien_image_list =  ["alien_one.png","alien_two.png","alien_three.png"] #list to store the image names

#create emenies and store them in the lists
for i in range(number_of_aliens):
    random_image = random.choice(alien_image_list)  #choose a random alien image
    load_image = pygame.image.load(random_image)    #load the random alien image
    random_xcor = random.randint(0,736)             #set random X-coordinate
    random_ycor = random.randint(50,150)            #set random Y-coordinate

    #store everything in the lists created
    alien_list.append(load_image)                          
    alien_xcor.append(random_xcor)
    alien_ycor.append(random_ycor)
    alien_xcor_change.append(8)
    alien_ycor_change.append(40)
    
#variable to store the game score
game_score = 0






#function to display the score
def display_score():
    #create a score board
    scoreboard_font = pygame.font.SysFont("cooperblack", 32)
    scoreboard = scoreboard_font.render("{}'s Score : {}".format(player_name,game_score), True, (255, 255, 255))
    window.blit(scoreboard , (10 , 10))


def display_highscore():
    global player_name
    #current Y-coordinate of the line
    line_ycor = 180

    #insert game score into the database
    insert_data(player_name , game_score)

    #retrieve the top 10 scores from the database
    highscores = get_data()

    #create a highscore board
    highscore_title_font = pygame.font.SysFont("cooperblack", 54)
    highscore_font = pygame.font.SysFont("cooperblack", 32)
    highscore_title = highscore_title_font.render("High Scores", True, (255, 92, 51))
    window.blit(highscore_title, (240,80))

    #display the top 10 highscores
    for i in highscores:
        name = i[0]
        score = i[1]
        display_highscore = highscore_font.render("{}" .format(name),True,(255,255,255))          
        window.blit(display_highscore, (200, line_ycor))
        display_highscore = highscore_font.render("{}" .format(score),True,(255,255,255))
        window.blit(display_highscore, (550, line_ycor))
        
        #move to the next line
        line_ycor = line_ycor + 30

#function to detect the events and handle them
def handle_events():
    global game_running , spaceship_xcor_change , spaceship_ycor_change , bullet_xcor , bullet_ycor , bullet_state
    global spaceship_xcor , spaceship_ycor
    
    #loop through all the pygame events
    for event in pygame.event.get():
        #if the player clicks on the 'X' button
        if event.type == pygame.QUIT:
            game_running = False #stop the game
            pygame.quit()        #close the window
            break                #break out of the loop

        #if any key on the keyboard is pressed
        if event.type == pygame.KEYDOWN:
            #if Esc key is pressed
            if event.key ==  pygame.K_ESCAPE:
                game_running = False #stop the game
                pygame.quit()        #close the window
                break                #break out of the loop
            
            #if right arrow key is pressed
            if event.key ==  pygame.K_RIGHT:
                spaceship_xcor_change = 5 
            #if left arrow key is pressed
            if event.key ==  pygame.K_LEFT:
                spaceship_xcor_change = -5 
            #if up arrow key is pressed
            if event.key ==  pygame.K_UP:
                spaceship_ycor_change = -5 
            #if down arrow key is pressed
            if event.key ==  pygame.K_DOWN:
                spaceship_ycor_change = 5 

            #if spacebar is pressed
            if event.key == pygame.K_SPACE:

                #if the bullet is in 'ready' state
                if bullet_state == "ready":
                    #play the bullet fired sound
                    bullet_sound = pygame.mixer.Sound("laser.wav")
                    bullet_sound.play()

                    #position the bullet behind the spaceship
                    bullet_xcor = spaceship_xcor
                    bullet_ycor = spaceship_ycor

                    #fire the bullet
                    bullet_state = "fire"
                    window.blit(bullet_image, (bullet_xcor+16,bullet_ycor+10))

        #if any key is released
        if event.type == pygame.KEYUP:
            #if the left or right arrow key has been released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship_xcor_change = 0
            #if the up or down arrow key has been released
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                spaceship_ycor_change = 0

#function to move the spaceship
def spaceship_animation():
    global spaceship_xcor_change , spaceship_ycor_change ,spaceship_xcor , spaceship_ycor
    
    #update the spacechip position
    spaceship_xcor = spaceship_xcor + spaceship_xcor_change
    spaceship_ycor = spaceship_ycor + spaceship_ycor_change

    #prevent spaceship from leaving the screen
    
    #check left border
    if spaceship_xcor <= 0:
        spaceship_xcor = 0
    #check right border
    elif spaceship_xcor >= 736:
        spaceship_xcor = 736
    #check top border
    elif spaceship_ycor <= 0:
        spaceship_ycor = 0
    #check bottom border
    elif spaceship_ycor >= 536:
        spaceship_ycor = 536

    window.blit(spaceship_image, (spaceship_xcor, spaceship_ycor))

#function to check collision with alien    
def check_collision(xcor , ycor , size , i):
    
    #center of an element
    center = size/2

    #coordinates of center of the element  
    center_xcor = xcor + center
    center_ycor = ycor + center

    #coordinates of center of the alien
    alien_center_xcor = alien_xcor[i] + 32
    alien_center_ycor = alien_ycor[i] + 32
            

    #if the distance between the centers is less than 32, collision occurred      
    if abs(center_xcor - alien_center_xcor) < 32 and abs(center_ycor - alien_center_ycor) < 32 :
        return True
    else:
        return False 



#function to check if game is over
def check_game_over():
    global spaceship_ycor , spaceship_xcor ,game_running

    #for all the aliens
    for i in range(number_of_aliens):

        #check if spacship hit the alien
        spaceship_collision = check_collision(spaceship_xcor , spaceship_ycor ,64 ,i)

        #if alien touched the bottom or the spacehsip
        if alien_ycor[i] > 400 or spaceship_collision == True:
                
            #clear all the enemeies
            for j in range(number_of_aliens):
                alien_xcor[j] = 2000
                alien_ycor[j] = 2000
 
            #play game over music
            pygame.mixer.music.pause()
            gameoverSound = pygame.mixer.Sound("GameOver.wav")
            gameoverSound.play()

            #display the highscores
            display_highscore()

            game_running = False        #stop the game
            break                       #break out of loop

#function to move the aliens
def alien_animation():
    global game_running , spaceship_xcor_change , spaceship_ycor_change , bullet_xcor , bullet_ycor , bullet_state
    global spaceship_xcor , spaceship_ycor ,game_score

    #for all the aliens
    for i in range(number_of_aliens):

        #check if any alien touches the spaceship
        alien_xcor[i] = alien_xcor[i] + alien_xcor_change[i]

        #if an alien leaves the boundary, position it back inside
        if alien_xcor[i] <= 0  or alien_xcor[i] >= 736 :
            alien_xcor_change[i] = alien_xcor_change[i] * -1
            alien_ycor[i] = alien_ycor[i] + alien_ycor_change[i]
        #elif alien_xcor[i] >= 736 :
            #alien_xcor_change[i] = -8
            #alien_ycor[i] = alien_ycor[i] + alien_ycor_change[i]
    
        #check if bullet hit an alien
        bullet_collision = check_collision(bullet_xcor , bullet_ycor ,40 ,i)

        #if a bullet hit an alien
        if bullet_collision == True:
            #play explosion sound
            explosion_sound = pygame.mixer.Sound("explosion.wav")
            explosion_sound.play()           

            #reset the bullet position
            bullet_ycor = spaceship_ycor
            bullet_xcor = spaceship_xcor
            bullet_state = "ready"

            #update the score
            game_score = game_score + 1

            #respwan the alien to a new position
            alien_xcor[i] = random.randint(0, 736)
            alien_ycor[i] = random.randint(50, 150)

        window.blit(alien_list[i], (alien_xcor[i], alien_ycor[i]))

#function to move the bullet
def bullet_animation():
    global bullet_ycor , bullet_state
    
    #if bullet leaves the screen
    if bullet_ycor <=0 :
        bullet_ycor = spaceship_ycor
        bullet_state = "ready" 

    #if bullet is fired
    if bullet_state == "fire":
        window.blit(bullet_image,  (bullet_xcor + 16, bullet_ycor + 10))
        #shoot the bullet
        bullet_ycor = bullet_ycor - bullet_ycor_change

game_exit = False 
game_running = True

#main game loop
while game_running:

    #display the background image
    window.blit(background, (0,0))
    
    #check events
    handle_events()

    #exit game
    if game_running == False:
        game_exit = True
        break

    #spaceship movement
    spaceship_animation()

    #check if game is
    
    check_game_over()

    #alien movement
    alien_animation()

    #bullet movement
    bullet_animation()

    #display the score
    display_score()

    #refresh the window
    pygame.display.update()


#wait for a mouse click to exit the game
while game_exit == False:
    event = pygame.event.wait()
    
    #if mouse button is pressed
    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.quit()       #close the window
        game_exit = True    #exit the game

