from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_s3 import FlaskS3
from elasticsearch import Elasticsearch
from flask_mail import Mail
from trial.config import Config


#Create a database Instance 
mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
s3 = FlaskS3() 

login_manager.login_view = 'users.login' 
login_manager.login_message_category = 'info' 






def create_app(config_class=Config):
    #Initialise flask
    app = Flask(__name__)
    app.config.from_object(Config)

    
    #Extensions Initialization
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    s3.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
   
    #Import the blueprint objects and register with our routes
    from trial.users.routes import users
    from trial.blogs.routes import blogs
    from trial.generalforms.routes import generalforms
    from trial.projects.routes import projects
    from trial.main.routes import main
    from trial.errors.handlers import errors
    from trial.admin.routes import admin

    #Register the blueprint
    app.register_blueprint(users)
    app.register_blueprint(blogs)
    app.register_blueprint(generalforms)
    app.register_blueprint(projects)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(admin)


    return app