import numpy as np 
import random as rd

# ----------------------------------- CLASSE -----------------------------------

class Othellier:
    '''
    Cette classe modélise le plateau de jeu (=l'othellier) 
    '''

    def __init__(self, cases):
        self.cases = cases 
    
    def case_libre(self, choix):
        '''
        Cette fonction permet de vérifier, pour un othellier donné, 
        si la case choisie par le joueur est libre. 
        '''
        try : 
            if self.cases[choix[0], choix[1]] != 0 : 
                case_libre = False
            else : 
                case_libre = True 
        except IndexError:
            case_libre = False
            pass

        return case_libre

    def a_des_voisins(self, choix, adversaire):
        '''
        Cette fonction permet de déterminer si une case choisie par le joueur, 
        pour un othellier donné, est accolée à un pion de l'adversaire 
        '''
        a_des_voisins = False # initialisation 
        indices_voisins = [ 
            [choix[0], choix[1]-1],     # indice du voisin de gauche 
            [choix[0], choix[1]+1],     # ------ -- voisin de droite 
            [choix[0]+1, choix[1]],     # ------ -- voisin du bas 
            [choix[0]-1, choix[1]],     # ------ -- voisin du haut 
            [choix[0]-1, choix[1]-1],   # ------ -- voisin en haut à gauche 
            [choix[0]+1, choix[1]+1],   # ------ -- voisin en bas à droite 
            [choix[0]+1, choix[1]-1],   # ------ -- voisin en bas à gauche 
            [choix[0]-1, choix[1]+1] ]  # ------ -- voisin en haut à droite 

        for i in range(len(indices_voisins)) :
            try:
                if 7 >= indices_voisins[i][0] >= 0 and 7>= indices_voisins[i][1]>=0:
                    if self.cases[indices_voisins[i][0], indices_voisins[i][1]] == adversaire :
                        a_des_voisins = True 
                        break
            except IndexError:
                pass # gestion des effets de bord 
                
        # if not a_des_voisins :
            #print("Tu ne peux pas placer ton pion ici, il doit etre accolé à au moins un pion de l'adversaire ")
        
        return a_des_voisins 


    def a_des_binomes(self, choix, joueur, adversaire):
        '''
        Cette fonction permet :
        - détermine si le choix de la case permet de capturer des jetons adverses. 
        - renvoie les indices des pions capturés 

        On part du pion et de sa potentielle position. 
        On scanne dans chacune des directions pour aller chercher le prochain pion de la même couleur 
        permettant de capturer les jetons adverses. 
        On appelle le pion trouvé "binome".
        Il faut qu'entre 2 binomes, il y ait en effet des pions adverses (que l'on note "captures") ! 
        '''

        # initialisation 
        a_un_binome = False 
        binomes = []
        captures = []
        sens = ['haut', 'bas', 'gauche', 'droite', 'diag_haut_droite', 'diag_haut_gauche', 'diag_bas_droite', 'diag_bas_gauche']
        
        for sens_ in sens :

            captures_temporaires = []
            for i in range(1,7): # 7 pas dans un sens pour essayer de trouver un binome. 
                try : 
                    directions = { 'haut' : (choix[0]-i, choix[1]), 
                        'bas' : (choix[0]+i, choix[1]), 
                        'gauche' : (choix[0], choix[1]-i), 
                        'droite' : (choix[0], choix[1]+i), 
                        'diag_haut_droite' : (choix[0]-i, choix[1]+i), 
                        'diag_haut_gauche' : (choix[0]-i, choix[1]-i), 
                        'diag_bas_droite' : (choix[0]+i, choix[1]+i),                   
                        'diag_bas_gauche' : (choix[0]+i, choix[1]-i)}

                    if 0 <= directions[sens_][0] <=7 and 0 <= directions[sens_][1] <=7: 
                    # NB : cette ligne complète le "try" car si les valeurs sont négatives, il n'y a pas d'exception levée pas le except ... 
                        if self.cases[directions[sens_][0], directions[sens_][1]] == adversaire:
                            captures_temporaires.append(directions[sens_]) 

                        elif self.cases[directions[sens_][0], directions[sens_][1]] == 0 :
                            # si on a trouvé une capture mais qu'il y a un trou ensuite, ça ne compte plus! 
                            captures_temporaires = []
                            break # Si il y a un trou, ça casse la dynamique !! 
                        
                        if self.cases[directions[sens_][0], directions[sens_][1]] == joueur and len(captures_temporaires)>0: # and joueur not in captures_temporaires:
                            binomes.append(directions[sens_])
                            print("captures_temporaires", captures_temporaires)
                            for item in captures_temporaires:
                                captures.append(item)
                            break # pas besoin d'aller voir plus loin une fois qu'on a trouvé un binome 
                        if self.cases[directions[sens_][0], directions[sens_][1]] == joueur and len(captures_temporaires) == 0:
                            # si on rencontre un pion de le meme couleur que celui du joueur, alors on ne captures rien! --> on arrete 
                            break
                except IndexError:
                    pass
            #print("les binomes trouvés pour le sens {sens} sont : ".format(sens = sens_), binomes)
            #print("les captures trouvées pour le sens {sens} sont : ".format(sens = sens_), captures_temporaires)      

        # if len(binomes) == 0:
            # print("tu ne peux pas placer ton jeton ici, tu ne captures aucun pion!")
        if len(binomes) != 0:
            a_un_binome = True
            #print('Bravo, ton coup te permet de capturer {n_capture} pion(s)'.format(n_capture = len(captures)))
        return a_un_binome, binomes, captures 
    
    def mise_a_jour(self, choix, captures, joueur):
        '''
        Cette fonction met à jour l'othellier à la suite du choix du joueur 
        ''' 
        try:
            self.cases[choix[0], choix[1]] = joueur # on place le pion sur la case choisie pas le joueur 
            for capture in captures:
                self.cases[capture[0], capture[1]] = joueur # on retourne les pions capturés 
        except IndexError:
            pass


    def peut_jouer(self, joueur, adversaire):
        '''
        on regarde parmi les cases libres restantes si le joueur peut y placer un jeton.
        Si ce n'est pas possible, il doit passer son tour.
        '''
        peut_jouer = False
        cases_libres = list(zip(np.where(self.cases == 0)[0], np.where(self.cases == 0)[1]))
        for case in cases_libres:
            if self.a_des_voisins((case[0],case[1]), adversaire) and self.a_des_binomes((case[0],case[1]), joueur, adversaire)[0]:
                peut_jouer = True
                # print("peut jouer car {case}".format(case = case))
                break # Si il y a au moins un possibilité pour le jouer de jouer, on arrete ici 
        return peut_jouer

    def qui_gagne(self):
        '''
        Cette fonction renvoie le numéro du joueur gagnant
        '''
        print("np.where(self.cases == 1)",np.where(self.cases == 1, True, False).sum())
        print("np.where(self.cases == 2)",np.where(self.cases == 2, True, False).sum())        
        if np.where(self.cases == 1, True, False).sum() > np.where(self.cases == 2, True, False).sum():
            print("joueur 1 a gagné")
        elif np.where(self.cases == 1, True, False).sum() < np.where(self.cases == 2, True, False).sum() : 
            print("joueur 2 a gagné")
        else : 
            print("égalité !!")

    def tour(self, choix, joueur, joueur_, adversaire):
        '''
        Cette fonction représente un tour de jeu. 
        On spécifie dans le paramètre "joueur" à quel joueur est le tour (1 ou 2) 
        Dans un tour : 
        - le joueur choisit la case sur laquelle il souhaite placer son jeton 
        - on compte et retourne les jetons capturés 
        - on met à jour l'othellier 
        '''
        # --------------------- choix de la case ----------------------------
        
        # Il ne peut pas entrer n'importe quelle case : 
        
        while est_sur_othellier(choix) == False or \
        self.case_libre(choix) == False or \
        self.a_des_voisins(choix,adversaire) == False or \
        self.a_des_binomes(choix, joueur, adversaire)[0] == False:

            if joueur_ == True : # on ne print que si c'est une personne réelle 

                # 1 - La case doit avoir un sens (ie être sur l'échiquier)
                if est_sur_othellier(choix) == False :
                    print("Merci de choisir des chiffres entre 1 et 8")

                # 2 - La case doit être libre  
                if self.case_libre(choix) == False:
                    print("Tu ne peux pas jouer là, la case est déjà prise")

                # 3 - La case choisie doit être accolée à au moins un pion de son adversaire
                if self.a_des_voisins(choix,adversaire) == False:
                    print("Tu ne peux pas placer ton pion ici, il doit etre accolé à au moins un pion de l'adversaire ")
                
                #  4 - On vérifie maintenant qu'en plaçant son pion ici, le joueur capture effectivement 
                # des jetons de son adversaire. Sinon, il n'a pas le droit de placer son pion ici.
                if self.a_des_binomes(choix, joueur, adversaire)[0] == False:
                    print("tu ne peux pas placer ton jeton ici, tu ne captures aucun pion!")

            choix = Choix(joueur, joueur_)

        # Une fois les 4 conditions vérifiées, on peut renvoyer l'othellier avec les nouvelles valeurs 
        print("Le joueur ", joueur, " a choisi la case ", (choix[0] + 1 ,choix[1] + 1 ))
        print('Bravo, son coup lui permet de capturer {n_capture} pion(s)'.format(n_capture = len(self.a_des_binomes(choix, joueur, adversaire)[2])))
        print( "en position ", self.a_des_binomes(choix, joueur, adversaire)[2])
        self.mise_a_jour(choix, self.a_des_binomes(choix, joueur, adversaire)[2], joueur)

