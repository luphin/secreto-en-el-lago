"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  SimpleGrid,
  Card,
  HStack,
  Badge,
  Spinner,
  Stack,
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";
import { LuBook, LuClock, LuCircleCheck, LuCircleAlert, LuCalendar } from "react-icons/lu";
import { useAuth } from "@/contexts/AuthContext";
import LoanService from "@/services/loan.service";
import type { LoanResponse } from "@/types/loan.types";
import { UserRole } from "@/types/auth.types";

export default function DashboardPage() {
  const { user, isLoading: authLoading } = useAuth();
  const [overdueLoans, setOverdueLoans] = useState<LoanResponse[]>([]);
  const [userLoans, setUserLoans] = useState<LoanResponse[]>([]);
  const [isLoadingOverdue, setIsLoadingOverdue] = useState(false);
  const [isLoadingLoans, setIsLoadingLoans] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);
  const observerTarget = useRef<HTMLDivElement>(null);

  const isStaff = user?.rol === UserRole.BIBLIOTECARIO || user?.rol === UserRole.ADMINISTRATIVO;

  // Calcular estadísticas dinámicas
  const activeLoansCount = userLoans.length >= 10 ? "+9" : userLoans.length.toString();
  const overdueCount = overdueLoans.length.toString();

  const stats = [
    { icon: LuBook, label: "Préstamos activos", value: activeLoansCount, color: "blue" },
    { icon: LuClock, label: "Reservas pendientes", value: "0", color: "orange" },
    { icon: LuCircleCheck, label: "Libros devueltos", value: "0", color: "green" },
    { icon: LuCircleAlert, label: "Por vencer", value: overdueCount, color: "red" },
  ];

  // Cargar préstamos vencidos 
  useEffect(() => {
    const loadOverdueLoans = async () => {
      if (!user || isLoadingLoans) return;

      setIsLoadingOverdue(true);
      try {
        const loans = await LoanService.getOverdueLoans();
        setOverdueLoans(loans);
      } catch (error) {
        console.error("Error al cargar préstamos vencidos:", error);
      } finally {
        setIsLoadingOverdue(false);
      }
    };

    loadOverdueLoans();
  }, [user, isLoadingLoans]);

  // Cargar préstamos del usuario con paginación
  const loadUserLoans = useCallback(async (pageNum: number) => {
    if (!user || isLoadingLoans) return;

    setIsLoadingLoans(true);
    try {
      const loans = await LoanService.getUserLoans(pageNum * 10, 10);

      if (loans.length < 10) {
        setHasMore(false);
      }

      if (pageNum === 0) {
        setUserLoans(loans);
      } else {
        setUserLoans((prev) => [...prev, ...loans]);
      }
    } catch (error) {
      console.error("Error al cargar préstamos:", error);
    } finally {
      setIsLoadingLoans(false);
    }
  }, [user, isLoadingLoans]);

  // Cargar primera página
  useEffect(() => {
    if (user) {
      loadUserLoans(0);
    }
  }, [user]);

  // Infinite scroll observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoadingLoans) {
          setPage((prev) => {
            const nextPage = prev + 1;
            loadUserLoans(nextPage);
            return nextPage;
          });
        }
      },
      { threshold: 0.1 }
    );

    const currentTarget = observerTarget.current;
    if (currentTarget) {
      observer.observe(currentTarget);
    }

    return () => {
      if (currentTarget) {
        observer.unobserve(currentTarget);
      }
    };
  }, [hasMore, isLoadingLoans, loadUserLoans]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("es-CL", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const getStatusColor = (estado: string) => {
    switch (estado) {
      case "activo":
        return "blue";
      case "vencido":
        return "red";
      case "devuelto":
        return "green";
      default:
        return "gray";
    }
  };

  if (authLoading) {
    return (
      <Box minH="100vh" bg="bg.canvas" display="flex" alignItems="center" justifyContent="center">
        <Spinner size="xl" color="blue.500" />
      </Box>
    );
  }

  return (
    <Box minH="100vh" bg="bg.canvas">
      <UserNav />

      <Container maxW="container.xl" py={8}>
        <VStack align="stretch" gap={8}>
          {/* Header */}
          <Box>
            <Heading size="2xl" mb={2}>
              Bienvenido, {user ? `${user.nombres} ${user.apellidos}` : "Usuario"}
            </Heading>
            <Text color="gray.600">
              Aquí está el resumen de tu actividad en la biblioteca
            </Text>
            {user && (
              <Text color="gray.500" fontSize="sm" mt={2}>
                {user.email} • {user.rol}
              </Text>
            )}
          </Box>

          {/* Stats */}
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

          {/* Préstamos Vencidos (solo para staff) */}

          <Box>
            <Heading size="xl" mb={4} color="red.600">
              <HStack>
                <LuCircleAlert />
                <Text>Préstamos Vencidos</Text>
              </HStack>
            </Heading>

            {isLoadingOverdue ? (
              <Box textAlign="center" py={8}>
                <Spinner size="lg" color="red.500" />
              </Box>
            ) : overdueLoans.length === 0 ? (
              <Card.Root p={6}>
                <Text color="gray.600" textAlign="center">
                  No hay préstamos vencidos
                </Text>
              </Card.Root>
            ) : (
              <VStack align="stretch" gap={4}>
                {overdueLoans.map((loan) => (
                  <Card.Root key={loan._id} p={6} borderLeftWidth="4px" borderLeftColor="red.500">
                    <HStack justify="space-between" align="start">
                      <VStack align="start" gap={2} flex="1">
                        <HStack>
                          <Badge colorPalette={getStatusColor(loan.estado)}>
                            {loan.estado.toUpperCase()}
                          </Badge>
                          <Badge colorPalette="purple">
                            {loan.tipo_prestamo.toUpperCase()}
                          </Badge>
                        </HStack>
                        <Text fontSize="sm" color="gray.600">
                          ID: {loan.item_id}
                        </Text>
                        <Text fontSize="sm" color="gray.600">
                          Usuario: {loan.user_id}
                        </Text>
                      </VStack>
                      <VStack align="end" gap={1}>
                        <HStack color="gray.600" fontSize="sm">
                          <LuCalendar size={16} />
                          <Text>Vencimiento:</Text>
                        </HStack>
                        <Text fontWeight="bold" color="red.600">
                          {formatDate(loan.fecha_devolucion_pactada)}
                        </Text>
                      </VStack>
                    </HStack>
                  </Card.Root>
                ))}
              </VStack>
            )}
          </Box>


          {/* Mis Préstamos Activos */}
          <Box>
            <Heading size="xl" mb={4}>
              <HStack>
                <LuBook />
                <Text>Mis Préstamos Activos</Text>
              </HStack>
            </Heading>

            {isLoadingLoans && page === 0 ? (
              <Box textAlign="center" py={8}>
                <Spinner size="lg" color="blue.500" />
              </Box>
            ) : userLoans.length === 0 ? (
              <Card.Root p={6}>
                <Text color="gray.600" textAlign="center">
                  No tienes préstamos activos
                </Text>
              </Card.Root>
            ) : (
              <VStack align="stretch" gap={4}>
                {userLoans.map((loan) => (
                  <Card.Root key={loan._id} p={6}>
                    <HStack justify="space-between" align="start">
                      <VStack align="start" gap={2} flex="1">
                        <HStack>
                          <Badge colorPalette={getStatusColor(loan.estado)}>
                            {loan.estado.toUpperCase()}
                          </Badge>
                          <Badge colorPalette="purple">
                            {loan.tipo_prestamo.toUpperCase()}
                          </Badge>
                        </HStack>
                        <Text fontSize="sm" color="gray.600">
                          ID del ejemplar: {loan.item_id}
                        </Text>
                        <HStack color="gray.600" fontSize="sm">
                          <LuClock size={16} />
                          <Text>Prestado: {formatDate(loan.fecha_prestamo)}</Text>
                        </HStack>
                      </VStack>
                      <VStack align="end" gap={1}>
                        <HStack color="gray.600" fontSize="sm">
                          <LuCalendar size={16} />
                          <Text>Devolver antes de:</Text>
                        </HStack>
                        <Text fontWeight="bold" color="blue.600">
                          {formatDate(loan.fecha_devolucion_pactada)}
                        </Text>
                      </VStack>
                    </HStack>
                  </Card.Root>
                ))}

                {/* Infinite scroll trigger */}
                <div ref={observerTarget} style={{ height: "20px" }}>
                  {isLoadingLoans && page > 0 && (
                    <Box textAlign="center" py={4}>
                      <Spinner size="md" color="blue.500" />
                    </Box>
                  )}
                </div>

                {!hasMore && userLoans.length > 0 && (
                  <Text textAlign="center" color="gray.500" fontSize="sm" py={4}>
                    No hay más préstamos para mostrar
                  </Text>
                )}
              </VStack>
            )}
          </Box>
        </VStack>
      </Container>
    </Box>
  );
}
