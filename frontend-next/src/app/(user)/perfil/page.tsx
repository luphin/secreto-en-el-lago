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
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";
import { Field } from "@/components/ui/field";

export default function PerfilPage() {
  return (
    <Box minH="100vh" bg="bg.canvas">
      <UserNav />

      <Container maxW="container.md">
        <VStack align="stretch" gap={6}>
          <Heading size="2xl">Mi Perfil</Heading>

          <Card.Root p={8}>
            <VStack align="stretch" gap={6}>
              <Heading size="lg" mb={2}>
                Informacion personal
              </Heading>

              <Field label="Nombre completo">
                <Input defaultValue="Juan Perez" size="lg" />
              </Field>

              <Field label="Correo electronico">
                <Input defaultValue="juan@email.com" size="lg" type="email" />
              </Field>

              <Field label="Telefono">
                <Input defaultValue="+56 9 1234 5678" size="lg" type="tel" />
              </Field>

              <Field label="Direccion">
                <Input defaultValue="Calle Ejemplo 123, Santiago" size="lg" />
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
                <Input type="password" placeholder="********" size="lg" />
              </Field>

              <Field label="Nueva contrasena">
                <Input type="password" placeholder="********" size="lg" />
              </Field>

              <Field label="Confirmar nueva contrasena">
                <Input type="password" placeholder="********" size="lg" />
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
