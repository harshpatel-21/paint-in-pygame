version='1'
#---------------------------------------------------------------------------

import pygame
import sys
from pygame.locals import *
# optional imports
# from colorama import Fore, Style
# from colorama import init as colorama_init
# colorama_init(convert=True)
pygame.init()
#pygame.display.set_caption("NAME" + 'version ' + version)
#icon = pygame.image.load('IMAGE_NAME.png')
#pygame.display.set_icon(icon)
font_size = 20

main_font = pygame.font.SysFont('comicsans',font_size)

inst1 = main_font.render('| hold left click to draw |',True,(255,255,255))
inst2 = main_font.render('c = clear |',True,(255,255,255))
inst3 = main_font.render('ctrl+z to undo smth |',True,(255,255,255))
inst4 = main_font.render('r,g,blue,w,black(L_shift+b) to change colors |',True,(255,255,255))
inst5 = main_font.render('press p(pen) (on by default) or f(fill) and then a color followed by color |',True,(255,255,255))
pygame.display.set_caption('Paint')
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

y2 = font_size+5
x2 = 20+inst1.get_width()
x3 = inst3.get_width()+20
x4 = x2+inst2.get_width()+20 #this is just a bunch of hard coded shit, couldn't rlly be asked to make it adaptaive
# alternative method | pygame.Freetype.font

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

colors = {
    'red':(255,0,0),
    'green':(0,255,0),
    'blue':(0,0,255),
    'white':(255,255,255),
    'black':(0,0,0)
}

def main():
    ticker = 0
    remove = False
    #grass = pygame.image.load('C://Users/Harsh/Desktop/A level CS/Pygame/Paint/grass.png')
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    s_rect = screen.get_rect() # getting a rect for screen surface
    text_surface = pygame.Surface((500,100))
    drawing_surf = pygame.Surface((screen.get_width(),screen.get_height()-(y2+40)))
    d_rect = drawing_surf.get_rect()
    difference = s_rect.height - d_rect.height

    main_menu = True

    draw = False
    positions=[]

    pen,fill=True,False
    pen_color = 'red'
    fill_color = 'white'
    factor = 10
    change_Size = True

    radius = 10
    tool = 'pen'
    canvas_border=5
    a = []
    to_draw = []
    while main_menu:

        normal = False
        add = True
        mods = pygame.key.get_mods() # this is used for the non alphanumeric keys
        screen.fill((8,8,8))
        drawing_surf.fill(colors[fill_color])

#-------------------------------- Events loop --------------------------------#

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                main_menu = False

            #--- Mouse clicking checker thing ----#
            if event.type == pygame.MOUSEBUTTONUP: # this essentially checks that once a button is lifted
                if event.button == 1: # if the left click is the one that the action has occured to
                    if len(a) > 0: # making sure its not empty... not sure why i did this but i did cuz saftey >>>>>>
                        positions.append(a) # go ahead and add the 'streak'/held down drawing coords to positions
                        a = [] # reset a for whatever is drawn next

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and mods & pygame.KMOD_CTRL: # it CTRL z is pressed

                    # to explain the logic of my absolutely elegent (not) ctrl +z:
                    # You have a list which is called to draw... now this is used to draw on the Surface
                    # in real time. To make it easier I could've done it so that the drawing is done after mouse is lifted
                    # and then those coords are added to positions...
                    # but lets be honest thassa bit dead. no one likes drawing shit with hella delay/lag
                    # So instead, each time mouse is held, those coords are added to an array, and once lifted they're added as a list in positions
                    # therefore for each index in positions it contains 'metadata' about each thing the user drew



                    '''---------------- old ----------------'''
                    # now you check each list of positions[-1] (the list named compare), and then each coordinate in to_draw and see if its present
                    # if it is present you remove the item for compare. Once gone through everything kinda, if length of compare == 0
                    # meaning that all coords in compare are present in to_draw, we re assign positions to equal everything before the last index
                    # which contains the last 'streak' of drawn stuff

                    # YES I KNOW O(N^2) IS ABSOLUTE DOG SHIT but its all i could think of
                    # to check each list within a list and compare
                    # Thus, the leading to the birth of the horrific nested for loop eew.

                    # if len(to_draw) > 0:
                    #     compare = positions[-1]
                    #     for posi in compare:
                    #         for j in range(len(to_draw)-1,-1,-1):
                    #             if to_draw[j] == compare[j]:
                    #                 compare.remove(to_draw[j])
                    #                 to_draw.remove(to_draw[j])
                    #     if len(compare) == 0:
                    #         positions = positions[:-1]

                    # SO cuz im rlly not a fan of n^2 cuz im afraid my laotop might crash lol
                    # Came up with an alternative method.

                    '''---------------- new ----------------'''

                    if len(to_draw) > 0:
                        compare = positions[-1] # since this is a 2d array
                        temp = list(map(lambda x: x,to_draw)) # cuz doing temp = to_draw links the two lists for some reason
                        # because we want to alter the 'to_draw' list, each iteration it will fuck up when indexes are compared in for loop
                        # hence why the temp list is made to remove the index and the original 'to_draw' is compared with 'compare' to reduce
                        # likelihood of errors, whilst the appropriate shit is removed from temp

                        # print(temp) # quick likkle chek up on the mandem
                        # print(f'{compare}, {len(compare)}')

                        # the range is len of to draw since that is gonna be == to or > than compare as its gonna contain all coords of drawn objects
                        # You can see now why the nested for loop was excessive because even tho compare is a 2d list, we can use the
                        # 'in' comparator to see if the current position list is inside compare.
                        # and remove it from the temp one to make sure that no 'list index errors occur' as thats what was happening before

                        for posi in range(len(to_draw)-1,-1,-1):
                            # now... I did starting from ending index, to 0 and in steps of -1 because when 'ctrl Z'ing, you're getting rid of the most recent thing...
                            # therefore I start at the end of 'to_draw' to check the most recent coords drawn
                            if to_draw[posi] in compare:
                                temp.remove(to_draw[posi])

                        # now there's probably a better more efficient way like.... idk removing last (len(compared)) items of to_draw
                        # which could infact actually work now that i think abuot it
                        # but I rlly cba and this here seems to be effective enough hence why I used this second for loop method
                        # cuz its not as terrible as the n^2 shit ew ew

                        to_draw = temp #once looping is done, and all required indexes are removed from the # TEMP:
                        # set to_draw equal to temp

                        positions = positions[:-1] # basically removing the last drawn object/ consecutive stuff drawn whilst mouse is down since thats what
                                                   # ctrl z does


                if event.key==pygame.K_s:
                    # This was mainly used during the debugging process to check the lengths and contents and shit,
                    # nothing too important
                    if len(positions) > 0 and len(to_draw)>0:
                        print(f'positions list: {positions}')
                        #print(f'{positions[-1]}')
                        print(f'to_draw lis: {to_draw}')


