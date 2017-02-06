import sys
import pygame
import random
import copy
from pygame.locals import *

width = 800
height = 800
col = 9
row = 9
square_size = 70
left = 0
right = 1
up = 2
down = 3
score = 0
boarder_color = (20, 20, 250)
background_color = (244, 66, 188)
#position the board in the middle
x_boarder = int((width-row*square_size)/2)
y_boarder = int((height-col*square_size)/2)
FPS = 30
cur_score = 0
def main():
    global x_boarder, y_boarder, square_size, boardrects, gemImages, clock, FPS, font, screen, ranking, cur_score
    
    pygame.init()
    font = pygame.font.Font(None, 48)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Bejeweled 2.0')
    clock = pygame.time.Clock()
    pygame.time.set_timer(USEREVENT+1, 1000)
    
    boardrects = []
    #Create the board rects
    for i in range(col):
        boardrects.append([])
        for j in range(row):
            square = pygame.Rect((x_boarder + (i*square_size), 
                            y_boarder + (j*square_size),
                            square_size, square_size))
            boardrects[i].append(square)  
    #initialized and scale gem images
    gemImages = []
    for i in range(0, 7):
        image = pygame.image.load("C:/Users/Wan-Ting/Desktop/Wendy's/College/CS242/Final_Project2/gem%s.png" % i)
        image = pygame.transform.smoothscale(image, (square_size, square_size))
        gemImages.append(image)    
 
    ranking = []
    while True:
        gamestart_text()
        gameLoop()
        pygame.display.flip()
             

#main game loop
def gameLoop():
    seconds = 60
    gameBoard = []
    #initialized gameBoard
    for i in range(col):
        gameBoard.append([-1]*row)
    fillBoard(gameBoard)
    firstGem = None
    mouseX = 0
    mouseY = 0
    pause = False
    score = 0

    while (seconds > -1 ):
        mouseClicked = None
        for event in pygame.event.get():
            #timer event
            if (event.type == USEREVENT + 1):
                    seconds -= 1
            #key event
            elif event.type == QUIT:
                end_game()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE :
                    end_game()
                elif event.key == K_r:
                    print("'r' pressed")
                    return
                elif event.key == K_p:
                    print("'p' pressed")
                    pause = True
                    paused()
                elif event.key == K_s:
                    print("'s' pressed")
                    pause = False

            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                
            elif event.type == MOUSEBUTTONUP:
                if event.pos == (mouseX, mouseY):
                    mouseClicked = checkGem(event.pos)
                    #print(mouseClicked)
                else:
                    firstGem = checkGem((mouseX, mouseY))
                    mouseClicked = checkGem(event.pos)
                    
        #if firstGem is None, set it to mouseClicked            
        if(mouseClicked and firstGem == None):
            firstGem = mouseClicked
            
        #two gems are selected
        elif(mouseClicked != None and firstGem != None and firstGem != mouseClicked):
            #normal mode 
            if(0 <= score <= 200 or 450 < score <=99999):
                swap_0, swap_1 = swapGem(gameBoard, firstGem, mouseClicked)
                #if unable to swap, deselect the gem first clicked
                if swap_0 == 0 and swap_1 == 0:
                    firstGem = None
                    continue
                boardCopy = boardWithoutGems(gameBoard, (swap_0, swap_1))
                animation(boardCopy, [swap_0, swap_1])
                gameBoard[swap_0['x']][swap_0['y']] = swap_1['image']
                gameBoard[swap_1['x']][swap_1['y']] = swap_0['image']
                matchedGems = matchingGems(gameBoard)
                if matchedGems == []:
                    animation(boardCopy, [swap_0, swap_1])
                    gameBoard[swap_0['x']][swap_0['y']] = swap_0['image']
                    gameBoard[swap_1['x']][swap_1['y']] = swap_1['image']
            #enter super mode 
            else:
                swap_0 = {'image' : gameBoard[firstGem[0]][firstGem[1]], 
                        'x' : firstGem[0],
                        'y' : firstGem[1]}
                swap_1 = {'image' : gameBoard[mouseClicked[0]][mouseClicked[1]], 
                        'x' : mouseClicked[0],
                        'y' : mouseClicked[1]} 
                gameBoard[swap_0['x']][swap_0['y']] = swap_1['image']
                gameBoard[swap_1['x']][swap_1['y']] = swap_0['image']
                matchedGems = matchingGems(gameBoard)
                if matchedGems == []:
                    gameBoard[swap_0['x']][swap_0['y']] = swap_0['image']
                    gameBoard[swap_1['x']][swap_1['y']] = swap_1['image']

            while matchedGems != []:
                for gemSet in matchedGems:
                    for gem in gemSet:
                        gameBoard[gem[0]][gem[1]] = -1
                    fillBoard(gameBoard)
                    matchedGems = matchingGems(gameBoard)
                    cur_score = int(10*(len(gemSet)) * (1+(seconds/float(100))))
                    score = cur_score + score
                    if(len(gemSet) >= 4):
                        seconds += 10
            firstGem = None            

        #display game over text when no more valid moves
        if (moveable(gameBoard) == False or seconds == -1):
            ranking.append(score)
            gameover_text()
            screen.fill((0, 0, 0))
            scoreBoard(ranking)
            
        #draw the board
        screen.fill(background_color)
        for i in range(col):
            for j in range(row):
                pygame.draw.rect(screen, boarder_color, boardrects[i][j], 3)
                gemToDraw = gameBoard[i][j]
                if (gemToDraw != -1):
                    screen.blit(gemImages[gemToDraw], boardrects[i][j])
                   

        if firstGem != None:
            pygame.draw.rect(screen, (55, 255, 255), boardrects[firstGem[0]][firstGem[1]], 5)

        if(200 < score < 450):
            mode_text()    
           
        score_text(score) 
        time_text(seconds) 
        
        pygame.display.update()
        clock.tick(FPS)      
                     

