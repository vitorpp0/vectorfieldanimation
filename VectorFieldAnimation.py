from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import math
import numpy as np

class VectorFieldAnimation():

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
        self.gradient = self._setGradient()
        self.frameParameters = self._determineFrameParameters()

        # Sets the figures instances
        self.fig, self.ax, self.vectorField = (0,)*3
        self._set_figure(title)

        # Animation variable
        self.animation = 'No animation has been instantiated yet.'

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
        self.fig.colorbar(self.vectorField)
    
    def _determineFrameParameters(self):
        frameParameters = []
        for frame in np.arange(start=0.002,stop=self.animationDuration*self.frameRate, step=1):
            time = frame/self.frameRate
            u = self.U(time, self.x, self.y, self.z),
            v = self.V(time, self.x, self.y, self.z)
            w = self.W(time, self.x, self.y, self.z)
            colorMap = self._colorByNorm(u,v,w)
            frameParameters.append([u,v,w,colorMap])
        return frameParameters

    def _setGradient(self):
        rgbGradient = [
            [125,71,144,1],[121,71,152,1],[114,71,153,1],[105,73,152,1],[104,73,151,1],[97,72,153,1],
            [92,76,151,1],[88,76,150,1],[79,75,151,1],[75,75,151,1],[69,77,151,1],[58,77,153,1],[51,79,151,1],
            [46,80,154,1],[46,80,152,1],[45,81,155,1],[46,80,151,1],[47,79,153,1],[43,84,150,1],[36,89,157,1],
            [15,99,164, 1],[15,100,164,1],[8,107,166,1],[12,113,165,1],[14,117,176,1],
            [12,126,180,1],[12,130,183,1],[14,136,183,1],[12,146,190,1],
            [12,164,190,1],[12,176,190,1],[12,190,182,1],[12,190,154,1],
            [12,190,137,1],[13,189,114,1],[14,188,88,1],[13,189,52,1],[13,189,26,1],
            [20,190,12,1],[48,189,13,1],[69,191,11,1],[83,190,12,1],[105,192,10,1],
            [138,193,9,1],[156,193,9,1],[168,190,12,1],[186,201,1,1],[194,200,2,1],
            [200,185,2,1],[200,170,2,1],[200,155,2,1],[201,171,1,1],[201,151,1,1],
            [201,131,1,1],[200,121,2,1],[201,86,1,1],[200,62,2,1],[201,46,1,1],[200,41,2,1],
            [198,33,4,1],[198,23,4,1],[198,14,4,1],[200,10,4,1], [220, 0, 0, 1], [230, 0, 0, 1],
            [240, 0, 0, 1],[245, 0, 0, 1],[250, 0, 0, 1], [255, 0, 0, 1]
            ]
        gradient = np.zeros((1,4))
        gradient = np.append(gradient, rgbGradient, axis=0)
        gradient = np.delete(gradient, 0, 0)
        gradient = gradient/255
        gradient[:,3] = 1
        return gradient
        
    def _setColor(self, value):
        colors = self.gradient.shape[0]-1
        color = math.floor(value*colors)
        if color > colors:
            print('Error, color bigger than 1')
        else:
            return self.gradient[color]
    
    def _colorByNorm(self, u, v, w):
        lengthArray = np.sqrt(np.power(u,2) + np.power(v,2) + np.power(w,2)).ravel()
        notZeroLengthArray = lengthArray[np.abs(lengthArray)>0]
        values = (notZeroLengthArray-notZeroLengthArray.min())/notZeroLengthArray.ptp()
        values = np.concatenate((values, np.repeat(values, 2)))
        colorMap = np.zeros((values.shape[0],4))
        for element in range(0, values.shape[0]):
            colorMap[element] = self._setColor(values[element])
        return colorMap

    def _update(self, frame):
        u,v,w,c = self.frameParameters[int(frame)]
        self.vectorField.remove()
        self.ax.set_title("Timer:{:0.2f} s".format(frame/self.frameRate))
        self.vectorField = self.ax.quiver(self.x,self.y,self.z,u,v,w,colors=c,length=self.length, normalize=True)
        return self.vectorField

    def animate(self):
        self.animation = ani.FuncAnimation(self.fig, self._update, blit=False,
                                    frames=np.arange(start=1,stop=self.animationDuration*self.frameRate, step=1))
        plt.show()
