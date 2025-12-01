/**
 * Servicio de usuarios
 * Maneja operaciones relacionadas con usuarios
 */
import apiClient from "@/lib/api";
import type { UserResponse } from "@/types/auth.types";
import { UserRole } from "@/types/auth.types";

export class UserService {
    /**
     * Obtiene usuarios con filtros opcionales
     */
    static async getUsers(
        skip: number = 0,
        limit: number = 100,
        rol?: UserRole
    ): Promise<UserResponse[]> {
        const params: Record<string, any> = { skip, limit };
        if (rol) {
            params.rol = rol;
        }

        const response = await apiClient.get<UserResponse[]>("/users/", {
            params,
        });
        return response.data;
    }

    /**
     * Obtiene un usuario específico por ID
     */
    static async getUserById(userId: string): Promise<UserResponse> {
        const response = await apiClient.get<UserResponse>(`/users/${userId}`);
        return response.data;
    }
}

export default UserService;
