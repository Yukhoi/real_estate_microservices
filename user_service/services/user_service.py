from models.user import User
from flask import current_app
from extensions import db

class UserService:

    @staticmethod
    def create_user(data):
        with current_app.app_context():
            user = User(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                birth_date=data.get('birth_date')
            )
            
            db.session.add(user)
            db.session.commit()
            user = User.query.get(user.id)
            return user

    @staticmethod
    def get_user_by_id(user_id):
        with current_app.app_context():
            return User.query.get_or_404(user_id)

    @staticmethod
    def update_user(user_id, data):
        with current_app.app_context():
            user = User.query.get_or_404(user_id)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.birth_date = data.get('birth_date', user.birth_date)
            db.session.commit()
            return user_id

    @staticmethod
    def delete_user(user_id):
        with current_app.app_context():
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}