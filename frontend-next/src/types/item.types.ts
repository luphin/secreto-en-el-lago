/**
 * Tipos de ejemplares (items)
 */

export enum ItemStatus {
    DISPONIBLE = "disponible",
    PRESTADO = "prestado",
    EN_RESTAURACION = "en_restauracion",
    RESERVADO = "reservado",
}

export interface ItemResponse {
    _id: string;
    document_id: string;
    ubicacion: string;
    estado: ItemStatus;
}

export interface ItemCreate {
    document_id: string;
    ubicacion: string;
    estado?: ItemStatus;
}

export interface ItemUpdate {
    ubicacion?: string;
    estado?: ItemStatus;
}
