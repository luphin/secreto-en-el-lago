/**
 * Servicio de autenticación
 * Maneja login, registro, logout y gestión de tokens
 */
import apiClient from "@/lib/api";
import type { LoginRequest, RegisterRequest, AuthResponse, UserResponse } from "@/types/auth.types";

const TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

export class AuthService {
    /**
     * Registra un nuevo usuario
     */
    static async register(data: RegisterRequest): Promise<UserResponse> {
        const response = await apiClient.post<UserResponse>("/auth/register", data);
        return response.data;
    }

    /**
     * Inicia sesión con email y contraseña
     */
    static async login(credentials: LoginRequest): Promise<AuthResponse> {
        const response = await apiClient.post<AuthResponse>("/auth/login", credentials);
        const { access_token, refresh_token } = response.data;

        // Guardar tokens en localStorage
        this.setToken(access_token);
        this.setRefreshToken(refresh_token);

        return response.data;
    }

    /**
     * Obtiene la información del usuario autenticado desde el backend
     */
    static async fetchUserInfo(): Promise<UserResponse> {
        const response = await apiClient.get<UserResponse>("/users/me");
        return response.data;
    }

    /**
     * Cierra la sesión del usuario
     */
    static logout(): void {
        this.removeToken();
        this.removeRefreshToken();
    }

    /**
     * Obtiene el token de acceso almacenado
     */
    static getToken(): string | null {
        if (typeof window === "undefined") return null;
        return localStorage.getItem(TOKEN_KEY);
    }

    /**
     * Guarda el token de acceso
     */
    static setToken(token: string): void {
        if (typeof window === "undefined") return;
        localStorage.setItem(TOKEN_KEY, token);
    }

    /**
     * Elimina el token de acceso
     */
    static removeToken(): void {
        if (typeof window === "undefined") return;
        localStorage.removeItem(TOKEN_KEY);
    }

    /**
     * Obtiene el refresh token almacenado
     */
    static getRefreshToken(): string | null {
        if (typeof window === "undefined") return null;
        return localStorage.getItem(REFRESH_TOKEN_KEY);
    }

    /**
     * Guarda el refresh token
     */
    static setRefreshToken(token: string): void {
        if (typeof window === "undefined") return;
        localStorage.setItem(REFRESH_TOKEN_KEY, token);
    }

    /**
     * Elimina el refresh token
     */
    static removeRefreshToken(): void {
        if (typeof window === "undefined") return;
        localStorage.removeItem(REFRESH_TOKEN_KEY);
    }

    /**
     * Verifica si el usuario está autenticado
     */
    static isAuthenticated(): boolean {
        return this.getToken() !== null;
    }
}

export default AuthService;
