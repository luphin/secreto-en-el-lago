"use client";

import { useState } from "react";
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
  Dialog,
  Spinner,
  Avatar,
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";
import { Field } from "@/components/ui/field";
import { useAuth } from "@/contexts/AuthContext";
import { toaster } from "@/components/ui/toaster";
import { PasswordInput } from "@/components/ui/password-input";
import { LuCamera, LuFingerprint } from "react-icons/lu";

export default function PerfilPage() {
  const { user } = useAuth();
  const [isLoadingFingerprint, setIsLoadingFingerprint] = useState(false);
  const [profileImage, setProfileImage] = useState<string | null>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileImage(reader.result as string);
        toaster.create({
          title: "Éxito",
          description: "Imagen de perfil cargada correctamente",
          type: "success",
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFingerprintClick = () => {
    setIsLoadingFingerprint(true);
    // Simular carga infinita - en producción aquí conectarías con el hardware
  };

  return (
    <Box minH="100vh" bg="bg.canvas">
      <UserNav />

      <Container maxW="container.md">
        <VStack align="stretch" gap={6}>
          <Heading size="2xl">Mi Perfil</Heading>
          <Text color="gray.500" fontSize="sm" mt={2}>
            {user?._id}
          </Text>

          {/* Sección de Foto de Perfil y Biometría */}
          <Card.Root p={8}>
            <VStack align="stretch" gap={6}>
              <Heading size="lg" mb={2}>
                Foto de perfil y biometría
              </Heading>

              <HStack gap={6} align="start">
                {/* Avatar */}
                <VStack gap={3}>
                  <Avatar.Root size="2xl">
                    <Avatar.Image
                      src={profileImage || user?.foto_url}
                    />
                    <Avatar.Fallback>
                      {user?.nombres?.[0]}{user?.apellidos?.[0]}
                    </Avatar.Fallback>
                  </Avatar.Root>
                  <input
                    type="file"
                    accept="image/*"
                    id="profile-image-upload"
                    style={{ display: "none" }}
                    onChange={handleImageUpload}
                  />
                  <label htmlFor="profile-image-upload" style={{ cursor: "pointer" }}>
                    <Button
                      as="span"
                      colorPalette="blue"
                      variant="outline"
                      size="sm"
                    >
                      <LuCamera />
                      Cambiar foto
                    </Button>
                  </label>
                </VStack>

                {/* Huella dactilar */}
                <VStack flex={1} align="stretch" gap={4}>
                  <Text fontWeight="semibold" fontSize="lg">Autenticación biométrica</Text>

                  {/* Info box */}
                  <Box
                    p={4}
                    bg="blue.50"
                    borderRadius="md"
                    borderWidth="1px"
                    borderColor="blue.200"
                  >
                    <VStack align="start" gap={2}>
                      <HStack gap={2}>
                        <LuFingerprint color="var(--chakra-colors-blue-600)" />
                        <Text fontWeight="semibold" color="blue.800" fontSize="sm">
                          ¿Para qué se usa la huella dactilar?
                        </Text>
                      </HStack>
                      <Text fontSize="sm" color="blue.700" lineHeight="1.6">
                        Tu huella dactilar se utiliza para verificar tu identidad al acceder a la biblioteca física.
                        Esto garantiza un proceso de préstamo más rápido y seguro, sin necesidad de recordar contraseñas
                        o presentar documentos adicionales.
                      </Text>
                      <Text fontSize="xs" color="blue.600" fontStyle="italic">
                        🔒 Tu información biométrica está protegida y encriptada.
                      </Text>
                    </VStack>
                  </Box>

                  <Button
                    colorPalette="blue"
                    onClick={handleFingerprintClick}
                    size="lg"
                  >
                    <LuFingerprint />
                    {user?.huella_ref ? "Actualizar huella" : "Registrar huella"}
                  </Button>

                  {user?.huella_ref ? (
                    <Text fontSize="sm" color="green.600" fontWeight="medium">
                      ✓ Huella registrada correctamente
                    </Text>
                  ) : (
                    <Text fontSize="sm" color="orange.600" fontWeight="medium">
                      ⚠ Huella aún no registrada
                    </Text>
                  )}
                </VStack>
              </HStack>
            </VStack>
          </Card.Root>

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

          {/* Diálogo de carga de huella dactilar */}
          <Dialog.Root
            open={isLoadingFingerprint}
            onOpenChange={(e) => setIsLoadingFingerprint(e.open)}
          >
            <Dialog.Backdrop />
            <Dialog.Positioner>
              <Dialog.Content>
                <Dialog.Header>
                  <Dialog.Title>Cargando equipo</Dialog.Title>
                  <Dialog.CloseTrigger />
                </Dialog.Header>

                <Dialog.Body>
                  <VStack gap={6} py={8}>
                    <Spinner size="xl" color="purple.500" />
                    <VStack gap={2}>
                      <Text fontSize="lg" fontWeight="semibold">
                        Inicializando lector de huellas...
                      </Text>
                      <Text fontSize="sm" color="gray.600" textAlign="center">
                        Por favor espere mientras se conecta con el dispositivo biométrico.
                      </Text>
                    </VStack>
                  </VStack>
                </Dialog.Body>
              </Dialog.Content>
            </Dialog.Positioner>
          </Dialog.Root>
        </VStack>
      </Container>
    </Box>
  );
}
