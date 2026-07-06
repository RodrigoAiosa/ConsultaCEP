# services/__init__.py
"""
Serviços de acesso a APIs externas.
"""
from . import viacep
from . import geocoding

__all__ = ["viacep", "geocoding"]
