from flask import Flask
from pathlib import Path


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        instance_relative_config=True,
    )
    app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"
    app.config["DATABASE"] = str(Path(app.instance_path) / "avilacosta_diagnosticos.db")

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from app.database import init_db
    from app.routes.main import main_bp

    init_db(app)
    app.register_blueprint(main_bp)

    return app
