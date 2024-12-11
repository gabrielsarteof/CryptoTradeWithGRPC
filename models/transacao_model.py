from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Transacao:
    id: Optional[int] = None
    carteira_id: Optional[int] = None  
    tipo: Optional[str] = None  
    moeda: Optional[str] = None 
    quantidade: Optional[float] = None
    preco: Optional[float] = None 
    data_hora: Optional[datetime] = None
