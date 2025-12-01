/**
 * Tipos de documentos bibliográficos
 */

export enum DocumentType {
    LIBRO = "libro",
    AUDIO = "audio",
    VIDEO = "video",
}

export interface DocumentResponse {
    _id: string;
    id_fisico: string;
    titulo: string;
    autor: string;
    editorial: string;
    edicion: string;
    ano_edicion: number;
    tipo: DocumentType;
    categoria: string;
    tipo_medio?: string;
    items_disponibles: number;
}

export interface DocumentCreate {
    id_fisico: string;
    titulo: string;
    autor: string;
    editorial: string;
    edicion: string;
    ano_edicion: number;
    tipo: DocumentType;
    categoria: string;
    tipo_medio?: string;
}

export interface DocumentUpdate {
    id_fisico?: string;
    titulo?: string;
    autor?: string;
    editorial?: string;
    edicion?: string;
    ano_edicion?: number;
    tipo?: DocumentType;
    categoria?: string;
    tipo_medio?: string;
}
