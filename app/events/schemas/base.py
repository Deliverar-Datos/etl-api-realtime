from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventTopic(str, Enum):
    ## Blockchain
    CRYPTO_PAYMENT = "crypto.payment"
    BUY_CRYPTO = "buy.crypto"
    SELL_CRYPTO = "sell.crypto"
    
    ## Marketplace
    TENANT_CREADO = "tenant.creado"
    COMERCIO_CREADO = "comercio.creado"
    CATEGORIA_CREADA = "categoria.creada"

    BI_TEST = "bi.test"

    ## Repartidor
    PEDIDO_ACEPTADO = "pedido.aceptado"
    PEDIDO_ASIGNADO = "pedido.asignado"
    PEDIDO_ENTREGADO = "pedido.entregado"
    PEDIDO_ARRIBO = "pedido.arribo"
    DELIVERY_NUEVOREPARTIDOR = "delivery.nuevoRepartidor"
    PEDIDO_ENCAMINO = "pedido.enCamino"
    PEDIDO_CANCELADO = "pedido.cancelado"

    ## Backoffice
    IVA_RESPUESTA = "iva.respuesta"

    ## 📊 Dashboard BI
    # → Promociones
    PROMO_REGISTRADA = "promo.registrada"
    PROMO_COMERCIO_ASOCIADA = "promo.comercio_asociada"
    PROMO_TENANT_ASOCIADA = "promo.tenant_asociada"
    # → Ordenes
    ORDEN_REGISTRADA = "orden.registrada"
    ORDEN_ESTADO_ACTUALIZADO = "orden.estadoActualizado"
    # → Clientes
    CLIENT_REGISTRADO = "cliente.registrado"
    # → Deliveries
    DELIVERY_REGISTRADO = "delivery.registrado"



class CallbackRequest(BaseModel):
    body: Optional[dict] = None
