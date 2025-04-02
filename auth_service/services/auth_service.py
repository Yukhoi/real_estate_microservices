import redis
import json
from datetime import timedelta
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from config import Config
import pika
import uuid

redis_client = redis.StrictRedis.from_url(Config.REDIS_URL, decode_responses=True)

class AuthService:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBITMQ_HOST))
        self.channel = self.connection.channel()

        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, action, email):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='user_service_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps({"action": action, "email": email})
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    @staticmethod
    def authenticate_user(email, password):
        rpc_client = AuthService()
        response = rpc_client.call("get_user_by_email", email)
        print("user not found", response)
        if "error" in response:
            return None
        if check_password_hash(response['hashed_password'], password):
            return response
        print("password not match")
        return None

    @staticmethod
    def create_access_token(user_data):
        return create_access_token(identity=user_data['email'], fresh=True)

    @staticmethod
    def store_token_in_redis(token, user_data):
        redis_client.setex(token, timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES), json.dumps(user_data))
        return True

    @staticmethod
    def get_user_data_from_redis(token):
        user_data = redis_client.get(token)
        if user_data:
            return json.loads(user_data)
        return None
    


