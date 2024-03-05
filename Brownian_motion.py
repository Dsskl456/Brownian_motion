import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

class BrownAnimation:
    def __init__(self):
        
        self.paused=False
        self.wall = 0
        self.randomly=0
        self.hurst=-1
        self.memory=2000
        self.a=math.pow(1,-self.hurst)/(self.hurst+0.5)
    
    def OneD(self):
        x=[[0,0]]
        y=[[0,0]]
        fgn=[]
        colors=['']
        fig, ax=plt.subplots()
        ax.plot(x,y)
        ax.grid()
        plt.title("One dimension")
        point,=ax.plot(0,0,marker="o",c="black")
        def update(i):
            step=self.get_random(fgn)

            x.append((x[-1][1],x[-1][1]+1))
            y.append((y[-1][1],y[-1][1]+step))

            self.check_colors(abs(step),colors,(0.2,0.4))
            self.check_wall(colors,1,ax,x,y)

            ax.plot(x[-1],y[-1],c=colors[-1])
            point.set_data(x[-1][1],y[-1][1])
        self.ani=FuncAnimation(fig=fig,func=update,interval=100,frames=100)
        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

        plt.show()
        
    def TwoD(self):
        x=[[0,0]]
        y=[[0,0]]
        x_fgn=[]
        y_fgn=[]
        colors=['']
        fig, ax=plt.subplots()
        ax.plot(x,y)
        ax.grid(True)
        plt.title("Two dimensions")
        point,=ax.plot(0,0,marker="o",c="black")
        def update(i):
            step_x=self.get_random(x_fgn)
            step_y=self.get_random(y_fgn)

            x.append((x[-1][1],x[-1][1]+step_x))
            y.append((y[-1][1],y[-1][1]+step_y))

            step_length=math.sqrt(step_x**2+step_y**2)
            self.check_colors(step_length,colors,(0.4,3))
            self.check_wall(colors,2,ax,x,y)

            ax.plot(x[-1],y[-1],c=colors[-1])
            point.set_data(x[-1][1],y[-1][1])
                
        self.ani=FuncAnimation(fig=fig,func=update,interval=100,frames=100)
        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)
        plt.show()
       
    def ThreeD(self):
        x=[[0,0]]
        y=[[0,0]]
        z=[[0,0]]
        ite=[[0,0]]
        x_fgn=[]
        y_fgn=[]
        z_fgn=[]
        colors=['']
        fig=plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(221, projection='3d')
        ax.title.set_text("Three dimensions")
        point,=ax.plot(0,0,0,marker="o",c="black")
        ax_x, point_x=self.new_subplot(222,'x',fig)
        ax_x.title.set_text("x axis")
        ax_y, point_y=self.new_subplot(223,'y',fig)
        ax_y.title.set_text("y axis")
        ax_z, point_z=self.new_subplot(224,'z',fig)
        ax_z.title.set_text("z axis")
        def update(i):
            step_x=self.get_random(x_fgn)
            step_y=self.get_random(y_fgn)
            step_z=self.get_random(z_fgn)

            x.append((x[-1][1],x[-1][1]+step_x))
            y.append((y[-1][1],y[-1][1]+step_y))
            z.append((z[-1][1],z[-1][1]+step_z))
            ite.append((ite[-1][1],ite[-1][1]+1))

            step_length=math.sqrt(step_x**2+step_y**2+step_z**2)
            self.check_colors(step_length,colors,(0.75,1.5))

            self.check_wall_3D(colors,ax,ax_x,ax_y,ax_z,x,y,z,ite)

            ax.plot(x[-1],y[-1],z[-1],c=colors[-1])
            ax_x.plot(ite[-1],x[-1],c=colors[-1])
            ax_y.plot(ite[-1],y[-1],c=colors[-1])
            ax_z.plot(ite[-1],z[-1],c=colors[-1])

            point.set_data(x[-1][1],y[-1][1])
            point.set_3d_properties(z[-1][1], 'z')

            point_x.set_data(ite[-1][1],x[-1][1])
            point_y.set_data(ite[-1][1],y[-1][1])
            point_z.set_data(ite[-1][1],z[-1][1])
            
        self.ani=FuncAnimation(fig=fig,func=update,interval=10,frames=100)
        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)
        plt.show()

    def check_colors(self,step_length,colors,range):
        if(step_length>range[1]):
            colors.append('orange')
        elif(step_length>range[0]):
            colors.append('green')
        else:
            colors.append('blue')

    def get_random(self,fgn):
        match self.randomly:
            case "1":
                m=min(len(fgn),self.memory)
                fgn.append(random.gauss(0,1))
                e1=math.pow(1,self.hurst-0.5)*fgn[-1]
                e3=0.0
                for l in range(1,m):
                    e2=(math.pow(l+1,self.hurst-0.5)-math.pow(l, self.hurst-0.5))*fgn[-l]
                    e3+=e2
                return self.a*(e1+e3)
            case "2":
                return random.uniform(-0.5,0.5)
            case "3":
                return random.choice([-0.5,0.5])
            case "4":
                return random.gauss(0,0.5)
            case "5":
                return random.lognormvariate(1,1)
            case "6":
                return random.betavariate(0.5,0.5)
            case "7":
                return random.gammavariate(3,2)
            case "8":
                return random.paretovariate(1)
            case "9":
                return random.weibullvariate(1,1.5)

    def check_wall_3D(self,colors,ax,ax_x,ax_y,ax_z,x,y,z,ite):
        def draw_wall(ax_):
            ax_.axhline(y = self.wall, color = 'r', linestyle = 'dashed')   
            ax_.axhline(y = -self.wall, color = 'r', linestyle = 'dashed')
        def split_3d(t,main,other1,other2):
            self.split_main(main,colors)
            self.split_other(t,other1)
            self.split_other(t,other2)
            self.split_other(t,ite)
            ax.plot(x[-2],y[-2],z[-2],c=colors[-1])
            ax_x.plot(ite[-2],x[-2],c=colors[-1])
            ax_y.plot(ite[-2],y[-2],c=colors[-1])
            ax_z.plot(ite[-2],z[-2],c=colors[-1])
        if(self.wall!=0):
            draw_wall(ax_x)
            draw_wall(ax_y)
            draw_wall(ax_z)
            if(x[-1][1]>self.wall or x[-1][1]<-self.wall) and (y[-1][1]>self.wall or y[-1][1]<-self.wall) and (z[-1][1]>self.wall or z[-1][1]<-self.wall):
                t_x=self.get_t(x)
                t_y=self.get_t(y)
                t_z=self.get_t(z)
                if (t_x<t_y and t_x<t_z):
                    split_3d(t_x,x,y,z)
                elif(t_y<t_x and t_y<t_z):
                    split_3d(t_y,y,x,z)
                else:
                    split_3d(t_z,z,x,y)
                self.check_wall_3D(colors,ax,ax_x,ax_y,ax_z,x,y,z,ite)
            if((x[-1][1]>self.wall or x[-1][1]<-self.wall) and (y[-1][1]>self.wall or y[-1][1]<-self.wall)):
                t_x=self.get_t(x)
                t_y=self.get_t(y)
                if t_x<t_y:
                    split_3d(t_x,x,y,z)
                else:
                    split_3d(t_y,y,x,z)
                self.check_wall_3D(colors,ax,ax_x,ax_y,ax_z,x,y,z,ite)
            elif((x[-1][1]>self.wall or x[-1][1]<-self.wall) and (z[-1][1]>self.wall or z[-1][1]<-self.wall)):
                t_x=self.get_t(x)
                t_z=self.get_t(z)
                if t_x<t_z:
                    split_3d(t_x,x,y,z)
                else:
                    split_3d(t_z,z,x,y)
                self.check_wall_3D(colors,ax,ax_x,ax_y,ax_z,x,y,z,ite)
            elif((y[-1][1]>self.wall or y[-1][1]<-self.wall) and (z[-1][1]>self.wall or z[-1][1]<-self.wall)):
                t_y=self.get_t(y)
                t_z=self.get_t(z)
                if t_y<t_z:
                    split_3d(t_y,y,x,z)
                else:
                    split_3d(t_z,z,x,y)
                self.check_wall_3D(colors,ax,ax_x,ax_y,ax_z,x,y,z,ite)
            if(x[-1][1]>self.wall or x[-1][1]<-self.wall):
                t= self.get_t(x)
                split_3d(t,x,y,z)
                self.check_wall_3D(colors,ax,ax_x,ax_y,ax_z,x,y,z,ite)
            elif(y[-1][1]>self.wall or y[-1][1]<-self.wall):
                t= self.get_t(y)
                split_3d(t,y,x,z)
                self.check_wall_3D(colors,ax,ax_x,ax_y,ax_z,x,y,z,ite)
            elif(z[-1][1]>self.wall or z[-1][1]<-self.wall):
                t= self.get_t(z)
                split_3d(t,z,x,y)
                self.check_wall_3D(colors,ax,ax_x,ax_y,ax_z,x,y,z,ite)
        
    def check_wall(self, colors, dimension, ax, x,y):
        if self.wall!=0:
            ax.axhline(y = self.wall, color = 'r', linestyle = 'dashed')   
            ax.axhline(y = -self.wall, color = 'r', linestyle = 'dashed')
            if dimension==1:
                if(y[-1][1]>self.wall or y[-1][1]<-self.wall):
                    print("x",x[-1])
                    print("y",y[-1])
                    t= self.get_t(y)
                    print("t=",t)
                    self.split_main(y,colors)
                    self.split_other(t,x)
                    print("x",x[-2],x[-1])
                    print("y",y[-2],y[-1])
                    ax.plot(x[-2],y[-2],c=colors[-1])
                    self.check_wall(colors,1,ax,x,y)
            if dimension ==2:
                ax.axvline(x = self.wall, color = 'r', linestyle = 'dashed')   
                ax.axvline(x = -self.wall, color = 'r', linestyle = 'dashed')
                if((x[-1][1]>self.wall or x[-1][1]<-self.wall) and (y[-1][1]>self.wall or y[-1][1]<-self.wall)):
                    t_x=self.get_t(x)
                    t_y=self.get_t(y)
                    if t_x<t_y:
                        self.split_main(x,colors)
                        self.split_other(t_x,y)
                    else:
                        self.split_main(y,colors)
                        self.split_other(t_y,x)

                    ax.plot(x[-2],y[-2],c=colors[-1])    
                    self.check_wall(colors,2,ax,x,y)
                            
                if (y[-1][1]>self.wall or y[-1][1]<-self.wall):
                    t= self.get_t(y)
                    self.split_main(y,colors)
                    self.split_other(t,x)
                    ax.plot(x[-2],y[-2],c=colors[-1])
                    self.check_wall(colors,2,ax,x,y)

                elif(x[-1][1]>self.wall or x[-1][1]<-self.wall):
                    t= self.get_t(x)
                    self.split_main(x,colors)
                    self.split_other(t,y)
                    ax.plot(x[-2],y[-2],c=colors[-1])
                    self.check_wall(colors,2,ax,x,y)

    def get_t(self,y):
        a, b =self.function([0,1],y)
        y2=y[-1][1]
        if(y2<self.wall):
            self.wall=-self.wall
        t=(self.wall-b)/a
        if(y2<self.wall):
            self.wall=-self.wall
        return t
        
    def split_main(self, y, colors):
        y1,y2=y[-1][0],y[-1][1]
        colors.append(colors[-1])
        if(y2<self.wall):
            self.wall=-self.wall
        y.pop()
        y.append((y1,self.wall))
        y.append((self.wall,self.wall-(y2-self.wall)))
        if(y2<self.wall):
            self.wall=-self.wall

    def split_other(self, t, x):
        a, b= self.function([0,1],x)
        x1,x2,=x[-1][0],x[-1][1]
        hitpoint=a*t+b
        x.pop()
        x.append((x1,hitpoint))
        x.append((hitpoint,x2))

    def function(self,x,y):
        x1,x2,y1,y2=x[0],x[1],y[-1][0],y[-1][1]
        if x2-x1==0:
            x2+=0.000001
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return a,b

    def toggle_pause(self,animation):
        if self.paused:
            self.ani.resume()
        else:
            self.ani.pause()
        self.paused = not self.paused

    def new_subplot(self,position,label,fig):
        ax = fig.add_subplot(position)
        ax.set_ylabel(label)
        ax.set_xlabel("i")
        ax.grid(True)
        point,=ax.plot(0,0,marker="o",c="black")
        return ax, point,

    def select(self):
        dimension=0
        while dimension not in ["1","2","3"]:
            dimension=input("Choose dimension (1,2,3): ")
        while self.randomly not in ["1","2","3","4","5","6","7","8","9","10"]:
            self.randomly = input("Choose random (1:fractional, 2:random, 3:point, 4:normal, 5:log, 6:beta, 7:gamma, 8:pareto, 9:weibull): ")
        if self.randomly=="1":
            while self.hurst <=0 or self.hurst>=1:
                self.hurst=float(input("Select Hurst parameter (0-1)[float]:"))

        match dimension:
            case "1":
                self.OneD()
            case "2":
                self.TwoD()
            case "3":
                self.ThreeD()
            case "test":
                self.test()

bm=BrownAnimation()
bm.select()

