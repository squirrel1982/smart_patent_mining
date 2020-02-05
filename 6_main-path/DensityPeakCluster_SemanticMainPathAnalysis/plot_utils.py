#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.pyplot as plt


def plot_scatter_diagram(which_fig, x, y, index,x_label='x', y_label='y', title='title', style_list=None):
    '''
    Plot scatter diagram

    Args:
            which_fig  : which sub plot
            x          : x array
            y          : y array
            x_label    : label of x pixel
            y_label    : label of y pixel
            title      : title of the plot
    '''
    xs_tmp = []
    ys_tmp = []
    styles = ['k.', 'gs', 'rs', 'cs', 'ms', 'ys', 'bs','b,','g,']
    assert len(x) == len(y)
    if style_list is not None:
        assert len(x) == len(style_list) and len(
            styles) >= len(set(style_list))
    #fig, ax = plt.subplots(figsize=(14, 7))
    plt.figure(which_fig,figsize=(10,10))
    plt.clf()
    if style_list is None:
        plt.plot(x, y, styles[0])
    else:
        clses = set(style_list)
        xs, ys = {}, {}
        for i in xrange(len(x)):
            try:
                xs[style_list[i]].append(x[i])
                ys[style_list[i]].append(y[i])
            except KeyError:
                xs[style_list[i]] = [x[i]]
                ys[style_list[i]] = [y[i]]
        added = 1
        for idx, cls in enumerate(clses):
            if cls == -1:
                style = styles[0]
                added = 0
            else:
                style = styles[idx + added]
                xs_tmp.append(xs[cls])
                ys_tmp.append(ys[cls])
            plt.plot(xs[cls], ys[cls], style)
        #plt.plot(xs_tmp, ys_tmp, 'r-')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    #plt.ylim(bottom=0)
    #plt.show()
    plt.savefig('image_cluster_based_mainPath_lenWeight_'+str(index)+'_denWeight_1.png')

def plot_scatter_diagram_raw(which_fig, x, y,x_label='x', y_label='y', title='title', style_list=None):
    '''
    Plot scatter diagram

    Args:
            which_fig  : which sub plot
            x          : x array
            y          : y array
            x_label    : label of x pixel
            y_label    : label of y pixel
            title      : title of the plot
    '''
    xs_tmp = []
    ys_tmp = []
    styles = ['k.', 'g.', 'r.', 'c.', 'm.', 'y.', 'b.','b,','g,']
    assert len(x) == len(y)
    if style_list is not None:
        assert len(x) == len(style_list) and len(
            styles) >= len(set(style_list))
    plt.figure(which_fig,figsize=(7,4))
    plt.clf()
    if style_list is None:
        plt.plot(x, y, styles[0])
    else:
        clses = set(style_list)
        xs, ys = {}, {}
        for i in xrange(len(x)):
            try:
                xs[style_list[i]].append(x[i])
                ys[style_list[i]].append(y[i])
            except KeyError:
                xs[style_list[i]] = [x[i]]
                ys[style_list[i]] = [y[i]]
        added = 1
        for idx, cls in enumerate(clses):
            if cls == -1:
                style = styles[0]
                added = 0
            else:
                style = styles[idx + added]
                xs_tmp.append(xs[cls])
                ys_tmp.append(ys[cls])
            plt.plot(xs[cls], ys[cls], style)
        #plt.plot(xs_tmp, ys_tmp, 'r-')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    #plt.ylim(bottom=0)
    #plt.show()
    plt.savefig('decision_graph.png')



