from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Producto, Pedido

app = FastAPI(title="API de Productos y Pedidos")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ==================== CRUD PRODUCTOS ====================

@app.post("/productos/", response_model=Producto)
def crear_producto(producto: Producto, session: Session = Depends(get_session)):
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

@app.get("/productos/", response_model=list[Producto])
def listar_productos(session: Session = Depends(get_session)):
    return session.exec(select(Producto)).all()

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"message": "Producto eliminado exitosamente"}

# ==================== CRUD PEDIDOS ====================

@app.post("/pedidos/", response_model=Pedido)
def crear_pedido(pedido: Pedido, session: Session = Depends(get_session)):
    producto = session.get(Producto, pedido.producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido

@app.get("/pedidos/", response_model=list[Pedido])
def listar_pedidos(session: Session = Depends(get_session)):
    return session.exec(select(Pedido)).all()
