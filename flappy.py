'''
Flappy Bird
Created by Jason Qian, June 11th 2024
(Instructions built in the game)
Please enjoy the game!
'''
from graphics import *
import random
import threading
from time import sleep
import math
import pygame

#sounds and music
pygame.mixer.init()
click_sound=pygame.mixer.Sound ("point.wav")
fall_sound=pygame.mixer.Sound ("falling.wav")
hit_sound=pygame.mixer.Sound ("hit.wav")
flap_sound=pygame.mixer.Sound ("flap.wav")
pygame.mixer.music.load("bgmusic.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


#window creation and background
win=GraphWin("Flappy Bird", 420, 760, autoflush=False)
bg=Image(Point(210, 380), "bg.gif")
bg.draw(win)

#starting screen asking whether they want to see the about or start the game
flappy=Image(Point(210, 150), "flappytext.gif")
flappy.draw(win)
start_about=Rectangle(Point(50, 550), Point(370, 450))
start_about.setWidth(0)
start_about.setFill(color_rgb(245,54,7))
start_about.draw(win)
start_about2=Text(Point(210, 500), "ABOUT")
start_about2.setSize(36)
start_about2.setFace("times roman")
start_about2.draw(win)
start_game=Rectangle(Point(50, 300), Point(370, 400))
start_game.setWidth(0)
start_game.setFill(color_rgb(245,54,7))
start_game.draw(win)
start_game2=Text(Point(210, 350), "START")
start_game2.setSize(36)
start_game2.setFace("times roman")
start_game2.draw(win)

#find out where they clicked and if it is on 'about', open the about screen
click_pos=win.getMouse()
click_sound.play()
about_click_X=click_pos.getX()
about_click_Y=click_pos.getY()
#loop to see where the player clicks
if ((about_click_X > 370) or (about_click_X < 50)) or ((about_click_Y > 400) or (about_click_Y < 300)):
    while True:
        if ((about_click_X < 370) and (about_click_X > 50)) and ((about_click_Y < 550) and (about_click_Y > 450)):
            flappy.undraw()
            start_about.undraw()
            start_about2.undraw()
            start_game.undraw()
            start_game2.undraw()
            about_rect=Rectangle(Point(50, 660), Point(370, 100))
            about_rect.setFill(color_rgb(245,54,7))
            about_rect.setOutline("black")
            about_rect.draw(win)
            about_text=Text(Point(210, 200), "ABOUT")
            about_text.setSize(36)
            about_text.setFace("times roman")
            about_text.setTextColor(color_rgb(240,175,53))
            about_text.draw(win)
            about_text2=Text(Point(210, 300), "Created by Jason Qian")
            about_text2.setSize(25)
            about_text2.setFace("times roman")
            about_text2.setTextColor(color_rgb(240,175,53))
            about_text2.draw(win)
            about_text3=Text(Point(210, 340), "June 11th, 2024")
            about_text3.setSize(25)
            about_text3.setFace("times roman")
            about_text3.setTextColor(color_rgb(240,175,53))
            about_text3.draw(win)
            about_text4=Text(Point(210, 375), "Inspired by the real Flappy Bird")
            about_text4.setSize(20)
            about_text4.setFace("times roman")
            about_text4.setTextColor(color_rgb(240,175,53))
            about_text4.draw(win)
            start_exit=Rectangle(Point(75, 625), Point(345, 550))
            start_exit.setWidth(4)
            start_exit.setFill(color_rgb(245,54,7))
            start_exit.draw(win)
            about_back=Text(Point(210, 583), "BACK")
            about_back.setSize(36)
            about_back.setFace("times roman")
            about_back.setTextColor(color_rgb(240,175,53))
            about_back.draw(win)
            theflappy=Image(Point (210, 475), "theflappy.gif")
            theflappy.draw(win)
            click_pos=win.getMouse()
            click_sound.play()
            about_click_X=click_pos.getX()
            about_click_Y=click_pos.getY()
            while True:
                if ((about_click_X < 345) and (about_click_X > 75)) and ((about_click_Y < 625) and (about_click_Y > 550)):
                    break
                else:
                    click_pos=win.getMouse()
                    click_sound.play()
                    about_click_X=click_pos.getX()
                    about_click_Y=click_pos.getY()
            about_text.undraw()
            about_text2.undraw()
            about_text3.undraw()
            about_text4.undraw()
            theflappy.undraw()
            start_exit.undraw()
            about_back.undraw()
            about_rect.undraw()
            flappy=Image(Point(210, 150), "flappytext.gif")
            flappy.draw(win)
            start_about=Rectangle(Point(50, 550), Point(370, 450))
            start_about.setWidth(0)
            start_about.setFill(color_rgb(245,54,7))
            start_about.draw(win)
            start_about2=Text(Point(210, 500), "ABOUT")
            start_about2.setSize(36)
            start_about2.draw(win)
            start_game=Rectangle(Point(50, 300), Point(370, 400))
            start_game.setWidth(0)
            start_game.setFill(color_rgb(245,54,7))
            start_game.draw(win)
            start_game2=Text(Point(210, 350), "START")
            start_game2.setSize(36)
            start_game2.draw(win)
        #if the click is on start, break this loop to start the game
        elif ((about_click_X < 370) and (about_click_X > 50)) and ((about_click_Y < 400) and (about_click_Y > 300)):
            break
        #if the click is not on either, go again until it is
        else:
            click_pos=win.getMouse()
            click_sound.play()
            about_click_X=click_pos.getX()
            about_click_Y=click_pos.getY()
            
start_about.undraw()
start_about2.undraw()
start_game.undraw()
start_game2.undraw()


#start screen text
start_text=Text(Point(210, 650), "Press any key to continue")
start_text.setSize(36)
start_text.setFace("times roman")
start_text.setTextColor(color_rgb(245,54,7))
start_text.draw(win)


#loop for the bird that goes across the screen
theflappy=Image(Point (-50,380), "theflappy.gif")
theflappy.draw(win)
yspeedstart=300
xtimetaken=0
startdistance=0
amt=100
while win.checkKey() == "":
    time.sleep(0.01)
    theflappy.move(5, (yspeedstart/100))
    startdistance+=1
    xtimetaken+=1
    randtimestart=random.randint(5, 30)
    if xtimetaken>randtimestart:
        yspeedstart=-1000
        xtimetaken=0
        amt=100
    amt=amt*1.05
    yspeedstart=yspeedstart+amt
    update()
    while startdistance>105:
        theflappy.undraw()
  
        randwaittime=random.randint(1,200)
        time.sleep(randwaittime/100)
        theflappy=Image(Point (-50,380), "theflappy.gif")
        theflappy.draw(win)
        yspeedstart=300
        xtimetaken=0
        startdistance=0
        amt=100
        time.sleep(0.01)
        theflappy.move(5, (yspeedstart/100))
        xtimetaken+=1
        randtimestart=random.randint(5, 40)
        if xtimetaken>randtimestart:
            yspeedstart=-1000
            xtimetaken=0
            amt=100
        amt=amt*1.05
        yspeedstart=yspeedstart+amt
        startdistance=0
        update()


flappy.undraw()
start_text.undraw()
theflappy.undraw()


#first instructions screen
ins_rect=Rectangle(Point(50, 660), Point(370, 100))
ins_rect.setFill(color_rgb(245,54,7))
ins_rect.setOutline("black")
ins_rect.draw(win)
ins_text=Text(Point(210, 200), "INSTRUCTIONS")
ins_text.setSize(36)
ins_text.setFace("times roman")
ins_text.setTextColor(color_rgb(240,175,53))
ins_text.draw(win)
ins_text2=Text(Point(210, 300), "Tap space to make Flappy jump")
ins_text2.setSize(22)
ins_text2.setFace("times roman")
ins_text2.setTextColor(color_rgb(240,175,53))
ins_text2.draw(win)
ins_next=Text(Point(210,600), "Press again to continue")
ins_next.setSize(30)
ins_next.setFace("times roman")
ins_next.setTextColor(color_rgb(240,175,53))
ins_next.draw(win)

#small gif for instructions page
theflappy=Image(Point (125, 350), "theflappy.gif")
theflappy.draw(win)
yspeedstart=300
xtimetaken=0
amt=100
ok_go=0
ins_tap=Image(Point(260, 500), "tap.gif")
ins_tap.draw(win)
while win.checkKey() == "":
    time.sleep(0.01)
    theflappy.move(5, (yspeedstart/100))
    xtimetaken+=1
    update()
    if xtimetaken>10:
        yspeedstart=-1600
        xtimetaken=0
        amt=100
        ok_go=ok_go+1
    amt=amt*1.05
    yspeedstart=yspeedstart+amt 
    if ok_go>0:
        for i in range(1, 20):
            time.sleep(0.01)
            theflappy.move(5, (yspeedstart/100))
            amt=amt*1.05
            yspeedstart=yspeedstart+amt
            update()
        theflappy.undraw()
        time.sleep(0.1)
        theflappy=Image(Point (125,350), "theflappy.gif")
        theflappy.draw(win)
        yspeedstart=300
        xtimetaken=0
        amt=100
        time.sleep(0.01)
        theflappy.move(5, (yspeedstart/100))
        xtimetaken+=1
        if xtimetaken>30:
            yspeedstart=-1000
            xtimetaken=0
            amt=100
        amt=amt*1.05
        yspeedstart=yspeedstart+amt
        ok_go=ok_go-1
        update()

theflappy.undraw()
ins_tap.undraw()
ins_text2.undraw()

#second instructions screen
ins2_text=Text(Point(210, 300), "Avoid the incoming pillars")
ins2_text.setSize(25)
ins2_text.setFace("times roman")
ins2_text.setTextColor(color_rgb(240,175,53))
ins2_text.draw(win)
theflappy=Image(Point (125,350), "theflappy.gif")
theflappy.draw(win)

#second gif for the instructions screen
pillarbottom=Image(Point(300,450), "egpillar.gif")
pillarbottom.draw(win)
masterbreak=0
yspeedstart=300
xtimetaken=0
amt=100
go_on=0
ok_go=0
while win.checkKey() == "":
    time.sleep(0.01)
    theflappy.move(5, (yspeedstart/100))
    xtimetaken+=1
    if xtimetaken>10:
        yspeedstart=-1600
        xtimetaken=0
        amt=100
        ok_go=ok_go+1
    amt=amt*1.05
    yspeedstart=yspeedstart+amt
    update()
    if ok_go>0:
        for i in range(1, 20):
            if i==15:
                masterbreak+=1
                time.sleep(1)
                break
            time.sleep(0.01)
            theflappy.move(5, (yspeedstart/100))
            amt=amt*1.05
            yspeedstart=yspeedstart+amt
            update()
        if masterbreak==2:
            go_on+=1
        if go_on!=2:
            theflappy.undraw()
            time.sleep(0.1)
            theflappy=Image(Point (125,350), "theflappy.gif")
            theflappy.draw(win)
            yspeedstart=300
            xtimetaken=0
            amt=100
            time.sleep(0.01)
            theflappy.move(5, (yspeedstart/100))
            xtimetaken+=1
            if xtimetaken>30: 
                yspeedstart=-1000
                xtimetaken=0
                amt=100
            amt=amt*1.05
            yspeedstart=yspeedstart+amt
            ok_go=ok_go-1

theflappy.undraw()
pillarbottom.undraw()
ins2_text.undraw()
ins_rect.undraw()
ins_next.undraw()
ins_text.undraw()

#actual game section

ground=Image(Point(210, 700), "ground.png")
ground.draw(win)
while True:
    #includes the bird's physics, the pillars movement (with loops to generate infinitely and randomly), and collision detection
    theflappy=Image(Point (50,380), "theflappy.gif")
    theflappy.draw(win)
    rand_y=random.randint(1, 200)
    pillary=338+(rand_y-100)
    pillarx=458
    pillarb=Image(Point(pillarx, pillary+440), "pillarb.png")
    pillart=Image(Point(pillarx, pillary-440), "pillart.png")
    pillarb.draw(win)
    pillart.draw(win)
    rand_y2=random.randint(1, 200)
    pillary2=338+(rand_y2-100)
    pillarx2=458
    pillarb2=Image(Point(pillarx2+175, pillary2+440), "pillarb.png")
    pillart2=Image(Point(pillarx2+175, pillary2-440), "pillart.png")
    pillarb2.draw(win)
    pillart2.draw(win)
    rand_y3=random.randint(1, 200)
    pillary3=338+(rand_y3-100)
    pillarx3=458
    pillarb3=Image(Point(pillarx3+350, pillary3+440), "pillarb.png")
    pillart3=Image(Point(pillarx3+350, pillary3-440), "pillart.png")
    pillarb3.draw(win)
    pillart3.draw(win)
    ground=Image(Point(210, 700), "ground.png")
    ground.draw(win)
    yspeed=0
    game_amt=100
    masterbreak=True
    flappy_y=380
    count=0
    countshown=0
    start_go=Text(Point(210, 200), "Tap space to get started!")
    start_go.setSize(36)
    start_go.setFace("times roman")
    start_go.setTextColor(color_rgb(245,54,7))
    start_go.draw(win)
    win.getKey()
    start_go.undraw()  
    count_shown=  Text (Point (210,150), str (countshown))
    count_shown.setSize(36)
    count_shown.setStyle("bold")
    count_shown.setFace("times roman")
    count_shown.draw (win)
    while masterbreak==True:
        
        #flappy physics
        while win.checkKey()!="space":
            time.sleep(0.01)
            theflappy.move(0, (yspeed/100))
            game_amt=game_amt*1.05
            yspeed=yspeed+game_amt
            if theflappy.getAnchor().getY() > 607:
                masterbreak=False
                break
            #moves pillars
            pillarb.move(-5, 0)
            pillart.move(-5, 0)
            pillarb2.move(-5, 0)
            pillart2.move(-5, 0)
            pillarb3.move(-5, 0)
            pillart3.move(-5, 0)
            count_shown.undraw()
            count_shown.draw (win)
            update()
            if pillart.getAnchor().getX() <= -67:
                rand_y=random.randint(1, 300)
                pillary=338+(rand_y-100)
                pillarx=458
                pillarb=Image(Point(pillarx, pillary+440), "pillarb.png")
                pillart=Image(Point(pillarx, pillary-440), "pillart.png")
                pillarb.draw(win)
                pillart.draw(win)
                ground.undraw()
                ground.draw(win)
            if pillart2.getAnchor().getX() <= -67:
                rand_y2=random.randint(1, 300)
                pillary2=338+(rand_y2-100)
                pillarx2=458
                pillarb2=Image(Point(pillarx2, pillary2+440), "pillarb.png")
                pillart2=Image(Point(pillarx2, pillary2-440), "pillart.png")
                pillarb2.draw(win)
                pillart2.draw(win)
                ground.undraw()
                ground.draw(win)
            if pillart3.getAnchor().getX() <= -67:
                rand_y3=random.randint(1, 300)
                pillary3=338+(rand_y3-100)
                pillarx3=458
                pillarb3=Image(Point(pillarx3, pillary3+440), "pillarb.png")
                pillart3=Image(Point(pillarx3, pillary3-440), "pillart.png")
                pillarb3.draw(win)
                pillart3.draw(win)
                ground.undraw()
                ground.draw(win)
                
            #end of pillars, start of collision

            if ((theflappy.getAnchor().getX() + 31) > (pillart.getAnchor().getX() - 39)) and ((theflappy.getAnchor().getX() - 28) < (pillart.getAnchor().getX() + 39)):
                if ((theflappy.getAnchor().getY() + 22) > (pillary+74)) or ((theflappy.getAnchor().getY() - 22) < (pillary-74)):
                    masterbreak=False
                    break
            if (theflappy.getAnchor().getX() + 31) > (pillart2.getAnchor().getX() - 39) and ((theflappy.getAnchor().getX() - 28) < (pillart2.getAnchor().getX() + 39)):
                if ((theflappy.getAnchor().getY() + 22) > (pillary2+74)) or ((theflappy.getAnchor().getY() - 22) < (pillary2-74)):
                    masterbreak=False
                    break
            if (theflappy.getAnchor().getX() + 31) > (pillart3.getAnchor().getX() - 39) and ((theflappy.getAnchor().getX() - 28) < (pillart3.getAnchor().getX() + 39)):
                if ((theflappy.getAnchor().getY() + 22) > (pillary3+74)) or ((theflappy.getAnchor().getY() - 22) < (pillary3-74)):
                    masterbreak=False
                    break
            count+=1
            if count == 85:
                countshown+=1
                click_sound.play()
                count_shown.setText (str(countshown))
                count_shown.undraw()
                count_shown.draw (win)
            if (count % 50 == 5) and (count>80):
                countshown+=1
                click_sound.play()
                count_shown.setText (str(countshown))
                count_shown.undraw()
                count_shown.draw (win)

        yspeed=-1300
        game_amt=100
        flap_sound.play()


    


    #when a collision is detected, whether the ground or a pillar, it should undraw and send to the death screen
    theflappy.undraw()
    pillart.undraw()
    pillarb.undraw()
    pillart2.undraw()
    pillarb2.undraw()
    pillart3.undraw()
    pillarb3.undraw()
    ground.undraw()
    count_shown.undraw()

    
    #death screen code
    supremebreak=True
    while supremebreak==True:
        hit_sound.play()
        time.sleep(0.5)
        fall_sound.play()
        time.sleep(2)
        death_rect=Rectangle(Point(50, 660), Point(370, 100))
        death_rect.setFill(color_rgb(245,54, 7))
        death_rect.setOutline("black")
        death_rect.draw(win)
        death_rect_Y=False
        death_sscore=Text(Point(260, 360), str(countshown))
        death_sscore.setSize(36)
        death_sscore.setFace("times roman")
        death_sscore.setTextColor(color_rgb(240,175,53))
        death_sscore.draw(win) 
        death_text=Image(Point(210, 250), "gameover.png")
        death_text.draw(win)
        death_score=Text(Point(160, 360), "Score:")
        death_score.setSize(30)
        death_score.setFace("times roman")
        death_score.setTextColor(color_rgb(240,175,53))
        death_score.draw(win)
        death_again=Rectangle(Point(75, 525), Point(345, 450))
        death_again.setWidth(4)
        death_again.setFill(color_rgb(245,54,7))
        death_again.draw(win)
        death_againtext=Text(Point(210, 483), "PLAY AGAIN")
        death_againtext.setSize(36)
        death_againtext.setFace("times roman")
        death_againtext.setTextColor(color_rgb(240,175,53))
        death_againtext.draw(win)
        death_exit=Rectangle(Point(75, 625), Point(345, 550))
        death_exit.setWidth(4)
        death_exit.setFill(color_rgb(245,54,7))
        death_exit.draw(win)
        death_exittext=Text(Point(210, 583), "EXIT GAME")
        death_exittext.setSize(36)
        death_exittext.setFace("times roman")
        death_exittext.setTextColor(color_rgb(240,175,53))
        death_exittext.draw(win)

        #ask for play again or exit window
        while True:
            death_click=win.getMouse()
            click_sound.play()
            death_click_X=death_click.getX()
            death_click_Y=death_click.getY()
            if ((death_click_X < 345) and (death_click_X > 75)) and ((death_click_Y < 525) and (death_click_Y > 450)):
                death_again.undraw()
                death_againtext.undraw()
                death_exit.undraw()
                death_exittext.undraw()
                death_text.undraw()
                death_score.undraw()
                death_rect.undraw()
                death_sscore.undraw()
                supremebreak=False
                break
            if ((death_click_X < 345) and (death_click_X > 75)) and ((death_click_Y < 625) and (death_click_Y > 550)):
                pygame.mixer.music.stop() 
                win.close()  





