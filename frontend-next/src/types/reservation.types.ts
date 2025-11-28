/**
 * Tipos de reservas
 */

export enum ReservationStatus {
    ACTIVA = "activa",
    COMPLETADA = "completada",
    EXPIRADA = "expirada",
}

export interface ReservationResponse {
    _id: string;
    document_id: string;
    user_id: string;
    fecha_reserva: string;
    fecha_creacion: string;
    estado: ReservationStatus;
}

export interface ReservationCreate {
    document_id: string;
    user_id: string;
    fecha_reserva: string;
}