#-----------------------------------------------------------------------------#

            # --- old method of toggline remove problem: you cant hold down ctrl + z, have to press down each time
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_z:
            #         if mods & pygame.KMOD_CTRL:
            #             remove=True

#------------------------------- Mouse presses -------------------------------#

        mouse_status = pygame.mouse.get_pressed()
        if mouse_status[0] == 1 and pen == True: #only do stuff with mouse positions if pen is selected
            pos = pygame.mouse.get_pos()


            if [pos[0],pos[1]-difference,pen_color] not in to_draw:
                # print('appending')
                            # this makes sure that if they're holding down left click
                            # in same position constantly, it doesn't append it.
                            #(a) takes up less memory (although it is quite minimal)
                            #(b) makes ctrl +Z ing more easier because dont have to del same thing
                            # again and again
                a.append([pos[0],pos[1]-difference,pen_color]) #identifies what color to draw
                to_draw.append([pos[0],pos[1]-difference,pen_color])

            # else:
            #     print('already in list')# another debugging thing
            #     #print(f'{[pos[0],pos[1],pen_color]} alredy in list')

#----------------------------- Keyboard Presses ------------------------------#

        #--------- get keys pressed ----------#

        key_press = pygame.key.get_pressed() # get all the keys pressed

        # ------ pen or fill checker. This makes it so that when the fill and pen color changes are independent
        if key_press[pygame.K_p]: #pen
            pen = True
            fill = False
        if key_press[pygame.K_f]: #fill
            fill = True
            pen = False

        # ----- clear the whole ting
        if key_press[pygame.K_c]: # if the key pressed is c, clear positions and to_draw
            positions = []
            to_draw = []
        # ----- color check assigns the color to which ever tool is selected
        if key_press[pygame.K_w]:
            if pen == True:
                pen_color ='white'
            elif fill == True:
                fill_color ='white'
        if key_press[pygame.K_r]:
            if pen == True:
                pen_color ='red'
            elif fill == True:
                fill_color ='red'
        if key_press[pygame.K_g]:
            if pen == True:
                pen_color ='green'
            elif fill == True:
                fill_color ='green'
        if key_press[pygame.K_b]:
            if pen == True:
                pen_color ='blue'
            elif fill == True:
                fill_color ='blue'
        if key_press[pygame.K_b] and mods & pygame.KMOD_LSHIFT:
            if pen == True:
                pen_color = 'black'
            elif fill == True:
                fill_color = 'black'

#----------------------------- Drawing ------------------------------#

        #------- canvas outline/border -------#

        pygame.draw.rect(drawing_surf, (colors['red']), (d_rect.x,d_rect.y, d_rect.width, d_rect.height),5) # kinda like a lil outline for the canvas

        #---------- Drawing circles ----------#

        if len(to_draw) > 0: # making sure there's something in to_draw
            for i in to_draw:
                pygame.draw.circle(drawing_surf, colors[i[2]], (i[0],i[1]), radius)
                #screen.blit(grass,(i[0]-(grass.get_width()//2),i[1]-(grass.get_height()//2)))


#------------------------------- BLITing shit --------------------------------#

        screen.blit(inst1,(10,10)) #label, xy coords | mouse control info
        screen.blit(inst2,(x2,10)) #label, xy coords | c for clear
        screen.blit(inst3,(10,y2))
        screen.blit(inst4,(x3,y2))
        screen.blit(inst5,(x4,10))

        # update display each iteration

#------------------------ Go ahead and update display ------------------------#
        screen.blit(drawing_surf,(0,y2+40)) # blitting it downwards by y2+40 cuz of instruction texts
        pygame.display.update()
        clock.tick(60)


main()
