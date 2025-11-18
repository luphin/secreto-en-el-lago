"use client";

import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  Table,
  Card,
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";

const historyItems = [
  {
    id: 1,
    title: "Cien años de soledad",
    author: "Gabriel Garcia Marquez",
    loanDate: "2023-11-01",
    returnDate: "2023-11-28",
  },
  {
    id: 2,
    title: "La sombra del viento",
    author: "Carlos Ruiz Zafon",
    loanDate: "2023-11-15",
    returnDate: "2023-12-10",
  },
  {
    id: 3,
    title: "El código Da Vinci",
    author: "Dan Brown",
    loanDate: "2023-12-01",
    returnDate: "2023-12-20",
  },
  {
    id: 4,
    title: "Harry Potter y la piedra filosofal",
    author: "J.K. Rowling",
    loanDate: "2023-12-15",
    returnDate: "2024-01-05",
  },
  {
    id: 5,
    title: "Los juegos del hambre",
    author: "Suzanne Collins",
    loanDate: "2024-01-01",
    returnDate: "2024-01-25",
  },
];

export default function HistorialPage() {
  return (
    <Box minH="100vh" bg="bg.canvas">
      <UserNav />

      <Container maxW="container.xl">
        <VStack align="stretch" gap={6}>
          <Box>
            <Heading size="2xl" mb={2}>
              Historial de Préstamos
            </Heading>
            <Text color="gray.600">
              Revisa todos los libros que has tomado prestados anteriormente
            </Text>
          </Box>

          <Card.Root>
            <Table.Root variant="outline" size="lg">
              <Table.Header>
                <Table.Row>
                  <Table.ColumnHeader>Libro</Table.ColumnHeader>
                  <Table.ColumnHeader>Autor</Table.ColumnHeader>
                  <Table.ColumnHeader>Fecha de préstamo</Table.ColumnHeader>
                  <Table.ColumnHeader>Fecha de devolución</Table.ColumnHeader>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {historyItems.map((item) => (
                  <Table.Row key={item.id}>
                    <Table.Cell fontWeight="semibold">{item.title}</Table.Cell>
                    <Table.Cell>{item.author}</Table.Cell>
                    <Table.Cell>{item.loanDate}</Table.Cell>
                    <Table.Cell>{item.returnDate}</Table.Cell>
                  </Table.Row>
                ))}
              </Table.Body>
            </Table.Root>
          </Card.Root>
        </VStack>
      </Container>
    </Box>
  );
}
