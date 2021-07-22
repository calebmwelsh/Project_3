import pygame,math

'''
---------------------------------------------------- functions ---------------------------------------------
'''
def advance(pos,rot,speed):
    pos[0] += math.cos(rot) * speed
    pos[1] += math.sin(rot) * speed
    return [pos[0],pos[1]]

'''
---------------------------------------------------- spark ---------------------------------------------
'''
class Spark():
    def __init__(self,pos,rot,speed,scale,color,type):
        # spark pos
        self.pos = list(pos)
        # spark rot
        self.rot = rot
        # spark speed
        self.speed = speed
        # only for impoloion
        self.max_speed = -speed
        # spark scale
        self.scale = scale
        # spark color
        self.color = color
        # spark type
        self.type = type

'''
---------------------------------------------------- projectile manager ---------------------------------------------
'''
# manage all sparks
class SparkManager():
    def __init__(self):
        self.sparks = []

    # reset sparks
    def reset(self):
        self.sparks = []

    # create a new spark
    def new(self,pos,rot,speed,scale,color,type):
        self.sparks.append(Spark(pos,rot,speed,scale,color,type))
        
    # update all sparks
    def update(self,display,scroll):
        for i,s in sorted(enumerate(self.sparks),reverse=True):
            if s.type == 's':
                advance(s.pos,s.rot,s.speed)
                s.speed += -.1
                if s.speed < 0:
                    self.sparks.pop(i)
                point_list = [
                        advance(s.pos.copy(),s.rot,s.speed * s.scale),
                        advance(s.pos.copy(),s.rot + math.pi / 2,s.speed * s.scale * .1),
                        advance(s.pos.copy(),s.rot + math.pi,s.speed * s.scale * .6),
                        advance(s.pos.copy(),s.rot - math.pi / 2,s.speed * s.scale * .1)
                ]
                # apply camera or scroll offset
                point_list = [[p[0] -scroll[0],p[1]-scroll[1]] for p in point_list]
                pygame.draw.polygon(display,s.color,point_list)
            elif s.type == 'i':
                advance(s.pos,s.rot,s.speed)
                s.speed += -.1
                if s.speed < s.max_speed:
                    self.sparks.pop(i)
                point_list = [
                        advance(s.pos.copy(),s.rot,s.speed * s.scale),
                        advance(s.pos.copy(),s.rot + math.pi / 2,s.speed * s.scale * .3),
                        advance(s.pos.copy(),s.rot + math.pi,s.speed * s.scale * .6),
                        advance(s.pos.copy(),s.rot - math.pi / 2,s.speed * s.scale * .3)
                ]
                # apply camera or scroll offset
                point_list = [[p[0] -scroll[0],p[1]-scroll[1]] for p in point_list]
                pygame.draw.polygon(display,s.color,point_list)
