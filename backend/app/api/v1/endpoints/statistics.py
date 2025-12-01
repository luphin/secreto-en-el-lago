"""
Endpoints de estadísticas y reportes
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from bson import ObjectId

from app.core.database import get_database
from app.api.dependencies import get_bibliotecario_user, get_current_user
from app.models.user import UserRole

router = APIRouter()


@router.get("/loans/history", response_model=List[Dict[str, Any]])
async def get_loan_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Obtiene el historial de préstamos del usuario actual
    """
    # Obtener préstamos del usuario
    loans_cursor = db.loans.find({
        "user_id": str(current_user["_id"])
    }).sort("fecha_prestamo", -1).skip(skip).limit(limit)
    
    loans = await loans_cursor.to_list(length=limit)
    
    # Enriquecer con información de documentos
    result = []
    for loan in loans:
        item = await db.items.find_one({"_id": ObjectId(loan["item_id"])})
        if item:
            # El document_id puede ser un ObjectId o un ID físico (string)
            document_id = item["document_id"]
            
            # Intentar buscar por ObjectId primero
            try:
                document = await db.documents.find_one({"_id": ObjectId(document_id)})
            except:
                # Si falla, buscar por ID físico
                document = await db.documents.find_one({"id_fisico": document_id})
            
            if document:
                result.append({
                    "loan_id": str(loan["_id"]),
                    "document": {
                        "title": document["titulo"],
                        "author": document["autor"],
                        "tipo": document["tipo"]
                    },
                    "tipo_prestamo": loan["tipo_prestamo"],
                    "fecha_prestamo": loan["fecha_prestamo"],
                    "fecha_devolucion_pactada": loan["fecha_devolucion_pactada"],
                    "fecha_devolucion_real": loan.get("fecha_devolucion_real"),
                    "estado": loan["estado"]
                })
    
    return result


