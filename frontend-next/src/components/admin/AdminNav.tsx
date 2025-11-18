"use client";

import { Box, Flex, Heading, Button, HStack, Link } from "@chakra-ui/react";
import { LuLayoutDashboard, LuBook, LuUsers, LuSettings, LuLogOut } from "react-icons/lu";
import NextLink from "next/link";

export function AdminNav() {
  return (
    <Box as="nav" bg="purple.600" color="white" py={4} px={6} mb={6}>
      <Flex justify="space-between" align="center">
        <Heading size="lg">Panel de Administracion</Heading>

        <HStack gap={4}>
          <Link asChild color="white" _hover={{ color: "purple.100" }}>
            <NextLink href="/admin">
              <LuLayoutDashboard /> Dashboard
            </NextLink>
          </Link>
          <Link asChild color="white" _hover={{ color: "purple.100" }}>
            <NextLink href="/admin/libros">
              <LuBook /> Libros
            </NextLink>
          </Link>
          <Link asChild color="white" _hover={{ color: "purple.100" }}>
            <NextLink href="/admin/usuarios">
              <LuUsers /> Usuarios
            </NextLink>
          </Link>
          <Link asChild color="white" _hover={{ color: "purple.100" }}>
            <NextLink href="/admin/configuracion">
              <LuSettings /> Configuracion
            </NextLink>
          </Link>
          <Button
            variant="outline"
            size="sm"
            color="white"
            borderColor="white"
            _hover={{ bg: "purple.700" }}
          >
            <LuLogOut /> Salir
          </Button>
        </HStack>
      </Flex>
    </Box>
  );
}
