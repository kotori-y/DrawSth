# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:41:19 2019

@Author: Zhi-Jiang Yang, Guo-Li Xiong
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; xgl150327@csu.edu.cn
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import auc
from load import load
from matplotlib.ticker import MultipleLocator


class Enrichment(object):
    
    def __init__(self, loadfile, label_col, Ascore_col, Dscore_col):
        self.loadfile = loadfile
        self.df = pd.DataFrame()
        self.length = 0
        self.hit_all = 0
        self.scores = pd.Series()
        self.score_col = Ascore_col + Dscore_col
        self.Ascore = Ascore_col
        self.Dscore = Dscore_col
        self.label_col = label_col
                              
    def Load(self):
        data = load(self.loadfile)
        self.df = data
#        self.df = abs(self.df)
        self.length = len(self.df)
        self.hit_all = len(self.df[self.df[self.label_col]==1])
        self.scorers = pd.Series(self.score_col)

    
    def sort_count(self,scorer):
        res = []
        if scorer in self.Ascore:
            ascending = 1
        else:
            ascending = 0
        df_i = self.df.sort_values(scorer,ascending=ascending)
        for scape in np.arange(0,1,0.01):
            sampled = int(self.length*scape)
            try:
                hit_sampled = df_i.iloc[:sampled+1,:][self.label_col].value_counts()[1]
            except KeyError:
                hit_sampled = 0
            res.append(hit_sampled)
        return res 

    def show_enrichment_roc(self):
        
        self.Load()
        
        f,ax = plt.subplots(figsize=(5,5))
        
        res = self.scorers.map(self.sort_count)
        for item,col in zip(res,self.score_col):
            AUC = auc(np.arange(0,1.00,0.01),[round(x/self.hit_all,2) for x in item])
            AUC = '%.3f'%AUC
            plt.plot(np.arange(0,1.00,0.01),item,label='{} (AUC={})'.format(col,AUC))
        ax.set_yticks([0,int(self.hit_all*0.2),
                       int(self.hit_all*0.4),
                       int(self.hit_all*0.6),
                       int(self.hit_all*0.8),
                       int(self.hit_all*1.0)])
#        plt.plot([0, 1], [0, self.hit_all], color='navy', lw=1, linestyle='--')
        ax.set_ylim([0,self.hit_all])
        ax.set_xlim([0,1])
        ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1.0])
#        ax.set_xticklabels([0,20,40,60,80,100])
        ml_x = MultipleLocator(0.1)
        ml_y = MultipleLocator(int(self.hit_all*0.1))
        ax.yaxis.set_minor_locator(ml_y)
        ax.xaxis.set_minor_locator(ml_x)
        ax.tick_params(direction='in', which='both', labelsize=12)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['top'].set_linewidth(1.5)
        ax.spines['right'].set_linewidth(1.5) 
        ax.tick_params(width=1.3)
        ax.legend(fontsize=8,ncol=2,loc=4)
        ax.set_xlabel('Fraction of Samples',size=12)
        ax.set_ylabel('Fraction of Actives',size=12)
        plt.show()
        return f
    

if '__main__' == __name__:       
    pic = Enrichment(r"pos_neg.xlsx", label_col='label', score_col=['ASP','PLP'])
    pic.show_enrichment_roc()