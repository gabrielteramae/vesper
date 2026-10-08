"""Consulta pública de username. Não busca pessoas, e-mail, telefone ou endereço."""

from vesper.check import check_username
from vesper.sites import normalize_username

__all__ = ["check_username", "normalize_username"]
__version__ = "0.1.0"
