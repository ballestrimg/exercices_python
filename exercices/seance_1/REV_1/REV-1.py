import datetime #datetime fournit des classes permettant de manipuler les dates et les heures

class Personne: # creation de la classe 'Personne'
    def __init__(self, data): # la methode __init__ reçoit un argument dont la variable est 'data'
        self.data = data # definit l'argument data
        
    def etat_civil(self): # la methode etat_civil ne recoit pas d'argument
        nom_complet = f"{data['prenom']} {data['nom']}" # recupere les valeurs associes aux cles 'prenom' et 'nom' 
        return nom_complet # returne une fstring contenant le nom complet de la personne 

    def age(self): # la methode age ne recoit pas d'argument
        anne_actuelle = datetime.date.today().year # variable 'anne_actuelle' recoit l'anne actuelle
        compteur_age = anne_actuelle - int(data['annee_naissance']) # variable compteur_age: recupere et somme la variable anne_actuelle et l'integer (int) de la clé 'anne_naissance'
        return compteur_age # returne l'age de la personne qui est le resultat de la somme de la variable compteur_age

data = {
    "annee_naissance": "1966",
    "nom" : "Dupont",
    "prenom": "Jean"
} # dict() 'data' avec trois cles et trois valeurs qui representent : anne de naissance, nom et prenom d'une personne

print(f'Cas 1 : Personne(data).data')
print(Personne(data).data) # affiche les paires cle-valeur du dict() 'data'
print(f'Cas 2 : Personne(data).etat_civil()')
print(Personne(data).etat_civil()) # affiche le prenom et nom
print(f'Cas 3 : Personne(data).age()')
print(Personne(data).age()) # affiche l'age