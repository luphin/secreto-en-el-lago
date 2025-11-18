"use client";

import {
  Box,
  Container,
  Flex,
  Heading,
  HStack,
  Text,
  VStack,
  SimpleGrid,
  Tag,
} from "@chakra-ui/react";
import { Header } from "@/components/catalog/Header";
import { Sidebar } from "@/components/catalog/Sidebar";
import { BookCard } from "@/components/catalog/BookCard";
import { LuDownload, LuVideo, LuHeadphones } from "react-icons/lu";

// Datos de ejemplo
const featuredBooks = [
  { id: 1, title: "Cien años de soledad", author: "Gabriel Garí­a árquez", available: true },
  { id: 2, title: "Don Quijote de la Mancha", author: "Miguel de Cervantes", available: true },
  { id: 3, title: "1984", author: "George Orwell", available: false },
  { id: 4, title: "El principito", author: "Antoine de Saint-ExupÃ©ry", available: true },
  { id: 5, title: "Orgullo y prejuicio", author: "Jane Austen", available: true },
];

const newBooks = [
  { id: 6, title: "Sapiens", author: "Yuval Noah Harari", available: true },
  { id: 7, title: "El código Da Vinci", author: "Dan Brown", available: true },
  { id: 8, title: "La sombra del viento", author: "Carlos Ruiz Zafán", available: false },
  { id: 9, title: "Los juegos del hambre", author: "Suzanne Collins", available: true },
  { id: 10, title: "Harry Potter y la piedra filosofal", author: "J.K. Rowling", available: true },
];

const digitalResources = [
  { icon: LuDownload, title: "E-books", count: 1200 },
  { icon: LuVideo, title: "Videos educativos", count: 350 },
  { icon: LuHeadphones, title: "Audiolibros", count: 450 },
];

const categories = [
  "Ficción",
  "No ficción",
  "Ciencia",
  "Historia",
  "Biografías",
  "Tecnologí­a",
  "Arte",
  "Filosofía",
  "Poeí­a",
  "Infantil",
  "Juvenil",
  "Autoayuda",
  "Negocios",
  "Cocina",
  "Deportes",
];

export default function CatalogPage() {
  return (
    <Box minH="100vh" bg="bg.canvas">
      <Header />

      <Flex direction={{ base: "column", md: "row" }}>
        <Sidebar />

        <Box
          as="main"
          flex="1"
					//overflowY="auto"
					//maxH={{ base: "auto", md: "calc(100vh - 80px)"}}
        >
          <Container maxW="container.xl" py={8}>
            <VStack align="stretch" gap={12}>
              {/* Sección Destacados */}
              <Box id="destacados">
                <Heading size="xl" mb={4} color="gray.800">
                  Destacados
                </Heading>
                <Box
                  overflowX="auto"
                  pb={4}
                  css={{
                    "&::-webkit-scrollbar": {
                      height: "8px",
                    },
                    "&::-webkit-scrollbar-track": {
                      background: "#f1f1f1",
                    },
                    "&::-webkit-scrollbar-thumb": {
                      background: "#888",
                      borderRadius: "4px",
                    },
                    "&::-webkit-scrollbar-thumb:hover": {
                      background: "#555",
                    },
                  }}
                >
                  <HStack gap={4} align="stretch">
                    {featuredBooks.map((book) => (
                      <BookCard
                        key={book.id}
                        title={book.title}
                        author={book.author}
                        available={book.available}
                      />
                    ))}
                  </HStack>
                </Box>
              </Box>

              {/* Sección Nuevos Ingresos */}
              <Box id="nuevos">
                <Heading size="xl" mb={4} color="gray.800">
                  Nuevos ingresos
                </Heading>
                <Box
                  overflowX="auto"
                  pb={4}
                  css={{
                    "&::-webkit-scrollbar": {
                      height: "8px",
                    },
                    "&::-webkit-scrollbar-track": {
                      background: "#f1f1f1",
                    },
                    "&::-webkit-scrollbar-thumb": {
                      background: "#888",
                      borderRadius: "4px",
                    },
                    "&::-webkit-scrollbar-thumb:hover": {
                      background: "#555",
                    },
                  }}
                >
                  <HStack gap={4} align="stretch">
                    {newBooks.map((book) => (
                      <BookCard
                        key={book.id}
                        title={book.title}
                        author={book.author}
                        available={book.available}
                      />
                    ))}
                  </HStack>
                </Box>
              </Box>

              {/* Sección Recursos Digitales */}
              <Box id="recursos">
                <Heading size="xl" mb={4} color="gray.800">
                  Recursos digitales
                </Heading>
                <SimpleGrid columns={{ base: 1, md: 3 }} gap={6}>
                  {digitalResources.map((resource) => {
                    const Icon = resource.icon;
                    return (
                      <Box
                        key={resource.title}
                        p={8}
                        borderWidth="1px"
                        borderRadius="lg"
                        bg="bg.muted"
                        textAlign="center"
                        transition="all 0.2s"
                        _hover={{
                          shadow: "lg",
                          transform: "translateY(-4px)",
                          cursor: "pointer",
                        }}
                      >
                        <VStack gap={3}>
                          <Box
                            p={4}
                            bg="blue.100"
                            borderRadius="full"
                            color="blue.600"
                          >
                            <Icon size={32} />
                          </Box>
                          <Heading size="md">{resource.title}</Heading>
                          <Text color="gray.600" fontSize="lg" fontWeight="bold">
                            {resource.count}+ disponibles
                          </Text>
                        </VStack>
                      </Box>
                    );
                  })}
                </SimpleGrid>
              </Box>

              {/* Sección Categorí­as */}
              <Box id="categorias" pb={8}>
                <Heading size="xl" mb={4} color="gray.800">
                  Categorí­as
                </Heading>
                <Flex wrap="wrap" gap={3}>
                  {categories.map((category) => (
                    <Tag.Root
                      key={category}
                      size="lg"
                      colorPalette="blue"
                      variant="outline"
                      cursor="pointer"
                      _hover={{
                        bg: "blue.50",
                        borderColor: "blue.500",
                      }}
                      transition="all 0.2s"
                    >
                      {category}
                    </Tag.Root>
                  ))}
                </Flex>
              </Box>
            </VStack>
          </Container>
        </Box>
      </Flex>
    </Box>
  );
}
