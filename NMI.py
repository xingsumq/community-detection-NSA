# -*- coding: utf-8 -*-
"""
Created on Tue May  8 17:13:39 2018

@author: Administrator
"""
import math

def entropy(C):
  n=0
  for kk in C.keys():
    n+=len(C[kk])
  #end of for kk in C.keys()
    
  sum=0
  for kk in C.keys():
    n_kk=len(C[kk])
    sum += -float(n_kk)/n*math.log(float(n_kk)/n)
  #end of for kk in C.keys()
         
  return sum
#end of function entropy(...)
  
  
def joint_entropy(C, P):  
  n=0
  for kk in C.keys():
    n += len(C[kk])
  #end of for kk in C.keys()
  
  sum=0
  for c in C.keys():
    for p in P.keys():
      n_cp=len(set(C[c]) & set(P[p]))
      if n_cp==0: 
        continue
      sum += -float(n_cp)/n*math.log(float(n_cp)/n)
    #end of for p in P.keys()
  #end of for c in C.keys()
      
  return sum
#end of function joint_entropy(...)  
  
def NMI(C, P):
  I=entropy(C)+entropy(P)-joint_entropy(P,C)
  return 2*I/(entropy(P)+entropy(C))
#end of function NMI(...)

def A(C, P):
  V=[]; vs={}; n=0
  for k in C:               ## 给每个顶点赋 ground_truth 的标签
    V+=C[k]; n+=len(C[k])
    for node in C[k]:
      vs[node]={}
      vs[node]['label']=k
  #end of for k in C
#  print len(vs), 'node properties: ', vs
  
  cnt={}
  for k in P:              ## 统计算法提取出的社团结构中每个 community 中 ground_truth 标签出现的次数
    cnt[k]={}
    for node in P[k]:
      cnt[k][vs[node]['label']]=1 if vs[node]['label'] not in cnt[k] else cnt[k][vs[node]['label']]+1
    #end of for node in P[k]
  #end of for k in P
  for k in P:
    cnt[k]=sorted(cnt[k].items(),key=lambda t: t[1], reverse=True)
  #end of for k in P    
#  print '\n', len(cnt), 'cnt: ', cnt
  
  while True:
    keys=C.keys()
    bContinue=False
    for label in keys:
      needProcess=[]
      for k in cnt:       ## 查找有无同一个 ground_truth 标签出现在多个 community 中的情况
        if label==cnt[k][0][0]: needProcess+=[k]
      #end of for k in cnt
      if len(needProcess)>1:  ## 有同一个 ground_truth 标签出现在多个 community 中的情况
        needProcess.sort(key=lambda k: cnt[k][0][1],reverse=True)
        del needProcess[0]    ## 在 P 中保留同一 ground_truth 标签出现次数最多的一个 community
        for key in needProcess:
          del cnt[key][0]
          if not cnt[key]:
            for v in P[key]:
              vs[v]['label*']='del'
            del cnt[key]
        #end of for key in needProcess
        bContinue=True     ## 有同一个 ground_truth 标签出现在多个 community 中的情况，去掉了
                           ## 其它定点数较的 community 的该 ground_truth 标签，需要继续处理
      #end of if len(needProcees)>1
    #end of for label in keys
    if not bContinue: break
  #end of while cnt
  for k in cnt:
    for v in P[k]:
      vs[v]['label*']=cnt[k][0][0]
    #end of for v in P[k]
  #end of for k in cnt
#  print 'nodes misclassified:\n\t'
  number=0
  for v in V:
    if vs[v]['label']==vs[v]['label*']: number+=1
#    else: print v,' ',
  #end of for v in V
    
  return float(number)/n 
