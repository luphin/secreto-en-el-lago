/**
 * Servicio de estadísticas
 * Maneja operaciones relacionadas con estadísticas y reportes
 */
import apiClient from "@/lib/api";

export interface LoanHistoryItem {
    loan_id: string;
    document: {
        title: string;
        author: string;
        tipo: string;
    };
    tipo_prestamo: string;
    fecha_prestamo: string;
    fecha_devolucion_pactada: string;
    fecha_devolucion_real?: string;
    estado: string;
}

export interface PopularDocument {
    document_id: string;
    titulo: string;
    autor: string;
    categoria: string;
    tipo: string;
    total_prestamos: number;
}

export interface DashboardStats {
    users: {
        total: number;
        sanctioned: number;
    };
    collection: {
        total_documents: number;
        total_items: number;
        items_disponibles: number;
        items_prestados: number;
    };
    loans: {
        active: number;
        overdue: number;
        last_month: number;
    };
    reservations: {
        active: number;
    };
}

export class StatisticsService {
    /**
     * Obtiene el historial de préstamos del usuario actual
     */
    static async getLoanHistory(skip: number = 0, limit: number = 10): Promise<LoanHistoryItem[]> {
        const response = await apiClient.get<LoanHistoryItem[]>("/statistics/loans/history", {
            params: { skip, limit },
        });
        return response.data;
    }

    /**
     * Obtiene los documentos más populares (requiere rol de bibliotecario/admin)
     */
    static async getPopularDocuments(limit: number = 10, days: number = 30): Promise<PopularDocument[]> {
        const response = await apiClient.get<PopularDocument[]>("/statistics/documents/popular", {
            params: { limit, days },
        });
        return response.data;
    }

    /**
     * Obtiene estadísticas del dashboard (requiere rol de bibliotecario/admin)
     */
    static async getDashboardStats(): Promise<DashboardStats> {
        const response = await apiClient.get<DashboardStats>("/statistics/dashboard");
        return response.data;
    }

    /**
     * Exporta préstamos a CSV (requiere rol de bibliotecario/admin)
     */
    static async exportLoans(startDate?: string, endDate?: string): Promise<Blob> {
        const response = await apiClient.get("/statistics/export/loans", {
            params: { start_date: startDate, end_date: endDate },
            responseType: "blob",
        });
        return response.data;
    }
}

export default StatisticsService;
