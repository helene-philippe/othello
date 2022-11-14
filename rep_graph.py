# -*- coding: cp1252 -*-

#######Importations des fonctions########

from tkinter import *
from random import * #pour la génération aléatoire des pions

#######Définition des fonctions##########
def cercle(x, y, r, coul ='red'):#pour le dessin des pions
    "tracé d'un cercle de centre (x,y) et de rayon r"
    can.create_oval(x-r, y-r, x+r, y+r, fill=coul)
    
def remplir(y):#calcul des coord de la ligne
    x=0
    liste=[]
    while x<1000:
        liste.append([x,y,x+125,y+125])
        x=x+125
    return liste

def figure():
    "dessiner le damier"
    global x,y,damier
    x=0
    y=0
    # Effacer d'abord tout dessin préexistant :
    can.delete(ALL)
    #definition de la matrice du damier
    damier=[]
    while y<1000:
        damier.append(remplir(y))#on remplit avec les coordonnées des cases de la ligne
        y=y+125
    a=0
    while a<8:#on trace la premiere partie du damier
        
        al=damier[a]
        b=0
        while b<8:
            al1=al[b]
            can.create_rectangle(al1[0],al1[+1],al1[2],al1[3],fill='green')
            b=b+1   
        a=a+1
   

def pointeur(event):
    """Dessine un pion la ou l'utilisateur a cliqué"""
    x=event.x%125
    x=(event.x-x)+62
    y=event.y%125
    y=(event.y-y)+62
    ##print x,y#debugging
    

    
    cercle(x,y,48,'green')

##### Programme principal : ############
global damier
fen = Tk()
can = Canvas(fen, width =1000, height =1000, bg ='white')
can.bind("<Button-1>", pointeur)
can.pack(side =TOP, padx =5, pady =5)
b1 = Button(fen, text ='damier', command =figure)
b1.pack(side =LEFT, padx =3, pady =3)
b3 = Button(fen, text ='Quitter', command =fen.destroy)
b3.pack(side =RIGHT,padx =3, pady =3)
fen.mainloop()