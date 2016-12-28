import copy
import time
def f1(a,b,c):
    if(b==1):
        b=0
    else:
        b=1
    if(c<1):
        return [f2(a,b),'lol']
    c+=-1
    d=-1
    g=-900
    h='I lose, you win'
    k=f2(a,b)/10
    m=0
    while(d<7):
        d+=1
        e=-1
        while(e<7):
            e+=1
            f=a[d][e]
            if(f[0]==b):
                j=copy.deepcopy(a)
                if(f[1]=='p'):
                    i=f3(j,b,c,d,e)
                    m+=i[2]
                    if(i[0]>g):
                        g=i[0]
                        h=i[1]
                    continue
                if(f[1]=='n'):
                    i=f4(a,b,c,d,e)
                    m+=i[2]
                    if(i[0]>g):
                        g=i[0]
                        h=i[1]
                    continue
                if(f[1]=='b'):
                    i=f5(a,b,c,d,e)
                    m+=i[2]
                    if(i[0]>g):
                        g=i[0]
                        h=i[1]
                    continue
                if(f[1]=='r'):
                    i=f6(a,b,c,d,e)
                    m+=i[2]
                    if(i[0]>g):
                        g=i[0]
                        h=i[1]
                    continue
                if(f[1]=='q'):
                    i=f7(a,b,c,d,e)
                    m+=i[2]
                    if(i[0]>g):
                        g=i[0]
                        h=i[1]
                    continue
                if(f[1]=='k'):
                    i=f8(a,b,c,d,e)
                    m+=i[2]
                    if(i[0]>g):
                        g=i[0]
                        h=i[1]
    return [k-m-g,h]
def f2(a,b):
    c=-1
    f=0
    while(c<7):
        c+=1
        d=-1
        while(d<7):
            d+=1
            e=a[c][d]
            if(e==[3,'_']):
                continue
            if(e[1]=='p'):
                if(e[0]==b):
                    if(e[0]==0):
                        f+=(9/10)+(c/10)
                    else:
                        f+=(9/10)+((7-c)/10)
                elif(e[0]==0):
                    f+=-((9/10)+(c/10))
                else:
                    f+=-((9/10)+((7-c)/10))
                continue
            if(e[1]=='b'):
                if(e[0]==b):
                    f+=3
                else:
                    f+=-3
                continue
            if(e[1]=='n'):
                if(e[0]==b):
                    f+=3
                else:
                    f+=-3
                continue
            if(e[1]=='r'):
                if(e[0]==b):
                    f+=5
                else:
                    f+=-5
                continue
            if(e[1]=='q'):
                if(e[0]==b):
                    f+=9
                else:
                    f+=-9
                continue
            if(e[1]=='k'):
                if(e[0]==b):
                    f+=60
                else:
                    f+=-60
    return -f
def f3(a,b,c,d,e):
    g=-900
    h='I lose, you win'
    i=[-1000,'error']
    m=0
    if(b==0):
        if(a[d+1][e]==[3,'_']):
            f=copy.deepcopy(a)
            if(d==6):
                f[d+1][e]=[0,'q']
            else:
                f[d+1][e]=[0,'p']
            f[d][e]=[3,'_']
            i=f1(f,b,c)
            m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d+1,e]]
            if(d==1):
                if(a[d+2][e]==[3,'_']):
                    f=copy.deepcopy(a)
                    f[d+2][e]=[0,'p']
                    f[d][e]=[3,'_']
                    i=f1(f,b,c)
                    m+=0.01
                    if(i[0]>g):
                        g=i[0]
                        h=[[d,e],[d+2,e]]
        if(e!=7):
            if(a[d+1][e+1][0]==1):
                f=copy.deepcopy(a)
                if(d==1):
                    f[d+1][e+1]=[0,'q']
                else:
                    f[d+1][e+1]=[0,'p']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
                if(i[0]>g):
                    g=i[0]
                    h=[[d,e],[d+1,e+1]]
        if(e!=0):
            if(a[d+1][e-1][0]==1):
                f=copy.deepcopy(a)
                if(d==1):
                    f[d+1][e-1]=[0,'q']
                else:
                    f[d+1][e-1]=[0,'p']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
                if(i[0]>g):
                    g=i[0]
                    h=[[d,e],[d+1,e-1]]
    else:
        if(a[d-1][e]==[3,'_']):
            f=copy.deepcopy(a)
            if(d==1):
                f[d-1][e]=[1,'q']
            else:
                f[d-1][e]=[1,'p']
            f[d][e]=[3,'_']
            i=f1(f,b,c)
            m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d-1,e]]
            if(d==6):
                if(a[d-2][e]==[3,'_']):
                    f=copy.deepcopy(a)
                    f[d-2][e]=[1,'p']
                    f[d][e]=[3,'_']
                    i=f1(f,b,c)
                    m+=0.01
                    if(i[0]>g):
                        g=i[0]
                        h=[[d,e],[d-2,e]]
        if(e!=7):
            if(a[d-1][e+1][0]==0):
                f=copy.deepcopy(a)
                if(d==1):
                    f[d-1][e+1]=[1,'q']
                else:
                    f[d-1][e+1]=[1,'p']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
                if(i[0]>g):
                    g=i[0]
                    h=[[d,e],[d-1,e+1]]
        if(e!=0):
            if(a[d-1][e-1][0]==0):
                f=copy.deepcopy(a)
                if(d==1):
                    f[d-1][e-1]=[1,'q']
                else:
                    f[d-1][e-1]=[1,'p']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
                if(i[0]>g):
                    g=i[0]
                    h=[[d,e],[d-1,e-1]]
    return [g,h,m]
