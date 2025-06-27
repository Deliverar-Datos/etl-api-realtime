from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL, DATE, BOOLEAN, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.database import Base

# ==========================
# 1. Dimensión: Repartidores
# ==========================
class DimRepartidor(Base):
    __tablename__ = "dim_repartidores"

    repartidor_id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    email = Column(String(100))
    telefono = Column(String(20))

    eventos = relationship("FactDeliveryEventos", back_populates="repartidor")
    resumenes = relationship("FactDeliveryResumenPedido", back_populates="repartidor")
    estadisticas = relationship("FactRepartidorEstadisticas", back_populates="repartidor", foreign_keys="[FactRepartidorEstadisticas.repartidor_id]")


# =================================
# 2. Tabla de hechos: Eventos crudos
# =================================
class FactDeliveryEventos(Base):
    __tablename__ = "fact_delivery_eventos"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(String(50))
    estado = Column(String(20))  # ASIGNADO, PENDIENTE, EN_CAMINO, ENTREGADO, ARRIBO
    fecha_evento = Column(TIMESTAMP, nullable=False)
    repartidor_id = Column(Integer, ForeignKey("dim_repartidores.repartidor_id"))  # solo si aplica
    latitud = Column(DECIMAL(9, 6))  # opcional si más adelante se agregan coordenadas
    longitud = Column(DECIMAL(9, 6))

    repartidor = relationship("DimRepartidor", back_populates="eventos")


# =====================================
# 3. Tabla resumen por pedido (precálculo)
# =====================================
class FactDeliveryResumenPedido(Base):
    __tablename__ = "fact_delivery_resumen_pedido"

    pedido_id = Column(String(50), primary_key=True)
    repartidor_id = Column(Integer, ForeignKey("dim_repartidores.repartidor_id"))
    fecha_asignado = Column(TIMESTAMP)
    fecha_aceptado = Column(TIMESTAMP)
    fecha_en_camino = Column(TIMESTAMP)
    fecha_arribo = Column(TIMESTAMP)
    fecha_entregado = Column(TIMESTAMP)
    tiempo_asignado_a_entregado_mins = Column(Integer)
    tiempo_total_mins = Column(Integer)
    estado_final = Column(String(20))

    repartidor = relationship("DimRepartidor", back_populates="resumenes")


# ==========================================
# 4. Tabla resumen por repartidor (precálculo)
# ==========================================
class FactRepartidorEstadisticas(Base):
    __tablename__ = "fact_repartidor_estadisticas"

    repartidor_id = Column(Integer, ForeignKey("dim_repartidores.repartidor_id"), primary_key=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    telefono = Column(String(20))
    email = Column(String(100))

    total_pedidos = Column(Integer)
    pedidos_entregados = Column(Integer)
    pedidos_en_camino = Column(Integer)
    pedidos_arribo = Column(Integer)
    pedidos_pendientes = Column(Integer)

    tasa_entregas = Column(DECIMAL(5, 2))
    tiempo_promedio_entrega_mins = Column(DECIMAL(6, 2))
    tiempo_maximo_entrega_mins = Column(Integer)
    tiempo_minimo_entrega_mins = Column(Integer)

    fecha_ultima_entrega = Column(TIMESTAMP)
    pedidos_ultimos_7_dias = Column(Integer)

    repartidor = relationship("DimRepartidor", back_populates="estadisticas")


# ==========================
# 5. Dimensión de fechas (opcional)
# ==========================
class DimFecha(Base):
    __tablename__ = "dim_fecha"

    fecha = Column(DATE, primary_key=True)
    dia = Column(Integer)
    mes = Column(Integer)
    anio = Column(Integer)
    nombre_dia = Column(String(20))
    nombre_mes = Column(String(20))
    es_fin_de_semana = Column(BOOLEAN)