# -------------------------------------- FONCTIONS -----------------------------------------

def Choix(joueur, joueur_):
    '''
    Le joueur chosit la case sur laquelle il veut placer son jeton 
    '''
    if joueur_ == True: 

        choix_ = False # Tant que le choix entrée n'est pas sous la bonne forme, on garde choix_ = False
        while choix_ == False:
            choix = input('joueur {joueur}, où veux tu placer ton pion ? '.format(joueur = joueur))
            # input fournit un str --> on fait en sorte d'avoir une liste 
            try:
                choix = [int(item) for item in choix.split(',')]
                # On réindexe le choix du joueur pour avoir une indexation à 0 (python-compatible)
                choix[0] = choix[0] - 1 # Réindexage de la ligne 
                choix[1] = choix[1] - 1 # Réindexage de la colonne 
                choix_ = True

            except ValueError:
                print("Rentre ton choix sous la forme <n°ligne>,<n°colonne> stp :) ")
    
    else : 
        # Dans le cas où c'est l'ordinateur qui joue, il choisit une case au hasard.
        # Si la case ne permet pas de jouer, il choisira de nouveau. 
        choix = [rd.randint(0,7), rd.randint(0,7)]

    return choix 

def est_sur_othellier(choix):
    '''
    Vérifier que la case choisie est bien sur un othellier 
    '''
    if choix[0]>7 or choix[0]<0 or choix[1]>7 or choix[0]<0 : 
        est_sur_othellier = False
    else : 
        est_sur_othellier = True

    return est_sur_othellier

