# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
from AI import AI
from Action import Action
import random

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__rowDimension = rowDimension
		self.__colDimension = colDimension
		self.__totalMines = totalMines
		self.__moveCount = 0
		self.__startX = startX
		self.__startY = startY		
		self.__tempx = 1
		self.__tempy = 1
		self.__x = 1
		self.__y = 1
		self.__solved = dict()
		self.__unexplored_zeros = []
		self.__Valid_Pos_list = []
		self.__phase = 0
		self.__f = 0
		self.__flagCount = 0
		self.__actioned = 0
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		total_turns = self.__rowDimension * self.__colDimension
		
		#If expert board, leave. My AI is not smart enough to solve these
		if self.__rowDimension != self.__colDimension:
			return Action(AI.Action.LEAVE)
		
		while self.__moveCount < total_turns:
			if self.__moveCount == 0:
				self.__x = self.__startX 
				self.__y = self.__startY 
				self.__tempx = self.__startX
				self.__tempy = self.__startY	
				self.__moveCount += 1
				
			else:
				#if the number is 0 and the coordinate is valid, add it to the list of zeros that are unexplored
				if ((number == 0) and (self.__f == 0)):
					self.__unexplored_zeros.append((self.__tempx, self.__tempy))

			
			#Update the list of currently solved coordinates with the current coordinate and its value
			if (self.__tempx, self.__tempy) not in self.__solved:
				self.__solved[self.__tempx, self.__tempy] = number
				if number == 0 and self.__phase == 1:
					self.__phase = 0
					self.__unexplored_zeros.append((self.__tempx, self.__tempy))
		
			if self.__phase == 1:	
				for key,value in self.__solved.items():
					if value != 0:
						empty_neighbors = []
						revealed_neigbors = []
						num_neighbor_mines = 0
						for i in range(-1, 2):
							for j in range(-1, 2):
								self.__tempx = j + key[0]
								self.__tempy = i + key[1]
								#validator
								#Makes sure that move is not out of bounds or not a tile that has been uncovered/flagged
								if((self.__tempx < 0) or (self.__tempy < 0) or (self.__tempx > self.__rowDimension -1) or (self.__tempy > self.__colDimension-1)):
									pass
								elif (self.__tempx,self.__tempy) in self.__solved:
									revealed_neigbors.append((self.__tempx,self.__tempy))
									if self.__solved[(self.__tempx,self.__tempy)] == -1:
										num_neighbor_mines += 1
								else:	
									empty_neighbors.append((self.__tempx,self.__tempy))
								
						
						if len(empty_neighbors) != 0:
							#solves for: if mine == value, then you know empty boxes are safe to uncover
							if value == num_neighbor_mines:
								self.__tempx = empty_neighbors[0][0]
								self.__tempy = empty_neighbors[0][1]
								self.__moveCount += 1
								action = AI.Action(1)
								self.__actioned = 1
								return Action(action, empty_neighbors[0][0], empty_neighbors[0][1])
							#solves for: if value == empty spaces, then u know that empty spaces are bombs
							elif (value - num_neighbor_mines) == len(empty_neighbors):
								self.__moveCount += 1
								self.__flagCount += 1
								action = AI.Action(2)
								self.__tempx = empty_neighbors[0][0]
								self.__tempy = empty_neighbors[0][1]
								self.__actioned = 2
								return Action(action, empty_neighbors[0][0], empty_neighbors[0][1])
							#If the total number of mines == to the total number of flags placed, the rest of the uncovered sqaures are safe
							elif self.__flagCount == self.__totalMines:
								self.__tempx = empty_neighbors[0][0]
								self.__tempy = empty_neighbors[0][1]
								self.__moveCount += 1
								action = AI.Action(1)
								self.__actioned = 3
								return Action(action, empty_neighbors[0][0], empty_neighbors[0][1])
				
				
				#Scenario only occurs when youre first click does not reveal enough info for basic algorithm. Will click a random coordinate
				if self.__flagCount == 0: 
					valid_move = 0
					while valid_move == 0:
						x = random.randint(0,self.__rowDimension -1)
						y = random.randint(0, self.__colDimension -1)
						if ((x,y)) not in self.__solved:
							self.__tempx = x
							self.__tempy = y
							self.__moveCount += 1
							action = AI.Action(1)
							valid_move = 1
							self.__actioned = 5
							return Action(action, self.__tempx, self.__tempy)		
				
				#Random guess occurs here
				valid_move = 0
				while valid_move == 0:
					x = random.randint(0,self.__rowDimension -1)
					y = random.randint(0, self.__colDimension -1)
					if ((x,y)) not in self.__solved:
						self.__tempx = x
						self.__tempy = y
						self.__moveCount += 1
						action = AI.Action(1)
						valid_move = 1
						self.__actioned = 5
						return Action(action, self.__tempx, self.__tempy)		
						
						
					
			elif self.__solved[(self.__x,self.__y)] == 0: 
				for i in range(-1, 2):
					for j in range(-1, 2):
						self.__tempx = j + self.__x
						self.__tempy = i + self.__y
						#validator
						if((self.__tempx < 0) or (self.__tempy < 0) or (self.__tempx > self.__rowDimension -1) or (self.__tempy > self.__colDimension-1) or ((self.__tempx,self.__tempy) in self.__solved)):
							self.__f = 1
							
						else:
							self.__f = 0
							self.__moveCount += 1
							action = AI.Action(1)
							self.__actioned = 6
							return Action(action, self.__tempx, self.__tempy)
			
				if len(self.__unexplored_zeros) != 0:
					self.__x = self.__unexplored_zeros[0][0]
					self.__y = self.__unexplored_zeros[0][1]
					self.__tempx = self.__x
					self.__tempy = self.__y
					self.__unexplored_zeros.remove((self.__x,self.__y))	
					
				else:
					#phase 1 means its ready to check for bombs, because we have explored all possible zeros in the board for now
					self.__tempx = self.__x
					self.__tempy = self.__y
					self.__phase = 1
			
		return Action(AI.Action.LEAVE)			
			
		########################################################################
		#						YOUR CODE ENDS							   #
		########################################################################
