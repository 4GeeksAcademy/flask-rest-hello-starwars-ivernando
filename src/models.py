from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # serialize the password, its a security breach
        }
    
class Usuario(db.Model):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)

    planetas_favoritos: Mapped[List["PlanetaFavorito"]] = relationship(back_populates="usuario")
    naves_favoritas: Mapped[List["NaveFavorita"]] = relationship(back_populates="usuario")
    personajes_favoritos: Mapped[List["PersonajeFavorito"]] = relationship(back_populates="usuario")
    

    def __repr__(self):
        return self.nombre 

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "personajes_favoritos": [
                {
                    "nombre": fav.personaje.nombre
                }
                for fav in self.personajes_favoritos
            ],
             "planetas_favoritos": [
                {
                    "nombre": fav.planeta.nombre
                }
                for fav in self.planetas_favoritos
            ]
        }
            # do not serialize the password, its a security breach
        
    
class Especie(db.Model):
    __tablename__ = "especie"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)

    personajes: Mapped[list["Personaje"]] = relationship(back_populates="especie")
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            # do not serialize the password, its a security breach
        }

    
class Nave(db.Model):
    __tablename__ = "nave"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    velocidad_kmh: Mapped[int] = mapped_column(nullable=False)
    
    naves_favoritas: Mapped[List["NaveFavorita"]] = relationship(back_populates="nave")
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            # do not serialize the password, its a security breach
        }
    
class Planeta(db.Model):
    __tablename__ = "planeta"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    clima: Mapped[str] = mapped_column(nullable=False)

    personajes: Mapped[list["Personaje"]] = relationship(back_populates="planeta")
    planetas_favoritos: Mapped[List["PlanetaFavorito"]] = relationship(back_populates="planeta")

    def __repr__(self):
        return self.nombre 

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima
            # do not serialize the password, its a security breach
        }
class Personaje(db.Model):
    __tablename__ = "personaje"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    especie_id: Mapped[int] = mapped_column(ForeignKey("especie.id"),nullable=True)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"),nullable=True)
    
    personajes_favoritos: Mapped[List["PersonajeFavorito"]] = relationship(back_populates="personaje")

    especie: Mapped["Especie"] = relationship(back_populates="personajes")
    planeta: Mapped["Planeta"] = relationship(back_populates="personajes")

    def __repr__(self):
        return self.nombre 

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        
            # do not serialize the password, its a security breach
        }

class PlanetaFavorito(db.Model):
    __tablename__ = "planeta_favorito"

    id: Mapped[int] = mapped_column(primary_key=True)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)

    planeta: Mapped["Planeta"] = relationship(back_populates="planetas_favoritos")
    usuario: Mapped["Usuario"] = relationship(back_populates="planetas_favoritos")

        


    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
            }
    
class NaveFavorita(db.Model):
    __tablename__ = "nave_favorita"

    id: Mapped[int] = mapped_column(primary_key=True)
    nave_id: Mapped[int] = mapped_column(ForeignKey("nave.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)

    nave: Mapped["Nave"] = relationship(back_populates="naves_favoritas")
    usuario: Mapped["Usuario"] = relationship(back_populates="naves_favoritas")

        


    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
            }
    
class PersonajeFavorito(db.Model):
    __tablename__ = "personaje_favorito"

    id: Mapped[int] = mapped_column(primary_key=True)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)

    personaje: Mapped["Personaje"] = relationship(back_populates="personajes_favoritos")
    usuario: Mapped["Usuario"] = relationship(back_populates="personajes_favoritos")

        


    def serialize(self):
        return {
            "id usuario": self.usuario.id,
            "id personaje favorito": self.personaje_id
            # do not serialize the password, its a security breach
            }    
