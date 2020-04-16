import collections
import math
import numpy as np
import copy
import random
import matplotlib.pyplot as plt
import os

PI = math.pi/180



class Draw:
    def __init__(self):
        self.x = [0 for i in range(25)]
        self.y = [0 for i in range(25)]
        self.e = [
            [0,1],
            [1,2],
            [2,3],
            [3,4],
            [1,5],
            [5,6],
            [6,7],
            [0,15],
            [15,17],
            [0,16],
            [16,18],
            [1,8],
            [8,9],
            [9,10],
            [10,11],
            [11,22],
            [22,23],
            [11,24],
            [8,12],
            [12,13],
            [13,14],
            [14,21],
            [14,19],
            [19,20]
        ]


    def draw_line(self,u,v):

        x = self.x
        y = self.y
        # if x[u]!=0 and x[v]!=0:
        x_list = [x[u],x[v]]
        y_list = [y[u],y[v]]

        ax = plt.gca()
        # plt.axis('equal')
        plt.xticks([])
        plt.yticks([])
        frame = plt.gca()
        frame.axes.get_yaxis().set_visible(False)
        frame.axes.get_xaxis().set_visible(False)
        ax.plot(x_list, y_list, color='black', linewidth=3)

    def draw_point(self):
        x = self.x
        y = self.y

        x_list = []
        y_list = []
        plt.axis('equal')
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ct = 0
        for i,j in zip(x,y):
            # if i!=0 and j!=0:
            x_list.append(i)
            y_list.append(j)    
            # plt.annotate(str(ct), xy=(i,j), xytext=(0, 0), textcoords='offset points')      
            ct += 1
        ax.scatter(x_list, y_list, c='black', s=10)

    def draw_pic(self,file):
        self.draw_point()

        for u,v in self.e:
            self.draw_line(u,v)
        # plt.show()
        savePath = os.getcwd() + "\\" + "test\\" + file.split('\\')[-1].strip(".json") + ".png"
        plt.savefig(savePath, format='png', dpi=300)
        # plt.save(file.strip('.json')[-5:] + ".png")
        plt.clf()

def rand():
    while True:
        res = random.randint(8,10)
        yield res

def rand2(up,low):
    while True:
        res = random.randint(up,low)
        yield res

