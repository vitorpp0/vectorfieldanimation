from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np

class vectorFieldAnimation():

    def __init__(self, space=[np.arange(-2, 2, 0.5), np.arange(-2, 2, 0.5), np.arange(-2, 2, 0.5)],
                     vectorComponents=["4*time*x", "-2*(time**2)*y", "4*np.multiply(x,z)"], animationDuration= 3, frameRate= 30,
                     title=r"$ Field: \overrightarrow{V} = 4tx\hat{\bf{i}} -2ty\hat{\bf{j}} +4xz\hat{\bf{k}}$", length=0.2):
        # Declares the space parameters
        self.x, self.y, self.z = (0,)*3
        self.U, self.V, self.W = (0,)*3
        self._set_space(space, vectorComponents)
        self.length = length
        
        # Sets the space parameters
        self.frameRate, self.animationDuration = frameRate, animationDuration

        # Sets the parameters frames
        self.frameParameters = self._determineFrameParameters()

        # Sets the figures instances
        self.fig, self.ax, self.vectorField = (0,)*3
        self._set_figure(title)

        # Animation variable
        self.animation = 0

    def _set_space(self, space, vectorComponents):
        self.x, self.y, self.z = np.meshgrid(space[0], space[1], space[2])
        self.U = eval('lambda time, x, y, z:' + vectorComponents[0])
        self.V = eval('lambda time, x, y, z:' + vectorComponents[1])
        self.W = eval('lambda time, x, y, z:' + vectorComponents[2])

    def _set_figure(self, title):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.suptitle(title)
        self.ax.set_xlabel(r'X axis($\hat{\bf{i}}$)')
        self.ax.set_ylabel(r'Y axis($\hat{\bf{j}}$)')
        self.ax.set_zlabel(r'Z axis($\hat{\bf{k}}$)')
        u, v, w, c = self.frameParameters[0]
        self.vectorField = self.ax.quiver(self.x,self.y,self.z,u,v,w,colors=c,length=self.length, normalize=True)
    
    def _determineFrameParameters(self):
        frameParameters = []
        for frame in np.arange(start=0,stop=self.animationDuration*self.frameRate, step=1):
            time = frame/self.frameRate
            u = self.U(time, self.x, self.y, self.z),
            v = self.V(time, self.x, self.y, self.z)
            w = self.W(time, self.x, self.y, self.z)
            colorMap = self._colorByNorm(u,v,w)
            frameParameters.append([u,v,w,colorMap])
        return frameParameters

    def _colorByNorm(self, u, v, w):
        lengthArray = np.sqrt(np.power(u,2) + np.power(v,2) + np.power(w,2)).ravel()
        notZeroLengthArray = lengthArray[np.abs(lengthArray)>0]
        colorMap = (notZeroLengthArray-notZeroLengthArray.min())/notZeroLengthArray.ptp()
        colorMap = np.concatenate((colorMap, np.repeat(colorMap, 2)))
        return plt.cm.jet(colorMap)

    def _update(self, frame):
        u,v,w,c = self.frameParameters[frame]
        self.vectorField.remove()
        self.ax.set_title("Timer:{:0.2f} s".format(frame/self.frameRate))
        self.vectorField = self.ax.quiver(self.x,self.y,self.z,u,v,w,colors=c,length=self.length, normalize=True)
        return self.vectorField

    def animate(self):
        self.animation = ani.FuncAnimation(self.fig, self._update, blit=False,
                                      frames=np.arange(start=1,stop=self.animationDuration*self.frameRate, step=1))
        plt.show()

