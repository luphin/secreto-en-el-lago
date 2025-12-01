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
  SimpleGrid,
} from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { PasswordInput } from "@/components/ui/password-input";
import { Toaster, toaster } from "@/components/ui/toaster";
import NextLink from "next/link";
import AuthService from "@/services/auth.service";
import type { RegisterRequest } from "@/types/auth.types";

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<RegisterRequest>({
    rut: "",
    nombres: "",
    apellidos: "",
    direccion: "",
    telefono: "",
    email: "",
    password: "",
  });
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (field: keyof RegisterRequest) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [field]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Validación básica
    if (!formData.rut || !formData.nombres || !formData.apellidos ||
      !formData.direccion || !formData.telefono || !formData.email || !formData.password) {
      toaster.create({
        title: "Error",
        description: "Por favor completa todos los campos",
        type: "error",
        duration: 3000,
      });
      return;
    }

    // Validar confirmación de contraseña
    if (formData.password !== confirmPassword) {
      toaster.create({
        title: "Error",
        description: "Las contraseñas no coinciden",
        type: "error",
        duration: 3000,
      });
      return;
    }

    // Validar longitud de contraseña
    if (formData.password.length < 6) {
      toaster.create({
        title: "Error",
        description: "La contraseña debe tener al menos 6 caracteres",
        type: "error",
        duration: 3000,
      });
      return;
    }

    setIsLoading(true);

    try {
      await AuthService.register(formData);

      toaster.create({
        title: "¡Registro exitoso!",
        description: "Tu cuenta ha sido creada. Por favor revisa tu email para activarla.",
        type: "success",
        duration: 5000,
      });

      // Redirigir al login después de un momento
      setTimeout(() => {
        router.push("/login");
      }, 2000);

    } catch (error: any) {
      console.error("Error en registro:", error);

      let errorMessage = "Error al registrar usuario";

      if (error.response?.status === 400) {
        if (error.response.data?.detail?.includes("email")) {
          errorMessage = "El email ya está registrado";
        } else if (error.response.data?.detail?.includes("RUT")) {
          errorMessage = "El RUT ya está registrado";
        } else {
          errorMessage = error.response.data?.detail || errorMessage;
        }
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
    <Box minH="100vh" bg="bg.canvas" display="flex" alignItems="center" justifyContent="center" py={8}>
      <Toaster />
      <Container maxW="2xl">
        <Card.Root p={8}>
          <form onSubmit={handleSubmit}>
            <VStack gap={6} align="stretch">
              <VStack gap={2}>
                <Heading size="xl" color="blue.600">
                  Crear cuenta
                </Heading>
                <Text color="gray.600">
                  Regístrate para acceder a todos los servicios
                </Text>
              </VStack>

              <VStack gap={4} align="stretch">
                <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
                  <Field label="RUT" required>
                    <Input
                      type="text"
                      placeholder="12345678-9"
                      size="lg"
                      value={formData.rut}
                      onChange={handleChange("rut")}
                      disabled={isLoading}
                    />
                  </Field>

                  <Field label="Teléfono" required>
                    <Input
                      type="tel"
                      placeholder="+56912345678"
                      size="lg"
                      value={formData.telefono}
                      onChange={handleChange("telefono")}
                      disabled={isLoading}
                    />
                  </Field>
                </SimpleGrid>

                <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
                  <Field label="Nombres" required>
                    <Input
                      type="text"
                      placeholder="Juan Pablo"
                      size="lg"
                      value={formData.nombres}
                      onChange={handleChange("nombres")}
                      disabled={isLoading}
                    />
                  </Field>

                  <Field label="Apellidos" required>
                    <Input
                      type="text"
                      placeholder="Pérez González"
                      size="lg"
                      value={formData.apellidos}
                      onChange={handleChange("apellidos")}
                      disabled={isLoading}
                    />
                  </Field>
                </SimpleGrid>

                <Field label="Dirección" required>
                  <Input
                    type="text"
                    placeholder="Calle Principal 123"
                    size="lg"
                    value={formData.direccion}
                    onChange={handleChange("direccion")}
                    disabled={isLoading}
                  />
                </Field>

                <Field label="Correo electrónico" required>
                  <Input
                    type="email"
                    placeholder="tu@email.com"
                    size="lg"
                    value={formData.email}
                    onChange={handleChange("email")}
                    disabled={isLoading}
                  />
                </Field>

                <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
                  <Field label="Contraseña" required>
                    <PasswordInput
                      placeholder="Mínimo 6 caracteres"
                      size="lg"
                      value={formData.password}
                      onChange={handleChange("password")}
                      disabled={isLoading}
                    />
                  </Field>

                  <Field label="Confirmar contraseña" required>
                    <PasswordInput
                      placeholder="Repite tu contraseña"
                      size="lg"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      disabled={isLoading}
                    />
                  </Field>
                </SimpleGrid>

                <Button
                  type="submit"
                  colorPalette="blue"
                  size="lg"
                  w="full"
                  loading={isLoading}
                >
                  {isLoading ? "Registrando..." : "Registrarse"}
                </Button>

                <Text textAlign="center" fontSize="sm" color="gray.600">
                  ¿Ya tienes cuenta?{" "}
                  <NextLink href="/login" style={{ color: "var(--chakra-colors-blue-600)", fontWeight: "500" }}>
                    Inicia sesión aquí
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
