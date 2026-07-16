"""
Modulo temporaneo di compatibilita.

Le funzioni di rumore BB84 sono state spostate in bb84_noise.py.
I nuovi sviluppi relativi a E91 saranno inseriti in e91_noise.py.
"""

try:
    from bb84_noise import *
except ImportError:
    from .bb84_noise import *
