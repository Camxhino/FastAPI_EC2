from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# --- Modelo Producto ---
class ProductoBase(SQLModel):
    nombre: str
    precio: float

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedidos: List["Pedido"] = Relationship(back_populates="producto")

# --- Modelo Pedido ---
class PedidoBase(SQLModel):
    cantidad: int
    producto_id: int = Field(foreign_key="producto.id")

class Pedido(PedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto: Optional[Producto] = Relationship(back_populates="pedidos")
