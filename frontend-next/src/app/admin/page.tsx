"use client";

import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  SimpleGrid,
  Card,
  HStack,
  Table,
} from "@chakra-ui/react";
import { AdminNav } from "@/components/admin/AdminNav";
import { LuBook, LuUsers, LuBookOpen, LuCircleAlert} from "react-icons/lu";

const stats = [
  { icon: LuBook, label: "Total de libros", value: "1,245", color: "purple" },
  { icon: LuUsers, label: "Usuarios activos", value: "342", color: "blue" },
  { icon: LuBookOpen, label: "Prestamos activos", value: "87", color: "green" },
  { icon: LuCircleAlert, label: "Prestamos vencidos", value: "12", color: "red" },
];

const recentLoans = [
  {
    id: 1,
    user: "Juan Perez",
    book: "1984",
    date: "2024-02-10",
    status: "Activo",
  },
  {
    id: 2,
    user: "Maria Garcia",
    book: "El principito",
    date: "2024-02-09",
    status: "Activo",
  },
  {
    id: 3,
    user: "Pedro Rodriguez",
    book: "Sapiens",
    date: "2024-02-08",
    status: "Vencido",
  },
  {
    id: 4,
    user: "Ana Martinez",
    book: "Don Quijote",
    date: "2024-02-07",
    status: "Activo",
  },
];

export default function AdminPage() {
  return (
    <Box minH="100vh" bg="bg.canvas">
      <AdminNav />

      <Container maxW="container.xl">
        <VStack align="stretch" gap={8}>
          <Box>
            <Heading size="2xl" mb={2}>
              Dashboard Administrativo
            </Heading>
            <Text color="gray.600">
              Resumen general del sistema de biblioteca
            </Text>
          </Box>

          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} gap={6}>
            {stats.map((stat) => {
              const Icon = stat.icon;
              return (
                <Card.Root key={stat.label} p={6}>
                  <VStack align="stretch" gap={3}>
                    <HStack justify="space-between">
                      <Box color={`${stat.color}.500`}>
                        <Icon size={28} />
                      </Box>
                      <Text fontSize="3xl" fontWeight="bold">
                        {stat.value}
                      </Text>
                    </HStack>
                    <Text fontSize="sm" color="gray.600">
                      {stat.label}
                    </Text>
                  </VStack>
                </Card.Root>
              );
            })}
          </SimpleGrid>

          <Box>
            <Heading size="xl" mb={4}>
              Prestamos recientes
            </Heading>
            <Card.Root>
              <Table.Root variant="outline" size="lg">
                <Table.Header>
                  <Table.Row>
                    <Table.ColumnHeader>Usuario</Table.ColumnHeader>
                    <Table.ColumnHeader>Libro</Table.ColumnHeader>
                    <Table.ColumnHeader>Fecha</Table.ColumnHeader>
                    <Table.ColumnHeader>Estado</Table.ColumnHeader>
                  </Table.Row>
                </Table.Header>
                <Table.Body>
                  {recentLoans.map((loan) => (
                    <Table.Row key={loan.id}>
                      <Table.Cell fontWeight="semibold">{loan.user}</Table.Cell>
                      <Table.Cell>{loan.book}</Table.Cell>
                      <Table.Cell>{loan.date}</Table.Cell>
                      <Table.Cell>
                        <Text
                          color={loan.status === "Vencido" ? "red.500" : "green.500"}
                          fontWeight="semibold"
                        >
                          {loan.status}
                        </Text>
                      </Table.Cell>
                    </Table.Row>
                  ))}
                </Table.Body>
              </Table.Root>
            </Card.Root>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
}
