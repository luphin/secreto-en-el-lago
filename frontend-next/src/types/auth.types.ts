/**
 * Tipos de autenticación para la aplicación
 */

export enum UserRole {
    LECTOR = "lector",
    BIBLIOTECARIO = "bibliotecario",
    ADMINISTRATIVO = "administrativo",
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest {
    rut: string;
    nombres: string;
    apellidos: string;
    direccion: string;
    telefono: string;
    email: string;
    password: string;
    foto_url?: string;
    huella_ref?: string;
}

export interface AuthResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface UserResponse {
    _id: string;
    rut: string;
    nombres: string;
    apellidos: string;
    direccion: string;
    telefono: string;
    email: string;
    rol: UserRole;
    activo: boolean;
    fecha_creacion: string;
    foto_url?: string;
    huella_ref?: string;
    sancion_hasta?: string;
}
