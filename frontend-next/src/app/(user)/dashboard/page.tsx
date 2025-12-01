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
  Button,
  Tabs,
  Accordion,
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";
import { QuickReservationDialog } from "@/components/user/QuickReservationDialog";
import { LuBook, LuClock, LuCircleCheck, LuCircleAlert, LuCalendar, LuPlus } from "react-icons/lu";
import { useAuth } from "@/contexts/AuthContext";
import { toaster } from "@/components/ui/toaster";
import LoanService from "@/services/loan.service";
import ReservationService from "@/services/reservation.service";
import { LoanStatus, type LoanResponse } from "@/types/loan.types";
import type { ReservationResponse } from "@/types/reservation.types";
import { UserRole } from "@/types/auth.types";

const stats = [
  { icon: LuBook, label: "Préstamos activos", value: "-", color: "blue" },
  { icon: LuClock, label: "Reservas pendientes", value: "-", color: "orange" },
  { icon: LuCircleCheck, label: "Libros devueltos", value: "-", color: "green" },
  { icon: LuCircleAlert, label: "Por vencer", value: "-", color: "red" },
];

export default function DashboardPage() {
  const { user, isLoading: authLoading } = useAuth();
  const [overdueLoans, setOverdueLoans] = useState<LoanResponse[]>([]);
  const [userLoans, setUserLoans] = useState<LoanResponse[]>([]);
  const [userReservations, setUserReservations] = useState<ReservationResponse[]>([]);
  const [isLoadingOverdue, setIsLoadingOverdue] = useState(false);
  const [isLoadingLoans, setIsLoadingLoans] = useState(false);
  const [isLoadingReservations, setIsLoadingReservations] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);
  const [isReservationDialogOpen, setIsReservationDialogOpen] = useState(false);
  const observerTarget = useRef<HTMLDivElement>(null);

  const isStaff = user?.rol === UserRole.BIBLIOTECARIO || user?.rol === UserRole.ADMINISTRATIVO;

  // Cargar préstamos vencidos (solo para staff)
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
      const loans = await LoanService.getUserLoans(pageNum * 10, 10, LoanStatus.ACTIVO);

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

  // Cargar reservas del usuario
  useEffect(() => {
    const loadUserReservations = async () => {
      if (!user) return;

      setIsLoadingReservations(true);
      try {
        const reservations = await ReservationService.getUserReservations(user._id, 0, 100);
        setUserReservations(reservations);
      } catch (error) {
        console.error("Error al cargar reservas:", error);
      } finally {
        setIsLoadingReservations(false);
      }
    };

    loadUserReservations();
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

  const calculateLateFee = (loan: LoanResponse): { daysLate: number; feeAmount: number } => {
    const dueDate = new Date(loan.fecha_devolucion_pactada);
    const now = new Date();
    const diffTime = now.getTime() - dueDate.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    const daysLate = Math.max(0, diffDays);
    const feeAmount = daysLate * 500; // $500 por día
    return { daysLate, feeAmount };
  };

  const getReservationStatusColor = (estado: string) => {
    switch (estado) {
      case "pendiente":
        return "orange";
      case "completada":
        return "green";
      case "cancelada":
        return "red";
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
            <HStack justify="space-between" align="start" mb={2}>
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
              <Button
                colorPalette="blue"
                size="lg"
                onClick={() => setIsReservationDialogOpen(true)}
              >
                <LuPlus />
                Nueva Reserva
              </Button>
            </HStack>
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


          {/* Mis Préstamos y Reservas - Tabs */}
          <Box>
            <Tabs.Root defaultValue="loans" variant="enclosed">
              <Tabs.List>
                <Tabs.Trigger value="loans">
                  <HStack>
                    <LuBook />
                    <Text>Mis Préstamos</Text>
                  </HStack>
                </Tabs.Trigger>
                <Tabs.Trigger value="reservations">
                  <HStack>
                    <LuClock />
                    <Text>Mis Reservas</Text>
                  </HStack>
                </Tabs.Trigger>
              </Tabs.List>

              {/* Tab de Préstamos */}
              <Tabs.Content value="loans">
                <Box pt={6}>
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
                    <VStack align="stretch" gap={6}>
                      {/* Préstamos Vencidos */}
                      {userLoans.filter(loan => new Date(loan.fecha_devolucion_pactada) < new Date()).length > 0 && (
                        <Box>
                          <HStack mb={4}>
                            <LuCircleAlert size={20} color="red" />
                            <Heading size="lg" color="red.600">
                              Préstamos Vencidos ({userLoans.filter(loan => new Date(loan.fecha_devolucion_pactada) < new Date()).length})
                            </Heading>
                          </HStack>
                          <VStack align="stretch" gap={4}>
                            {userLoans
                              .filter(loan => new Date(loan.fecha_devolucion_pactada) < new Date())
                              .map((loan) => {
                                const { daysLate, feeAmount } = calculateLateFee(loan);
                                return (
                                  <Card.Root key={loan._id} borderColor="red.300" borderWidth="2px">
                                    <Accordion.Root collapsible>
                                      <Accordion.Item value={loan._id}>
                                        <Accordion.ItemTrigger p={6} cursor="pointer" _hover={{ bg: "red.50" }}>
                                          <HStack justify="space-between" align="start" w="full">
                                            <VStack align="start" gap={2} flex="1">
                                              <HStack>
                                                <Badge colorPalette="red">
                                                  VENCIDO
                                                </Badge>
                                                <Badge colorPalette="purple">
                                                  {loan.tipo_prestamo.toUpperCase()}
                                                </Badge>
                                                <Badge colorPalette="orange" variant="subtle">
                                                  {daysLate} {daysLate === 1 ? 'día' : 'días'} de atraso
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
                                              <HStack color="red.600" fontSize="sm">
                                                <LuCalendar size={16} />
                                                <Text>Debió devolverse:</Text>
                                              </HStack>
                                              <Text fontWeight="bold" color="red.600" fontSize="lg">
                                                {formatDate(loan.fecha_devolucion_pactada)}
                                              </Text>
                                              <Text fontSize="xs" color="red.500" fontWeight="semibold">
                                                Click para ver multa
                                              </Text>
                                            </VStack>
                                          </HStack>
                                        </Accordion.ItemTrigger>

                                        <Accordion.ItemContent>
                                          <Box px={6} pb={6}>
                                            <Box p={4} bg="red.50" borderRadius="md" borderWidth="1px" borderColor="red.200">
                                              <VStack align="stretch" gap={3}>
                                                <HStack justify="space-between">
                                                  <Text fontSize="sm" color="red.700" fontWeight="semibold">
                                                    💰 Información de Multa por Atraso
                                                  </Text>
                                                </HStack>

                                                <HStack justify="space-between" p={2} bg="white" borderRadius="md">
                                                  <Text fontSize="sm" color="gray.700">
                                                    Días de atraso:
                                                  </Text>
                                                  <Badge colorPalette="red" size="lg">
                                                    {daysLate} {daysLate === 1 ? 'día' : 'días'}
                                                  </Badge>
                                                </HStack>

                                                <HStack justify="space-between" p={2} bg="white" borderRadius="md">
                                                  <Text fontSize="sm" color="gray.700">
                                                    Tarifa por día:
                                                  </Text>
                                                  <Text fontWeight="semibold">$500</Text>
                                                </HStack>

                                                <Box h="1px" bg="red.200" />

                                                <HStack justify="space-between" p={3} bg="red.100" borderRadius="md">
                                                  <Text fontSize="md" fontWeight="bold" color="red.700">
                                                    Total a pagar:
                                                  </Text>
                                                  <Text fontSize="2xl" fontWeight="bold" color="red.600">
                                                    ${feeAmount.toLocaleString('es-CL')}
                                                  </Text>
                                                </HStack>

                                                <Text fontSize="xs" color="gray.600" textAlign="center" mt={1}>
                                                  ⚠️ Debes pagar esta multa al devolver el libro en biblioteca
                                                </Text>
                                              </VStack>
                                            </Box>
                                          </Box>
                                        </Accordion.ItemContent>
                                      </Accordion.Item>
                                    </Accordion.Root>
                                  </Card.Root>
                                );
                              })}
                          </VStack>
                        </Box>
                      )}

                      {/* Préstamos Activos */}
                      {userLoans.filter(loan => new Date(loan.fecha_devolucion_pactada) >= new Date()).length > 0 && (
                        <Box>
                          <HStack mb={4}>
                            <LuBook size={20} color="blue" />
                            <Heading size="lg" color="blue.600">
                              Préstamos Activos ({userLoans.filter(loan => new Date(loan.fecha_devolucion_pactada) >= new Date()).length})
                            </Heading>
                          </HStack>
                          <VStack align="stretch" gap={4}>
                            {userLoans
                              .filter(loan => new Date(loan.fecha_devolucion_pactada) >= new Date())
                              .map((loan) => (
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
                          </VStack>
                        </Box>
                      )}

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
              </Tabs.Content>

              {/* Tab de Reservas */}
              <Tabs.Content value="reservations">
                <Box pt={6}>
                  {isLoadingReservations ? (
                    <Box textAlign="center" py={8}>
                      <Spinner size="lg" color="orange.500" />
                    </Box>
                  ) : userReservations.length === 0 ? (
                    <Card.Root p={6}>
                      <Text color="gray.600" textAlign="center">
                        No tienes reservas registradas
                      </Text>
                    </Card.Root>
                  ) : (
                    <VStack align="stretch" gap={4}>
                      {userReservations.map((reservation) => (
                        <Card.Root key={reservation._id} p={6}>
                          <HStack justify="space-between" align="start">
                            <VStack align="start" gap={2} flex="1">
                              <HStack>
                                <Badge colorPalette={getReservationStatusColor(reservation.estado)}>
                                  {reservation.estado.toUpperCase()}
                                </Badge>
                              </HStack>
                              <Text fontSize="sm" color="gray.600">
                                ID del ejemplar: {reservation.document_id}
                              </Text>
                              <HStack color="gray.600" fontSize="sm">
                                <LuCalendar size={16} />
                                <Text>Reservado para: {formatDate(reservation.fecha_reserva)}</Text>
                              </HStack>
                            </VStack>
                            <VStack align="end" gap={1}>
                              <Text fontSize="xs" color="gray.500">
                                ID: {reservation._id}
                              </Text>
                            </VStack>
                          </HStack>
                        </Card.Root>
                      ))}
                    </VStack>
                  )}
                </Box>
              </Tabs.Content>
            </Tabs.Root>
          </Box>
        </VStack>

        {/* Quick Reservation Dialog */}
        {user && (
          <QuickReservationDialog
            isOpen={isReservationDialogOpen}
            onClose={() => setIsReservationDialogOpen(false)}
            onSuccess={() => {
              setIsReservationDialogOpen(false);
              // Recargar reservas después de crear una nueva
              if (user) {
                ReservationService.getUserReservations(user._id, 0, 100)
                  .then(setUserReservations)
                  .catch(console.error);
              }
            }}
            userId={user._id}
          />
        )}
      </Container>
    </Box>
  );
}
