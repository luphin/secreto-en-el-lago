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
import { LoanStatus, type LoanResponse } from "@/types/loan.types";
import { UserRole } from "@/types/auth.types";
import MercadoPagoButton from "@/components/checkout/MercadoPagoButton";

const stats = [
  { icon: LuBook, label: "Préstamos activos", value: "3", color: "blue" },
  { icon: LuClock, label: "Reservas pendientes", value: "1", color: "orange" },
  { icon: LuCircleCheck, label: "Libros devueltos", value: "12", color: "green" },
  { icon: LuCircleAlert, label: "Por vencer", value: "1", color: "red" },
];

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

// Función para calcular días de atraso
const getDaysOverdue = (dateString: string) => {
  const today = new Date();
  const dueDate = new Date(dateString);
  const diffTime = today.getTime() - dueDate.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays > 0 ? diffDays : 0;
};

// Función para calcular multa ($1.000 por día)
const calculateFine = (days: number) => {
  return days * 1000;
};

// Componente interno para cada tarjeta de préstamo
const LoanItemCard = ({ loan, userEmail }: { loan: LoanResponse, userEmail: string }) => {
  // Usamos test@testuser.com por defecto para testing
  const emailToPay = "test@testuser.com";
  
  const daysOverdue = getDaysOverdue(loan.fecha_devolucion_pactada.toString());
  const fineAmount = calculateFine(daysOverdue);
  const isOverdue = daysOverdue > 0;

  // Items para Mercado Pago
  const paymentItems = isOverdue ? [{
    title: `Multa por atraso (${daysOverdue} días) - ID: ${loan.item_id}`,
    quantity: 1,
    unit_price: fineAmount
  }] : [];

  return (
    <Card.Root 
      key={loan._id} 
      p={6} 
      borderLeftWidth={isOverdue ? "4px" : "0"}
      borderLeftColor={isOverdue ? "red.500" : "transparent"}
    >
      <Stack direction={{ base: "column", md: "row" }} justify="space-between" align="start" gap={4}>
        <VStack align="start" gap={2} flex="1">
          <HStack>
            <Badge colorPalette={isOverdue ? "red" : getStatusColor(loan.estado)}>
              {isOverdue ? "ATRASADO" : loan.estado.toUpperCase()}
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
            <Text>Prestado: {formatDate(loan.fecha_prestamo.toString())}</Text>
          </HStack>
        </VStack>
        
        <VStack align={{ base: "start", md: "end" }} gap={2} width={{ base: "100%", md: "auto" }}>
          <HStack color="gray.600" fontSize="sm">
            <LuCalendar size={16} />
            <Text>Devolver antes de:</Text>
          </HStack>
          <Text fontWeight="bold" color={isOverdue ? "red.600" : "blue.600"}>
            {formatDate(loan.fecha_devolucion_pactada.toString())}
          </Text>
          
          {isOverdue && (
            <Box mt={2} p={4} bg="red.50" borderRadius="md" border="1px solid" borderColor="red.200" width="100%">
              <Text color="red.700" fontWeight="bold" mb={2}>
                ¡Préstamo Vencido!
              </Text>
              <Text fontSize="sm" color="red.600" mb={3}>
                Tienes {daysOverdue} días de atraso.
                <br/>
                Multa: ${fineAmount.toLocaleString('es-CL')}
              </Text>
              
              <MercadoPagoButton 
                items={paymentItems}
                userEmail={emailToPay}
                buttonText="Pagar Multa"
              />
            </Box>
          )}
        </VStack>
      </Stack>
    </Card.Root>
  );
};

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

  // Cargar préstamos vencidos (solo para staff)
  useEffect(() => {
    const loadOverdueLoans = async () => {
      if (!user || !isStaff || isLoadingLoans) return;

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
  }, [user, isStaff, isLoadingLoans]);

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
          {isStaff && (
            <Box>
              <Heading size="xl" mb={4} color="red.600">
                <HStack>
                  <LuCircleAlert />
                  <Text>Préstamos Vencidos (Vista Staff)</Text>
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
          )}

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
                  <LoanItemCard 
                    key={loan._id} 
                    loan={loan} 
                    userEmail={user?.email || ""}
                  />
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
