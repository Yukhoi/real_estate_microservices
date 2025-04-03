from models.user import User
from flask import current_app
from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash
import pika
import json
import time
import threading

class UserService:

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user.hashed_password, password)

    @staticmethod
    def create_user(data):
        with current_app.app_context():
            user = User(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                birth_date=data.get('birth_date'),
                email=data.get('email'),
                hashed_password=UserService.hash_password(data.get('password'))
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
    def get_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "hashed_password": user.hashed_password,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        return {"error": "User not found"}

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
        
def on_request(ch, method, props, body):
    from app import create_app  # 确保可以创建 Flask 应用
    app = create_app()

    data = json.loads(body)
    response = {}

    with app.app_context():  # 激活 Flask 应用上下文
        if data['action'] == 'get_user_by_email':
            email = data['email']
            user = User.query.filter_by(email=email).first()
            if user:
                response = {
                    "id": user.id,
                    "email": user.email,
                    "hashed_password": user.hashed_password,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            else:
                response = {"error": "User not found"}

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id), 
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def connect_to_rabbitmq():
    for _ in range(5): 
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after multiple attempts")

def start_rabbitmq_consumer():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='user_service_queue')
    channel.basic_consume(queue='user_service_queue', on_message_callback=on_request)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()

# Start RabbitMQ Consumer in a separate thread
rabbitmq_thread = threading.Thread(target=start_rabbitmq_consumer, daemon=True)
rabbitmq_thread.start()