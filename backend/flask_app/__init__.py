"""Flask application database configuration."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app: Flask) -> None:
    """Initialize database settings for the Flask app."""
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///tasks.db")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    db.init_app(app)
