from flask import Flask
from app.config import get_config
from app.extensions import db, migrate, jwt


def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        app.config.from_object(config)
    else:
        app.config.from_object(get_config())

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.api import api_bp

    try:
        import confirmroi_enterprise
        confirmroi_enterprise.register_blueprints(app)
    except ImportError:
        pass
    except Exception as e:
        app.logger.warning(f"Enterprise blueprints failed to register: {e}")

    app.register_blueprint(api_bp, url_prefix="/api")

    try:
        import confirmroi_enterprise
        confirmroi_enterprise.register_services(app)
        app.logger.info("Enterprise services registered successfully")
    except ImportError as e:
        app.logger.warning(f"Enterprise services not available (ImportError): {e}")
    except Exception as e:
        app.logger.warning(f"Enterprise services failed to initialize: {e}")
        import traceback
        app.logger.warning(traceback.format_exc())

    with app.app_context():
        from app import models  # noqa: F401 - ensure models are registered
        db.create_all()
        from app.services.seed import seed_formulas, seed_default_user
        seed_formulas()

        enterprise_installed = True
        try:
            import confirmroi_enterprise  # noqa: F401
        except ImportError:
            enterprise_installed = False

        if not enterprise_installed:
            seed_default_user()

    return app
