import sys
import pygame
import random
import copy
import game
import unittest



class Test(unittest.TestCase):            
    def test_gemAtXY(self):
        gameBoard = []
        for i in range(3):
                gameBoard.append([-1]*3)
        gameBoard[0][1] = 2
        t = game.gemAtXY(gameBoard, 0, 1)
        self.assertEqual(t, 2)
        
    def test_moveGem(self):
        gameBoard = []
        for i in range(3):
                gameBoard.append([-1]*3)
        gameBoard[0][1] = 2
        gemList = []    
        for i in range(3):
            for j in range(3):
                if(gameBoard[i][j] == -1):
                    newGem = random.randint(0, 5)
                    gameBoard[i][j] = newGem
                    gemList.append({'image': newGem, 'x':i, 'y':j, 'direction':0})
                else:
                    gemList.append({'image':gameBoard[i][j], 'x':i, 'y':j, 'direction':0})
        gameBoardCopy = copy.deepcopy(gameBoard)
        t = game.moveGem(gameBoard, gemList)
        self.assertEqual(t[1], gameBoardCopy[2])
    
    def test_matchingGems(self):
        gameBoard = []
        for i in range(3):
                gameBoard.append([-1]*3)
        gameBoard[0][0] = 2
        gameBoard[0][1] = 2
        gameBoard[0][2] = 2
        gemList = []    
        for i in range(3):
            for j in range(3):
                if(gameBoard[i][j] == -1):
                    newGem = random.randint(0, 5)
                    gameBoard[i][j] = newGem
                    gemList.append({'image': newGem, 'x':i, 'y':j, 'direction':0})
                else:
                    gemList.append({'image':gameBoard[i][j], 'x':i, 'y':j, 'direction':0})
        t = game.matchingGems(gameBoard)
        self.assertEqual(t[0], 2)
    
    def test_checkAdjacentGems(self):
        gameBoard = []
        for i in range(3):
                gameBoard.append([-1]*3)
        gameBoard[0][0] = 2
        gameBoard[0][1] = 2
        gameBoard[0][2] = 2
        gemList = []    
        for i in range(3):
            for j in range(3):
                if(gameBoard[i][j] == -1):
                    newGem = random.randint(0, 5)
                    gameBoard[i][j] = newGem
                    gemList.append({'image': newGem, 'x':i, 'y':j, 'direction':0})
                else:
                    gemList.append({'image':gameBoard[i][j], 'x':i, 'y':j, 'direction':0})
        t =  game.swapGem(gameBoard, gemList[0], gemList[5])
        t1 = game.swapGem(gameBoard, gemList[0], gemList[1])
        self.assertEqual(t[0], None )
        self.assertEqual(t1[0]['x'], 0)
    
    def test_moveable(self):
        gameBoard = []
        for i in range(3):
                gameBoard.append([-1]*3)
        gameBoard[0][0] = 2
        gameBoard[1][0] = 3
        gameBoard[2][0] = 2
        gameBoard[1][1] = 2
        gemList = []    
        for i in range(3):
            for j in range(3):
                if(gameBoard[i][j] == -1):
                    newGem = random.randint(0, 5)
                    gameBoard[i][j] = newGem
                    gemList.append({'image': newGem, 'x':i, 'y':j, 'direction':0})
                else:
                    gemList.append({'image':gameBoard[i][j], 'x':i, 'y':j, 'direction':0})
        t = game.moveable(gameBoard)
        self.assertEqual(t, True)
        
if __name__ == '__main__':
    unittest.main()