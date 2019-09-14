#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:29:38 2019
@author: pedro

"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import cPickle as pickle
import bz2 as bzip
import itertools

import statsmodels as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats import multitest

def statsmodel_anova(df, query):
    model_lm = ols(query, data=df).fit()
    table = anova_lm(model_lm, typ=2) # Type 2 ANOVA DataFrame
    return table

def run_anova_df(df, var, genotype):
    anova_query = var + ' ~ C('+genotype+')'    
    return statsmodel_anova(df, anova_query)
    
def t_test_df(df, y_var, x_var, groups):
    combinations = list(itertools.combinations(groups, 2))
    t_tests = []
    for combination in combinations:
        t_tests.append(('%s vs. %s'%(combination[0], combination[1]), combination,  stats.ttest_ind(df.query(x_var +' == "'+combination[0]+'"')[y_var], 
                                             df.query(x_var +' == "'+combination[1]+'"')[y_var])))
    return t_tests


class AnnotatedPlots:
    """
    Class for plotting violin plots with annotation on p-values
    
    
    Methods:
    --------    
    violin_plot_df(df, y_var, x_var, order=None, title=None, xlabel=None, ylabel=None, plot_id=None, x_labels=None)
        Generates a violinplot with the p-value annotations on it.       
            
    """
    
    def __init__(self):
        pass
    
    def plot_annotated_graph(self, df, y_var, x_var, order=None, title=None, xlabel=None, ylabel=None, plot_id=None, x_ticks=None, font_scale=1.3, plot_function=sns.violinplot, plot_args={}):
        """
        Generates a graph with the p-value annotations on it.
        
        Parameters
        -----------        
        df : pandas.DataFrame
            dataframe with the data to plot.
        y_var : String
            name of the column to be plotted on the Y-Axis
        x_var : String
            name of the column to be plotted on the X-Axis
        order : array, optional
            Order in which the X-Axis columns should be displayed. If None, it will use the default ordenation.
            `Note: the array should contain all the unique elements (pd.Series.unique()) of the dataframe column named by x_var.`
        title : String, optional
            The title of the plot. If not defined, the plot will have no title.
        xlabel : String, optional
            The name of the x-axis. If not defined, the x-axis will be named after the x_var variable.
        ylabel : String, optional
            The name of the y-axis. If not defined, the y-axis will be named after the y_var variable.
        plot_id : String, optional
            The ID of the plot, to be printed on the upper left corner (usually represented by one letter or number, e.g., A, B, C, etc). If not defined, the plot will not have any identification printed on the corner.
        x_ticks : array, optional
            If defined, will replace the ticks in the x-axis by the items in this list (in order).
            Note: x_ticks must have the same size of the number of items in the x-axis.
        font_scale: float, optional
            scaling factor for the "font_size" attribute on seaborn. Default 1.1 .
        plot_function : function, optional
            Defines the function used to generate the graphs. This function is still experimental and its default value is seaborn.violinplot.
        plot_args : dict, optional
            Defines the additional arguments from the curent plot_function to be used on the plot function.
        Returns
        -------
        g : matplotlib.axes._subplots.AxesSubplot
            Violin plot with the annotations.
        anova : pandas.DataFrame
            Dataframe with the results of the anova test
        t_tests : list
            List of post-hoc T-tests for all categories
            
        """
        # Increase overall fontsize
        sns.set(font_scale = font_scale)        
        sns.set_style("ticks")
        # Check for integrity in order:
        if order != None:
            if not np.all([i in df[x_var].unique() for i in pd.Series(order).unique()]) or len(df[x_var].unique()) != len(pd.Series(order).unique()):
                raise Exception('The list of order of the elements must contain all unique elements from the X-Axis variable')
        else:
            order = df[x_var].unique()
        # Check for integrity in x_ticks
        if x_ticks != None:
            if len(x_ticks) != len(df[x_var].unique()):
                raise Exception('x_ticks must be of the same size of the items in the x-axis')
        
        # Instantiate the figure
        plt.figure()
        g = plot_function(data=df, x=x_var, y=y_var, order=order, **plot_args)
        
        # Apply the defined x_ticks
        if x_ticks != None:
            g.set(xticklabels=x_ticks)
        
        # remove the top and right axis
        g.spines['right'].set_visible(False)
        g.spines['top'].set_visible(False)
        
        # get the x and y-axis limits
        ylim = g.get_ylim()[1]
        xlim = g.get_xlim()[1]
        
        # get the distance from bottom to upper limit of each axis
        dist_y = g.get_ylim()[1] - g.get_ylim()[0]
        #dist_x = g.get_xlim()[1] - g.get_xlim()[0]
        
        # print the ANOVA test results
        # TODO: find a way of printing it ON the violinplot
        t_tests = t_test_df(df, y_var, x_var, groups=order)
        anova = run_anova_df(df, y_var, x_var)
        print 'ANOVA for %s (%s): %.3f' % (x_var, y_var, anova['PR(>F)'].values[0])
    
        # Plot the statistical annotation for combinations on the graph
        for ti, t in enumerate(t_tests):            
            # Format the p-value for plotting
            p_value = t[2][1]
            if p_value > 0.05:
                p_value = "n.s" # non-significant
            elif p_value < 0.001:
                p_value = '0.001' # if below 0.001, leaves it as 0.001
            else:
                p_value = format(np.around(p_value, 3))
            
            # Define the postion of x1 and x2 on the graph to plot the bracket
            x1 = int([i for i, group in enumerate(order) if group == t[1][0]][0])
            x2 = int([i for i, group in enumerate(order) if group == t[1][1]][0])
            
            factor = (x2 - x1)
            
            # Define the height of the bracket    
            h = dist_y*0.08
            
            # Define the y position of the bracket base
            y = ylim - dist_y*0.1
                    
            # Define the color of the bracket (black)
            col = 'k'
            
            g.plot([x1+xlim*0.01, x1+xlim*0.01, x2-xlim*0.01, x2-xlim*0.01], 
                    [y+h*0.5+(factor*1.4*h), y+h+(factor*1.4*h), y+h+(factor*1.4*h), y+h*0.5+(factor*1.4*h)], lw=1, c=col)
            g.plot((x2+x1)*0.5, y+h+(factor*1.7*h))                        
            g.text((x2+x1)*0.5,y+h+(factor*1.4*h), 'p=%s'%p_value, ha='center', va='bottom', color=col)    
        
        if title != None and False:
            g.set_title(title)
        if xlabel != None:
            g.set_xlabel(xlabel)
        if ylabel != None:
            g.set_ylabel(ylabel)
        if plot_id != None:
            g.text(-0.05, 1.05, plot_id, fontsize=14, transform=g.transAxes)
        return g, anova, t_tests