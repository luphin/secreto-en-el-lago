"use client";

import { Box, VStack, Text, Link } from "@chakra-ui/react";
import NextLink from "next/link";

interface SidebarProps {
  currentSection?: string;
}

const sections = [
  { id: "destacados", label: "Destacados" },
  { id: "nuevos", label: "Nuevos ingresos" },
  { id: "recursos", label: "Recursos digitales" },
  { id: "categorias", label: "Categorías" },
];

export function Sidebar({ currentSection }: SidebarProps) {
  return (
    <Box
      as="aside"
      w={{ base: "full", md: "250px" }}
      h={{ base: "auto", md: "100vh" }}
      position={{ base: "relative", md: "sticky" }}
      top="0"
      bg="bg.subtle"
      p={6}
      borderRightWidth="1px"
      overflowY="auto"
    >
      <VStack align="stretch" gap={4}>
        <Text fontSize="xl" fontWeight="bold" mb={2}>
          Navegación
        </Text>

        <VStack align="stretch" gap={2}>
          {sections.map((section) => (
            <Link
              key={section.id}
              asChild
              color={currentSection === section.id ? "blue.600" : "gray.700"}
              fontWeight={currentSection === section.id ? "bold" : "normal"}
              _hover={{
                color: "blue.500",
                textDecoration: "none",
                transform: "translateX(4px)",
              }}
              transition="all 0.2s"
              fontSize="md"
            >
              <NextLink href={`#${section.id}`}>
                {section.label}
              </NextLink>
            </Link>
          ))}
        </VStack>

        <Box mt={6}>
          <Text fontSize="sm" fontWeight="semibold" mb={2} color="gray.600">
            Enlaces rápidos
          </Text>
          <VStack align="stretch" gap={2}>
            <Link asChild fontSize="sm" color="gray.600" _hover={{ color: "blue.500" }}>
              <NextLink href="/login">Iniciar sesión</NextLink>
            </Link>
            <Link asChild fontSize="sm" color="gray.600" _hover={{ color: "blue.500" }}>
              <NextLink href="/register">Registrarse</NextLink>
            </Link>
          </VStack>
        </Box>
      </VStack>
    </Box>
  );
}
