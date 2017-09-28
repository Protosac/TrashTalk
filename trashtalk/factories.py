from flask import Flask
from flask_login import LoginManager
from werkzeug.utils import find_modules, import_string

import factory
from faker import Faker

from trashtalk.models import *
from trashtalk.views import *

login_manager = LoginManager()
fake = Faker()


def app_factory(config_obj):
    """
    Create a new application instance.
    :param config_obj: `str` with dot notation (ex. 'app.settings.Production')
    :return: `Flask` app object
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Initialize modules
    init_db(app)
    login_manager.init_app(app)

    # Register all blueprints
    register_all_blueprints(app)

    # Return application process
    return app


def register_all_blueprints(app):
    """
    Searches the Views directory for blueprints and registers them.

    All views must have a `bp` attribute whose value is a Blueprint(). Ex.:
        `bp = Blueprint('my_view', __name__)`

    It will not be registered with the current application unless it has
    this attribute!

    :param app: The application for registration
    :return:
    """
    for view in find_modules('trashtalk.views'):
        uniq = set()
        if hasattr(view, 'bp'):
            # Avoid duplicate imports
            if view not in uniq:
                uniq.add(view)
                app.register_blueprint(view.bp)
    app.logger.info("Blueprints registered.")


def location_factory(data):
    location = Location(
        number=data.get('address'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    location.save()
    return location


def cleanup_factory(data):

    cleanup = Cleanup(
        # SQL cannot currently handle the commented out values

        name=data.get('name'),
        description=data.get('description'),
        location=data.get('location'),
        date=data.get('date'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        image=data.get('image'),
        host=data.get('host')
    )
    print("Image: ",data.get('image'))
    cleanup.save()
    return cleanup


def user_factory(**data):
    user = User(
        username=data.get('username'),
        password=data.get('password'),
        email=data.get('email')
    )
    user.save()
    return user


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db_session

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'User%d' % n)
    password = 'password'
    email = factory.Sequence(lambda n: 'user%d@example.com' % n)