def f4(a,b,c,d,e):
    g=-900
    h='I lose, you win'
    i=[-1000,'error']
    m=0
    if(d>0):
        if(e>1):
            if(a[d-1][e-2][0]!=b):
                f=copy.deepcopy(a)
                f[d-1][e-2]=[b,'n']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d-1,e-2]]
        if(d>1 and e>0):                
            if(a[d-2][e-1][0]!=b):
                f=copy.deepcopy(a)
                f[d-2][e-1]=[b,'n']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d-2,e-1]]
        if(d>1 and e<7): 
            if(a[d-2][e+1][0]!=b):
                f=copy.deepcopy(a)
                f[d-2][e+1]=[b,'n']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d-2,e+1]]
        if(e<6):
            if(a[d-1][e+2][0]!=b):
                f=copy.deepcopy(a)
                f[d-1][e+2]=[b,'n']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d-1,e+2]]
    if(d<7):
        if(e>1):
            if(a[d+1][e-2][0]!=b):
                f=copy.deepcopy(a)
                f[d+1][e-2]=[b,'n']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d+1,e-2]]
        if(d<6 and e>0):
            if(a[d+2][e-1][0]!=b):
                f=copy.deepcopy(a)
                f[d+2][e-1]=[b,'n']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d+2,e-1]]
        if(d<6 and e<7): 
            if(a[d+2][e+1][0]!=b):
                f=copy.deepcopy(a)
                f[d+2][e+1]=[b,'n']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d+2,e+1]]
        if(e<6):
            if(a[d+1][e+2][0]!=b):
                f=copy.deepcopy(a)
                f[d+1][e+2]=[b,'n']
                f[d][e]=[3,'_']
                i=f1(f,b,c)
                m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d+1,e+2]]
    return [g,h,m]
def f5(a,b,c,d,e):
    g=-900
    h='I lose, you win'
    i=[-1000,'error']
    f=1
    m=0
    while(d+f<8 and e+f<8):
        if(a[d+f][e+f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d+f][e+f]=[b,'b']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d+f,e+f]]
        if(a[d+f][e+f][0]!=3):
            break
        f+=1
    f=1
    while(e+f<8 and d-f>-1):
        if(a[d-f][e+f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d-f][e+f]=[b,'b']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d-f,e+f]]
        if(a[d-f][e+f][0]!=3):
            break
        f+=1
    f=1
    while(d-f>-1 and e-f>-1):
        if(a[d-f][e-f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d-f][e-f]=[b,'b']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d-f,e-f]]
        if(a[d-f][e-f][0]!=3):
            break
        f+=1
    f=1
    while(e-f>-1 and d+f<8):
        if(a[d+f][e-f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d+f][e-f]=[b,'b']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d+f,e-f]]
        if(a[d+f][e-f][0]!=3):
            break
        f+=1
    return [g,h,m]
