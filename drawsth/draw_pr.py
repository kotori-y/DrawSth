# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:23:07 2019

@Author: Zhi-Jiang Yang, Guo-Li Xiong
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; xgl150327@csu.edu.cn
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import matplotlib.pyplot as plt
from load import load
from sklearn.metrics import precision_recall_curve,auc


def draw_pr(file, label_col, Ascore_col, Dscore_col,figsize=(5,5)):   
   data = load(file)
   score_col = Ascore_col+Dscore_col
   label = data.pop(label_col)
   font_kws = {'family':'arial','size':18}
   f,ax = plt.subplots(figsize=figsize) 
   for col in score_col:
       score = data.loc[:,col] 
       if col in Ascore_col:
           score = 1 - score
       else:
           pass
       precision, recall, _ = precision_recall_curve(label, score, pos_label=1)
       AUC = auc(recall, precision)   
       ax.plot(recall,precision,linewidth=1.5,label=col+' (auc=%.3f)'%AUC)
   ax.set_title('Precision/Recall Curve')# give plot a title
   ax.set_xlabel('Recall', fontdict=font_kws)# make axis labels
   ax.set_ylabel('Precision', fontdict=font_kws)
   ax.tick_params(direction='in', which='both', labelsize=12)
   ax.set_ylim([0.0,1.0])
   ax.set_xlim([0.0,1.0])
   ax.legend(fontsize=6.5)
   plt.show()
   return f
   
   

