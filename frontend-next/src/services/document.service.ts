/**
 * Servicio de documentos bibliográficos
 * Maneja operaciones CRUD de documentos
 */
import apiClient from "@/lib/api";
import type { DocumentResponse, DocumentCreate, DocumentUpdate } from "@/types/document.types";

export class DocumentService {
    /**
     * Obtiene la lista de documentos con filtros opcionales
     */
    static async getDocuments(params?: {
        skip?: number;
        limit?: number;
        titulo?: string;
        autor?: string;
        categoria?: string;
        search?: string;
    }): Promise<DocumentResponse[]> {
        const response = await apiClient.get<DocumentResponse[]>("/documents/", { params });
        return response.data;
    }

    /**
     * Obtiene un documento por su ID
     */
    static async getDocumentById(documentId: string): Promise<DocumentResponse> {
        const response = await apiClient.get<DocumentResponse>(`/documents/${documentId}`);
        return response.data;
    }

    /**
     * Obtiene un documento por su ID físico
     */
    static async getDocumentByPhysicalId(idFisico: string): Promise<{ id_fisico: string; document_id: string }> {
        const response = await apiClient.get<{ id_fisico: string; document_id: string }>(
            `/documents/by-physical-id/${idFisico}`
        );
        return response.data;
    }

    /**
     * Crea un nuevo documento (requiere permisos de bibliotecario)
     */
    static async createDocument(document: DocumentCreate): Promise<DocumentResponse> {
        const response = await apiClient.post<DocumentResponse>("/documents/", document);
        return response.data;
    }

    /**
     * Actualiza un documento (requiere permisos de bibliotecario)
     */
    static async updateDocument(documentId: string, document: DocumentUpdate): Promise<DocumentResponse> {
        const response = await apiClient.put<DocumentResponse>(`/documents/${documentId}`, document);
        return response.data;
    }

    /**
     * Elimina un documento (requiere permisos de bibliotecario)
     */
    static async deleteDocument(documentId: string): Promise<void> {
        await apiClient.delete(`/documents/${documentId}`);
    }
}

export default DocumentService;
