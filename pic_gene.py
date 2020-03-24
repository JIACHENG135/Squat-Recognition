import matplotlib.pyplot as plt
import json

import os


class Parser:
    def __init__(self):
        self.files = []

        for root, dirs, files in os.walk(".", topdown=False):
            if "False" not in root:
                for file in files:
                    if ".json" in file:
                    # print(os.getcwd()+file)
                        self.files.append(os.getcwd() + "\\"+ root + "\\" + file)


class Draw:
    def __init__(self,file):
        self.file = file
        self.x = []
        self.y = []
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
        with open(file,'r') as load_f:
            load_dict = json.load(load_f)

            for p in load_dict['people']:
                x = []
                y = []
                if p["pose_keypoints_2d"]:
                    for i in range(25):
                        x.append(-int(p["pose_keypoints_2d"][3*i]))
                        y.append(-int(p["pose_keypoints_2d"][3*i+1]))
                    self.x.append(x)
                    self.y.append(y)

    def draw_line(self,u,v,p):

        x = self.x[p]
        y = self.y[p]
        if x[u]!=0 and x[v]!=0:
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

    def draw_point(self,p):
        x = self.x[p]
        y = self.y[p]

        x_list = []
        y_list = []
        plt.axis('equal')
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        for i,j in zip(x,y):
            if i!=0 and j!=0:
                x_list.append(i)
                y_list.append(j)
        ax.scatter(x_list, y_list, c='black', s=20)

    def draw_pic(self,p,file):
        self.draw_point(p)

        for u,v in self.e:
            self.draw_line(u,v,p)
        # plt.show()
        savePath = os.getcwd() + "\\" + "test\\" + file.split('\\')[-1].strip(".json") + ".png"
        plt.savefig(savePath, format='png', dpi=300)
        # plt.save(file.strip('.json')[-5:] + ".png")
        plt.clf()






p = Parser()
for ind,file in enumerate(p.files):
    print(file)
    if ".json" in file:
        if ind%100 == 0:
            print("Generating {} pic".format(ind))
        pen = Draw(file)
        try:
            pen.draw_pic(0,pen.file)
        except:
            print("No people in pic")






# x_list = [1,2,3]
# y_list = [4,5,6]


# plt.figure('Scatter fig')
# ax = plt.gca()

# ax.set_xlabel('x')
# ax.set_ylabel('y')


# ax.scatter(x_list, y_list, c='r', s=20, alpha=0.5)

# plt.show()
