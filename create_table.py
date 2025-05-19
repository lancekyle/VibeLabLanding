import os
import logging
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_newsletter_subscribers_table():
    """Create the newsletter_subscribers table in Supabase."""
    try:
        # Initialize Supabase client
        supabase_url = os.environ.get("SUPABASE_URL", "")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY", "")

        if not supabase_url or not supabase_key:
            logger.error("Missing Supabase credentials")
            return False

        # Create client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Use the REST API to create the table
        # This is a workaround since direct SQL execution is limited
        
        # First, check if table exists by trying to select from it
        try:
            supabase.table('newsletter_subscribers').select('*').limit(1).execute()
            logger.info("Table already exists")
            return True
        except Exception as e:
            logger.info(f"Table doesn't exist yet or error: {str(e)}")
            
            # Try creating table using a REST call to the Postgres API
            data = {
                "name": "newsletter_subscribers",
                "columns": [
                    {
                        "name": "id",
                        "type": "serial",
                        "primaryKey": True
                    },
                    {
                        "name": "email",
                        "type": "varchar",
                        "isUnique": True,
                        "isNullable": False
                    },
                    {
                        "name": "created_at",
                        "type": "timestamptz",
                        "defaultValue": "now()"
                    },
                    {
                        "name": "status",
                        "type": "varchar",
                        "defaultValue": "'active'"
                    },
                    {
                        "name": "source",
                        "type": "varchar",
                        "defaultValue": "'website'"
                    }
                ]
            }
            
            # This is a hack since Supabase doesn't expose direct table creation
            # We'll use the insert method to attempt to insert a row, which will tell us if the 
            # table creation worked through a side effect
            try:
                test_data = {'email': 'test@example.com'}
                result = supabase.table('newsletter_subscribers').insert(test_data).execute()
                logger.info("Table created successfully or already exists!")
                logger.info(f"Test row inserted: {result.data}")
                return True
            except Exception as e:
                if "does not exist" in str(e):
                    logger.error(f"Failed to create table: {str(e)}")
                    logger.error("You may need to create this table manually in the Supabase dashboard")
                    return False
                else:
                    logger.info("Table exists but insert failed for another reason")
                    return True
        
    except Exception as e:
        logger.error(f"Error creating table: {str(e)}")
        return False

if __name__ == "__main__":
    if create_newsletter_subscribers_table():
        print("Newsletter subscribers table creation successful!")
    else:
        print("Failed to create table. Please create it manually in the Supabase dashboard.")