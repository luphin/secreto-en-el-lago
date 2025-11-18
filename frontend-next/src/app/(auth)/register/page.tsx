"use client";

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
import NextLink from "next/link";

export default function RegisterPage() {
  return (
    <Box minH="100vh" bg="bg.canvas" display="flex" alignItems="center" justifyContent="center">
      <Container maxW="md">
        <Card.Root p={8}>
          <VStack gap={6} align="stretch">
            <VStack gap={2}>
              <Heading size="xl" color="blue.600">
                Crear cuenta
              </Heading>
              <Text color="gray.600">
                Registrate para acceder a todos los servicios
              </Text>
            </VStack>

            <VStack gap={4} align="stretch">
              <Field label="Nombre completo">
                <Input
                  type="text"
                  placeholder="Tu nombre"
                  size="lg"
                />
              </Field>

              <Field label="Correo electronico">
                <Input
                  type="email"
                  placeholder="tu@email.com"
                  size="lg"
                />
              </Field>

              <Field label="Contrasena">
                <Input
                  type="password"
                  placeholder="********"
                  size="lg"
                />
              </Field>

              <Field label="Confirmar contrasena">
                <Input
                  type="password"
                  placeholder="********"
                  size="lg"
                />
              </Field>

              <Button colorPalette="blue" size="lg" w="full">
                Registrarse
              </Button>

              <Text textAlign="center" fontSize="sm" color="gray.600">
                Ya tienes cuenta?{" "}
                <NextLink href="/login" style={{ color: "var(--chakra-colors-blue-600)", fontWeight: "500" }}>
                  Inicia sesion aquí
                </NextLink>
              </Text>

              <Text textAlign="center" fontSize="sm">
                <NextLink href="/" style={{ color: "var(--chakra-colors-gray-600)" }}>
                  Volver al catálogo
                </NextLink>
              </Text>
            </VStack>
          </VStack>
        </Card.Root>
      </Container>
    </Box>
  );
}
