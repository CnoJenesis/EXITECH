from flask import Flask
import sys
import os

# Add the parent directory to the path so we can import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the app from the main app.py file
from app import app as flask_app

# This is required for Vercel serverless functions
app = flask_app 