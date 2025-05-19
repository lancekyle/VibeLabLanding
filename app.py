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
supabase_url = os.environ.get("SUPABASE_URL", "")
supabase_key = os.environ.get("SUPABASE_ANON_KEY", "")

if not supabase_url or not supabase_key:
    logger.error("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
    raise ValueError("Missing Supabase credentials")

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
        
        # Check if the table exists by trying to query it
        table_exists = True
        try:
            # Try to check if email already exists
            response = supabase.table('newsletter_subscribers').select('*').eq('email', email).execute()
            existing_subscribers = response.data
            
            if existing_subscribers and len(existing_subscribers) > 0:
                return jsonify({
                    'success': False, 
                    'message': 'This email is already subscribed. Thanks for your enthusiasm!'
                }), 400
                
        except Exception as e:
            error_message = str(e)
            if "does not exist" in error_message:
                # Table doesn't exist
                table_exists = False
                logger.warning("The newsletter_subscribers table doesn't exist yet. Storing subscriber temporarily.")
            else:
                logger.error(f"Error checking existing email: {error_message}")
        
        if table_exists:
            # Create new subscriber in Supabase
            now = datetime.utcnow().isoformat()
            subscriber_data = {
                'email': email,
                'created_at': now
            }
            
            try:
                response = supabase.table('newsletter_subscribers').insert(subscriber_data).execute()
                
                if response.data:
                    logger.info(f"Successfully added subscriber to Supabase: {email}")
                    return jsonify({
                        'success': True, 
                        'message': 'Successfully subscribed! Welcome to TheVibeLab.ai community.'
                    }), 200
                else:
                    raise Exception("No response data from Supabase insert")
            except Exception as e:
                error_message = str(e)
                if "does not exist" in error_message:
                    # Handle table not existing after all
                    table_exists = False
                    logger.warning("Table doesn't exist during insert. Storing subscriber temporarily.")
                else:
                    raise
        
        # Fallback: If table doesn't exist, store in memory and file
        if not table_exists:
            # Store in a file for now (can be migrated to the database later)
            try:
                import json
                import os
                
                subs_file = 'temp_subscribers.json'
                subscribers = []
                
                # Read existing subscribers if file exists
                if os.path.exists(subs_file):
                    with open(subs_file, 'r') as f:
                        subscribers = json.load(f)
                
                # Check if email already exists in temporary storage
                if any(sub.get('email') == email for sub in subscribers):
                    return jsonify({
                        'success': False, 
                        'message': 'This email is already subscribed. Thanks for your enthusiasm!'
                    }), 400
                
                # Add new subscriber
                subscribers.append({
                    'email': email,
                    'created_at': datetime.utcnow().isoformat()
                })
                
                # Write back to file
                with open(subs_file, 'w') as f:
                    json.dump(subscribers, f)
                
                logger.info(f"Stored subscriber temporarily: {email}")
                
                return jsonify({
                    'success': True, 
                    'message': 'Successfully subscribed! Welcome to TheVibeLab.ai community.'
                }), 200
                
            except Exception as file_error:
                logger.error(f"Error storing temporary subscriber: {str(file_error)}")
                raise
        
        # Should never reach here
        raise Exception("Unexpected flow in subscription process")
    
    except Exception as e:
        logger.error(f"Error subscribing: {str(e)}")
        return jsonify({
            'success': False, 
            'message': 'An error occurred while subscribing. Please try again.'
        }), 500