def f6(a,b,c,d,e):
    m=0
    g=-900
    h='I lose, you win'
    i=[-1000,'error']
    f=1
    while(d+f<8):
        if(a[d+f][e][0]==b):
            break
        j=copy.deepcopy(a)
        j[d+f][e]=[b,'r']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d+f,e]]
        if(a[d+f][e][0]!=3):
            break
        f+=1
    f=1
    while(e+f<8):
        if(a[d][e+f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d][e+f]=[b,'r']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d,e+f]]
        if(a[d][e+f][0]!=3):
            break
        f+=1
    f=1
    while(d-f>-1):
        if(a[d-f][e][0]==b):
            break
        j=copy.deepcopy(a)
        j[d-f][e]=[b,'r']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d-f,e]]
        if(a[d-f][e][0]!=3):
            break
        f+=1
    f=1
    while(e-f>-1):
        if(a[d][e-f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d][e-f]=[b,'r']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d,e-f]]
        if(a[d][e-f][0]!=3):
            break
        f+=1
    return [g,h,m]
def f7(a,b,c,d,e):
    g=-900
    h='I lose, you win'
    i=[-1000,'error']
    f=1
    m=0
    while(d+f<8):
        if(a[d+f][e][0]==b):
            break
        j=copy.deepcopy(a)
        j[d+f][e]=[b,'q']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d+f,e]]
        if(a[d+f][e][0]!=3):
            break
        f+=1
    f=1
    while(e+f<8):
        if(a[d][e+f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d][e+f]=[b,'q']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d,e+f]]
        if(a[d][e+f][0]!=3):
            break
        f+=1
    f=1
    while(d-f>-1):
        if(a[d-f][e][0]==b):
            break
        j=copy.deepcopy(a)
        j[d-f][e]=[b,'q']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d-f,e]]
        if(a[d-f][e][0]!=3):
            break
        f+=1
    f=1
    while(e-f>-1):
        if(a[d][e-f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d][e-f]=[b,'q']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d,e-f]]
        if(a[d][e-f][0]!=3):
            break
        f+=1
    f=1
    while(d+f<8 and e+f<8):
        if(a[d+f][e+f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d+f][e+f]=[b,'q']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d+f,e+f]]
        if(a[d+f][e+f][0]!=3):
            break
        f+=1
    f=1
    while(e+f<8 and d-f>-1):
        if(a[d-f][e+f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d-f][e+f]=[b,'q']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d-f,e+f]]
        if(a[d-f][e+f][0]!=3):
            break
        f+=1
    f=1
    while(d-f>-1 and e-f>-1):
        if(a[d-f][e-f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d-f][e-f]=[b,'q']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d-f,e-f]]
        if(a[d-f][e-f][0]!=3):
            break
        f+=1
    f=1
    while(e-f>-1 and d+f<8):
        if(a[d+f][e-f][0]==b):
            break
        j=copy.deepcopy(a)
        j[d+f][e-f]=[b,'q']
        j[d][e]=[3,'_']
        i=f1(j,b,c)
        m+=0.01
        if(i[0]>g):
            g=i[0]
            h=[[d,e],[d+f,e-f]]
        if(a[d+f][e-f][0]!=3):
            break
        f+=1
    return [g,h,m]
def f8(a,b,c,d,e):
    g=-900
    h='I lose, you win'
    i=[-1000,'error']
    f=copy.deepcopy(a)
    m=0
    if(d<7):
        if(f[d+1][e][0]!=b):
            f=copy.deepcopy(a)
            f[d][e]=[3,'_']
            f[d+1][e]=[b,'k']
            i=f1(f,b,c)
            m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d+1,e]]
        if(e<7):
            if(f[d+1][e+1][0]!=b):
                f=copy.deepcopy(a)
                f[d][e]=[3,'_']
                f[d+1][e+1]=[b,'k']
                i=f1(f,b,c)
                m+=0.01
                if(i[0]>g):
                    g=i[0]
                    h=[[d,e],[d+1,e+1]]
        if(e>0):
            if(f[d+1][e-1][0]!=b):
                f=copy.deepcopy(a)
                f[d][e]=[3,'_']
                f[d+1][e-1]=[b,'k']
                i=f1(f,b,c)
                m+=0.01
                if(i[0]>g):
                    g=i[0]
                    h=[[d,e],[d+1,e-1]]
    if(d>0):
        if(f[d-1][e][0]!=b):
            f=copy.deepcopy(a)
            f[d][e]=[3,'_']
            f[d-1][e]=[b,'k']
            i=f1(f,b,c)
            m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d-1,e]]
        if(e<7 and f[d-1][e+1][0]!=b):
            f=copy.deepcopy(a)
            f[d][e]=[3,'_']
            f[d-1][e+1]=[b,'k']
            i=f1(f,b,c)
            m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d-1,e+1]]
        if(e>0 and f[d-1][e-1][0]!=b):
            f=copy.deepcopy(a)
            f[d][e]=[3,'_']
            f[d-1][e-1]=[b,'k']
            i=f1(f,b,c)
            m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d-1,e-1]]
    if(e>0):
        if(f[d][e-1][0]!=b):
            f=copy.deepcopy(a)
            f[d][e]=[3,'_']
            f[d][e-1]=[b,'k']
            i=f1(f,b,c)
            m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d,e-1]]
    if(e<7):
        if(f[d][e+1][0]!=b):
            f=copy.deepcopy(a)
            f[d][e]=[3,'_']
            f[d][e+1]=[b,'k']
            i=f1(f,b,c)
            m+=0.01
            if(i[0]>g):
                g=i[0]
                h=[[d,e],[d,e+1]]
    return [g,h,m]
