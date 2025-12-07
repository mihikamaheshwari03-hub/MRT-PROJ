#here we will make the basic class of the bots from which their attributes will me controlled

import rclpy 
import sys
from rclpy.node import Node
from std_msgs.msg import Int16
from mapping.mapping_shi import GeneratedMap
from messages.srv import Mapinfo
from messages.msg import Map
class bot(Node):
    def __init__(self,id,parent = None,coord=(1,1),color="white",returning=False,map=GeneratedMap()):
        super().__init__("bot_node")
        parent.map.grid[coord]= 2
        self.id=id
        self.coord=coord
        self.color=color
        self.returning=returning
        self.path=[]
        self.follow_leader=None    #initially following none
        self.LOS=3  #line of sight
        self.get_map = self.create_client(Mapinfo, 'map_info')
        self.map = map
        self.send_map = self.create_publisher(Map,'send_map',10)
        self.parent = parent #the swarm object that created this bot
    def get_map_info(self,x,y):
        while not self.get_map.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        request = Mapinfo.Request()
        request.x = x
        request.y = y
        future = self.get_map.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result().status 
    def sendmap(self,x,y,status):
        msg = Map()
        msg.x = x 
        msg.y = y
        msg.status = status
        self.send_map.publish(msg)

    def see(self):
        for x in range(self.x - self.LOS + 1, self.x + self.LOS):
            for y in range(self.y - self.LOS + 1, self.y + self.LOS):
                
                if (x == self.x and y == self.y):
                    continue
    
                dx = x - self.x
                dy = y - self.y 
    
                is_blocked = False
                
                if abs(dx) > 0 and abs(dy) > 0:
                    sign_x = 1 if dx > 0 else -1
                    sign_y = 1 if dy > 0 else -1
                    
                    point_1 = (x - sign_x, y)
                    point_2 = (x, y - sign_y)
                    middle_point = (x - sign_x, y - sign_y)
                    
                    if self.get_map_info.get(point_1) == 1 and self.get_map_info.get(point_2) == 1:
                        is_blocked = True
    
    
                else:
                    prev_x = x - (1 if dx > 0 else -1) if dx != 0 else x
                    prev_y = y - (1 if dy > 0 else -1) if dy != 0 else y
                    
                    if (prev_x, prev_y) != (self.x, self.y) and self.get_map_info.get((prev_x, prev_y)) == 1:
                        is_blocked = True
    
                if not is_blocked:
                    self.self.get_map_info.setValue(x, y, self.get_map_info[(x, y)])
    
    
        #now for outer box
        is_blocked = 0
        for dx in range(1,self.LOS):
            if self.get_self.get_map_info_info((self.x + dx, self.y)) == 1:
                is_blocked = 1
                break
        if not is_blocked:
            self.self.get_map_info.setValue(self.x + self.LOS, self.y, self.get_map_info[(self.x + self.LOS, self.y)])
        
    
        is_blocked = 0
        for dy in range(1,self.LOS):
            if self.self.get_map_info.get((self.x , self.y + dy)) == 1:
                is_blocked = 1
                break
        if not is_blocked:
            self.self.get_map_info.setValue(self.x, self.y + self.LOS, self.get_map_info[(self.x, self.y + self.LOS)])
    
        is_blocked = 0
        for dx in range(1,self.LOS):
            if self.self.get_map_info.get((self.x - dx, self.y)) == 1:
                is_blocked = 1
                break
        if not is_blocked:
            self.self.get_map_info.setValue(self.x - self.LOS, self.y, self.get_map_info[(self.x - self.LOS, self.y)])
        
    
        is_blocked = 0
        for dy in range(1,self.LOS):
            if self.self.get_map_info.get((self.x , self.y - dy)) == 1:
                is_blocked = 1
                break
        if not is_blocked:
            self.self.get_map_info.setValue(self.x ,self.y - self.LOS, self.get_map_info[(self.x, self.y - self.LOS)])
    
        self.parent.self.get_map_info.grid[self.coord]= 2
        self.parent.update_data()
        self.parent.self.get_map_info.update_frontiers()
    
    def move(self,coord: tuple):
        if coord == (self.coord[0]+1,self.coord[1]) or (self.coord[0]-1,self.coord[1]) or (self.coord[0],self.coord[1]+1) or (self.coord[0],self.coord[1]-1):
            self.coord = coord
            self.see()
    def follow_path(self,path):
        for i in range(len(path)):
            self.move(path[i])
    def leader(self):
        self.color="blue"
        self.update_map()
    def follower(self):
        self.color="green"
        self.update_map()
    def explorer(self):
        self.color="yellow"
        self.update_map()
    def is_returning(self):
        self.returning=True
        self.color="red"
        self.update_map()
    def follow(self,leader):
        self.follow_leader=leader
    def is_leader(self):
        return self.color=="blue"
    def update_map(self): #called everytime a bot object is made or colour updated so that map can be updated
        #publish the id and colour of bot 
        pass

