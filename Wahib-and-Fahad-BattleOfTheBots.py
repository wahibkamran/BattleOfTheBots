import network
import random,time,os

name = input ("Please enter your name: ")

dispBoard, size, shipSize, mines = network.createBoards(name, True)

hitList=[]
for r in range(size):
	for c in range(size):
		hitList.append(str(r)+','+str(c))

def randomGuess():
	r=random.randint(0,9)
	c=random.randint(0,9)
	while str(r)+''+str(c) in hitList:
		r=random.randint(0,9)
		c=random.randint(0,9)
	return r,c

def hintPossibilities():
	hintList=[]
	for r in [rHint-1,rHint,rHint+1]:
		for c in [cHint-1,cHint,cHint+1]:
			if r in range(size) and c in range(size):
				hintList.append(str(r)+','+str(c))
	for i in hintList:
		if i not in hitList:
			hintList.remove(i)
	random.shuffle(hintList)
	return hintList

def hitLocationVicinity():
	hitVicinityList=[]
	hitVicinityList.append(str(rHit)+','+str(cHit-1))
	hitVicinityList.append(str(rHit-1)+','+str(cHit))
	hitVicinityList.append(str(rHit)+','+str(cHit+1))
	hitVicinityList.append(str(rHit+1)+','+str(cHit))
	for i in hitVicinityList:
		if i not in hitList:
			hitVicinityList.remove(i)
	return hitVicinityList

locateShip=[]
horShip=[]
vertShip=[]
counter=0
cnt=0
vert=0
hor=0
end=0
haha=0
rekt=0
rHint=''
cHint=''
rHit=-1
cHit=-2
rFinal=-8
cFinal=-7
rEnd=-20
cEnd=-19
rWater=-50
cWater=-49

while True:

	ans = network.receive()

	if rekt==0:
		for m in range(10):
			for n in range(10):
				if dispBoard[m][n]==' ':
					rWater=m
					cWater=n
					rekt+=1

	if cnt==0:
		for k in range(10):
			for l in range(10):
				if dispBoard[k][l]=='x':
					rHit=k
					cHit=l
					locateShip.append(str(k)+','+str(l))
					cnt+=1
	elif cnt==1:
		for r in [rHit-1,rHit,rHit+1]:
			for c in [cHit-1,cHit,cHit+1]:
				if r in range(size) and c in range(size):
					if dispBoard[r][c]=='x' and not str(r)+','+str(c) in locateShip:
						rFinal=r
						cFinal=c
						locateShip.append(str(r)+','+str(c))
						locateShip.sort()
						cnt+=1
	elif haha==0:
		for r in range(10):
			for c in range(10):
				if dispBoard[r][c]=='x' and not str(r)+','+str(c) in locateShip:
					rEnd=r
					cEnd=c
					locateShip.append(str(r)+','+str(c))
					locateShip.sort()
					cnt+=1
					haha+=1

	if ans == 'lost':
		break

	elif ans!= None and rHint=='':
		ans = list(map(int,ans.split(',')))
		print (ans[0],ans[1], "is nearby location of the ship")	
		if counter==0:
			rHint=ans[0]
			cHint=ans[1]
			hintList= hintPossibilities()
			counter+=1

	if rHint!='' and cnt==0:
		for i in hintList:
			if i in hitList:
				guess=i
				hintList.remove(i)
				hitList.remove(i)
				break

	elif cnt==1:
		hitVicinityList=hitLocationVicinity()
		for i in hitVicinityList:
			if i in hitList:
				guess=i
				hitVicinityList.remove(i)
				hitList.remove(i)
				break

	elif cnt==2 :
		hitPositions=[]
		if locateShip[0][0]==locateShip[1][0]:
			hitPositions.append(locateShip[0][0]+','+str(int(locateShip[0][2])-1))
			hitPositions.append(locateShip[0][0]+','+str(int(locateShip[len(locateShip)-1][2])+1))
			hor=1
		elif locateShip[0][2] == locateShip[1][2]:
			hitPositions.append(str(int(locateShip[0][0])-1)+','+locateShip[0][2])
			hitPositions.append(str(int(locateShip[len(locateShip)-1][0])+1)+','+locateShip[0][2])
			vert=1
		for i in hitPositions:
			if i not in hitList:
				hitPositions.remove(i)
		for x in hitPositions:
			if x in hitList:
				guess = x
				hitList.remove(x)
				break
	else:
		if hor==1:
			if end==0:
				if cEnd+1 in range(size):
					if dispBoard[rEnd][cEnd+1]=='x' and dispBoard[rEnd][cEnd+2]=='x':
						for c in [cEnd-1,cEnd+3]:
							horShip.append(str(rEnd)+','+str(c))
						end+=1
				
					else:
						for c in [cEnd-3,cEnd+1]:
							horShip.append(str(rEnd)+','+str(c))
						end+=1
			for i in horShip:
				if i not in hitList:
					horShip.remove(i)
			for i in horShip:
				if i in hitList:
					guess=i
					horShip.remove(i)
					break

		elif vert==1:
			if end==0:
				if rEnd+1 in range(size):
					if dispBoard[rEnd+1][cEnd]=='x' and dispBoard[rEnd+2][cEnd]=='x':
						for r in [rEnd-1,rEnd+3]:
							vertShip.append(str(r)+','+str(cEnd))
						end+=1
				
					else:
						for r in [rEnd-3,rEnd+1]:
							vertShip.append(str(r)+','+str(cEnd))
						end+=1
			for i in vertShip:
				if i not in hitList:
					vertShip.remove(i)
			for i in vertShip:
				if i in hitList:
					guess=i
					vertShip.remove(i)
					break
		
		else:
			if rekt==1:
				guess=str(rWater)+','+str(cWater)
				print("CREDITS: Tofunmi")
			else:	
				r,c=randomGuess()
			
				while dispBoard[r][c]!='.':
					r,c=randomGuess()

				guess=str(r)+','+str(c)
				hitList.remove(guess)
		
	ans = network.send(guess)

	if ans == 'win':
		break
	elif ans == 'wrong input':
		print ("Your input was wrong")
	else:
		guessList = list(map(int,guess.split(',')))
		dispBoard[guessList[0]][guessList[1]]=ans

	time.sleep(2)

if ans == 'win':
	guessList = list(map(int,guess.split(',')))
	dispBoard[guessList[0]][guessList[1]]='x'
	network.printBoard()
	print (name, "has won the game")
else:
	network.printBoard()
	print (name,"has lost the game")