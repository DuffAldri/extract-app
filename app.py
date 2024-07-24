from flask import Flask
from config import Config

# Initialize Flask app
app = Flask(__name__, static_url_path='/assets')
app.config.from_object(Config)

# Register blueprints
from controllers.main_controller import main_bp
from controllers.prediction_controller import prediction_bp

app.register_blueprint(main_bp)
app.register_blueprint(prediction_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
