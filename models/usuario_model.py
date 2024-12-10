from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    senha: Optional[str] = None
    tema: Optional[str] = None
    perfil: Optional[int] = None