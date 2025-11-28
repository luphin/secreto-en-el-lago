/**
 * Servicio de préstamos
 * Maneja operaciones relacionadas con préstamos de libros
 */
import apiClient from "@/lib/api";
import type { LoanResponse, LoanCreate, LoanStatus } from "@/types/loan.types";

export class LoanService {
    /**
     * Obtiene los préstamos del usuario actual
     */
    static async getUserLoans(skip: number = 0, limit: number = 10, estado: LoanStatus): Promise<LoanResponse[]> {
        const response = await apiClient.get<LoanResponse[]>("/loans/", {
            params: { skip, limit, estado },
        });
        return response.data;
    }

    /**
     * Obtiene los préstamos vencidos (solo para bibliotecarios/admin)
     */
    static async getOverdueLoans(): Promise<LoanResponse[]> {
        const response = await apiClient.get<LoanResponse[]>("/loans/overdue");
        return response.data;
    }

    /**
     * Obtiene un préstamo específico por ID
     */
    static async getLoanById(loanId: string): Promise<LoanResponse> {
        const response = await apiClient.get<LoanResponse>(`/loans/${loanId}`);
        return response.data;
    }

    /**
     * Crea un nuevo préstamo (solo para bibliotecarios/admin)
     */
    static async createLoan(loan: LoanCreate): Promise<LoanResponse> {
        const response = await apiClient.post<LoanResponse>("/loans/", loan);
        return response.data;
    }

    /**
     * Procesa la devolución de un préstamo (solo para bibliotecarios/admin)
     */
    static async returnLoan(loanId: string): Promise<LoanResponse> {
        const response = await apiClient.post<LoanResponse>(`/loans/${loanId}/return`);
        return response.data;
    }
}

export default LoanService;