def f9(a):
    #print(a)
    b=-1
    while(b<7):
        b+=1
    return 0
def f10(a,b):
    c=copy.deepcopy(a)
    d=b
    e=c[d[0][0]][d[0][1]]
    if(e[1]=='p'):
        if(d[1][0]==0 or d[1][0]==7):
            e[1]='q'
    c[d[1][0]][d[1][1]]=e
    c[d[0][0]][d[0][1]]=[3,'_']
    #print(c)
    return c
def f11(a,b):
    if(b[2]=='0'):
        if(a[int(b[0])][int(b[1])]==[1,'p']):
            c=input('what piece do you want?')
            a[int(b[0])][int(b[1])]=[1,c]
    if(b[2]=='7'):
        if(a[int(b[0])][int(b[1])]==[0,'p']):
            c=input('what piece do you want?')
            a[int(b[0])][int(b[1])]=[0,c]
    a[int(b[2])][int(b[3])]=a[int(b[0])][int(b[1])]
    a[int(b[0])][int(b[1])]=[3,'_']
    return a
def f12(a):
    if(a=='.'):
        return [3,'_']
    if(a=='p'):
        return [0,'p']
    if(a=='P'):
        return [1,'p']
    if(a=='r'):
        return [0,'r']
    if(a=='R'):
        return [1,'r']
    if(a=='n'):
        return [0,'n']
    if(a=='N'):
        return [1,'n']
    if(a=='b'):
        return [0,'b']
    if(a=='B'):
        return [1,'b']
    if(a=='k'):
        return [0,'k']
    if(a=='K'):
        return [1,'k']
    if(a=='q'):
        return [0,'q']
    if(a=='Q'):
        return [1,'q']
    return [3,'_']
def f13(a):
    if(a==[3,'_']):
        return '.'
    if(a==[0,'p']):
        return 'p'
    if(a==[1,'p']):
        return 'P'
    if(a==[0,'r']):
        return 'r'
    if(a==[1,'r']):
        return 'R'
    if(a==[0,'b']):
        return 'b'
    if(a==[1,'b']):
        return 'B'
    if(a==[0,'n']):
        return 'n'
    if(a==[1,'n']):
        return 'N'
    if(a==[0,'q']):
        return 'q'
    if(a==[1,'q']):
        return 'Q'
    if(a==[0,'k']):
        return 'k'
    if(a==[1,'k']):
        return 'K'
    return'.'


def main(history, white_time, black_time):
    # m is the depth of the search
    # j is time remaining
    # f is the board
    j = white_time if len(history)%2 else black_time
    f = [[f12(piece) for piece in row] for row in history[-1]]
    f.reverse()
    e = 0 if len(history)%2 else 1
    if j > 30:
        m = 3
        if j > 1000:
            m = 4
    else:
        m = 2
    f = f10(f, f1(f, e, m)[1])
    f.reverse()
    return [[f13(piece) for piece in row] for row in f]

#[[[0,'r'],[0,'n'],[0,'b'],[0,'q'],[0,'k'],[0,'b'],[0,'n'],[0,'r']],[[0,'p'],[0,'p'],[0,'p'],[0,'p'],[0,'p'],[0,'p'],[0,'p'],[0,'p']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[1,'p'],[1,'p'],[1,'p'],[1,'p'],[1,'p'],[1,'p'],[1,'p'],[1,'p']],[[1,'r'],[1,'n'],[1,'b'],[1,'q'],[1,'k'],[1,'b'],[1,'n'],[1,'r']]]
#[[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[0,'p'],[0,'p'],[0,'p'],[0,'p'],[0,'p'],[0,'p'],[0,'p'],[0,'p']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[1,'p'],[1,'p'],[1,'p'],[1,'p'],[1,'p'],[1,'p'],[1,'p'],[1,'p']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']]]
#[[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']],[[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_'],[3,'_']]]
