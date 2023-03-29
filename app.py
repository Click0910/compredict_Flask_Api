from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config=None):
    app = Flask(__name__)

    # load configuration
    if config is None:
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_object(config)

    # enable CORS
    CORS(app)

    # configure JWT authentication
    jwt = JWTManager(app)

    # import blueprints
    from api.views import api_bp

    # register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
