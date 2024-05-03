from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""

prérequis basique pour une application:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
Source: "A Minimal Application" https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart

Modèle rélationnel de données (mrd): .\exercices\seance_3\REV_3\statics\mrd.png
Source : https://maximechallon.github.io/CoursM2TNAH_Flask_supports_public/Seance3/img/mrd.png

Legende mrd.png
- - - - - - - - - - 
Clé jaune: clé primaire
Clé rouge: clé primaire, mais aussi clé étrangère dans la table en question
diamant blanc: accepte valeurs nulles, donc nullable = True
Source: https://stackoverflow.com/questions/10778561/what-do-the-mysql-workbench-column-icons-mean

lazy=Mode
lazy=True = select / True (valeur par défaut, mais il est préférable d'être explicite) signifie que SQLAlchemy chargera les données au besoin en une seule fois en utilisant une instruction select standard.
lazy='subquery' = fonctionne comme joined mais au lieu de cela, SQLAlchemy utilisera une sous-requête.
Source: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

fonction def : on retournera pour la plupart la variable plus informatif pour les humains dans notre modèle. Par exemple, le nom d'utilisateur plutôt que l'id de l'utilisateur.

"""

# création de la classe 'User'
# Classe liée à la table principale, donc en premier
class User(db.Model):
    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(45), unique=True, nullable=False)
    user_firstname = db.Column(db.String(45))
    user_surname = db.Column(db.String(45))
    user_mail = db.Column(db.Text, unique=True, nullable=False)
    user_password_hash = db.Column(db.Text)
    user_birthyear = db.Column(db.Integer)
    user_promotion_date = db.Column(db.String(45))
    user_description = db.Column(db.Text)
    user_last_seen = db.Column(db.DateTime)
    user_linkedin = db.Column(db.Text, unique=True)
    user_github = db.Column(db.Text, unique=True)
    user_inscription_date = db.Column(db.DateTime)

    # propriétés de rélation 
    # syntaxe : var = db.relationship(SomeClass, backref='var', lazy=Mode)
    comments = db.relationship('Comment', backref='comments', lazy=True)
    competences = db.relationship('Competences', backref='competences', lazy=True)
    cvs = db.relationship('CV', backref='cvs', lazy=True)
    followers = db.relationship('Followers', backref='followers', lazy=True)
    messages = db.relationship('Message', backref='messages', lazy=True)    
    posts = db.relationship('Post', backref='posts', lazy=True)

    # relation vers la table de relation 'skills' qui relie 'User' et 'Competences'
    # syntax var = db.relationship(Classe, secondary=var_table_jointure, lazy=Mode), backref = db.backref('classes_lies', lazy=Mode)
    skills_relation = db.relationship('Competences', secondary=skills, lazy='subquery', backref=db.backref('skills_relation', lazy=True))
    
    def __repr__(self):
        # return la variable 'user_name'
        return '<User %r>' % (self.user_name)

# création de la classe 'Comment'
class Comment(db.Model): 
    __tablename__ = "Comment"

    id = db.Column(db.Integer, primary_key=True)
    comment_message = db.Column(db.Text)
    comment_html = db.Column(db.Text)
    comment_date = db.Column(db.DateTime)

    # clé étrangère
    comment_post = db.Column(
        db.Integer,
        db.ForeignKey('Post.post_auteur')
    )
    comment_auteur = db.Column(
        db.Integer,
        db.ForeignKey('User.id')
    )

    def __repr__(self):
        # return la variable 'comment_message'
        return '<Comment %r>' % (self.comment_message)

# création de la classe 'Competences'
class Competences(db.Model): 
    __tablename__ = "Competences"
    
    competences_id = db.Column(db.Integer, primary_key=True)
    competences_label = db.Column(db.String(45))

    def __repr__(self):
        # return la variable 'competences_label'
        return '<Competences %r>' % (self.competences_label)

# création de la classe 'CV'    
class CV(db.Model):
    __tablename__ = "CV"
    
    cv_id = db.Column(db.Integer, primary_key=True)
    cv_nom_poste = db.Column(db.Text)
    cv_nom_employeur = db.Column(db.Text)
    cv_ville = db.Column(db.String(45))
    cv_annee_debut = db.Column(db.Integer)
    cv_annee_fin = db.Column(db.Integer)
    cv_description_poste = db.Column(db.Text)
    
    # clé étrangère
    cv_utilisateur = db.Column(
        db.Integer,
        db.ForeignKey('User.id')
    )  

    def __repr__(self):
        # return la variable 'cv_nom_poste'
        return '<CV %r>' % (self.cv_nom_poste)

# création de la classe 'Followers'
class Followers(db.Model):
    __tablename__ = "followers"
    
    # clés étrangères
    follower_id = db.Column(
        db.Integer,
        db.ForeignKey('User.id'), 
        primary_key=True
    ) 
    followed_id = db.Column(
        db.Integer,
        db.ForeignKey('User.id'),
        primary_key=True
    )

# création de la classe 'Message'
class Message(db.Model):
    __tablename__ = "Message"
    
    message_id = db.Column(db.Integer, primary_key=True)
    message_message = db.Column(db.Text)
    message_html = db.Column(db.Text)
    message_date = db.Column(db.DateTime)

    # clés étrangères
    message_expediteur_id = db.Column(
        db.Integer,
        ForeignKey('User.id')
    )
    message_destinataire_id = db.Column(
        db.Integer,
        ForeignKey('User.id')
    )

    def __repr__(self):
        # return la variable 'message_message'
        return '<Message %r>' % (self.message_message)

# création de la classe 'Post'
class Post(db.Model): 
    __tablename__ = "Post"
    
    post_id = db.Column(db.Integer, primary_key=True)
    post_titre = db.Column(db.String(45))
    post_message = db.Column(db.Text)
    post_date = db.Column(db.DateTime)
    post_indexation = db.Column(db.String(45))
    html = db.Column(db.Text)

    # clé étrangère
    post_auteur = db.Column(
        db.Integer,
        db.ForeignKey('User.id')
    )

    def __repr__(self):
        # return la variable 'post_titre'
        return '<Post %r>' % (self.post_titre)

# table de jointure 'skills' : 'User' et 'Competences' (many-to-many)
skills = db.Table('skills',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('competence_id', db.Integer, db.ForeignKey('Competences.competences_id'), primary_key=True)
)
