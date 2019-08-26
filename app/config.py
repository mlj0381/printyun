import os,redis
from app import app



SECRET_KEY = os.getenv('SECRET_KEY','SECRET KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
#数据库自行配置
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://connect2:123456@localhost:3306/print'
secret_key = '111111'

POST_PER_PAGE = 5
