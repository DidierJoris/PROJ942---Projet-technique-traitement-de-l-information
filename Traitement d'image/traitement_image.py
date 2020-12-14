# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 09:35:05 2020

@author: didierj
"""

import cgitb
import numpy as np
import sys
import os
from skimage import io
from PIL import Image
cgitb.enable()

#analyse image

#Fonction de recadrage vertical haut
def recadrage_image_vertical_haut(x,y,yh,xd,seuil,im):        
    for x in range(xd): #Parcours de l'image pixel par pixel sur sa largeur
        profil_vert = im[:,x,1] #Récupération de tous les pixels verticaux pour une coordonnée x
        for y in range(yh): #Parcours de tous les pixels verticaux pour une coordonnée x
            if profil_vert[y] < seuil and y < yh: #Si le pixel a une intensité inférieur au seuil fixé et que sa coordonnée en y est inférieure à la valeur précédente de yh
                yh = y #Définition de la nouvelle valeur de yh à prendre en compte pour le recadrage vertical haut
    return yh
            
              
#Fonction de recadrage horizontal droite              
def recadrage_image_horizontal_droite(x,y,xd,yh,moy,seuil,im):     
    for y in range(int(yh*moy)): #Parcours de l'image pixel par pixel sur la moitié de sa hauteur  
        profil_hori = im[y,:,1] #Récupération de tous les pixels horizontaux pour une coordonnée y
        for x in range(xd): #Parcours de tous les pixels horizontaux pour une coordonnée y
            if profil_hori[x] < seuil and x < xd: #Si le pixel a une intensité inférieur au seuil fixé et que sa coordonnée en x est inférieure à la valeur précédente de yd
                xd = x #Définition de la nouvelle valeur de xd à prendre en compte pour le recadrage horizontal à droite
    return xd           

            
#Fonction de recadrage horizontal gauche              
def recadrage_image_horizontal_gauche(x,y,xg,yh,xd,moy,seuil,im):  
    for y in range(int(yh*moy)): #Parcours de l'image pixel par pixel sur la moitié de sa hauteur
        profil_hori = im[y,:,1] #Récupération de tous les pixels horizontaux pour une coordonnée y
        for x in range(xd-1,0,-1): #Parcours de tous les pixels horizontaux pour une coordonnée y
            if profil_hori[x] < seuil and x > xg: #Si le pixel a une intensité inférieur au seuil fixé et que sa coordonnée en x est inférieure à la valeur précédente de xg
                xg = x #Si le pixel a une intensité inférieur au seuil fixé et que sa coordonnée en x est inférieure à la valeur précédente de xg
    return xg
    
#Fonction de recadrage vertical bas
def recadrage_image_vertical_bas(y, xd, xg,yb,coeff_prop):  
    yb = y + int((xg-xd)*coeff_prop) #Calcul de la coordonnée en y pour le recadrage horizontal bas de l'image
    return yb
#Calcul des différentes coordonnées pour le recadrage de l'image
#Reconnaissance de visage
    
def asRowMatrix (X):
    if len (X) == 0:
        return np.array([])
    mat = np.empty((0 , X[0].size), dtype=X[0].dtype )
    for row in X:
        mat = np.vstack((mat,np.asarray(row).reshape(1,-1)))
    return mat

    
def asColumnMatrix (X): #Fonction permettant le calcul des vecteurs colonnes
    if len (X) == 0:
        return np.array ([])
    mat = np.empty ((X [0].size , 0) , dtype =X [0].dtype )
    for col in X:
        mat = np.hstack (( mat , np.asarray ( col ).reshape( -1 ,1)))
    return mat  
    
def pca(X, y, num_components =0): #Fonction permettant le calcul des vecteurs propres associés à chaque image 
    [n,d] = X.shape
    if ( num_components <= 0) or ( num_components > n):
        num_components = n
    mu = X.mean ( axis = 0)
    X = X - mu
    if n>d:
        C = np.dot (X.T,X)
        [ eigenvalues , eigenvectors ] = np.linalg.eigh (C)
    else :
        C = np.dot (X,X.T)
        [ eigenvalues , eigenvectors ] = np.linalg.eigh (C)
        eigenvectors = np.dot (X.T, eigenvectors )
        for i in range (n):
            eigenvectors [:,i] = eigenvectors [:,i]/ np.linalg.norm ( eigenvectors [:,i])
    # or simply perform an economy size decomposition
    # eigenvectors , eigenvalues , variance = np.linalg.svd (X.T, full_matrices = False )
    # sort eigenvectors descending by their eigenvalue
    idx = np.argsort (- eigenvalues )
    eigenvalues = eigenvalues [idx ]
    eigenvectors = eigenvectors [:, idx ]
    # select only num_components
    eigenvalues = eigenvalues [0: num_components ].copy ()
    eigenvectors = eigenvectors [: ,0: num_components ].copy ()
    print("values = " + str(eigenvalues))
    print(len(mu))
    return [ eigenvalues , eigenvectors , mu]
    
def project (W, X, mu= None ):
    if mu is None :
        return np.dot (X,W)
    return np.dot (X - mu , W)
    
def reconstruct (W, Y, mu= None ): #Fonction permettant la reconstruction d'une image
    if mu is None :
        return np.dot(Y,W.T)
    return np.dot (Y,W.T) + mu
        
def normalize (X, low , high , dtype = None ):
    X = np.asarray (X)
    minX , maxX = np.min (X), np.max (X)
    # normalize to [0...1].
    X = X - float ( minX )
    X = X / float (( maxX - minX ))
    # scale to [ low...high ].
    X = X * (high - low )
    X = X + low
    if dtype is None :
        return np.asarray (X)
    return np.asarray (X, dtype = dtype )
    
def create_font ( fontname ='Tahoma', fontsize =10) :
    return { 'fontname': fontname , 'fontsize': fontsize } 

        
class AbstractDistance ( object ):
    
    def __init__(self , name ):
            self._name = name
    def __call__(self ,p,q):
        raise NotImplementedError (" Every AbstractDistance must implement the __call__method.")
    @property
    def name ( self ):
        return self._name
    def __repr__( self ):
        return self._name
        
class EuclideanDistance ( AbstractDistance ): 
    def __init__( self ):
        AbstractDistance.__init__(self ," EuclideanDistance ")
    def __call__(self , p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        return np.sqrt(np.sum (np.power((p-q) ,2)))
    
class CosineDistance ( AbstractDistance ):
    def __init__( self ):
        AbstractDistance.__init__(self ," CosineDistance ")
    def __call__(self , p, q):
        p = np.asarray (p).flatten ()
        q = np.asarray (q).flatten ()
        return -np.dot(p.T,q) / (np.sqrt (np.dot(p,p.T)*np.dot(q,q.T)))


class BaseModel ( object ):
    def __init__ (self , X=None , y=None , dist_metric = EuclideanDistance () , num_components=0) :
        self.dist_metric = dist_metric
        self.num_components = 0
        self.projections = []
        self.W = []
        self.mu = []
        if (X is not None ) and (y is not None ):
            self.compute (X,y)
            
    def compute (self , X, y):
        raise NotImplementedError (" Every BaseModel must implement the compute method.")
        
    def predict (self , X):
        minDist = np.finfo('float').max
        minClass = -1
        Q = project ( self.W, X.reshape (1 , -1) , self.mu)
        for i in range (len( self.projections )):
            dist = self.dist_metric ( self.projections [i], Q)
            if dist < minDist :
                minDist = dist
                minClass = self.y[i]
        return minClass
        
class EigenfacesModel ( BaseModel ):
    def __init__ (self , X=None , y=None , dist_metric = EuclideanDistance () , num_components=0) :
        super ( EigenfacesModel , self ).__init__ (X=X,y=y, dist_metric = dist_metric , num_components = num_components )
        
    def compute (self , X, y):
        [D, self.W, self.mu] = pca ( asRowMatrix (X),y, self.num_components )
        # store labels
        self.y = y
        # store projections
        for xi in X:
            self.projections.append ( project ( self.W, xi.reshape (1 , -1) , self.mu))
    
            
#Fonction permettant le recadrage et le redimenssionnement d'une image
def resize(image):                
    
    imageName = "base_visage/"+str(image)+".jpg" #Définition du nom de l'image à acquérir
    im = io.imread(imageName)
    height, width, depth = im.shape#Récupération des dimensions de l'image initiale
    
    
    # Initialisation des variables utiles pour le recadrage
    x=0 #RAZ des coordonées du point initial
    y=0 
    yh=height #Initilisation de la coordonée du curseur pour le recadrage vertical haut
    xg=0 #Initilisation des coordonées du curseur pour le recadrage horizontal (gauche et droite)
    xd=width 
    yb=0 #Initilisation de la coordonée du curseur pour le recadrage vertical bas
    moy=0.5
    seuil = 80 #Définition du seuil d'intensité à prendre en compte pour le recadrage
    coeff_prop = 1.3 #Définition du coefficient de proportionnalité entre la hauteur et la largeur du visage
    
	#Calcul des différentes coordonnées
    y_haut = recadrage_image_vertical_haut(x,y,yh,xd,seuil,im)
    x_droite = recadrage_image_horizontal_droite(x,y,xd,yh,moy,seuil,im)
    x_gauche = recadrage_image_horizontal_gauche(x,y,xg,yh,xd,moy,seuil,im)
    y_bas = recadrage_image_vertical_bas(y_haut, x_droite, x_gauche,yb,coeff_prop)
    
    #Recadrage de l'image
    im_cropped = im[y_haut:y_bas, x_droite:x_gauche]
    
    
    #Sauvegarde de l'image recadrée
    Im_cropped2save = Image.fromarray(im_cropped);
    
    #Redimensionnement de l'image recadrée aux dimensions 92*112
    width_resize = 92;
    heigh_resize = 112;
    Im_resized = Im_cropped2save.resize((width_resize, heigh_resize), Image.ANTIALIAS)    # best down-sizing filter
    Im_resized.save(imageName);            
                
    # append tinyfacerec to module search path
    sys.path.append ("..")
    print("image resized")

#Dimensions standards pour le redimensionnement des images
def calculRessemblance(image):
	
    imageName = "base_visage/"+str(image)+".jpg"
    [X,y]=read_images("E:\\Cours\\FI5\\PROJ942\\Fichier_Serveur\\base_visage")
        
    imtest = Image.open(imageName)
    imtest = imtest.convert ("L")
    
    test = np.asarray (imtest , dtype =np.uint8 )
    
    # model computation
    model = EigenfacesModel (X , y)
    nom=["Antonin","Baptiste","Clement","Joris","Pierre","Vincent"] #Définition du nom des individus de la base dans l'ordre alphabétique
    print  ("predicted =", nom[model.predict(test)]) #Affichage du résultat prédit
    return nom[model.predict(test)]
    os.remove(imageName)    



def read_images (path):
    c = 0
    X,y = [], []
    for dirname, dirnames, filenames in os.walk(path):
        dirnames.sort()
        for subdirname in dirnames :
            subject_path = os.path.join(dirname, subdirname )
            for filename in os.listdir(subject_path ):
                    im = Image.open(os.path.join (subject_path , filename ))
                    im = im.convert ("L")
                    # resize to given size (if given )
                    X.append (np.asarray (im , dtype =np.uint8 ))
                    y.append (c)
            c = c+1
    return [X,y]

#resize("abc")
calculRessemblance("IMG_20201125_163457")
