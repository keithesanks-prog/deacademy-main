# Use AWS Lambda Python 3.9 base image
# ⚠️ NOTE: We use --platform=linux/amd64 to ensure this image is compatible 
# with the standard AWS Lambda (x86_64) runtime, even if you build this
# on an ARM machine (like an Apple M1/M2/M3).
FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9

# Set working directory to /var/task (AWS Lambda default)
WORKDIR /var/task

# Optimize Cache: Copy requirements first so we only re-install if requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (This changes most often, so do it last)
COPY calendly_lambda.py .

# Set the entry point (The Driver) and handler (The Destination)
ENTRYPOINT [ "/var/lang/bin/python3.9", "-m", "awslambdaric" ]
CMD [ "calendly_lambda.lambda_handler" ]
