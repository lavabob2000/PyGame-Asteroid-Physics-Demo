import pygame
import random

from Ball import *
from Constants import *

pygame.init()


#set up pygame
window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Asteroid Physcis Demo")
clock = pygame.time.Clock()


#create an array of balls
balls = []

nOfBalls = 25
for i in range(nOfBalls):
	balls.append(Ball(pygame.math.Vector2(random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT)), random.randint(5, 35)))




collisions = []#array of collisions to check

clickedBall = -1

running = True
while running:
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			break

		elif event.type == pygame.MOUSEBUTTONDOWN:
			#get the object that is clicked on
			clickStart = pygame.mouse.get_pos()
			for i in range(len(balls)):
				if balls[i].pos.distance_squared_to(clickStart) <= ball.radius*ball.radius:#check if the mouse is within the ball
					clickedBall = i
					break
			break

		elif event.type == pygame.MOUSEBUTTONUP:
			#get vector between ball clicked on and the current mouse pos and add it to the balls velocity
			if clickedBall != -1:			#check if a ball has been selected
				vel = (balls[clickedBall].pos-pygame.math.Vector2(pygame.mouse.get_pos()))		#get a vector between mouse and ball
				vel /= 10						#scale it down so the speeds are not absurdely large values
				balls[clickedBall].vel = vel
				clickedBall = -1				#reset clicked ball
			break
				
			
	
		
	#update each ball
	for i in range(len(balls)):
		#update the balls position
		balls[i].move()

		#check for collisions with other balls
		for j in range(len(balls)):
			if i != j: #dont check a ball against itself
				#if distance between balls is greater than their radiuses added together then they are touching
				if balls[i].pos.distance_squared_to(balls[j].pos) < (balls[i].radius + balls[j].radius)**2:
					
					#stop the balls from touching, as one cannot physically be inside another
					#get vector between ball centers and move each ball away by half that so they are no longer inside each other
					dist = balls[i].pos.distance_to(balls[j].pos)

					overlap = (dist-balls[i].radius-balls[j].radius)/2 #get half the distance they overlap by
					# get a vector of the overlap and normalise it
					overlapVec = balls[i].pos - balls[j].pos
					if dist != 0:
						overlapVec.x /= dist
						overlapVec.y /= dist

					#move the balls away form eachother
					balls[i].pos -= overlapVec*overlap
					balls[j].pos += overlapVec*overlap
					collisions.append((i,j))#add to a list of collisions to check later



	#resolve all of the collisions and calculate the physics for them
	for i in collisions:
		ball1 = i[0]
		ball2 = i[1]

		dist = balls[ball1].pos.distance_to(balls[ball2].pos)#get the distance

		#calculate the normal vector of the collision
		nX = (balls[ball2].pos.x - balls[ball1].pos.x)
		nY = (balls[ball2].pos.y - balls[ball1].pos.y)
		if dist != 0:
			nX /= dist
			nY /= dist

		#get the tangent vector
		tX = -nY
		tY = nX

		#get the tangent dot product for each of the balls
		dpTan1 = balls[ball1].vel.x * tX + balls[ball1].vel.y * tY
		dpTan2 = balls[ball2].vel.x * tX + balls[ball2].vel.y * tY

		#and get the normal dot product
		dpNorm1 = balls[ball1].vel.x * nX + balls[ball1].vel.y * nY
		dpNorm2 = balls[ball2].vel.x * nX + balls[ball2].vel.y * nY


		#apply conservation of momentum in 1D
		m1 = (dpNorm1 * (balls[ball1].mass - balls[ball2].mass) + 2 * balls[ball2].mass * dpNorm2) / (balls[ball1].mass + balls[ball2].mass)
		m2 = (dpNorm1 * (balls[ball2].mass - balls[ball1].mass) + 2 * balls[ball1].mass * dpNorm1) / (balls[ball1].mass + balls[ball2].mass)

		#update the velocity of both balls
		balls[ball1].vel = pygame.math.Vector2(tX * dpTan1 + nX * m1, tY * dpTan1 + nY * m1)
		balls[ball2].vel = pygame.math.Vector2(tX * dpTan2 + nX * m2, tY * dpTan2 + nY * m2)
		#print(balls[ball1].vel, balls[ball2].vel)


	collisions.clear()#clear the list of collisions

	#clear screen
	window.fill((0,0,0))

	#draw to screen
	
	for ball in balls:
		pygame.draw.circle(window, (255, 255, 255), ball.pos, ball.radius, width=2)

	#draw line from clicked ball to mouse
	if clickedBall != -1:
		pygame.draw.line(window, (0,0,255), balls[clickedBall].pos, pygame.mouse.get_pos())
	
	#update screen
	pygame.display.update()
   #fps
	clock.tick(60)

pygame.quit()