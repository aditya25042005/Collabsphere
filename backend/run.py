"""
Entry point for the Collabsphere Flask backend.

Usage:
    python run.py
"""
import sys
import os

# Make sure the backend directory is in sys.path so that
# the legacy `sql`, `auth`, etc. modules are importable.
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(debug=True)
