from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    senha: Optional[str] = None
    carteira: Optional[str] = None