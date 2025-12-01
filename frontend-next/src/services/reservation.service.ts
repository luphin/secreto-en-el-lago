/**
 * Servicio de reservas
 * Maneja operaciones de reservas
 */
import apiClient from "@/lib/api";
import type { ReservationResponse, ReservationCreate, ReservationStatus } from "@/types/reservation.types";

export class ReservationService {
    /**
     * Obtiene la lista de reservas con filtros opcionales
     */
    static async getReservations(params?: {
        skip?: number;
        limit?: number;
        user_id?: string;
        document_id?: string;
        estado?: ReservationStatus;
    }): Promise<ReservationResponse[]> {
        const response = await apiClient.get<ReservationResponse[]>("/reservations/", { params });
        return response.data;
    }

    /**
     * Obtiene las reservas de un usuario específico
     */
    static async getUserReservations(userId: string, skip: number = 0, limit: number = 100): Promise<ReservationResponse[]> {
        const response = await apiClient.get<ReservationResponse[]>("/reservations/", {
            params: { skip, limit, user_id: userId }
        });
        return response.data;
    }

    /**
     * Obtiene una reserva por su ID
     */
    static async getReservationById(reservationId: string): Promise<ReservationResponse> {
        const response = await apiClient.get<ReservationResponse>(`/reservations/${reservationId}`);
        return response.data;
    }

    /**
     * Crea una nueva reserva
     */
    static async createReservation(reservation: ReservationCreate): Promise<ReservationResponse> {
        const response = await apiClient.post<ReservationResponse>("/reservations/", reservation);
        return response.data;
    }

    /**
     * Cancela una reserva
     */
    static async cancelReservation(reservationId: string): Promise<ReservationResponse> {
        const response = await apiClient.post<ReservationResponse>(`/reservations/${reservationId}/cancel`);
        return response.data;
    }

    /**
     * Completa una reserva (requiere permisos de bibliotecario)
     */
    static async completeReservation(reservationId: string): Promise<ReservationResponse> {
        const response = await apiClient.post<ReservationResponse>(`/reservations/${reservationId}/complete`);
        return response.data;
    }
}

export default ReservationService;
