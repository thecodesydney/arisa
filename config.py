import os
from pathlib import Path
from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))
basedir = Path(__file__).parent
load_dotenv(basedir / '.env')


class Config(object):
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20

    # Sendgrid settings
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    MAIL_FROM = os.environ.get('MAIL_FROM')
    MAIL_ADMINS = os.environ.get('MAIL_ADMINS')

    # Google recaptcha
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_OPTIONS = {'theme': 'black'}

    # Arisa custom default settings
    FORGOT_PASSWORD_TOKEN_EXPIRE = 600  # in seconds

    # Location of reports folder used to send email attachment to user
    REPORT_FOLDER = basedir / 'app/static/reports'

    # Dev only so browser doesnt cache for CSS
    # SEND_FILE_MAX_AGE_DEFAULT = 0
