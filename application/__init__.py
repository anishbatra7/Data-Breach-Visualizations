"""Initialize app."""
from flask import Flask

def create_app():
    """Construct the core application."""
    app = Flask(__name__,
                instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import main Blueprint
        from . import routes
        app.register_blueprint(routes.main_bp)
        # Import Dash application
        from .dashboard import data_dash, wikipedia_dash, kaggle_dash, stock_dash
        app = data_dash.Add_Dash(app)
        app = wikipedia_dash.Add_Dash(app)
        app = kaggle_dash.Add_Dash(app)
        app = stock_dash.Add_Dash(app)

        # Compile assets
        from .assets import compile_assets
        compile_assets(app)

        return app
