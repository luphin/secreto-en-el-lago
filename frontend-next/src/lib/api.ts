/**
 * Configuración base de Axios para comunicación con el backend
 */
import axios, { AxiosError, InternalAxiosRequestConfig, AxiosResponse } from "axios";

// URL base del backend - ajustar según el entorno
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

// Crear instancia de axios con configuración base
export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// Interceptor para agregar el token de autenticación a las peticiones
apiClient.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error: AxiosError) => {
        return Promise.reject(error);
    }
);

// Interceptor para manejar errores de respuesta
apiClient.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error: AxiosError) => {
        // Si el token expiró (401), limpiar el almacenamiento y redirigir al login
        if (error.response?.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");

            // Solo redirigir si estamos en el navegador y NO estamos ya en una página de login
            if (typeof window !== "undefined") {
                const currentPath = window.location.pathname;
                const isOnLoginPage = currentPath === "/login" || currentPath === "/admin/login";

                // No redirigir si ya estamos en una página de login
                if (!isOnLoginPage) {
                    // Redirigir a la página de login apropiada según la ruta actual
                    if (currentPath.startsWith("/admin")) {
                        window.location.href = "/admin/login";
                    } else {
                        window.location.href = "/login";
                    }
                }
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;
