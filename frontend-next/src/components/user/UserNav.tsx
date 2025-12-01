"use client";

import { Box, Flex, Heading, Button, HStack, Link } from "@chakra-ui/react";
import { LuUser, LuBook, LuHistory, LuLogOut, LuChrome } from "react-icons/lu";
import NextLink from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { toaster } from "@/components/ui/toaster";

export function UserNav() {
  const { logout } = useAuth();

  const handleLogout = () => {
    // Mostrar mensaje de confirmación
    toaster.create({
      title: "Sesión cerrada",
      description: "Has cerrado sesión exitosamente",
      type: "success",
      duration: 2000,
    });

    // Cerrar sesión (ya incluye la redirección)
    logout();
  };

  return (
    <Box as="nav" bg="blue.600" color="white" py={4} px={6} mb={6}>
      <Flex justify="space-between" align="center">
        <Heading size="lg">Mi Biblioteca</Heading>

        <HStack gap={4}>
          <Link asChild color="white" _hover={{ color: "blue.100" }}>
            <NextLink href="/dashboard">
              <LuChrome /> Inicio
            </NextLink>
          </Link>
          <Link asChild color="white" _hover={{ color: "blue.100" }}>
            <NextLink href="/historial">
              <LuHistory /> Historial
            </NextLink>
          </Link>
          <Link asChild color="white" _hover={{ color: "blue.100" }}>
            <NextLink href="/perfil">
              <LuUser /> Perfil
            </NextLink>
          </Link>
          <Button
            variant="outline"
            size="sm"
            color="white"
            borderColor="white"
            _hover={{ bg: "blue.700" }}
            onClick={handleLogout}
          >
            <LuLogOut /> Salir
          </Button>
        </HStack>
      </Flex>
    </Box>
  );
}
