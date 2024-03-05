import pygame
import pymunk
import pymunk.pygame_util
import random
import math

pygame.init()

pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 700, 700
FPS = 60
SPEEDO=200
PARTICLE_NUMBER=500

font = pygame.font.Font(None, 24)

window = pygame.display.set_mode(RES)

class Particle():
    def __init__(self, x, y, space):
        self.mass= 1
        self.radius = 3
        self.moment = pymunk.moment_for_circle(self.mass, 0,self.radius)
        self.body = pymunk.Body(self.mass,self.moment)
        self.body.position = x,y
        self.body.velocity = random.uniform(-SPEEDO,SPEEDO), random.uniform(-SPEEDO,SPEEDO) 
        self.shape = pymunk.Circle(self.body,self.radius)
        self.shape.elasticity = 1

        space.add(self.body, self.shape)

    def speedUP(self):
        self.body._set_velocity(self.body.velocity*1.1)
        
    def speedDown(self):
        self.body._set_velocity(self.body.velocity*0.9)

    def removeMe(self,space):
        space.remove(self.body, self.shape)
    

class Pollen():
    def __init__(self,space):
        self.mass=50
        self.radius = 50
        self.moment = pymunk.moment_for_circle(self.mass, 49,self.radius)
        self.body = pymunk.Body(self.mass,self.moment)
        self.body.position = WIDTH/2, HEIGHT/2
        self.shape = pymunk.Circle(self.body,self.radius)
        self.shape.elasticity = 1
        self.shape.color = (255,0,0,255)
        space.add(self.body, self.shape)

    def get_speed(self):
        x=abs(self.body.velocity.x)
        y=abs(self.body.velocity.y)
        return math.sqrt(x**2 + y**2)
    
    def get_position(self):
        return (int(self.body.position.x), int(self.body.position.y))
    
    def speedUP(self):
        self.body._set_velocity(self.body.velocity*1.1)
        
    def speedDown(self):
        self.body._set_velocity(self.body.velocity*0.9)


def create_boundries(space):
    rect=[
        [(WIDTH/2, HEIGHT-10), (WIDTH, 20)],
        [(WIDTH/2, 10), (WIDTH, 20)],
        [(10, HEIGHT/2), (20,HEIGHT)],
        [(WIDTH-10, HEIGHT/2), (20,HEIGHT)]
    ]

    for pos,size in rect:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body,size)
        shape.elasticity=1
        space.add(body,shape)


def run(window,RES):
    clock = pygame.time.Clock()
    space= pymunk.Space()
    paused=False
    particles=[Particle(random.randint(20,WIDTH-20),random.randint(20,HEIGHT-20), space) for i in range(0,PARTICLE_NUMBER)]
    pollen=Pollen(space)
    pollen_trace = []
    create_boundries(space)
    draw_options = pymunk.pygame_util.DrawOptions(window)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
            if event.type==pygame.KEYDOWN:
                if event.key ==pygame.K_RIGHT:
                    print("speed up")
                    [particle.speedUP() for particle in particles]
                    pollen.speedUP()                
                if event.key==pygame.K_LEFT:
                    print("speed down")
                    [particle.speedDown() for particle in particles]
                    pollen.speedDown() 
                if event.key==pygame.K_SPACE:
                    paused= not paused
                if event.key==pygame.K_UP:
                    [particles.append(Particle(random.randint(20,WIDTH-20),random.randint(20,HEIGHT-20), space)) for i in range(0,10)]
                    print("new particles (",len(particles),")")
                if event.key==pygame.K_DOWN:
                    if(len(particles)>0):
                        [particles[-i].removeMe(space)  for i in range(1,11)]
                        [particles.pop() for i in range(0,10)]
                        print("delete particles(",len(particles),")")
                    else:
                        print("You can't delete something that doesn't already exist")       
            
        if not paused:
            pollen_trace.append(pollen.get_position())
            fps = clock.get_fps()
            
            window.fill("black")

            fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
            window.blit(fps_text, (20, 20))
            speed_text= font.render(f"SPEED: {pollen.get_speed():.2f}", True, (255, 255, 255))
            window.blit(speed_text, (20,50))

            for trace in pollen_trace:
                pygame.draw.circle(window,"white",trace,1)
            space.debug_draw(draw_options)
            pygame.display.update() 

            space.step(1/FPS)
            clock.tick(FPS)


if __name__ =="__main__":
    run(window, RES)