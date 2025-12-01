"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  Card,
  HStack,
  Badge,
  Spinner,
  Stack,
} from "@chakra-ui/react";
import { UserNav } from "@/components/user/UserNav";
import { LuBook, LuCalendar, LuClock } from "react-icons/lu";
import StatisticsService, { type LoanHistoryItem } from "@/services/statistics.service";

export default function HistorialPage() {
  const [history, setHistory] = useState<LoanHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);
  const observerTarget = useRef<HTMLDivElement>(null);

  // Cargar historial con paginación
  const loadHistory = useCallback(async (pageNum: number) => {
    if (isLoading) return;

    setIsLoading(true);
    try {
      const items = await StatisticsService.getLoanHistory(pageNum * 10, 10);

      if (items.length < 10) {
        setHasMore(false);
      }

      if (pageNum === 0) {
        setHistory(items);
      } else {
        setHistory((prev) => [...prev, ...items]);
      }
    } catch (error) {
      console.error("Error al cargar historial:", error);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  // Cargar primera página
  useEffect(() => {
    loadHistory(0);
  }, []);

  // Infinite scroll observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoading) {
          setPage((prev) => {
            const nextPage = prev + 1;
            loadHistory(nextPage);
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
  }, [hasMore, isLoading, loadHistory]);

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

  const getStatusLabel = (estado: string) => {
    switch (estado) {
      case "activo":
        return "ACTIVO";
      case "vencido":
        return "VENCIDO";
      case "devuelto":
        return "DEVUELTO";
      default:
        return estado.toUpperCase();
    }
  };

  return (
    <Box minH="100vh" bg="bg.canvas">
      <UserNav />

      <Container maxW="container.xl" py={8}>
        <VStack align="stretch" gap={6}>
          <Box>
            <Heading size="2xl" mb={2}>
              Historial de Préstamos
            </Heading>
            <Text color="gray.600">
              Revisa todos los libros que has tomado prestados anteriormente
            </Text>
          </Box>

          {isLoading && page === 0 ? (
            <Box textAlign="center" py={8}>
              <Spinner size="xl" color="blue.500" />
            </Box>
          ) : history.length === 0 ? (
            <Card.Root p={8}>
              <Text color="gray.600" textAlign="center" fontSize="lg">
                No tienes historial de préstamos
              </Text>
            </Card.Root>
          ) : (
            <VStack align="stretch" gap={4}>
              {history.map((item) => (
                <Card.Root key={item.loan_id} p={6}>
                  <Stack direction={{ base: "column", md: "row" }} justify="space-between" gap={4}>
                    {/* Información del libro */}
                    <VStack align="start" gap={2} flex="1">
                      <HStack>
                        <LuBook size={20} color="var(--chakra-colors-blue-500)" />
                        <Text fontSize="lg" fontWeight="bold">
                          {item.document.title}
                        </Text>
                      </HStack>
                      <Text color="gray.600" fontSize="sm">
                        {item.document.author}
                      </Text>
                      <HStack gap={2}>
                        <Badge colorPalette={getStatusColor(item.estado)}>
                          {getStatusLabel(item.estado)}
                        </Badge>
                        <Badge colorPalette="purple">
                          {item.tipo_prestamo.toUpperCase()}
                        </Badge>
                        <Badge colorPalette="gray">
                          {item.document.tipo.toUpperCase()}
                        </Badge>
                      </HStack>
                    </VStack>

                    {/* Fechas */}
                    <VStack align={{ base: "start", md: "end" }} gap={2} minW="200px">
                      <HStack color="gray.600" fontSize="sm">
                        <LuClock size={16} />
                        <Text>Prestado:</Text>
                        <Text fontWeight="semibold">{formatDate(item.fecha_prestamo)}</Text>
                      </HStack>
                      <HStack color="gray.600" fontSize="sm">
                        <LuCalendar size={16} />
                        <Text>Devolución pactada:</Text>
                        <Text fontWeight="semibold">{formatDate(item.fecha_devolucion_pactada)}</Text>
                      </HStack>
                      {item.fecha_devolucion_real && (
                        <HStack color="green.600" fontSize="sm">
                          <LuCalendar size={16} />
                          <Text>Devuelto:</Text>
                          <Text fontWeight="semibold">{formatDate(item.fecha_devolucion_real)}</Text>
                        </HStack>
                      )}
                    </VStack>
                  </Stack>
                </Card.Root>
              ))}

              {/* Infinite scroll trigger */}
              <div ref={observerTarget} style={{ height: "20px" }}>
                {isLoading && page > 0 && (
                  <Box textAlign="center" py={4}>
                    <Spinner size="md" color="blue.500" />
                  </Box>
                )}
              </div>

              {!hasMore && history.length > 0 && (
                <Text textAlign="center" color="gray.500" fontSize="sm" py={4}>
                  No hay más registros para mostrar
                </Text>
              )}
            </VStack>
          )}
        </VStack>
      </Container>
    </Box>
  );
}
