from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""

prérequis basique pour une application:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
Source: "A Minimal Application" https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart

Modèle rélationnel de données 2 (mrd2) : .\exercices\seance_3\REV_3\statics\mrd2.png
Source : https://maximechallon.github.io/CoursM2TNAH_Flask_supports_public/Seance3/img/mrd2.png 

Legende mrd2.png
- - - - - - - - - - 
Clé jaune: clé primaire
Clé rouge: clé primaire, mais aussi clé étrangère dans la table en question
diamant blanc: accepte valeurs nulles, donc nullable = True
diamant bleu: attribut NOT NULL, donc nullable=False
diamant rouge: clé étrangère NOT NULL
Source: https://stackoverflow.com/questions/10778561/what-do-the-mysql-workbench-column-icons-mean

lazy=Mode
lazy=True = select / True (valeur par défaut, mais il est préférable d'être explicite) signifie que SQLAlchemy chargera les données au besoin en une seule fois en utilisant une instruction select standard.
lazy='subquery' = fonctionne comme joined mais au lieu de cela, SQLAlchemy utilisera une sous-requête.
Source: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

fonction def : on retournera pour la plupart la variable plus informatif pour les humains dans notre modèle. Par exemple, le nom d'utilisateur plutôt que l'id d'utilisateur.

"""

# création de la classe 'CoursEau'
# Classe liée à la table principale, donc en premier
class CoursEau(db.Model):
    __tablename__ = "CoursEau"
    
    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.String(45), nullable=False)
    longueur = db.Column(db.Integer)
    derniere_crue_majeure = db.Column(db.DateTime)

    # clé étrangère
    typeid = db.Column(
        db.Integer,
        db.ForeignKey('TypeCoursEau.id', nullable=False)
    )

    # propriétés de rélation 
    affluences = db.relationship('Affluence', backref='affluences', lazy=True)

    # relation vers la table de relation 'traverse' qui relie 'CoursEau' et 'SousDivisionGeographique'
    # syntax var = db.relationship(Classe, secondary=nom_var_table_jointure, lazy=Mode), backref = db.backref('classes_lies', lazy=Mode)
    traverses = db.relationship('SousDivisionGeographique', secondary=traverse_table, lazy='subquery', backref=db.backref('traverses', lazy=True))

    def __repr__(self):
        # return la variable 'denomination'
        return '<CoursEau %r>' % (self.denomination)
    
# création de la classe 'Affluence'
class Affluence(db.Model):
    __tablename__ = "Affluence"

    # clés étrangères
    affluent = db.Column(
        db.Integer,
        db.ForeignKey('CoursEau.typeid', nullable=False)
    )
    effluent = db.Column(
        db.Integer,
        db.ForeignKey('CoursEau.typeid', nullable=False)
    )
    
# création de la classe 'TypeCoursEau'
class TypeCoursEau(db.Model):
    __tablename__ = "TypeCoursEau"
    
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(45)) # triangulo azul
    commentaire = db.Column(db.Text)

    def __repr__(self):
        # return la variable 'label'
        return '<TypeCoursEau %r>' % (self.label)

# table de jointure 'traverse' : 'SousDivision_Geographique' et 'CoursEau' (relation many-to-many)
traverse_table = db.Table('traverse',
    db.Column('sousDivision', db.Integer, db.ForeignKey('SousDivision_Geographique.id'), primary_key=True,nullable=False),
    db.Column('coursEau', db.Integer, db.ForeignKey('CoursEau.competences_id'), primary_key=True, nullable=False)
)

# création de la classe 'SousDivisionGeographique'
class SousDivisionGeographique(db.Model): 

    """
    J'ai choisi de nommer la classe sans soulignement entre 'SousDivision' et 'Geographique', car il n'est pas obligatoire que la classe ait le même nom que la table, et parce que c'est plus lisible et plus facile à distinguer
    """
    __tablename__ = "SousDivision_Geographique"
    
    type = db.Column(db.Integer, nullable=False)
    denomination = db.Column(db.String(45), nullable=False)
    code_officiel = db.Column(db.String(12))

    # clés étrangères
    id = db.Column(
        db.Integer,
        db.ForeignKey('TypeSousDivision.id'),
        primary_key=True
    )
    pays = db.Column(
        db.Integer,
        db.ForeignKey('Pays.id'),
        nullable=False
    )

    def __repr__(self):
        # return la variable 'denomination'
        return '<SousDivisionGeographique %r>' % (self.denomination)

# création de la classe 'Pays'    
class Pays(db.Model):
    __tablename__ = "Pays"

    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        # return la variable 'denomination'
        return '<Pays %r>' % (self.denomination)

# création de la classe 'TypeSousDivision'
class TypeSousDivision(db.Model):
    __tablename__ = "skills"
    
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(45), nullable=True)
    commentaire = db.Column(db.Text)

    def __repr__(self):
        # return la variable 'label'
        return '<TypeSousDivision %r>' % (self.label)
