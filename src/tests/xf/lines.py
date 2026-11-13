import sys,re
a=open(sys.argv[1],'rb').read().split(b'\n'); b=open(sys.argv[2],'rb').read().split(b'\n')
num=re.compile(rb'^\s*-?\d+(\.\d*)?([eE][-+]?\d+)?\s*$')
# пары: сравнить последовательность кодов; вставки допустимы
i=j=0;chg=0;ins=0;bad=[]
A=[(a[k].strip(),a[k+1].rstrip(b'\r')) for k in range(0,len(a)-1,2)]
B=[(b[k].strip(),b[k+1].rstrip(b'\r')) for k in range(0,len(b)-1,2)]
while i<len(A) and j<len(B):
    if A[i][0]==B[j][0]:
        if A[i][1]!=B[j][1]:
            if not(num.match(A[i][1]) and num.match(B[j][1])): bad.append((A[i],B[j]))
            chg+=1
        i+=1;j+=1
    else: ins+=1;j+=1
print('pairs',len(A),'changed',chg,'inserted',ins+len(B)-j,'leftover',len(A)-i,'BAD',len(bad),bad[:3])
