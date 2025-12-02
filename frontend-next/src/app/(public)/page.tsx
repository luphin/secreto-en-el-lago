"use client";

import { useState } from "react";
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
import { CarouselStatic } from "@/components/catalog/Carousel";
import { BookDetailDialog } from "@/components/catalog/BookDetailDialog";

// Datos de ejemplo
const featuredBooks = [
  {
    id: 1,
    title: "Cien años de soledad",
    author: "Gabriel García Márquez",
    available: true,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9780307474728-L.jpg",
    description: "Una obra maestra de la literatura latinoamericana que narra la historia de la familia Buendía a lo largo de varias generaciones en el pueblo ficticio de Macondo.",
    location: "Estantería A, Nivel 2",
    editorial: "Editorial Sudamericana",
    year: 1967,
    category: "Ficción"
  },
  {
    id: 2,
    title: "Don Quijote de la Mancha",
    author: "Miguel de Cervantes",
    available: true,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9788417958596-L.jpg",
    description: "La obra cumbre de la literatura española que narra las aventuras de un hidalgo que pierde la razón y se cree caballero andante.",
    location: "Estantería B, Nivel 1",
    editorial: "Hispamérica Books, S.L.",
    year: 2022,
    category: "Ficción clásica"
  },
  {
    id: 3,
    title: "1984",
    author: "George Orwell",
    available: false,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg",
    description: "Una distopía sobre un futuro totalitario donde el Gran Hermano todo lo ve y controla.",
    location: "Estantería C, Nivel 3",
    editorial: "Signet Classics",
    year: 1949,
    category: "Ciencia ficción"
  },
  {
    id: 4,
    title: "El principito",
    author: "Antoine de Saint-Exupéry",
    available: true,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9780156012195-L.jpg",
    description: "Un cuento poético que narra las aventuras de un pequeño príncipe que viaja de planeta en planeta.",
    location: "Estantería D, Nivel 1",
    editorial: "Harcourt",
    year: 1943,
    category: "Infantil"
  },
  {
    id: 5,
    title: "Orgullo y prejuicio",
    author: "Jane Austen",
    available: true,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9788415083696-L.jpg",
    description: "Una novela romántica que explora las complejidades del amor y las clases sociales en la Inglaterra del siglo XIX.",
    location: "Estantería E, Nivel 2",
    editorial: "Albor Libros",
    year: 2017,
    category: "Romance clásico"
  }

];

const newBooks = [
  {
    id: 6,
    title: "Sapiens",
    author: "Yuval Noah Harari",
    available: true,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg",
    description: "Una exploración de la historia de la humanidad desde la Edad de Piedra hasta la era moderna.",
    location: "Estantería F, Nivel 3",
    editorial: "Harper",
    year: 2011,
    category: "Historia"
  },
  {
    id: 7,
    title: "El código Da Vinci",
    author: "Dan Brown",
    available: true,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9780307474278-L.jpg",
    description: "Un thriller que mezcla arte, historia y misterio en una búsqueda del Santo Grial.",
    location: "Estantería G, Nivel 2",
    editorial: "Doubleday",
    year: 2003,
    category: "Thriller"
  },
  {
    id: 8,
    title: "La sombra del viento",
    author: "Carlos Ruiz Zafón",
    available: false,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9780143034902-L.jpg",
    description: "Un misterio literario ambientado en la Barcelona de posguerra.",
    location: "Estantería H, Nivel 1",
    editorial: "Penguin Books",
    year: 2001,
    category: "Misterio"
  },
  {
    id: 9,
    title: "Los juegos del hambre",
    author: "Suzanne Collins",
    available: true,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg",
    description: "Una distopía juvenil sobre una competencia mortal en un futuro postapocalíptico.",
    location: "Estantería I, Nivel 2",
    editorial: "Scholastic",
    year: 2008,
    category: "Juvenil"
  },
  {
    id: 10,
    title: "Harry Potter y la piedra filosofal",
    author: "J.K. Rowling",
    available: true,
    imageUrl: "https://covers.openlibrary.org/b/isbn/9780439708180-L.jpg",
    description: "El inicio de la saga mágica sobre un joven mago y sus aventuras en Hogwarts.",
    location: "Estantería J, Nivel 1",
    editorial: "Scholastic",
    year: 1997,
    category: "Fantasía juvenil"
  }

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
  const [selectedBook, setSelectedBook] = useState<typeof featuredBooks[0] | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const handleBookClick = (book: typeof featuredBooks[0]) => {
    setSelectedBook(book);
    setIsDialogOpen(true);
  };
  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setSelectedBook(null);
  };


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
            <CarouselStatic />

            <VStack align="stretch" gap={12}>
              {/* Sección Destacados */}
              <Box id="destacados">
                <Heading size="xl" mb={4} color="gray.800">
                  Destacados
                </Heading>
                <SimpleGrid columns={{ base: 2, sm: 3, md: 4, lg: 5 }} gap={4}>
                  {featuredBooks.map((book) => (
                    <BookCard
                      key={book.id}
                      title={book.title}
                      author={book.author}
                      available={book.available}
                      imageUrl={book.imageUrl}
                      onClick={() => handleBookClick(book)}
                    />
                  ))}
                </SimpleGrid>
              </Box>

              {/* Sección Nuevos Ingresos */}
              <Box id="nuevos">
                <Heading size="xl" mb={4} color="gray.800">
                  Nuevos ingresos
                </Heading>
                <SimpleGrid columns={{ base: 2, sm: 3, md: 4, lg: 5 }} gap={4}>
                  {newBooks.map((book) => (
                    <BookCard
                      key={book.id}
                      title={book.title}
                      author={book.author}
                      available={book.available}
                      imageUrl={book.imageUrl}
                      onClick={() => handleBookClick(book)}
                    />
                  ))}
                </SimpleGrid>
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
      {/* Book Detail Dialog */}
      {selectedBook && (
        <BookDetailDialog
          isOpen={isDialogOpen}
          onClose={handleCloseDialog}
          book={selectedBook}
        />
      )}
    </Box>
  );
}
