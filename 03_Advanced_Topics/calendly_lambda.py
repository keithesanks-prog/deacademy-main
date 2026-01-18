import json
import os
import boto3
import pandas as pd
import requests
import datetime
from io import StringIO
import logging

# ==========================================
# 🔧 SETUP & CONFIGURATION
# ==========================================

# Setup logging (so we can see what's happening in CloudWatch)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment Variables
# These are like "Settings" for our script. We set them in the Lambda Configuration.
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'your-bucket-name')
S3_FOLDER_PATH = os.getenv('S3_FOLDER_PATH', 'calendly/')

# ⚠️ SECURITY NOTE: 
# In a real production app, we might use AWS Secrets Manager.
# For this lab, we use a simple Environment Variable for cost & simplicity.
CALENDLY_TOKEN = os.getenv('CALENDLY_TOKEN')

# Initialize AWS Client for S3 (Simple Storage Service)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    🚀 AWS Lambda Handler Function.
    This is the entry point. When Lambda wakes up, it runs this function first.
    """
    
    # 1. Validation: Ensure we have the API Key
    if not CALENDLY_TOKEN:
        logger.error("CALENDLY_TOKEN is missing.")
        return {"statusCode": 500, "body": "Error: CALENDLY_TOKEN not set."}

    # Prepare standard headers for Calendly API
    headers = {
        "Authorization": f"Bearer {CALENDLY_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # ==========================================
        # STEP 1: Who am I? (Get User Profile)
        # ==========================================
        # We need the "Organization URI" to fetch events for the whole user scope.
        logger.info("Fetching User Profile...")
        user_resp = requests.get("https://api.calendly.com/users/me", headers=headers)
        
        if user_resp.status_code != 200:
            return {"statusCode": user_resp.status_code, "body": "Failed to get user profile"}

        user_data = user_resp.json()
        org_uri = user_data.get("resource", {}).get("current_organization")
        
        if not org_uri:
            return {"statusCode": 404, "body": "Organization URI not found"}

        logger.info(f"Found Org URI: {org_uri}")

        # ==========================================
        # STEP 2: Get Events (Using Org URI)
        # ==========================================
        logger.info("Fetching Scheduled Events...")
        events_resp = requests.get(
            "https://api.calendly.com/scheduled_events", 
            params={'organization': org_uri}, 
            headers=headers
        )

        if events_resp.status_code != 200:
             return {"statusCode": events_resp.status_code, "body": "Failed to get events"}

        events_data = events_resp.json()
        events_list = events_data.get("collection", [])
        
        # ==========================================
        # STEP 3: Process Data with Pandas 🐼
        # ==========================================
        # Pandas is great for turning raw JSON lists into structured Tables (DataFrames)
        
        if not events_list:
            logger.info("No events found.")
            return {"statusCode": 200, "body": "No events to process."}

        # Create DataFrame (Table)
        df = pd.DataFrame(events_list)
        
        # Select & Clean useful columns
        # We only want specific data points to keep our storage clean.
        cols_to_keep = ['uri', 'name', 'status', 'start_time', 'end_time']
        
        # Only keep columns that actually exist in the data (List Comprehension)
        final_cols = [c for c in cols_to_keep if c in df.columns]
        df = df[final_cols]

        # ==========================================
        # STEP 4: Save to S3 (The "Storage") 📦
        # ==========================================
        # We create a CSV in memory (RAM) instead of saving a file to the disk.
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        
        # Generate Unique Filename with Timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{S3_FOLDER_PATH}calendly_events_{timestamp}.csv"
        
        logger.info(f"Uploading to S3: {S3_BUCKET_NAME}/{file_name}")
        
        # Upload the CSV buffer to the S3 Bucket
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME, 
            Key=file_name, 
            Body=csv_buffer.getvalue()
        )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Success! Data saved to s3://{S3_BUCKET_NAME}/{file_name}")
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Internal Error: {str(e)}")
        }

# ==========================================
# 🧪 LOCAL TESTING BLOCK
# ==========================================
# This block only runs when you execute the script directly on your machine
# (e.g., `python calendly_lambda.py`). It is IGNORED by Lambda.
if __name__ == "__main__":
    
    print("--- 🧪 Starting Local Test ---")
    
    # Check for Env Vars
    if not os.environ.get('CALENDLY_TOKEN'):
        print("⚠️  WARNING: CALENDLY_TOKEN not set. API calls will fail.")
        print("   Run: $env:CALENDLY_TOKEN='your_token' (PowerShell)")
    
    if not os.environ.get('S3_BUCKET_NAME'):
        print("⚠️  WARNING: S3_BUCKET_NAME not set. S3 Upload will fail.")

    # Call the handler with Dummy Event Data
    result = lambda_handler(None, None)
    
    print("\n--- 🏁 Test Result ---")
    print(json.dumps(result, indent=2))