class Parser:
    def __init__(self):
        self.c = [[1,2],[1,5],[1,8],[1,0],[0,15],[0,16],[15,17],[16,18],[2,3],[3,4],[5,6],[6,7],[8,9],[9,10],[10,11],[11,24],[11,22],[22,23],[8,12],[12,13],[13,14],[14,21],[14,19],[19,20]]
        self.g = collections.defaultdict(set)
        for u,v in self.c:
            self.g[u].add(v)
            self.g[v].add(u)

        self.rand = rand()
        self.randangle = rand2(10,30)

        self.matrix = {
            'x': lambda angle: [[1,0,0],[0,math.cos(angle),-math.sin(angle)],[0,math.sin(angle),math.cos(angle)]],
            'y': lambda angle: [[math.cos(angle),0,math.sin(angle)],[0,1,0],[-math.sin(angle),0,math.cos(angle)]],
            'z': lambda angle: [[math.cos(angle),-math.sin(angle),0],[math.sin(angle),math.cos(angle),0],[0,0,1]],
        }


        self.scheme = collections.defaultdict(list)

        self.scheme[(1,8)] = [['y',180]]
        self.scheme[(1,5)] = [['y',270]]
        self.scheme[(1,2)] = [['y',90]]
        self.scheme[(1,0)] = [['y',0]]

        self.scheme[(2,3)] = [['y',120]]
        self.scheme[(3,4)] = [['x',-90]]

        self.scheme[(5,6)] = [['y',210]]
        self.scheme[(6,7)] = [['x',-90]]

        self.scheme[(8,9)] = [['y',90]]
        self.scheme[(9,10)] = [['y',180]]
        self.scheme[(10,11)] = [['y',180]]
        self.scheme[(11,24)] = [['y',225]]
        self.scheme[(11,22)] = [['y',150]]
        self.scheme[(22,23)] = [['y',45]]

        self.scheme[(8,12)] = [['y',270]]
        self.scheme[(12,13)] = [['y',180]]
        self.scheme[(13,14)] = [['y',180]]
        self.scheme[(14,19)] = [['y',210]]
        self.scheme[(14,21)] = [['y',135]]
        self.scheme[(19,20)] = [['y',315]]   

        self.scheme[(0,16)] = [['y',315]]
        self.scheme[(16,18)] = [['y',225]]
        self.scheme[(0,15)] = [['y',45]]
        self.scheme[(15,17)] = [['y',135]]


        self.leng = collections.defaultdict(int)

        self.leng[(0,1)] = 39
        self.leng[(1,8)] = 100

        self.leng[(9,10)] = 64
        self.leng[(12,13)] = 64

        self.leng[(10,11)] = 60
        self.leng[(13,14)] = 60

        self.leng[(8,9)] = 17
        self.leng[(8,12)] = 17

        self.leng[(1,2)] = 35
        self.leng[(1,5)] = 35

        self.leng[(2,3)] = 42
        self.leng[(5,6)] = 42

        self.leng[(3,4)] = 40
        self.leng[(6,7)] = 40




        copyscheme = copy.deepcopy(self.scheme)
        copyleng = copy.deepcopy(self.leng)

        for key in self.leng:
            copyleng[(key[1],key[0])] = self.leng[key]

        for key in self.scheme:
            copyscheme[(key[1],key[0])] = self.scheme[key]

        self.leng = copyleng
        self.scheme = copyscheme




    def _norm(self,vec):
        return math.sqrt(sum(i**2 for i in vec))

    def _add(self,N,vec):
        return [x+y for x,y in zip(N,vec)]


    def _rotate(self,axis,angle,node):
        res =  np.dot(np.array(self.matrix[axis](angle)),np.array(node).reshape(3,1))
        return list([float(i) for i in res])

    def _perform(self,seg,scheme):
        self.scheme[seg].extend(scheme)
        self.scheme[(seg[1],seg[0])].extend(scheme)
        # print(self.scheme[seg])

    def _generate(self):
        visited = set()
        state = collections.defaultdict(list)
        state[1] = [0,0,0]
        def dfs(n):
            visited.add(n)
            for nei in self.g[n]:
                if nei not in visited:
                    dist = self.leng[(nei,n)]
                    if dist == 0:
                        dist = next(self.rand)

                    node = [0,0,dist]
                    sequens = self.scheme[(nei,n)]
                    for tmp in sequens:
                        axis,angle = tmp
                        node = list(self._rotate(axis,angle*PI,node))

                    state[nei] = self._add(node,state[n])

                    dfs(nei)


        dfs(1)
        return state


    def _project(self,angle,node):
        # Only consider horithontal
        x,y,z = node
        A = math.sin(angle)
        B = -math.cos(angle)
        C = 0
        D = 0

        xp = ((B**2 + C**2)*x - A*(B*y+C*z+D))/(A**2+B**2+C**2)
        yp = ((A**2 + C**2)*y - B*(A*x+C*z+D))/(A**2+B**2+C**2)
        zp = ((A**2 + B**2)*z - C*(A*x+B*y+D))/(A**2+B**2+C**2)

        return [xp,yp,zp]

    def action_set(self):
        actions = collections.defaultdict()
        actions['leg_curve'] = lambda i,j :[[(9,10),[['x',i],['z',-j]]],[(12,13),[['x',i],['z',j]]],[(10,11),[['x',-i],['z',-j]]],[(13,14),[['x',-i],['z',j]]]]
        actions['hug'] = lambda i,j :[[(2,3),[['x',i]]],[(5,6),[['x',i]]]]
        
        return actions

rand_view = rand2(30,80)
if __name__ == "__main__":
    vec = [1,2,3]
    
    k = 20

    for _ in range(100):
        i = next(rand_view)

        for j in range(60,320,10):
            p = Parser()
            actions = p.action_set()
            leg_curve = actions['leg_curve']
            hug = actions['hug']
            for seg,schemes in leg_curve(i,k):
                p._perform(seg,schemes)
            for seg,scheme in hug(i,k):
                p._perform(seg,schemes)

            state = p._generate()

            d = Draw()
            angle = j*PI
            for key in state:
                cor = p._project(angle,state[key])
                d.x[key] = cor[1]
                d.y[key] = cor[2]

            d.draw_pic("first_test"+str(j)+ '-' +str(_))

    
