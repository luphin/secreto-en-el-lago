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
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";
import { LuBook, LuClock, LuCircleCheck, LuCircleAlert } from "react-icons/lu";

const stats = [
  { icon: LuBook, label: "Prestamos activos", value: "3", color: "blue" },
  { icon: LuClock, label: "Reservas pendientes", value: "1", color: "orange" },
  { icon: LuCircleCheck, label: "Libros devueltos", value: "12", color: "green" },
  { icon: LuCircleAlert, label: "Por vencer", value: "1", color: "red" },
];

const activeLoans = [
  { title: "1984", author: "George Orwell", dueDate: "2024-02-15" },
  { title: "El principito", author: "Antoine de Saint-Exupery", dueDate: "2024-02-20" },
  { title: "Sapiens", author: "Yuval Noah Harari", dueDate: "2024-02-25" },
];

export default function DashboardPage() {
  return (
    <Box minH="100vh" bg="bg.canvas">
      <UserNav />

      <Container maxW="container.xl">
        <VStack align="stretch" gap={8}>
          <Box>
            <Heading size="2xl" mb={2}>
              Bienvenido, Usuario
            </Heading>
            <Text color="gray.600">
              Aqui esta el resumen de tu actividad en la biblioteca
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
              Prestamos activos
            </Heading>
            <VStack align="stretch" gap={4}>
              {activeLoans.map((loan) => (
                <Card.Root key={loan.title} p={6}>
                  <HStack justify="space-between">
                    <VStack align="start" gap={1}>
                      <Text fontWeight="bold" fontSize="lg">
                        {loan.title}
                      </Text>
                      <Text color="gray.600" fontSize="sm">
                        {loan.author}
                      </Text>
                    </VStack>
                    <VStack align="end" gap={1}>
                      <Text fontSize="sm" color="gray.600">
                        Fecha de devolucion
                      </Text>
                      <Text fontWeight="bold">{loan.dueDate}</Text>
                    </VStack>
                  </HStack>
                </Card.Root>
              ))}
            </VStack>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
}
