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

export default function LoginPage() {
  return (
    <Box minH="100vh" bg="bg.canvas" display="flex" alignItems="center" justifyContent="center">
      <Container maxW="md">
        <Card.Root p={8}>
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

              <Button colorPalette="blue" size="lg" w="full">
                Iniciar sesión
              </Button>

              <Text textAlign="center" fontSize="sm" color="gray.600">
                No tienes cuenta?{" "}
                <NextLink href="/register" style={{ color: "var(--chakra-colors-blue-600)", fontWeight: "500" }}>
                  Registrate aquí
                </NextLink>
              </Text>

              <Text textAlign="center" fontSize="sm">
                <NextLink href="/" style={{ color: "var(--chakra-colors-gray-600)" }}>
                  Volver al catalogo
                </NextLink>
              </Text>
            </VStack>
          </VStack>
        </Card.Root>
      </Container>
    </Box>
  );
}
