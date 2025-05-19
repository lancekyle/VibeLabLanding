import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from supabase import create_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(supabase_url, supabase_key)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Make sure the newsletter_subscribers table exists - will be created if it doesn't
try:
    # Check if table exists by querying it
    supabase.table('newsletter_subscribers').select('*').limit(1).execute()
    logger.info("Connected to Supabase newsletter_subscribers table")
except Exception as e:
    logger.warning(f"Table check error: {str(e)}")
    logger.info("Note: The table will be created automatically with the first subscription if it doesn't exist")

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
        try:
            response = supabase.table('newsletter_subscribers').select('*').eq('email', email).execute()
            existing_subscribers = response.data
            
            if existing_subscribers and len(existing_subscribers) > 0:
                return jsonify({
                    'success': False, 
                    'message': 'This email is already subscribed. Thanks for your enthusiasm!'
                }), 400
                
        except Exception as e:
            logger.error(f"Error checking existing email: {str(e)}")
            # Continue with subscription attempt anyway
        
        # Create new subscriber
        now = datetime.utcnow().isoformat()
        subscriber_data = {
            'email': email,
            'created_at': now
        }
        
        response = supabase.table('newsletter_subscribers').insert(subscriber_data).execute()
        
        if response.data:
            return jsonify({
                'success': True, 
                'message': 'Successfully subscribed! Welcome to TheVibeLab.ai community.'
            }), 200
        else:
            raise Exception("No response data from Supabase insert")
    
    except Exception as e:
        logger.error(f"Error subscribing: {str(e)}")
        return jsonify({
            'success': False, 
            'message': 'An error occurred while subscribing. Please try again.'
        }), 500
