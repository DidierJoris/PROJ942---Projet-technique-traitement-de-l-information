# Traitement d'image

Cette partie a pour objectif de faire un traitement minutieux sur les photos. Tout d'abord, lorsque nous prenons une photo, nous devrons procéder aux mêmes traitements afin que la comparaison soit la plus optimale. Ainsi deux étapes vont devoir être traitées:

## Création d’une bibliothèque d'images.

### Programme de traitement d’image.

- Recadrage et normalisation

l'image capturée doit être recadrée. Pour faire cela nous parcourons les différents axes de la photo.

Pour le recadrage horizontal haut, nous scannons les pixels verticaux (Axe Y) pour chaque point de l’axe horizontal (Axe X). Lorsque l’intensité du pixel est inférieure au seuil fixé, et que la valeur en y calculée est inférieure à sa valeur précédente, alors le balayage est stoppé. Cela signifie en effet que nous avons atteint le point du visage le plus haut. Le seuil étant fixé à 80 sur 255 (Ce qui correspond à l’intensité de vert).

Pour le recadrage vertical droit, nous numérisons l'image pixel par pixel jusqu'à la moitié de la hauteur. Puis, on scanne les pixels sur l’horizontal (Axe X) pour chaque point de l’axe vertical (Axe Y).

Ensuite, lorsque l’intensité du pixel est inférieure au seuil fixé, et que la valeur en x est inférieure à la valeur du pixel précédent, le balayage est arreté.\\

Le recadrage vertical gauche est fait de la même manière que pour le côté droit. La seule différence réside dans les coordonnées d’origine définie au lancement du balayage. En effet, le balayage ne se fait dans ce cas plus de (0 à Xn) mais de (Xn-1 à 0).

``
y_{bas} = y_{haut} + 1,1 (x_{droit}-x_{gauche})
``

On note que certaines images peuvent présentées un étirement léger dû à la perte des porportions largeur/hauteur. Cette déformation fût jugée comme négligeable et ne remet pas en cause la reconnaissance du visage car la base de donnée elle-même est soumise au même étirement.

- Comparaison avec la Base de Donnée 

On s’intéresse maintenant au fonctionnement de la méthode ACP (Analyse en composantes principales), cette dernière commence par extraire l‘ensemble de ses composantes et calcule la matrice de covariance associée. Cette matrice permet de calculer la corrélation existante entre chacune des composantes et ainsi d’en déduire celles qui possèdent le gain d’information le plus important. Les valeurs propres et vecteurs propres de chacune des composantes sont par la suite calculés et ces derniers constituent une nouvelle base avec laquelle l’image est reconstruite. Le nombre de valeurs propres à prendre en considération dans la reconstruction est un critère important puisqu’il définit la qualité de l’image reconstruite et donc les performances de la reconnaissance. Plus ce nombre est important, meilleure sera la reconnaissance mais plus grande sera la taille des données. Il faut donc trouver un juste milieu entre ces deux paramètres. En ce qui concerne la reconnaissance, le principe est de comparer (i.e. de calculer la distance euclidienne) les vecteurs propres d’une image inconnue à un ensemble de vecteurs propres de différentes images afin d’en déduire la différence (i.e. la distance euclidienne) la plus faible. Nous pouvons alors juger que l’image de la base impliquant des distances euclidiennes les plus faibles correspond à l’image inconnue. Afin de mettre en œuvre cette méthode au sein de notre application, nous nous sommes basés sur un programme python mis à notre disposition par l’un de nos enseignants encadrants. Ce dernier permet la lecture d’une image inconnue et d’une base d’images d’apprentissage dont les chemins sont spécifiés en paramètre, le calcul de leurs valeurs propres et vecteurs propres respectives ainsi que le calcul des distances inter-images (entre l’image inconnue et la base d’apprentissage) afin d’en déduire l’identité de l’image inconnue. Pour ce faire, le programme Python fait appel à diverses librairies et fonctions spécifiques au traitement de l’image comme les libraires cv2, PIL et numpy. Il était alors nécessaire d’analyser les fonctions prédéfinies afin de l’adapter à notre application. Par exemple, nous avons choisis de calculer un nombre de composantes principales supérieur au nombre initial. Cela permet ainsi d’assurer une reconnaissance plus performa