#drop new gems to fill in the hole    
def dropGem(gameBoard):
    boardCopy = copy.deepcopy(gameBoard)
    dropGems = []
    for i in range(col):
        for j in range(row-2, -1, -1):         
            if (boardCopy[i][j+1] == -1 and boardCopy[i][j]!= -1):
                dropGems.append({'image': boardCopy[i][j], 'x': i, 'y':j, 'direction': down})
                boardCopy[i][j] = -1
    return dropGems
        
#fill the board with gems
def fillBoard(gameBoard):
    boardCopy = copy.deepcopy(gameBoard)
    for i in range(col):
        col_gem = []
        for j in range(row):
            if (boardCopy[i][j]!=-1):
                col_gem.append(boardCopy[i][j])

        boardCopy[i] = ([-1]*(row-len(col_gem))) + col_gem
    slots = []
    for i in range(col):
        slots.append([])
        for j in range(row-1, -1, -1):
            if(boardCopy[i][j] == -1):
                newGem = randomGem(boardCopy, i, j)
                boardCopy[i][j] = newGem
                slots[i].append(newGem)

    while (slots != col*[[]]):
        dropGems = dropGem(gameBoard)
        for x in range(col):
            if(len(slots[x])!=0):
                dropGems.append({'image':slots[x][0], 'x':x, 'y': -1, 'direction':down})
        boardCopy = boardWithoutGems(gameBoard, dropGems)
        animation(boardCopy, dropGems)
        newGameBoard = moveGem(gameBoard, dropGems)
        for x in range(col):
            if (len(slots[x])==0):
                continue
            newGameBoard[x][0] = slots[x][0]
            del slots[x][0]

            
#randomized gem to minimize repetition 
def randomGem(gameBoard, i, j): 
    gemChoice = [x for x in range(7)]
    for x_offset, y_offset in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        neighbor = gemAtXY(gameBoard, i+x_offset, j+y_offset)
        if neighbor in gemChoice and neighbor != None:
            gemChoice.remove(neighbor)                    
    newGem = random.choice(gemChoice)
    return newGem           
    
#check if position clicked is inside a rectangle           
def checkGem(mousePos):
    for x in range(row):
        for y in range(col):
            if boardrects[x][y].collidepoint(mousePos[0], mousePos[1]):
                return (x, y)
    return None                
            

#return the gem number at positon (x, y)
def gemAtXY(gameBoard, x, y):
    if((x >= 0 and x < col) and (y >= 0 and y < row)):
        return gameBoard[x][y]
    else:
        return None
        
