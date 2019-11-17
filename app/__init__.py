from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
import os
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
login = LoginManager()
# Which page to redirect to page if user is not logged in
login.login_view = 'auth.login'
migrate = Migrate()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        login.init_app(app)
        migrate.init_app(app, db)
        moment.init_app(app)

        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.agent import bp as agent_bp
        app.register_blueprint(agent_bp, url_prefix='/agent')

        from app.chatbot import bp as chatbot_bp
        app.register_blueprint(chatbot_bp, url_prefix='/admin')

        from app.sitemap import bp as sitemap_bp
        app.register_blueprint(sitemap_bp)

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # only do logging for production not development
        if not app.debug:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            # Log size rotates at 100KB so file size doesn't grow too big
            # Keeps the last 5 log files as backup
            file_handler = RotatingFileHandler('logs/blog.log', maxBytes=102400, backupCount=5)
            # Provide custom formatting for log messages
            file_handler.setFormatter(logging.Formatter( \
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]' \
            ))
            # set logging level to INFO in file logger
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            # set logging level to INFO in application logger
            app.logger.setLevel(logging.INFO)
            app.logger.info('Blog startup')

    return app
