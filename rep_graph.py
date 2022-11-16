from tkinter import *
from random import * #pour la génération aléatoire des pions
from othellier import *

debut_partie = np.zeros([8,8]) 
debut_partie[4,3] = 1   # pion noir 
debut_partie[3,4] = 1   # pion noir 
debut_partie[3,3] = 2   # pion blanc 
debut_partie[4,4] = 2

#######Définition des fonctions##########
def cercle(x, y, r, coul ='white'):#pour le dessin des pions
    "tracé d'un cercle de centre (x,y) et de rayon r"
    can.create_oval(x-r, y-r, x+r, y+r, fill=coul)
    
def remplir(y):#calcul des coord de la ligne
    x=0
    liste=[]
    while x<8:
        liste.append([x*125,y*125,(x+1)*125,(y+1)*125])
        x+=1
    return liste

def figure():
    "dessiner le damier"
    y=0
    # Effacer d'abord tout dessin préexistant :
    can.delete(ALL)
    damier = []
    #definition de la matrice du damier
    a=0
    while y<8:
        damier.append(remplir(y))#on remplit avec les coordonnées des cases de la ligne
        y=y+1
    while a<8:#on trace la premiere partie du damier
        al=damier[a]
        b=0
        while b<8:
            al1=al[b]
            can.create_rectangle(al1[0],al1[+1],al1[2],al1[3],fill='green')
            b=b+1   
        a=a+1
    for i in range (8):
        for j in range (8):
            if debut_partie[i,j]==2:
                cercle((i*125)+62, (j*125)+62, 50, coul ='white')  
            elif debut_partie[i,j]==1:
                cercle((i*125)+62, (j*125)+62, 50, coul ='black')  

def pointeur(event):
    """Dessine un pion la ou l'utilisateur a cliqué"""
    x=event.x%125
    x=(event.x-x)+62
    y=event.y%125
    y=(event.y-y)+62
    cercle(x,y,48,'black')
    

##### Programme principal : ############
fen = Tk()
can = Canvas(fen, width =1000, height =1000, bg ='white')
figure()
can.bind("<Button-1>", pointeur)
can.pack(side =TOP, padx =5, pady =5)
b3 = Button(fen, text ='Quitter', command =fen.destroy)
b3.pack(side =BOTTOM,padx =3, pady =3)
fen.mainloop()