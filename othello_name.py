
# -*- coding: utf-8 -*-


from operator import add as add
from numpy import array


def newGame(player1,player2): 
    '''
    Initialize a new game
    '''

    game = {
        'player1' : player1, 
        'player2' : player2,
        'who': 1,
        'board' : [[0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,2,1,0,0,0],
                   [0,0,0,1,2,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0]]
        }
    
    return game


def printBoard(board):
    '''
    Print a nicely formatted board: printBoard(board)
    '''
    print(' |a|b|c|d|e|f|g|h|')
    print(' +-+-+-+-+-+-+-+-+')
    
    for i in range(8):
        print(i+1, end='')
        for j in range(8):
            if board[i][j]==0:
                print('|%s' % (' '), end='')
            elif board[i][j]==1:
                print('|%s' % ('X'), end='')
            elif board[i][j]==2:
                print('|%s' % ('O'), end='')
            else:
                raise ValueError('Invalid Input')
        print('|')
        
    print(' +-+-+-+-+-+-+-+-+')


def strToIndex(s):
    '''
    Convert position string to indices: strToIndex(s)
    '''
    
    #valid input values
    valid1=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    valid2=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    valid3=['1', '2', '3', '4', '5', '6', '7', '8']
    
    ls=list(sorted(s))
    ls=list(filter(lambda a: a in valid1 or a in valid2 or a in valid3, ls)) 
    
    if len(ls)!=2:
        raise ValueError('Invalid Input')
    
    row=int(ls[0])-1 #index is 0-based
    
    if ls[1] in valid1:
        col=valid1.index(ls[1])
    else: 
        col=valid2.index(ls[1])
    
    return((row,col))

def IndexToStr(t):
    '''
    Convert indices to position string: indexToStr(t)
    '''
    
    for number in t:
        if len(t)!=2 or number<0 or number>8 or type(number)!=int:
            raise ValueError('Invalid Input')
            
    #valid output alphabet
    valid=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    s=valid[t[1]]+str(t[0])
    
    return s

def loadGame():
    '''
    Load a game from a file: loadGame()
    '''
    #The following codes are copied from
    #https://stackoverflow.com/questions/3925614/how-do-you-read-a-file-into-a-list-in-python
    lines=[]
    with open('game.txt', mode='rt', encoding='utf8') as f:
        for line in f: 
            line = line.strip() #or some other preprocessing
            lines.append(line) #storing everything in memory!
    
    board=[]
    for line in lines[3:11]:
        line=list(line)
        line=list(filter(lambda a: a!=',', line))
        numbers = [int(i) for i in line]
        if len(numbers)!=8:
            #if board is not in right shape, raise ValueError
            raise ValueError('input board is not in the right shape') 
        board.append(numbers)
    
    if len(board)!=8:
        #if board is not in right shape, raise ValueError
        raise ValueError('input board is not in the right shape')
    
    game={
        'player1' : str(lines[0]), 
        'player2' : str(lines[1]),
        'who': int(lines[2]), 
        #make sure who is an integer, if it's not, the function will automatically raise ValueError
        'board': board
        #if there is an unwanted element on board, printBoard() function will raise ValueError
            }
    
    return game

#game=loadGame()
    
def getLine(board,who,position,direction):
    '''
    Line of opponent’s pieces: getLine(board,who,position,direction)
    '''
    board=array(board)
    move=tuple(map(add, position, direction))
    
    if any(number>7 for number in move):
        return [] #Board has no valid place on the direction
    
    elif board[position]!=0:
        raise ValueError('Position occupied')
        
    else:
        line=[]
        try:
            while board[move]!=0 and board[move]!=who:
                line.append(move)
                move=tuple(map(add, move, direction))
        except:
            pass
     
        if line!=[]:
            
            check_last=tuple(map(add, line[-1], direction))  
            
            if all(number<=7 for number in check_last):
                if board[check_last]==who:
                    return line     
                else:
                    return [] #The direction has no end of player's disk
            else:
                return [] #The direction has no end of player's disk
            
        else:
            return [] #line=[]

