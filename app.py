import os
from flask import Flask, render_template, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure SQLite database for simplicity
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///vibe_lab.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension
db.init_app(app)

# Import routes after app is initialized
from models import Subscriber

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        email = request.form.get('email')
        
        # Simple validation
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        
        # Check if email already exists
        existing_subscriber = Subscriber.query.filter_by(email=email).first()
        if existing_subscriber:
            return jsonify({'success': False, 'message': 'Email already subscribed'}), 400
        
        # Create new subscriber
        new_subscriber = Subscriber(email=email)
        db.session.add(new_subscriber)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Successfully subscribed!'}), 200
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error subscribing: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while subscribing. Please try again.'}), 500

# Initialize database
with app.app_context():
    db.create_all()
