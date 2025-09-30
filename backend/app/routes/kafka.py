from fastapi import APIRouter, HTTPException
from app.services.kafka_manager import kafka_manager

router = APIRouter()

@router.get("/topics")
async def list_topics():
    """Lista todos los topics de Kafka"""
    try:
        topics = await kafka_manager.list_topics()
        return {"topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando topics: {str(e)}")

@router.get("/topics/{topic_name}")
async def get_topic_info(topic_name: str):
    """Obtiene información de un topic específico"""
    try:
        topic_info = await kafka_manager.get_topic_info(topic_name)
        return {"topic": topic_name, "info": topic_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo información del topic: {str(e)}")

@router.post("/topics/{topic_name}")
async def create_topic(topic_name: str):
    """Crea un nuevo topic (solo para desarrollo)"""
    try:
        # En producción, esto debería estar restringido
        await kafka_manager.create_topics([topic_name])
        return {"message": f"Topic {topic_name} creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando topic: {str(e)}")

@router.delete("/topics/{topic_name}")
async def delete_topic(topic_name: str):
    """Elimina un topic (solo para desarrollo)"""
    try:
        success = await kafka_manager.delete_topic(topic_name)
        if success:
            return {"message": f"Topic {topic_name} eliminado exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="No se pudo eliminar el topic")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando topic: {str(e)}")
