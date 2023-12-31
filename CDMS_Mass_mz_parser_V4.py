# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 14:01:12 2022

@author: cleary.186
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:22:51 2021

@author: cleary.186
"""

#import glob as glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from matplotlib.patches import Rectangle
from matplotlib.widgets import SpanSelector
import argparse

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list           

def zero_charge(mass_axis,x,y,cs):
    """
    Steps
    1. create x_axis outside this function
    2. interpolate y values
    3. return y_list
    """
    mass_y = []
    y_full = np.zeros(len(mass_axis))
    for i in range(len(cs)):
        y_temp1 = []
        y_temp2 = []
        real_axis = []
        final = []
        finall = []
        for j in range(len(x[i])):
            x[i][j] = x[i][j]*cs[i]
        for j in range(len(mass_axis)):
            if mass_axis[j]<x[i][0]:
                y_temp1.append(0)
            elif mass_axis[j]>x[i][-1]:
                y_temp2.append(0)
            elif mass_axis[j] > x[i][0] and mass_axis[j] <x[i][-1]:
                real_axis.append(mass_axis[j])   
        temp = np.interp(real_axis,x[i],y[i])
        final.append(y_temp1)
        final.append(temp)
        final.append(y_temp2)
        for j in range(len(final)):
            for k in range(len(final[j])):
                finall.append(final[j][k])
                
        mass_y.append(finall)
    
    for i in range(len(mass_y)):
        for j in range(len(mass_y[i])):
            y_full[j] = y_full[j] + mass_y[i][j]
        
    return y_full
    
    
def cs_finder(x,cs_list):
    """
    Steps:
    1. Multiply each max by adjacent charge states
    2. calaulate the mean and standard deviation
    3. find the lowest deviation.  This is the assinged charge states
    4. return the charge states
    """
    max_len = len(x)
    stdev = []
    if max_len == 1:
        return stdev
    else:
        for i in range(len(cs_list)-max_len+1):
            if max_len == 1:
                continue
            else:
                cs_check = np.linspace(i+1,i+max_len,max_len)
                stdev_temp = []
                for j in range(len(cs_check)):
                    stdev_temp.append(cs_check[j]*x[j])
                stdev.append([np.std(stdev_temp),cs_check])
        min_int = 0
        for i in range(len(stdev)):
            if stdev[i][0] < stdev[min_int][0]:
                min_int = i
            else:
                continue
        return stdev[min_int][1]
 
    
def line_select_callback(eclick, erelease):
    toggle_selector.RS.x1, toggle_selector.RS.y1 = eclick.xdata, eclick.ydata
    toggle_selector.RS.x2, toggle_selector.RS.y2 = erelease.xdata, erelease.ydata
    

def toggle_selector(event):
    if toggle_selector.RS.x1 < toggle_selector.RS.x2:
        x1 = toggle_selector.RS.x1
        x2 = toggle_selector.RS.x2
    if toggle_selector.RS.y1 < toggle_selector.RS.y2:
        y1 = toggle_selector.RS.y1
        y2 = toggle_selector.RS.y2
    if toggle_selector.RS.x2 < toggle_selector.RS.x1:
        x2 = toggle_selector.RS.x1
        x1 = toggle_selector.RS.x2
    if toggle_selector.RS.y2 < toggle_selector.RS.y1:
        y2 = toggle_selector.RS.y1
        y1 = toggle_selector.RS.y2
    
    if event.key == 'enter':
    
        rec = Rectangle((x1,y1), (x2-x1),(y2-y1), edgecolor='r', 
                        fc='None', lw=2)
        
        ax1.add_patch(rec)
        plt.draw()
    
    if event.key == "p":
        #yedges is m/z axis, xedges is mass axis
        heatmap_new = heatmap*0
        for i in range(len(yedges)):
            for j in range(len(xedges)):
                if yedges[i] > x1 and yedges[i] < x2 and xedges[j] > y1 and xedges[j]<y2:
                    heatmap_new[j][i] = heatmap[j][i]
        
        toggle_selector.y_axis = np.zeros(len(yedges))
        for i in range(len(yedges)-1):
            value = 0
            for j in range(len(xedges)-1):
                value += heatmap_new[j][i]
            toggle_selector.y_axis[i] = value
        
        ax2.plot(yedges,toggle_selector.y_axis)
        plt.draw()



def onselect(xmin, xmax):
    temp_list_x = []
    temp_list_y = []
    
    
    for i in range(len(yedges)):
        if yedges[i] > xmin and yedges[i] < xmax:
            temp_list_x.append(yedges[i])
            temp_list_y.append(toggle_selector.y_axis[i])
    ax2.plot(temp_list_x,temp_list_y, color = 'r')
    x_plots.append(temp_list_x)
    y_plots.append(temp_list_y)
    max_tupple = list(np.where(temp_list_y == max(temp_list_y)))
    max_value = max_tupple[0]
    max_list.append(temp_list_x[max_value[0]])
    cs = cs_finder(max_list, cs_range)
    mass_y = zero_charge(mass_axis,x_plots,y_plots,cs)
    if len(cs) > 0:
        ax3.cla()
        ax3.plot(mass_axis,mass_y)
    plt.draw()


    
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default='all')
parser.add_argument('-bmz', '--bins_mz', default = 300)
parser.add_argument('-bm', '--bins_mass', default = 30)
parser.add_argument('-bz', '--bins_charge', default = 300)
parser.add_argument('-sf', '--smooth_function', default = 'gaussian')
#parser.add_argument('-m', '--slope', required = True)
#Please input a calibration coefficient from calibration curve, which is instrument dependednt
parser.add_argument('-m', '--slope', default = 49051.84)
args = parser.parse_args()

args.bins_mz = int(args.bins_mz)
args.bins_mass = int(args.bins_mass)
args.bins_slope = int(args.bins_charge)
slope_convert = float(args.slope)


#files = glob.glob("*.csv")
#df = pd.read_csv(files[0])

files = input("Enter file name:")+".csv"
df = pd.read_csv(files)

#for i in range(1,len(files)):
#    df_temp = pd.read_csv(files[i], delimiter='\t')
#    df = [df,df_temp]
#    df = pd.concat(df)

df = df.loc[df['RSquared'] >= 0.99]
df = df.loc[df['TimeOfBirth'] <= 0.1]
#df = df.loc[df['Time of Death'] <= 1.8]
#df.to_csv('Full_dataframe.csv')
charge = np.array(df["Slope"])/slope_convert
slope = np.array(df["Slope"])
mz_axis = np.array(df["Mz"])
mass = np.array(df["Mz"]) * charge/1000
#frequency = np.array(df["Frequency"])

np.savetxt("unidec_file.txt", np.c_[mz_axis,slope])

heatmap, xedges, yedges = np.histogram2d(mass, mz_axis, 
                                         bins=[args.bins_mass, args.bins_mz])

#fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
fig4, ax4 = plt.subplots(1)
fig2, ax2 = plt.subplots(1)
fig3, ax3 = plt.subplots(1)
fig1, ax1 = plt.subplots(1)

ax1.imshow(heatmap, aspect = 'auto', vmax = 50, origin = 'lower',
               cmap = 'jet', interpolation= args.smooth_function,
               extent=[yedges[0], yedges[-1], xedges[0],xedges[-1]])
line2, = ax3.plot([], [])
span = SpanSelector(
    ax2,
    onselect,
    "horizontal",
    useblit=True
)

ax1.set_xlabel('m/z')
ax1.set_ylabel('mass (kDa)')

y_axis = np.zeros(len(yedges))
max_list = []
x_plots = []
y_plots = []
cs_range = np.linspace(1,100,100)
mass_axis = np.arange(0,np.ceil(yedges[-1]*100),10)
print(mass_axis)
toggle_selector.RS = RectangleSelector(ax1, line_select_callback,
                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
plt.connect('key_press_event', toggle_selector)


plt.show()
