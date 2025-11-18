"use client";

import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  Card,
  HStack,
  Button,
  Tag,
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";

const loans = [
  {
    id: 1,
    title: "1984",
    author: "George Orwell",
    loanDate: "2024-01-15",
    dueDate: "2024-02-15",
    status: "active",
  },
  {
    id: 2,
    title: "El principito",
    author: "Antoine de Saint-Exupery",
    loanDate: "2024-01-20",
    dueDate: "2024-02-20",
    status: "active",
  },
  {
    id: 3,
    title: "Sapiens",
    author: "Yuval Noah Harari",
    loanDate: "2024-01-25",
    dueDate: "2024-02-25",
    status: "active",
  },
  {
    id: 4,
    title: "Don Quijote de la Mancha",
    author: "Miguel de Cervantes",
    loanDate: "2024-01-10",
    dueDate: "2024-02-10",
    status: "overdue",
  },
];

export default function MisPrestamosPage() {
  return (
    <Box minH="100vh" bg="bg.canvas">
      <UserNav />

      <Container maxW="container.xl">
        <VStack align="stretch" gap={6}>
          <Box>
            <Heading size="2xl" mb={2}>
              Mis Prestamos
            </Heading>
            <Text color="gray.600">
              Administra tus libros prestados y fechas de devolucion
            </Text>
          </Box>

          <VStack align="stretch" gap={4}>
            {loans.map((loan) => (
              <Card.Root key={loan.id} p={6}>
                <HStack justify="space-between" align="start">
                  <VStack align="start" gap={2} flex="1">
                    <HStack gap={3}>
                      <Heading size="lg">{loan.title}</Heading>
                      <Tag.Root
                        colorPalette={loan.status === "overdue" ? "red" : "green"}
                        variant="solid"
                      >
                        {loan.status === "overdue" ? "Vencido" : "Activo"}
                      </Tag.Root>
                    </HStack>
                    <Text color="gray.600">{loan.author}</Text>
                    <HStack gap={6} mt={2}>
                      <VStack align="start" gap={0}>
                        <Text fontSize="xs" color="gray.500">
                          Fecha de prestamo
                        </Text>
                        <Text fontSize="sm" fontWeight="semibold">
                          {loan.loanDate}
                        </Text>
                      </VStack>
                      <VStack align="start" gap={0}>
                        <Text fontSize="xs" color="gray.500">
                          Fecha de devolucion
                        </Text>
                        <Text
                          fontSize="sm"
                          fontWeight="semibold"
                          color={loan.status === "overdue" ? "red.500" : "inherit"}
                        >
                          {loan.dueDate}
                        </Text>
                      </VStack>
                    </HStack>
                  </VStack>

                  <VStack gap={2}>
                    <Button colorPalette="blue" variant="outline">
                      Renovar
                    </Button>
                    <Button colorPalette="green">
                      Devolver
                    </Button>
                  </VStack>
                </HStack>
              </Card.Root>
            ))}
          </VStack>
        </VStack>
      </Container>
    </Box>
  );
}
