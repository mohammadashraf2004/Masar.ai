"""
Shared slowapi Limiter instance.

Lives in its own module (not app.main) so controllers can import it
without creating a circular import with app.main, which imports the
controllers to register their routers.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
