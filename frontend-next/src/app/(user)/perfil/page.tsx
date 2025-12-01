"use client";

import {
  Box,
  Container,
  VStack,
  Heading,
  Input,
  Button,
  Card,
  HStack,
  Text,
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";
import { Field } from "@/components/ui/field";
import { useAuth } from "@/contexts/AuthContext";
import { toaster } from "@/components/ui/toaster";
import { PasswordInput } from "@/components/ui/password-input";

export default function PerfilPage() {
  const { user } = useAuth();

  return (
    <Box minH="100vh" bg="bg.canvas">
      <UserNav />

      <Container maxW="container.md">
        <VStack align="stretch" gap={6}>
          <Heading size="2xl">Mi Perfil</Heading>
          <Text color="gray.500" fontSize="sm" mt={2}>
            {user?._id}
          </Text>

          <Card.Root p={8}>
            <VStack align="stretch" gap={6}>
              <Heading size="lg" mb={2}>
                Informacion personal
              </Heading>

              <Field label="Nombres">
                <Input defaultValue={user?.nombres} size="lg" />
              </Field>

              <Field label="Apellidos">
                <Input defaultValue={user?.apellidos} size="lg" />
              </Field>

              <Field label="Correo electronico">
                <Input defaultValue={user?.email} size="lg" type="email" />
              </Field>

              <Field label="Telefono">
                <Input defaultValue={user?.telefono} size="lg" type="tel" />
              </Field>

              <Field label="Direccion">
                <Input defaultValue={user?.direccion} size="lg" />
              </Field>

              <HStack justify="end" gap={4} mt={4}>
                <Button variant="outline" size="lg">
                  Cancelar
                </Button>
                <Button colorPalette="blue" size="lg">
                  Guardar cambios
                </Button>
              </HStack>
            </VStack>
          </Card.Root>

          <Card.Root p={8}>
            <VStack align="stretch" gap={6}>
              <Heading size="lg" mb={2}>
                Cambiar contrasena
              </Heading>

              <Field label="Contrasena actual">
                <PasswordInput placeholder="********" size="lg" />
              </Field>

              <Field label="Nueva contrasena">
                <PasswordInput placeholder="********" size="lg" />
              </Field>

              <Field label="Confirmar nueva contrasena">
                <PasswordInput placeholder="********" size="lg" />
              </Field>

              <HStack justify="end" gap={4} mt={4}>
                <Button variant="outline" size="lg">
                  Cancelar
                </Button>
                <Button colorPalette="blue" size="lg">
                  Actualizar contrasena
                </Button>
              </HStack>
            </VStack>
          </Card.Root>
        </VStack>
      </Container>
    </Box>
  );
}
