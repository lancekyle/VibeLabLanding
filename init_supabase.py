import os
import logging
from supabase import create_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_newsletter_subscribers_table():
    """Create the newsletter_subscribers table in Supabase if it doesn't exist."""
    try:
        # Initialize Supabase client
        supabase_url = os.environ.get("SUPABASE_URL", "")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY", "")

        if not supabase_url or not supabase_key:
            logger.error("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
            return False

        # Create client
        supabase = create_client(supabase_url, supabase_key)
        
        # Define the SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            status VARCHAR(50) DEFAULT 'active',
            source VARCHAR(100) DEFAULT 'website'
        );

        -- Create an index on email for faster lookups
        CREATE INDEX IF NOT EXISTS idx_newsletter_subscribers_email ON newsletter_subscribers(email);

        -- Add a comment to the table for documentation
        COMMENT ON TABLE newsletter_subscribers IS 'Table for storing newsletter subscribers from TheVibeLab.ai';
        """
        
        # Execute the SQL query
        response = supabase.rpc('exec_sql', {'query': create_table_query}).execute()
        
        logger.info("Newsletter subscribers table created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error creating newsletter subscribers table: {str(e)}")
        return False

if __name__ == "__main__":
    if create_newsletter_subscribers_table():
        print("Table created successfully!")
    else:
        print("Failed to create table. Check the logs for details.")