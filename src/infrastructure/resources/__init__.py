from .contact import bp as contact_bp
from .health import bp as health_bp
from .root import bp as root_bp
from .auth import bp as auth_bp
from .games.hangman import bp as hangman_bp

__all__ = ['contact_bp', 'health_bp', 'root_bp', 'auth_bp', 'hangman_bp']
