"use client";

import { Box, Flex, Heading, Button, HStack, Link } from "@chakra-ui/react";
import { LuLayoutDashboard, LuBook, LuUsers, LuSettings, LuLogOut } from "react-icons/lu";
import NextLink from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { toaster } from "@/components/ui/toaster";
import { UserRole } from "@/types/auth.types";

export function AdminNav() {
  const { logoutAdmin, user } = useAuth();
  const isStaff = user?.rol === UserRole.BIBLIOTECARIO;

  const handleLogout = () => {
    // Mostrar mensaje de confirmación
    toaster.create({
      title: "Sesión cerrada",
      description: "Has cerrado sesión exitosamente",
      type: "success",
      duration: 2000,
    });

    // Cerrar sesión (ya incluye la redirección)
    logoutAdmin();
  };

  return (
    <Box as="nav" bg="purple.600" color="white" py={4} px={6} mb={6}>
      <Flex justify="space-between" align="center">
        <Heading size="lg">Panel de {user?.rol}</Heading>

        <HStack gap={4}>
          <Link asChild color="white" _hover={{ color: "purple.100" }}>
            <NextLink href="/admin">
              <LuLayoutDashboard /> Dashboard
            </NextLink>
          </Link>
          {isStaff && (
            <Link asChild color="white" _hover={{ color: "purple.100" }}>
              <NextLink href="/admin/libros">
                <LuBook /> Libros
              </NextLink>
            </Link>
          )}
          {isStaff && (
            <Link asChild color="white" _hover={{ color: "purple.100" }}>
              <NextLink href="/admin/usuarios">
                <LuUsers /> Usuarios
              </NextLink>
            </Link>
          )}
          <Link asChild color="white" _hover={{ color: "purple.100" }}>
            <NextLink href="/admin/configuracion">
              <LuSettings /> Configuración
            </NextLink>
          </Link>
          <Button
            variant="outline"
            size="sm"
            color="white"
            borderColor="white"
            _hover={{ bg: "purple.700" }}
            onClick={handleLogout}
          >
            <LuLogOut /> Salir
          </Button>
        </HStack>
      </Flex>
    </Box>
  );
}
