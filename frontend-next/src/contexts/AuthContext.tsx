"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter, usePathname } from "next/navigation";
import AuthService from "@/services/auth.service";
import type { UserResponse } from "@/types/auth.types";

interface AuthContextType {
    user: UserResponse | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    logoutAdmin: () => void;
    refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
    children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
    const [user, setUser] = useState<UserResponse | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();
    const pathname = usePathname();

    // Cargar información del usuario al montar el componente
    useEffect(() => {
        const loadUser = async () => {
            const token = AuthService.getToken();

            if (token) {
                try {
                    const userInfo = await AuthService.fetchUserInfo();
                    setUser(userInfo);
                } catch (error) {
                    console.error("Error al cargar usuario:", error);
                    // Si falla, limpiar tokens
                    AuthService.logout();
                    setUser(null);
                }
            }

            setIsLoading(false);
        };

        loadUser();
    }, []);

    const login = async (email: string, password: string) => {
        await AuthService.login({ email, password });

        // Obtener información del usuario
        const userInfo = await AuthService.fetchUserInfo();
        setUser(userInfo);
    };

    // logout normal
    const logout = () => {
        AuthService.logout();
        setUser(null);
        router.push("/");
    };
    // logout admin
    const logoutAdmin = () => {
        AuthService.logout();
        setUser(null);
        router.push("/admin/login");
    };
    const refreshUser = async () => {
        try {
            const userInfo = await AuthService.fetchUserInfo();
            setUser(userInfo);
        } catch (error) {
            console.error("Error al refrescar usuario:", error);
            // Solo limpiar tokens sin redirigir
            AuthService.logout();
            setUser(null);
        }
    };

    const value: AuthContextType = {
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        logout,
        logoutAdmin,
        refreshUser,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth debe ser usado dentro de un AuthProvider");
    }
    return context;
}
