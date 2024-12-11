from dataclasses import dataclass
from typing import Optional

@dataclass
class Transacao:
    carteira_id: int  
    moeda: str
    quantidade: float
    preco_unitario: float
    valor_total: float
    data: str
    tipo: str  
    id: Optional[int] = None
