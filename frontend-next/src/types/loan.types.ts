/**
 * Tipos de préstamos para la aplicación
 */

export enum LoanType {
    SALA = "sala",
    DOMICILIO = "domicilio",
}

export enum LoanStatus {
    ACTIVO = "activo",
    DEVUELTO = "devuelto",
    VENCIDO = "vencido",
}

export interface LoanResponse {
    _id: string;
    item_id: string;
    user_id: string;
    tipo_prestamo: LoanType;
    fecha_prestamo: string;
    fecha_devolucion_pactada: string;
    fecha_devolucion_real?: string;
    estado: LoanStatus;
}

export interface LoanCreate {
    item_id: string;
    user_id: string;
    tipo_prestamo: LoanType;
}