@router.get("/documents/popular", response_model=List[Dict[str, Any]])
async def get_popular_documents(
    limit: int = Query(10, ge=1, le=50),
    days: int = Query(30, ge=1, le=365),
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Obtiene los documentos más populares (más prestados)
    Requiere rol de bibliotecario o administrativo
    """
    # Fecha límite para contar préstamos
    date_limit = datetime.utcnow() - timedelta(days=days)
    
    # Agregar préstamos por documento
    pipeline = [
        {
            "$match": {
                "fecha_prestamo": {"$gte": date_limit}
            }
        },
        {
            "$lookup": {
                "from": "items",
                "localField": "item_id",
                "foreignField": "_id",
                "as": "item"
            }
        },
        {
            "$unwind": "$item"
        },
        {
            "$group": {
                "_id": "$item.document_id",
                "total_prestamos": {"$sum": 1}
            }
        },
        {
            "$sort": {"total_prestamos": -1}
        },
        {
            "$limit": limit
        }
    ]
    
    results = await db.loans.aggregate(pipeline).to_list(length=limit)
    
    # Enriquecer con información de documentos
    popular_docs = []
    for result in results:
        document = await db.documents.find_one({"_id": ObjectId(result["_id"])})
        if document:
            popular_docs.append({
                "document_id": str(document["_id"]),
                "titulo": document["titulo"],
                "autor": document["autor"],
                "categoria": document["categoria"],
                "tipo": document["tipo"],
                "total_prestamos": result["total_prestamos"]
            })
    
    return popular_docs


@router.get("/users/active", response_model=List[Dict[str, Any]])
async def get_active_users(
    limit: int = Query(10, ge=1, le=50),
    days: int = Query(30, ge=1, le=365),
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Obtiene los usuarios más activos (más préstamos)
    Requiere rol de bibliotecario o administrativo
    """
    date_limit = datetime.utcnow() - timedelta(days=days)
    
    pipeline = [
        {
            "$match": {
                "fecha_prestamo": {"$gte": date_limit}
            }
        },
        {
            "$group": {
                "_id": "$user_id",
                "total_prestamos": {"$sum": 1}
            }
        },
        {
            "$sort": {"total_prestamos": -1}
        },
        {
            "$limit": limit
        }
    ]
    
    results = await db.loans.aggregate(pipeline).to_list(length=limit)
    
    # Enriquecer con información de usuarios
    active_users = []
    for result in results:
        user = await db.users.find_one({"_id": ObjectId(result["_id"])})
        if user:
            active_users.append({
                "user_id": str(user["_id"]),
                "nombre": f"{user['nombres']} {user['apellidos']}",
                "email": user["email"],
                "total_prestamos": result["total_prestamos"]
            })
    
    return active_users


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_stats(
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Obtiene estadísticas generales para el dashboard
    Requiere rol de bibliotecario o administrativo
    """
    # Contar totales
    total_users = await db.users.count_documents({"rol": "lector"})
    total_documents = await db.documents.count_documents({})
    total_items = await db.items.count_documents({})
    items_disponibles = await db.items.count_documents({"estado": "disponible"})
    items_prestados = await db.items.count_documents({"estado": "prestado"})
    
    # Préstamos activos
    active_loans = await db.loans.count_documents({"estado": "activo"})
    overdue_loans = await db.loans.count_documents({"estado": "vencido"})
    
    # Reservas activas
    active_reservations = await db.reservations.count_documents({"estado": "activa"})
    
    # Préstamos del último mes
    date_limit = datetime.utcnow() - timedelta(days=30)
    loans_last_month = await db.loans.count_documents({
        "fecha_prestamo": {"$gte": date_limit}
    })
    
    # Usuarios sancionados
    sanctioned_users = await db.users.count_documents({
        "sancion_hasta": {"$gte": datetime.utcnow()}
    })
    
    return {
        "users": {
            "total": total_users,
            "sanctioned": sanctioned_users
        },
        "collection": {
            "total_documents": total_documents,
            "total_items": total_items,
            "items_disponibles": items_disponibles,
            "items_prestados": items_prestados
        },
        "loans": {
            "active": active_loans,
            "overdue": overdue_loans,
            "last_month": loans_last_month
        },
        "reservations": {
            "active": active_reservations
        }
    }


@router.get("/export/loans")
async def export_loans_csv(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Exporta préstamos a CSV
    Requiere rol de bibliotecario o administrativo
    """
    from fastapi.responses import StreamingResponse
    import io
    import csv
    
    # Construir query
    query = {}
    if start_date or end_date:
        query["fecha_prestamo"] = {}
        if start_date:
            query["fecha_prestamo"]["$gte"] = start_date
        if end_date:
            query["fecha_prestamo"]["$lte"] = end_date
    
    # Obtener préstamos
    loans = await db.loans.find(query).to_list(length=None)
    
    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escribir encabezados
    writer.writerow([
        'ID Préstamo', 'Usuario', 'Documento', 'Tipo Préstamo',
        'Fecha Préstamo', 'Fecha Devolución Pactada', 'Fecha Devolución Real',
        'Estado'
    ])
    
    # Escribir datos
    for loan in loans:
        user = await db.users.find_one({"_id": ObjectId(loan["user_id"])})
        item = await db.items.find_one({"_id": ObjectId(loan["item_id"])})
        document = None
        if item:
            # El document_id puede ser un ObjectId o un ID físico (string)
            document_id = item["document_id"]
            try:
                document = await db.documents.find_one({"_id": ObjectId(document_id)})
            except:
                document = await db.documents.find_one({"id_fisico": document_id})
        
        writer.writerow([
            str(loan["_id"]),
            f"{user['nombres']} {user['apellidos']}" if user else "N/A",
            document["titulo"] if document else "N/A",
            loan["tipo_prestamo"],
            loan["fecha_prestamo"].strftime("%Y-%m-%d %H:%M"),
            loan["fecha_devolucion_pactada"].strftime("%Y-%m-%d %H:%M"),
            loan["fecha_devolucion_real"].strftime("%Y-%m-%d %H:%M") if loan.get("fecha_devolucion_real") else "N/A",
            loan["estado"]
        ])
    
    # Preparar respuesta
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=prestamos.csv"}
    )

