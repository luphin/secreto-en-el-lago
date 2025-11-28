"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import {
    Box,
    Container,
    VStack,
    Heading,
    Input,
    Button,
    Text,
    Card,
} from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { PasswordInput } from "@/components/ui/password-input";
import { Toaster, toaster } from "@/components/ui/toaster";
import NextLink from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { UserRole } from "@/types/auth.types";

export default function AdminLoginPage() {
    const router = useRouter();
    const { login } = useAuth();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (!email || !password) {
            toaster.create({
                title: "Error",
                description: "Por favor completa todos los campos",
                type: "error",
                duration: 3000,
            });
            return;
        }

        setIsLoading(true);

        try {
            await login(email, password);

            // Verificar que el usuario sea admin o bibliotecario
            const userInfo = await import("@/services/auth.service").then(m => m.default.fetchUserInfo());

            if (userInfo.rol !== UserRole.BIBLIOTECARIO && userInfo.rol !== UserRole.ADMINISTRATIVO) {
                toaster.create({
                    title: "Acceso denegado",
                    description: "No tienes permisos de administrador",
                    type: "error",
                    duration: 4000,
                });

                // Logout y redirigir
                await import("@/services/auth.service").then(m => m.default.logout());
                return;
            }

            toaster.create({
                title: "¡Bienvenido!",
                description: "Has iniciado sesión como administrador",
                type: "success",
                duration: 2000,
            });

            setTimeout(() => {
                router.push("/admin");
            }, 500);

        } catch (error: any) {
            console.error("Error en login:", error);

            let errorMessage = "Error al iniciar sesión";

            if (error.response?.status === 401) {
                errorMessage = "Email o contraseña incorrectos";
            } else if (error.response?.status === 403) {
                errorMessage = "Cuenta no activada. Por favor revisa tu email.";
            } else if (error.response?.data?.detail) {
                errorMessage = error.response.data.detail;
            }

            toaster.create({
                title: "Error",
                description: errorMessage,
                type: "error",
                duration: 4000,
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box minH="100vh" bg="purple.50" display="flex" alignItems="center" justifyContent="center">
            <Container maxW="md">
                <VStack gap={8}>
                    <VStack gap={2} textAlign="center">
                        <Heading size="2xl" color="purple.700">
                            Panel de Administración
                        </Heading>
                        <Text color="gray.600">
                            Ingresa tus credenciales de administrador
                        </Text>
                    </VStack>

                    <Card.Root w="full" p={8}>
                        <form onSubmit={handleSubmit}>
                            <VStack gap={6}>
                                <Field label="Correo electrónico" required>
                                    <Input
                                        type="email"
                                        placeholder="admin@biblioteca.com"
                                        size="lg"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        disabled={isLoading}
                                    />
                                </Field>

                                <Field label="Contraseña" required>
                                    <PasswordInput
                                        placeholder="********"
                                        size="lg"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        disabled={isLoading}
                                    />
                                </Field>

                                <Button
                                    type="submit"
                                    colorPalette="purple"
                                    size="lg"
                                    w="full"
                                    loading={isLoading}
                                >
                                    {isLoading ? "Iniciando sesión..." : "Iniciar sesión"}
                                </Button>

                                <Text fontSize="sm" color="gray.600" textAlign="center">
                                    ¿Eres usuario regular?{" "}
                                    <NextLink href="/login" style={{ color: "var(--chakra-colors-purple-600)", fontWeight: "500" }}>
                                        Ir al login de usuarios
                                    </NextLink>
                                </Text>
                            </VStack>
                        </form>
                    </Card.Root>
                </VStack>
            </Container>
            <Toaster />
        </Box>
    );
}
