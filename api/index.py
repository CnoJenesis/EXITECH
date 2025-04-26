from flask import Flask
import sys
import os

# Add the parent directory to the path so we can import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up PostgreSQL adapter for Vercel environment
try:
    from vercel_adapter import VercelPostgresAdapter
    print("Setting up PostgreSQL adapter for Vercel deployment")
    VercelPostgresAdapter.setup()
    print("PostgreSQL adapter setup complete")
except ImportError as e:
    print(f"Error loading PostgreSQL adapter: {e}")
    print("Continuing with default database settings...")

# Import the app from the main app.py file
from app import app as flask_app

# This is required for Vercel serverless functions
app = flask_app 