#check if two gems selected are adjacent to each other and swap them
def swapGem(gameBoard, gem0_click, gem1_click):
    gem0 = {'image' : gameBoard[gem0_click[0]][gem0_click[1]], 
            'x' : gem0_click[0],
            'y' : gem0_click[1]}
    gem1 = {'image' : gameBoard[gem1_click[0]][gem1_click[1]], 
            'x' : gem1_click[0],
            'y' : gem1_click[1]}         
    if((gem0['x'] == gem1['x']+1) and (gem0['y'] == gem1['y'])):
        gem0['direction'] = left
        gem1['direction'] = right
    elif((gem0['x'] == gem1['x'] -1) and (gem0['y'] == gem1['y'])):
        gem0['direction'] = right
        gem1['direction'] = left
    elif((gem0['x'] == gem1['x']) and (gem0['y'] == gem1['y'] + 1)):
        gem0['direction'] = up
        gem1['direction'] = down
    elif((gem0['x'] == gem1['x']) and (gem0['y'] == gem1['y'] - 1)):
        gem0['direction'] = down
        gem1['direction'] = up
    else:
        return 0, 0
    return gem0, gem1

#go through gemList to move each gem according to its 'direction', return a new board
def moveGem(gameBoard, gemList):
    for gem in gemList:
        if gem['y'] != -1:
            gameBoard[gem['x']][gem['y']] = -1
            x_dir = 0
            y_dir = 0
            #move left
            if gem['direction'] == left:
                x_dir = -1
            #move right
            elif gem['direction'] == right:
                x_dir = 1
            #move up
            elif gem['direction'] == up:
                y_dir = -1
            #move down
            elif gem['direction'] == down:
                y_dir = 1
            gameBoard[gem['x'] + x_dir][gem['y'] + y_dir] = gem['image']
        else:
            gameBoard[gem['x']][0] = gem['image']
    return gameBoard


#return an 2D array of matching gems
def matchingGems(gameBoard):
    matchingGems = []
    boardCopy = copy.deepcopy(gameBoard)
    #loop through every single space to check theres matching gems
    for x in range(row):
        for y in range(col):
            #check for horizontal matches
            if (gemAtXY(boardCopy, x, y) == gemAtXY(boardCopy, x+1, y) == gemAtXY(boardCopy, x+2, y)):     
                gemToRemoved = boardCopy[x][y]
                count = 0
                gemSet = []
                #loop through to include any gem that has more than 3 matching gems
                while (gemAtXY(boardCopy, x+count, y) == gemToRemoved):
                    gemSet.append((x+count, y))
                    boardCopy[x+count][y] = -1
                    count += 1
                matchingGems.append(gemSet)
            
            #check for vertical matches
            if (gemAtXY(boardCopy, x, y) == gemAtXY(boardCopy, x, y+1) == gemAtXY(boardCopy, x, y+2)):
               gemToRemoved = boardCopy[x][y]
               count = 0
               gemSet = []
               while (gemAtXY(boardCopy, x, y+count) == gemToRemoved):
                   gemSet.append((x, y+count))
                   boardCopy[x][y+count] = -1
                   count += 1
               matchingGems.append(gemSet)
            
    return matchingGems 
    
#animate swapping gems
def animate_gem(gem, rate):
    x_dir = 0
    y_dir = 0
    rate *= 0.01  #rate at 0 means beginning of the animation, 100 means finished 
    
    if gem['direction'] == left:
        x_dir = -int(rate * square_size)
    elif gem['direction'] == right:
        x_dir = int(rate * square_size)
    elif gem['direction'] == up:
        y_dir = -int(rate * square_size)
    elif gem['direction'] == down:
        y_dir = int(rate * square_size)

    rect = pygame.Rect(((x_boarder + (gem['x'] * square_size)) + x_dir, 
                     (y_boarder + (gem['y'] * square_size)) + y_dir, 
                     square_size, square_size))
    screen.blit(gemImages[gem['image']], rect)

#animate the dropping gems   
def animation(gameBoard, gems):
    #rate at 0 means beginning of the animation, 80 means finished. 
    rate = 0
    while rate < 80:
        screen.fill(background_color);
        for i in range(col):
            for j in range(row):
                pygame.draw.rect(screen, boarder_color, boardrects[i][j], 3)
                gemToDraw = gameBoard[i][j]
                if (gemToDraw != -1):
                    screen.blit(gemImages[gemToDraw], boardrects[i][j])
        for gem in gems:
            animate_gem(gem, rate)
        pygame.display.update()
        clock.tick(FPS)
        rate += 20 #display the next frame faster 
            
