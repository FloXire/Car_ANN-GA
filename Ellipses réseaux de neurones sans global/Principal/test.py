"""'''
Created on 29 deSc. 2017

@author: flo-1
'''


from matplotlib import patches
from matplotlib import pyplot
import matplotlib
pyplot.axis('equal')
figure = pyplot.figure(figsize = (10, 10))
# suppression des marges
figure.subplots_adjust(0, 0, 1, 1)
axes = figure.add_subplot(111)

# pas de cadre
axes.set_frame_on(False)
# pas de graduations d'axes
axes.xaxis.set_visible(False)
axes.yaxis.set_visible(False)
axes.add_artist(
    patches.Rectangle((0.2, 0.2), 0.4, 0.3,
                      edgecolor = 'black', facecolor = 'orange',
                      fill = True, hatch = '/', linestyle = 'dashed',
                      linewidth = 3, zorder = 1))
axes.add_artist(
    patches.Rectangle((0.4, 0.4), 0.5, 0.2,
                      edgecolor = 'black', facecolor = 'pink',
                      fill = True, hatch = '|', linestyle = 'dashdot',
                      linewidth = 3, alpha = 0.7, zorder = 3))
axes.add_artist(
    patches.Circle((0.5, 0.6), 0.15, color = 'cyan', zorder = 2))
axes.add_artist(
    patches.Ellipse((0.2, 0.7), 0.3, 0.2, 45,
                    edgecolor = 'magenta', facecolor = 'yellow', zorder = 2))
axes.add_artist(
    patches.Arc((0.7, 0.7), 0.3, 0.2, 20, 0, 120, color = 'red', linewidth = 5))


pyplot.show()"""

a = [i for i in range(10)]
a *= 2
print a