import pygame
import random
import math

class Map():
    def __init__(self):
        self.map = []
        self.ClearMap()
        self.GenerateMap()
        self.MakeMap()

    def ClearMap(self):
        self.map = []
        for x in range(300):
            self.map.append([])
            for y in range(100):
                self.map[x].append('air')

    def GenerateMap(self):
        self.noise = []
        for x in range(len(self.map)):
            self.noise.append(random.randint(30,38))
        self.SmoothMap()
        self.SmoothMap()
        for x in range(len(self.noise)):
            self.map[x][self.noise[x]] = 'dirt'

        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if not self.map[x][y] == 'air':
                    for i in range(y + 1, len(self.map[x])):
                        self.map[x][i] = 'dirt'
                    break

        for x in (0, len(self.map) - 1):
            for y in range(len(self.map[x])):
                self.map[x][y] = 'barrier'

    def UpdateMap(self,posx, posy):
        for x in range(posx - 25, posx + 25):
            for y in range(posy - 15, posy + 15):
                if self.map[x][y] == 'dirt' and self.map[x][y - 1] == 'air':
                    self.map[x][y] = 'grass_block'
                if self.map[x][y] == 'grass_block' and not self.map[x][y - 1] == 'air':
                    self.map[x][y] = 'dirt'



    def SmoothMap(self):
        self.newnoise = []
        for x in range(len(self.noise)):
            if x == 0:
                self.newnoise.append((self.noise[x] + self.noise[x + 1])//2)
            elif x == len(self.map)-1:
                self.newnoise.append((self.noise[x - 1] + self.noise[x])//2)
            elif x > 0 and x < len(self.map)-1:
                self.newnoise.append((self.noise[x - 1] + self.noise[x] + self.noise[x + 1])//3)
        self.noise = self.newnoise
        del self.newnoise


    def MakeMap(self):
        self.dirt = dirt()
        self.barrier = barrier()
        self.grass_block = grass_block()

    def DrawMap(self, screen, posx, posy, offsetx=0, offsety=0):
        self.UpdateMap(posx,posy)
        for x in range(posx - 25, posx + 25):
            for y in range(posy - 15, posy + 15):
                if self.map[x][y] == 'dirt':
                    screen.blit(self.dirt.block_texture, (x*30+offsetx,y*30+offsety))
                if self.map[x][y] == 'grass_block':
                    screen.blit(self.grass_block.block_texture, (x * 30 + offsetx, y * 30 + offsety))
                if self.map[x][y] == 'barrier':
                    screen.blit(self.barrier.block_texture, (x * 30 + offsetx, y * 30 + offsety))


class dirt():
    def __init__(self, havegrass = False):
        self.havegrass = havegrass
        self.block_texture = self.GetTexture("Textures/dirt.png")
        self.block_texture = pygame.transform.scale(self.block_texture, (30,30))

    def GetTexture(self, file):
        return pygame.image.load(file)

class grass_block():
    def __init__(self, havegrass = False):
        self.havegrass = havegrass
        self.block_texture = self.GetTexture("Textures/grass.png")
        self.block_texture = pygame.transform.scale(self.block_texture, (30,30))

    def GetTexture(self, file):
        return pygame.image.load(file)

class barrier():
    def __init__(self):
        self.block_texture = self.GetTexture("Textures/barrier.png")
        self.block_texture = pygame.transform.scale(self.block_texture, (30, 30))

    def GetTexture(self, file):
        return pygame.image.load(file)


class Player():
    def __init__(self, posx = 15, posy = 5, rot=90):
        self.rot = rot
        self.speed = 3
        self.fallspeed = 0
        self.rect = (30,60)
        self.pos = [posx * 30, posy * 30]
        self.surf1 = pygame.Surface((900,600))
        self.surf1.fill((0,0,0))
        self.isjumping = True
        self.goleft = True
        self.goright = True
        self.canjump = 0
        self.offsetx = -150
        self.offsety = -900

    def Move(self, map):
        self.canjump += 1
        self.goleft = True
        self.goright = True
        if self.isjumping == False:
            self.fallspeed = 0

        if self.pos[1] >= 400:
            self.pos[1] = 400
            self.offsety -= self.fallspeed
        else:
            self.pos[1] += self.fallspeed

        if self.pos[1] <= 200:
            self.pos[1] = 200
            self.offsety -= self.fallspeed
        else:
            self.pos[1] += self.fallspeed


        if map[(self.pos[0]+22 - self.offsetx)//30][(self.pos[1] - self.offsety)//30+2] == 'air' \
                and map[(self.pos[0]+8 - self.offsetx)//30][(self.pos[1] - self.offsety)//30+2] == 'air':
            self.fallspeed += 1
            self.isjumping = True
        else:
            self.isjumping = False
            self.pos[1] = ((self.pos[1] - self.offsety)//30+2)*30 + self.offsety - 60

        if not map[(self.pos[0] + 22 - self.offsetx) // 30][(self.pos[1] - 1 - self.offsety) // 30] == 'air' \
                or not map[(self.pos[0] + 8 - self.offsetx) // 30][(self.pos[1] - 1 - self.offsety) // 30] == 'air':
            self.pos[1] = ((self.pos[1] - 1 - self.offsety) // 30) * 30 + self.offsety + 30

        if not map[(self.pos[0] - 1 - self.offsetx)//30][(self.pos[1] + 29 - self.offsety)//30] == 'air'\
                or not map[(self.pos[0] - 1 - self.offsetx)//30][(self.pos[1] + 29 - self.offsety)//30+1] == 'air':
            self.pos[0] = ((self.pos[0] - 1 - self.offsetx)//30) * 30 + self.offsetx + 30

        if not map[(self.pos[0] + 1 - self.offsetx)//30 + 1][(self.pos[1] + 29 - self.offsety)//30] == 'air'\
                or not map[(self.pos[0] + 1 - self.offsetx)//30 + 1][(self.pos[1] + 29 - self.offsety)//30+1] == 'air':
            self.pos[0] = ((self.pos[0] + 1 - self.offsetx)//30 + 1) * 30 + self.offsetx - 30





        self.events = pygame.key.get_pressed()
        if self.events[pygame.K_SPACE] and not self.isjumping and self.canjump > 40:
            self.isjumping = True
            self.fallspeed = -7
            self.canjump = 0

        if self.events[pygame.K_a]:
            if map[(self.pos[0] - 1 - self.offsetx)//30][(self.pos[1] + 29 - self.offsety)//30] == 'air' \
                    and not map[(self.pos[0] - 1 - self.offsetx)//30][(self.pos[1] + 29 - self.offsety)//30+1] == 'air' \
                    and not self.isjumping:
                self.isjumping = True
                self.fallspeed = -7
            if self.goleft:
                if self.pos[0] <= 300:
                    self.pos[0] = 300
                    self.offsetx += self.speed
                else:
                    self.pos[0] -= self.speed

        if self.events[pygame.K_d]:
            if map[(self.pos[0] + 1 - self.offsetx)//30+1][(self.pos[1]+29 - self.offsety)//30] == 'air' \
                    and not map[(self.pos[0] + 1 - self.offsetx)//30+1][(self.pos[1]+29 - self.offsety)//30+1] == 'air' \
                    and not self.isjumping:
                self.isjumping = True
                self.fallspeed = -7
            if self.goright:
                if self.pos[0] >= 600:
                    self.pos[0] = 600
                    self.offsetx -= self.speed
                else:
                    self.pos[0] += self.speed

    def Mouse(self, map):
        self.mousepos = pygame.mouse.get_pos()
        self.mousepress = pygame.mouse.get_pressed()
        if (self.mousepos[0] - self.offsetx) // 30 < len(map.map) - 1 and (self.mousepos[0] - self.offsetx) // 30 > 0:
            if math.sqrt((self.mousepos[1]-(self.pos[1]+30))**2+(self.mousepos[0]-(self.pos[0]+15))**2)//30 <= 3:
                if self.mousepress[2] and not [(self.pos[0]+15-self.offsetx)//30, (self.pos[1]+15-self.offsety)//30] ==[(self.mousepos[0] - self.offsetx) // 30, (self.mousepos[1] - self.offsety) // 30]\
                        and not [(self.pos[0]+15-self.offsetx)//30, (self.pos[1]+15-self.offsety)//30+1] ==[(self.mousepos[0] - self.offsetx) // 30, (self.mousepos[1] - self.offsety) // 30]:
                    map.map[(self.mousepos[0] - self.offsetx) // 30][(self.mousepos[1]- self.offsety) // 30] = 'dirt'
                if self.mousepress[0]:
                    map.map[(self.mousepos[0] - self.offsetx) // 30][(self.mousepos[1] - self.offsety) // 30] = 'air'



class window():
    def __init__(self, WindowName, WindowSize):
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption(WindowName)
        self.screen = pygame.display.set_mode(WindowSize)
        self.map = Map()
        self.player = Player()



    def MainLoop(self):
        self.clock.tick(30)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.screen.fill((101, 222, 224))
            self.map.DrawMap(self.screen, (self.player.pos[0] - self.player.offsetx)//30, (self.player.pos[1] - self.player.offsety)//30, self.player.offsetx, self.player.offsety)
            self.player.Mouse(self.map)
            self.player.Move(self.map.map)
            pygame.draw.rect(self.screen,(0,0,0),(self.player.pos[0], self.player.pos[1],
                                                  self.player.rect[0], self.player.rect[1]))


            pygame.display.update()

if __name__ == "__main__":
    Window = window("PyCraft", (900, 600))
    Window.MainLoop()


