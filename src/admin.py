import os
from flask_admin import Admin
from models import db, Personaje, Planeta, Usuario, PersonajeFavorito, PlanetaFavorito
from flask_admin.contrib.sqla import ModelView

class PersonajeFavoritoAdmin(ModelView):
     column_list = ("usuario", "personaje")
     form_columns = ("usuario", "personaje")

class PlanetaFavoritoAdmin(ModelView):
     column_list = ("usuario", "planeta")
     form_columns = ("usuario", "planeta")     

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin


    admin.add_view(ModelView(Personaje, db.session))

    admin.add_view(ModelView(Planeta, db.session))

    admin.add_view(ModelView(Usuario, db.session))

    admin.add_view(PersonajeFavoritoAdmin(PersonajeFavorito, db.session))

    admin.add_view(PlanetaFavoritoAdmin(PlanetaFavorito, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))