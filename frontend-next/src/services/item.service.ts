/**
 * Servicio de ejemplares (items)
 * Maneja operaciones CRUD de ejemplares
 */
import apiClient from "@/lib/api";
import type { ItemResponse, ItemCreate, ItemUpdate, ItemStatus } from "@/types/item.types";

export class ItemService {
    /**
     * Obtiene la lista de ejemplares con filtros opcionales
     */
    static async getItems(params?: {
        skip?: number;
        limit?: number;
        document_id?: string;
        estado?: ItemStatus;
    }): Promise<ItemResponse[]> {
        const response = await apiClient.get<ItemResponse[]>("/items/", { params });
        return response.data;
    }

    /**
     * Obtiene un ejemplar por su ID
     */
    static async getItemById(itemId: string): Promise<ItemResponse> {
        const response = await apiClient.get<ItemResponse>(`/items/${itemId}`);
        return response.data;
    }

    /**
     * Crea un nuevo ejemplar (requiere permisos de bibliotecario)
     */
    static async createItem(item: ItemCreate): Promise<ItemResponse> {
        const response = await apiClient.post<ItemResponse>("/items/", item);
        return response.data;
    }

    /**
     * Actualiza un ejemplar (requiere permisos de bibliotecario)
     */
    static async updateItem(itemId: string, item: ItemUpdate): Promise<ItemResponse> {
        const response = await apiClient.put<ItemResponse>(`/items/${itemId}`, item);
        return response.data;
    }

    /**
     * Elimina un ejemplar (requiere permisos de bibliotecario)
     */
    static async deleteItem(itemId: string): Promise<void> {
        await apiClient.delete(`/items/${itemId}`);
    }
}

export default ItemService;