#loop through valid moves with current (x, y) to check if there are still moveable gems or else game over
def moveable(gameBoard):
    validMoves = (((0, 0), (0, 2), (0, 3)), #vertical valid move
                  ((0, 0), (0, 1), (0, 3)), 
                  ((0, 0), (1, 0), (2, 1)), #horizontal valid move
                  ((0, 0), (1, 1), (2, 0)),
                  ((0, 1), (1, 0), (2, 0)),
                  ((0, 1), (1, 1), (2, 0)),
                  ((0, 1), (1, 0), (2, 1)),
                  ((0, 0), (1, 1), (2, 1)))
    for i in range(row):
        for j in range(col):
            for move in validMoves:
                if((gemAtXY(gameBoard, i+move[0][0], j+move[0][1]) ==
                   gemAtXY(gameBoard, i+move[1][0], j+move[1][1]) ==
                   gemAtXY(gameBoard, i+move[2][0], j+move[2][1])) or 
                   (gemAtXY(gameBoard, i+move[0][1], j+move[0][0]) ==
                   gemAtXY(gameBoard, i+move[1][1], j+move[1][0]) ==
                   gemAtXY(gameBoard, i+move[2][1], j+move[2][0]))):
                    return True
    return False
    
def boardWithoutGems(gameBoard, gems):
    boardCopy = copy.deepcopy(gameBoard)
    for gem in gems:
        if gem['y'] != -1:
            boardCopy[gem['x']][gem['y']] = -1
    return boardCopy  

#paused function when user pressed "p"   
def paused():
    font = pygame.font.SysFont("Rooto_Bold", 200)
    text = font.render("PAUSED", 1, (10, 10, 10)) 
    textpos = text.get_rect()
    textpos.center = (400, 400)
    screen.blit(text, textpos)  
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    end_game()
                elif event.key == K_s:
                    print("'s' pressed")
                    return
        pygame.display.update()
        clock.tick(15)                 

def end_game():
    pygame.quit()
    sys.exit(0)

def score_animation(score):
    score = font.render("+" + str(score), 1, (100, 100, 105)) 
    scoreRect = score.get_rect()
    scoreRect.bottomleft = (70, height-45)
    screen.blit(score, scoreRect)
    

def score_text(score):
    score = font.render("Score: " + str(score), 1, (20, 30, 105)) 
    scoreRect = score.get_rect()
    scoreRect.bottomleft = (10, height - 10)
    screen.blit(score, scoreRect)
    
def mode_text():
    font = pygame.font.SysFont("Tahoma", 40)
    mode = font.render("Super Mode Activated!", 1, (20, 30, 105)) 
    modeRect = mode.get_rect()
    modeRect.center = (400, 30)
    font1 = pygame.font.SysFont("Times New Roman", 30)
    text = font1.render("Swap any two gems", 1, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (400, 60)
    screen.blit(mode, modeRect)
    screen.blit(text, textRect)
    
    
def time_text(time):
    time = font.render("Time: " + str(time), 1, (20, 30, 105))
    timeRect = time.get_rect()
    timeRect.bottomleft = (600, height - 10)
    screen.blit(time, timeRect)
        
def gameover_text():
    font = pygame.font.SysFont("Monotype Corsiva", 100)
    text = font.render("GAME OVER", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.center = (400, 400)
    screen.blit(text, textpos) 
    pygame.display.update()
    pygame.time.wait(2000)
    
def gamestart_text():
    screen.fill(background_color)
    font = pygame.font.SysFont("Monotype Corsiva", 100)
    text = font.render("GAME START", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.center = (400, 400)
    screen.blit(text, textpos) 
    pygame.display.update()
    pygame.time.wait(500)

def scoreBoard(rankings):
    font = pygame.font.SysFont("Garamond", 80)
    text = font.render("Score Board", 1, (225, 225, 225))
    textpos = text.get_rect()
    textpos.center = (400, 100)
    screen.blit(text, textpos) 
    screen_height = 500
    count = 1
    list_rank = []
    #sort the rankings
    if (rankings!=[]):
        rankings.sort()
        list_rank = rankings[::-1]
        
    for rank in list_rank:
        rank_font = pygame.font.SysFont("Lucida Console", 60)
        score_rank = rank_font.render(str(count)+ "..............." + str(rank), 1, (225, 225, 225))
        score_rank_rect = score_rank.get_rect()
        score_rank_rect.center = (400, height - screen_height)
        screen.blit(score_rank, score_rank_rect)
        screen_height-=70
        count+=1
    pygame.display.update()
    pygame.time.wait(5000)

if __name__ == '__main__':

    main()

 