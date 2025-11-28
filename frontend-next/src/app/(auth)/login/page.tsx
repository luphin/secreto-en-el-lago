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

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Validación básica
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

      toaster.create({
        title: "¡Bienvenido!",
        description: "Has iniciado sesión exitosamente",
        type: "success",
        duration: 2000,
      });

      // Redirigir al dashboard
      setTimeout(() => {
        router.push("/dashboard");
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
    <Box minH="100vh" bg="bg.canvas" display="flex" alignItems="center" justifyContent="center">
      <Toaster />
      <Container maxW="md">
        <Card.Root p={8}>
          <form onSubmit={handleSubmit}>
            <VStack gap={6} align="stretch">
              <VStack gap={2}>
                <Heading size="xl" color="blue.600">
                  Iniciar sesión
                </Heading>
                <Text color="gray.600">
                  Accede a tu cuenta de biblioteca
                </Text>
              </VStack>

              <VStack gap={4} align="stretch">
                <Field label="Correo electrónico" required>
                  <Input
                    type="email"
                    placeholder="theo@test.com"
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
                  colorPalette="blue"
                  size="lg"
                  w="full"
                  loading={isLoading}
                >
                  {isLoading ? "Iniciando sesión..." : "Iniciar sesión"}
                </Button>

                <Text textAlign="center" fontSize="sm" color="gray.600">
                  ¿No tienes cuenta?{" "}
                  <NextLink href="/register" style={{ color: "var(--chakra-colors-blue-600)", fontWeight: "500" }}>
                    Regístrate aquí
                  </NextLink>
                </Text>

                <Text textAlign="center" fontSize="sm">
                  <NextLink href="/" style={{ color: "var(--chakra-colors-gray-600)" }}>
                    Volver al catálogo
                  </NextLink>
                </Text>
              </VStack>
            </VStack>
          </form>
        </Card.Root>
      </Container>
    </Box>
  );
}
