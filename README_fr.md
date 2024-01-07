
# Le jeu de la vie de Conway
Voici une version pythonique du jeu de la vie de Conway.
## Initialisation manuelle
```python
gol = GameOfLife(height = 6, width = 10) # Crée une grille de dimension 6x10.
gol.edit_state((3, 5), True)
gol.edit_state((2, 5), True)
gol.edit_state((1, 5), True)
print(gol.view())
```
*Résultat* : 
```
- - - - - - - - - -
- - - - - # - - - -
- - - - - # - - - -
- - - - - # - - - -
- - - - - - - - - -
- - - - - - - - - -
```
Vous pouvez ensuite lancer la simulation avec la méthode `run` : `gol.run()`.
## Intialisation par configuration
Il est aussi possible de lancer la simulation à partir d'un fichier de configuration défini à l'aide de deux caractères, qui sont ensuite spécifiés lors de l'initialisation de l'objet `GameOfLife`.

Exemple de fichier de configuration (Glider Gun - `configs/glidergun.gol`) :
```
-----------------------------------------------------
-----------------------------------------------------
--------------------------#--------------------------
------------------------#-#--------------------------
--------------##------##------------##---------------
-------------#---#----##------------##---------------
--##--------#-----#---##-----------------------------
--##--------#---#-##----#-#--------------------------
------------#-----#-------#--------------------------
-------------#---#-----------------------------------
--------------##-------------------------------------
-----------------------------------------------------
-----------------------------------------------------
```
> *Note : Les espaces sont supportés entre les caractères.* 

Ensuite, dans le fichier python :
```python
gol = GameOfLife(config = 'configs/glidergun.gol')
```
> *Note : Lors de l'utilisation d'un fichier de configuration, la taille de la grille est automatiquement définie.*

Si vous voulez charger une configuration comportant des caractères différents pour les cellules vivantes et mortes, vous devez spécifier un argument `custom_config` comme ceci :
```python
gol = GameOfLife(config = 'configs/glidergun.gol', custom_config = {
    1: '@',
    0: '\''
}) # 1/0 ou True/False peuvent être utilisés pour spécifier les cellules vivantes et mortes.
```
**Attention : cela ne change pas l'apparence des cellules dans la console !** Vous devez utiliser les arguments de classe `alive_char` et `dead_char` pour cela.
## Initialisation aléatoire
Si jamais vous voulez lancer une simulation avec une grille aléatoire, vous pouvez utiliser la valeur spéciale `__random__` pour l'argument `config` :
```python
gol = GameOfLife(config = '__random__', height = 30, width = 20)
```

## Graphic view
Cependant, il n'est pas toujours très pratique d'utiliser la console pour voir la simulation. C'est la raison pour laquelle cette classe possède une interface graphique. Pour l'utiliser, les librairies `PyQt5` et `pyqtgraph` doivent être installées (il suffit d'utiliser le fichier `requirements.txt` pour installer directement toutes les dépendances à jour de la classe). Il est ensuite possible d'ajouter l'argument `graphic = True` à l'initialisation de l'objet `GameOfLife` :

Exemple avec une simulation aléatoire :
```python
gol = GameOfLife(config = '__random__', height = 30, width = 20, graphic = True)
```