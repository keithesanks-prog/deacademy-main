# 🚀 Deployment Guide: Calendly Lambda Function

Since we used the standard `urllib3` library instead of `requests`, you **DO NOT** need to create any special zip files or layers. You can copy-paste the code directly into the AWS Console.

## Step 1: Create the Function
1. Go to the **AWS Lambda Console**.
2. Click **Create function**.
3. Choose **Author from scratch**.
4. Name: `CalendlyFetcher`.
5. Runtime: **Python 3.12** (or 3.xx).
6. Click **Create function**.

## Step 2: Add the Code
1. Scroll down to the **Code Source** editor.
2. Open `lambda_function.py` (the default file).
3. **Delete** all the content there.
4. **Copy-Paste** the content of `calendly_lambda.py` from this project.
   *(Note: You can omit the bottom "LOCAL TESTING BLOCK" if you want, but it doesn't hurt to keep it)*.
5. Click **Deploy**.

## Step 3: Set the API Token (Security)
Never hardcode tokens in the main code window!
1. Go to the **Configuration** tab.
2. Click **Environment variables** on the left menu.
3. Click **Edit**.
4. Click **Add environment variable**.
   - Key: `CALENDLY_TOKEN`
   - Value: `(Paste your long access token here)`
5. Click **Save**.

## Step 4: Test in Cloud
1. Go to the **Test** tab.
2. Create a new event (name it "Test1", leave default JSON as is).
3. Click **Test**.
4. You should see a green "Execution result: succeeded" and a list of your meetings in the response body!