def getValidMoves(board,who):
    '''
    Get list of all valid moves: getValidMoves(board,who)
    '''
        
    #list of all possible direction
    ls_of_dir=[(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    #get empty positions on the board
    where_empty=[]
    for i in range(8):
        for j in range(8):
            if board[i][j]==0:
                where_empty.append((i,j))
    
    moves=[]
    for position in where_empty:
        for direction in ls_of_dir:
            if getLine(board, who, position, direction)!=[]:
                moves.append(position)
    
    if moves==[]:
        return None
    else:
        return moves
    
 
def makeMove(board, move, who):
    '''
    Make a move: makeMove(board,move,who)
    '''
    new_board=array(board)
    
    if new_board[move]!=0:
        raise ValueError('Position occupied')
        
    else:
        #list of all possible direction
        ls_of_dir=[(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        change_lines=[]
        for direction in ls_of_dir:
            if getLine(board, who, move, direction)!=[]:
                change_lines.append(getLine(board, who, move, direction))
        
        if change_lines!=[]:  
            
            new_board[move]=who
            
            for line in change_lines:
                for position in line:
                    new_board[position]=who
            
            return new_board.tolist()
        
        else:
            return board

    
def scoreBoard(board):
    '''
    Score the board: scoreBoard(board)
    '''
    
    score1=0
    score2=0
    
    for i in range(8):
        for j in range(8):
            if board[i][j]==1:
                score1=score1+1
            if board[i][j]==2:
                score2=score2+1
            
    return score1-score2
            
    
def suggestMove1(board, who):
    '''
    An easy computer opponent: suggestMove1(board,who)
    '''
    
    valid_moves=getValidMoves(board, who)
    
    if valid_moves==None:
        return None
    
    else:
        new_scores=[]
        for move in valid_moves:
            new_scores.append(scoreBoard(makeMove(board, move, who)))
    
        if who==1:
            #player1 takes + score
            ind=new_scores.index(max(new_scores))
            
            return valid_moves[ind]
        
        else:
            #player2 takes - score
            ind=new_scores.index(min(new_scores))
            
            return valid_moves[ind]
                
# ------------------- Main function --------------------
            
def play():
    '''
    Play a game: play()
    '''
    print("*"*55)
    print("***"+" "*8+"WELCOME TO STEFAN'S OTHELLO GAME!"+" "*8+"***") 
    print("*"*55,"\n")

    #The following lines used ideas from
    #https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
    while True:
        player1=input("Please enter player1's name, or type 'C' or 'L'. \n")
        if player1=='':
            print("Sorry, your response is invalid.")
            continue
        else:
            player1=player1.capitalize()
            break
    
    if player1=='L':
        game=loadGame()
        player1=game['player1']
        player2=game['player2']
        
    else:
        while True:
            player2=input("Please enter player2's name, or [c]omputer: \n")
            if player2=='':
                print("Sorry, your response is invalid.")
                continue
            else:
                player2=player2.capitalize()
                break
        
        game=newGame(player1, player2)
        
    #Game Begin
    printBoard(game['board'])
    
    #Game ends when both players have no move
    while getValidMoves(game['board'], 1)!=None or getValidMoves(game['board'], 2)!=None:
        
        if game['who']==1 and player1!='C':
            #senario1: player 1 is NOT a computer
            valid_moves=getValidMoves(game['board'], game['who'])
            
            if valid_moves==None:
                #switch to player2 if no valid move available for player1
                print('No valid move available for '+player1)
                game['who']=2 
                
            else:    
                while True:
                    move=input(player1+': Which move to make? ')              
                    try:
                        move=strToIndex(move)
                        if not move in valid_moves:
                            print('Invalid input. Try again!')
                            continue
                        else:
                            break
                        break
                    except:
                        print('Invalid input. Try again!')
                
                #update game board
                game['board']=makeMove(game['board'], move, game['who'])
                printBoard(game['board'])
                
                #switch to player2
                game['who']=2
                
                
        if game['who']==2 and player2!='C':
            #senario2: player2 is NOT a computer
            valid_moves=getValidMoves(game['board'], game['who'])
            
            if valid_moves==None:
                #switch to player1 if no valid move available for player2
                print('No valid move available for '+player2)
                game['who']=1 
                
            else:    
                while True:
                    move=input(player2+': Which move to make? ')              
                    try:
                        move=strToIndex(move)
                        if not move in valid_moves:
                            print('Invalid input. Try again!')
                            continue
                        else:
                            break
                        break
                    except:
                        print('Invalid input. Try again!')
                
                #update game board
                game['board']=makeMove(game['board'], move, game['who']) 
                printBoard(game['board'])
                
                #switch to player1
                game['who']=1
        
        if game['who']==1 and player1=='C':
            #senario3: player1 is a computer
            valid_moves=getValidMoves(game['board'], game['who'])
            
            if valid_moves==None:
                #switch to player2 if no valid move available for player1
                print('No valid move available for computer')
                game['who']=2
                
            else:
                move=suggestMove1(game['board'], game['who'])
                print('Computer is thinking and ... and chose to move to '+IndexToStr(move))
            
                #update game board
                game['board']=makeMove(game['board'], move, game['who']) 
                printBoard(game['board'])
                
                #switch to player2
                game['who']=2
            
        if game['who']==2 and player2=='C':
            #senario4: player2 is a computer
            valid_moves=getValidMoves(game['board'], game['who'])
            
            if valid_moves==None:
                #switch to player1 if no valid move available for player2
                print('No valid move available for '+player1)
                game['who']=1
                
            else:
                move=suggestMove1(game['board'], game['who'])
                print('Computer is thinking and ... and chose to move to '+IndexToStr(move))
            
                #update game board
                game['board']=makeMove(game['board'], move, game['who'])
                printBoard(game['board'])
                
                #switch to player1
                game['who']=1
                
    print('No more valid moves for both players. Game over.')
    
    score=scoreBoard(game['board'])
    
    if score>0:
        print('The winner is '+player1+' with a score of ', score)
    elif score<0:
        print('The winner is '+player2+' with a score of ', -score)
    else:
        print('Draw')
        

# the following allows your module to be run as a program        
if __name__ == '__main__' or __name__ == 'builtins': 
    play()       
            
            
            
                
               
            
            
    

        
    
    
    
    
    
    