def arrowplot(axes, x, y, narrs=30, dspace=0.5, direc='pos', \
                          hl=0.3, hw=6, c='black'):
    ''' narrs  :  Number of arrows that will be drawn along the curve

        dspace :  Shift the position of the arrows along the curve.
                  Should be between 0. and 1.

        direc  :  can be 'pos' or 'neg' to select direction of the arrows

        hl     :  length of the arrow head

        hw     :  width of the arrow head

        c      :  color of the edge and face of the arrow head
    '''

    # r is the distance spanned between pairs of points
    r = [0]
    for i in range(1,len(x)):
        dx = x[i]-x[i-1]
        dy = y[i]-y[i-1]
        r.append(np.sqrt(dx*dx+dy*dy))
    r = np.array(r)

    # rtot is a cumulative sum of r, it's used to save time
    rtot = []
    for i in range(len(r)):
        rtot.append(r[0:i].sum())
    rtot.append(r.sum())

    # based on narrs set the arrow spacing
    aspace = r.sum() / narrs

    if direc is 'neg':
        dspace = -1.*abs(dspace)
    else:
        dspace = abs(dspace)

    arrowData = [] # will hold tuples of x,y,theta for each arrow
    arrowPos = aspace*(dspace) # current point on walk along data
                                 # could set arrowPos to 0 if you want
                                 # an arrow at the beginning of the curve

    ndrawn = 0
    rcount = 1
    while arrowPos < r.sum() and ndrawn < narrs:
        x1,x2 = x[rcount-1],x[rcount]
        y1,y2 = y[rcount-1],y[rcount]
        da = arrowPos-rtot[rcount]
        theta = np.arctan2((x2-x1),(y2-y1))
        ax = np.sin(theta)*da+x1
        ay = np.cos(theta)*da+y1
        arrowData.append((ax,ay,theta))
        ndrawn += 1
        arrowPos+=aspace
        while arrowPos > rtot[rcount+1]:
            rcount+=1
            if arrowPos > rtot[-1]:
                break

    # could be done in above block if you want
    for ax,ay,theta in arrowData:
        # use aspace as a guide for size and length of things
        # scaling factors were chosen by experimenting a bit

        dx0 = np.sin(theta)*hl/2. + ax
        dy0 = np.cos(theta)*hl/2. + ay
        dx1 = -1.*np.sin(theta)*hl/2. + ax
        dy1 = -1.*np.cos(theta)*hl/2. + ay

        if direc is 'neg' :
          ax0 = dx0
          ay0 = dy0
          ax1 = dx1
          ay1 = dy1
        else:
          ax0 = dx1
          ay0 = dy1
          ax1 = dx0
          ay1 = dy0

        axes.annotate('', xy=(ax0, ay0), xycoords='data',
                xytext=(ax1, ay1), textcoords='data',
                arrowprops=dict( headwidth=hw, frac=1., ec=c, fc=c))


    axes.plot(x,y, color = c)
    axes.set_xlim(x.min()*.9,x.max()*1.1)
    axes.set_ylim(y.min()*.9,y.max()*1.1)

def plot_scatter_diagram_20_loop_center_combined( x, y,x_label='x', y_label='y', title='title', style_list=None):
    '''
    Plot scatter diagram

    Args:
            x          : x array
            y          : y array
            x_label    : label of x pixel
            y_label    : label of y pixel
            title      : title of the plot
    '''

    styles = ['k.', 'go-', 'ro-', 'bo-', 'co-', 'mo-', 'yo-','wo-,','g,']
    assert len(x) == len(y)
    tmp = []
    tmp_1 = []
    for index,i in enumerate(style_list):
        for index_1,j in enumerate(i):
            if index_1==0:
                tmp.append(j)
            else:
                if style_list[index][index_1]==style_list[index][index_1-1]:
                    pass
                else:
                    tmp.append(j)
        tmp_1.append(tmp)
        tmp = []
    style_list = tmp_1
    if style_list is not None:
        assert len(styles) >= len(style_list)

    #fig, ax = plt.subplots(figsize=(14, 7))
    plt.figure(1,figsize=(10,6))
    plt.clf()
    if style_list is None:
        plt.plot(x, y, styles[0])
    else:

        xs, ys = {}, {}
        for i in xrange(len(x)):
            try:
                xs[-1].append(x[i])
                ys[-1].append(y[i])
            except KeyError:
                xs[-1] = [x[i]]
                ys[-1] = [y[i]]
        style = styles[0]
        #plt.plot(xs[-1], ys[-1], style)

        for index,i in enumerate(style_list):
            xs_tmp = []
            ys_tmp = []
            for j,k in i:
                xs_tmp.append(j)
                ys_tmp.append(k)
            plt.plot(xs_tmp, ys_tmp, styles[index+1])

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    #plt.ylim(bottom=0)
    #plt.show()
    plt.savefig('image_draw_100_withoutBackground_loop_center_combine.png')

if __name__ == '__main__':
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 7, 7])
    y = np.array([2, 3, 4, 5, 6, 2, 4, 8, 5, 6])
    cls = np.array([1, 4, 2, 3, 5, -1, -1, 6, 6, 6])
    plot_scatter_diagram(0, x, y, style_list=cls)
