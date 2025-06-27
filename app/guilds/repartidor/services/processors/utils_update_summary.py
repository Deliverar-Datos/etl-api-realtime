from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.guilds.repartidor.models.star_schema import (
    FactDeliveryEventos,
    FactDeliveryResumenPedido,
    FactRepartidorEstadisticas,
    DimRepartidor,
)
from sqlalchemy.exc import SQLAlchemyError

def update_fact_delivery_resumen_pedido(db: Session, pedido_id: str):
    try:
        # Obtener todos los eventos relacionados con el pedido_id
        eventos = db.query(FactDeliveryEventos).filter(FactDeliveryEventos.pedido_id == pedido_id).all()
        if not eventos:
            return

        # Inicializar fechas por estado
        fechas_estado = {
            "ASIGNADO": None,
            "PENDIENTE": None,
            "EN_CAMINO": None,
            "ARRIBO": None,
            "ENTREGADO": None,
            "CANCELADO": None,
        }

        # Extraer fechas de cada estado
        for evento in eventos:
            estado = evento.estado.upper()
            if estado in fechas_estado:
                if fechas_estado[estado] is None or evento.fecha_evento < fechas_estado[estado]:
                    fechas_estado[estado] = evento.fecha_evento

        # Calcular métricas de tiempo
        fecha_asignado = fechas_estado["ASIGNADO"]
        fecha_entregado = fechas_estado["ENTREGADO"]

        tiempo_asignado_a_entregado_mins = None
        tiempo_total_mins = None
        estado_final = None

        if fecha_asignado and fecha_entregado:
            tiempo_asignado_a_entregado_mins = int((fecha_entregado - fecha_asignado).total_seconds() / 60)
            tiempo_total_mins = tiempo_asignado_a_entregado_mins
            estado_final = "ENTREGADO"
        elif fechas_estado["CANCELADO"]:
            estado_final = "CANCELADO"
            # Para cancelados, asignar tiempo_total_mins igual a tiempo_hasta_cancelacion_mins
            tiempo_total_mins = None
            if fecha_asignado and fechas_estado["CANCELADO"]:
                tiempo_total_mins = int((fechas_estado["CANCELADO"] - fecha_asignado).total_seconds() / 60)
        else:
            # Si no está entregado ni cancelado, tomar el último estado conocido
            estados_orden = ["ASIGNADO", "PENDIENTE", "EN_CAMINO", "ARRIBO", "ENTREGADO", "CANCELADO"]
            for estado in reversed(estados_orden):
                if fechas_estado[estado]:
                    estado_final = estado
                    break

        # Obtener repartidor_id del primer evento con pedido_id
        repartidor_id = None
        for evento in eventos:
            if evento.repartidor_id:
                repartidor_id = evento.repartidor_id
                break

        fecha_cancelado = fechas_estado["CANCELADO"]
        pedido_cancelado = fecha_cancelado is not None
        tiempo_hasta_cancelacion_mins = None
        if fecha_asignado and fecha_cancelado:
            tiempo_hasta_cancelacion_mins = int((fecha_cancelado - fecha_asignado).total_seconds() / 60)

        # Insertar o actualizar en fact_delivery_resumen_pedido
        resumen = db.query(FactDeliveryResumenPedido).filter(FactDeliveryResumenPedido.pedido_id == pedido_id).first()
        if not resumen:
            resumen = FactDeliveryResumenPedido(pedido_id=pedido_id)
            db.add(resumen)

        resumen.repartidor_id = repartidor_id
        resumen.fecha_asignado = fecha_asignado
        resumen.fecha_aceptado = fechas_estado.get("PENDIENTE")  # Asumiendo pendiente como aceptado
        resumen.fecha_en_camino = fechas_estado.get("EN_CAMINO")
        resumen.fecha_arribo = fechas_estado.get("ARRIBO")
        resumen.fecha_entregado = fecha_entregado
        resumen.tiempo_asignado_a_entregado_mins = tiempo_asignado_a_entregado_mins
        resumen.tiempo_total_mins = tiempo_total_mins
        resumen.estado_final = estado_final

        resumen.fecha_cancelado = fecha_cancelado
        resumen.pedido_cancelado = pedido_cancelado
        resumen.tiempo_hasta_cancelacion_mins = tiempo_hasta_cancelacion_mins

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def update_fact_repartidor_estadisticas(db: Session, repartidor_id: int):
    try:
        # Consultar todos los pedidos del repartidor
        pedidos = db.query(FactDeliveryResumenPedido).filter(FactDeliveryResumenPedido.repartidor_id == repartidor_id).all()
        if not pedidos:
            return

        total_pedidos = len(pedidos)
        pedidos_entregados = sum(1 for p in pedidos if p.estado_final == "ENTREGADO")
        pedidos_en_camino = sum(1 for p in pedidos if p.estado_final == "EN_CAMINO")
        pedidos_arribo = sum(1 for p in pedidos if p.estado_final == "ARRIBO")
        pedidos_pendientes = sum(1 for p in pedidos if p.estado_final == "PENDIENTE")
        pedidos_cancelados = sum(1 for p in pedidos if p.estado_final and p.estado_final.strip().upper() == "CANCELADO")

        tasa_entregas = (pedidos_entregados / total_pedidos) * 100 if total_pedidos > 0 else 0

        tiempos_entrega = [
            p.tiempo_asignado_a_entregado_mins for p in pedidos if p.tiempo_asignado_a_entregado_mins is not None
        ]

        tiempo_promedio_entrega_mins = (
            sum(tiempos_entrega) / len(tiempos_entrega) if tiempos_entrega else None
        )
        tiempo_maximo_entrega_mins = max(tiempos_entrega) if tiempos_entrega else None
        tiempo_minimo_entrega_mins = min(tiempos_entrega) if tiempos_entrega else None

        fecha_ultima_entrega = None
        pedidos_ultimos_7_dias = 0
        now = datetime.utcnow()
        for p in pedidos:
            if (p.fecha_entregado and (now - p.fecha_entregado) <= timedelta(days=7)) or (p.fecha_cancelado and (now - p.fecha_cancelado) <= timedelta(days=7)):
                pedidos_ultimos_7_dias += 1
                # Actualizar fecha_ultima_entrega considerando entregas y cancelaciones
                if not fecha_ultima_entrega or (p.fecha_entregado and p.fecha_entregado > fecha_ultima_entrega):
                    fecha_ultima_entrega = p.fecha_entregado
                if not fecha_ultima_entrega or (p.fecha_cancelado and p.fecha_cancelado > fecha_ultima_entrega):
                    fecha_ultima_entrega = p.fecha_cancelado

        repartidor = db.query(FactRepartidorEstadisticas).filter(FactRepartidorEstadisticas.repartidor_id == repartidor_id).first()
        if not repartidor:
            repartidor = FactRepartidorEstadisticas(repartidor_id=repartidor_id)
            db.add(repartidor)

        print(f"Repartidor {repartidor_id} - total_pedidos: {total_pedidos}, pedidos_cancelados: {pedidos_cancelados}")

        repartidor.total_pedidos = total_pedidos
        repartidor.pedidos_entregados = pedidos_entregados
        repartidor.pedidos_en_camino = pedidos_en_camino
        repartidor.pedidos_arribo = pedidos_arribo
        repartidor.pedidos_pendientes = pedidos_pendientes
        repartidor.pedidos_cancelados = pedidos_cancelados
        repartidor.tasa_entregas = tasa_entregas
        repartidor.tiempo_promedio_entrega_mins = tiempo_promedio_entrega_mins
        repartidor.tiempo_maximo_entrega_mins = tiempo_maximo_entrega_mins
        repartidor.tiempo_minimo_entrega_mins = tiempo_minimo_entrega_mins
        repartidor.fecha_ultima_entrega = fecha_ultima_entrega
        repartidor.pedidos_ultimos_7_dias = pedidos_ultimos_7_dias

        # Actualizar datos personales del repartidor (opcional)
        # Se puede obtener de otra tabla o evento si es necesario
        dim_repartidor = db.query(DimRepartidor).filter(DimRepartidor.repartidor_id == repartidor_id).first()
        if dim_repartidor:
            repartidor.nombre = dim_repartidor.nombre
            repartidor.apellido = dim_repartidor.apellido
            repartidor.telefono = dim_repartidor.telefono
            repartidor.email = dim_repartidor.email

        db.merge(repartidor)
        db.flush()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
