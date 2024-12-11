from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Carteira:
    id: Optional[int] = None
    usuario_id: Optional[int] = None  
    saldos: Optional[Dict[str, float]] = None  
    saldo_fiat: Optional[float] = None  
