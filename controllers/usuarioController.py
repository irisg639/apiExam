from models.user import User
from config import db
from flask import jsonify
from flask_jwt_extended import create_access_token

def get_all_users():
    try:
        return [user.to_dict() for user in User.query.all()]
    except Exception as e:
        return jsonify({"error": str(e)})

def get_user_by_id(id):
    try:
        user = User.query.get(id)
        if user:
            return user.to_dict()
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_user(name, email, password):
    try:
        new_user = User(name, email, password)
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})

def edit_user(id, name, email):
    user=User.query.get(id)
    if not user:
        return jsonify({"error": "el usuario no existe"})
    
    user.name=name
    user.email=email
    try:
        db.session.commit()
        return jsonify({"message": "Usuario modificado"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creando el usuario: {str(e)}"})

def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "El usuario no existe"})
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error eliminando el usuario: {str(e)}"})

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        })
    return jsonify({"msg": "Credenciales inválidas"}), 401
