"use client";

import { useState, useEffect } from "react";
import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  SimpleGrid,
  Card,
  HStack,
  Button,
  Spinner,
  Table,
} from "@chakra-ui/react";
import { AdminNav } from "@/components/admin/AdminNav";
import { LuUsers, LuBook, LuBookOpen, LuCircleAlert, LuDownload } from "react-icons/lu";
import { useAuth } from "@/contexts/AuthContext";
import StatisticsService, { type DashboardStats, type PopularDocument } from "@/services/statistics.service";
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";
import { Pie, Bar } from "react-chartjs-2";

// Registrar componentes de Chart.js
ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function AdminDashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [popularDocs, setPopularDocs] = useState<PopularDocument[]>([]);
  const [isLoadingStats, setIsLoadingStats] = useState(true);
  const [isLoadingDocs, setIsLoadingDocs] = useState(true);
  const [isExporting, setIsExporting] = useState(false);

  const isAdmin = user?.rol === "administrativo";
  const isBibliotecario = user?.rol === "bibliotecario";

  useEffect(() => {
    if (isAdmin) {
      loadDashboardStats();
    } else {
      setIsLoadingStats(false);
    }
    loadPopularDocuments();
  }, [isAdmin]);

  const loadDashboardStats = async () => {
    try {
      const data = await StatisticsService.getDashboardStats();
      setStats(data);
    } catch (error) {
      console.error("Error al cargar estadísticas:", error);
    } finally {
      setIsLoadingStats(false);
    }
  };

  const loadPopularDocuments = async () => {
    try {
      const docs = await StatisticsService.getPopularDocuments(10, 30);
      setPopularDocs(docs);
    } catch (error) {
      console.error("Error al cargar documentos populares:", error);
    } finally {
      setIsLoadingDocs(false);
    }
  };

  const handleExportLoans = async () => {
    setIsExporting(true);
    try {
      const blob = await StatisticsService.exportLoans();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `prestamos_${new Date().toISOString().split("T")[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Error al exportar préstamos:", error);
    } finally {
      setIsExporting(false);
    }
  };

  // Datos para gráfico de colección
  const collectionChartData = stats ? {
    labels: ["Disponibles", "Prestados"],
    datasets: [
      {
        label: "Ejemplares",
        data: [stats.collection.items_disponibles, stats.collection.items_prestados],
        backgroundColor: ["rgba(34, 197, 94, 0.8)", "rgba(59, 130, 246, 0.8)"],
        borderColor: ["rgba(34, 197, 94, 1)", "rgba(59, 130, 246, 1)"],
        borderWidth: 1,
      },
    ],
  } : null;

  // Datos para gráfico de préstamos
  const loansChartData = stats ? {
    labels: ["Activos", "Vencidos", "Último mes"],
    datasets: [
      {
        label: "Préstamos",
        data: [stats.loans.active, stats.loans.overdue, stats.loans.last_month],
        backgroundColor: [
          "rgba(59, 130, 246, 0.8)",
          "rgba(239, 68, 68, 0.8)",
          "rgba(168, 85, 247, 0.8)",
        ],
        borderColor: [
          "rgba(59, 130, 246, 1)",
          "rgba(239, 68, 68, 1)",
          "rgba(168, 85, 247, 1)",
        ],
        borderWidth: 1,
      },
    ],
  } : null;

  const getRoleLabel = () => {
    if (isAdmin) return "Administrador";
    if (isBibliotecario) return "Bibliotecario";
    return user?.rol;
  };

  if (isLoadingStats && isAdmin) {
    return (
      <Box minH="100vh" bg="bg.canvas">
        {isBibliotecario && <AdminNav />}
        <Box display="flex" alignItems="center" justifyContent="center" minH="50vh">
          <Spinner size="xl" color="purple.500" />
        </Box>
      </Box>
    );
  }

  return (
    <Box minH="100vh" bg="bg.canvas">
      {isBibliotecario && <AdminNav />}

      <Container maxW="container.xl" py={8}>
        <VStack align="stretch" gap={8}>
          {/* Header */}
          <HStack justify="space-between">
            <Box>
              <Heading size="2xl" mb={2}>
                {isAdmin ? "Panel Administrativo" : "Panel de Biblioteca"}
              </Heading>
              <Text color="gray.600">
                {user?.nombres} {user?.apellidos} • {getRoleLabel()}
              </Text>
            </Box>
            {isAdmin && (
              <Button
                colorPalette="purple"
                onClick={handleExportLoans}
                loading={isExporting}
              >
                <LuDownload />
                Exportar Préstamos
              </Button>
            )}
          </HStack>

          {/* Stats Cards - Solo para Administrador */}
          {isAdmin && stats && (
            <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} gap={6}>
              <Card.Root p={6} borderTopWidth="4px" borderTopColor="blue.500">
                <VStack align="start" gap={3}>
                  <HStack justify="space-between" w="full">
                    <Box color="blue.500">
                      <LuUsers size={28} />
                    </Box>
                    <Text fontSize="3xl" fontWeight="bold">
                      {stats?.users.total || 0}
                    </Text>
                  </HStack>
                  <Text fontSize="sm" color="gray.600">
                    Total Usuarios
                  </Text>
                  <Text fontSize="xs" color="red.600">
                    {stats?.users.sanctioned || 0} sancionados
                  </Text>
                </VStack>
              </Card.Root>

              <Card.Root p={6} borderTopWidth="4px" borderTopColor="green.500">
                <VStack align="start" gap={3}>
                  <HStack justify="space-between" w="full">
                    <Box color="green.500">
                      <LuBook size={28} />
                    </Box>
                    <Text fontSize="3xl" fontWeight="bold">
                      {stats?.collection.total_documents || 0}
                    </Text>
                  </HStack>
                  <Text fontSize="sm" color="gray.600">
                    Total Documentos
                  </Text>
                  <Text fontSize="xs" color="gray.500">
                    {stats?.collection.total_items || 0} ejemplares
                  </Text>
                </VStack>
              </Card.Root>

              <Card.Root p={6} borderTopWidth="4px" borderTopColor="purple.500">
                <VStack align="start" gap={3}>
                  <HStack justify="space-between" w="full">
                    <Box color="purple.500">
                      <LuBookOpen size={28} />
                    </Box>
                    <Text fontSize="3xl" fontWeight="bold">
                      {stats?.loans.active || 0}
                    </Text>
                  </HStack>
                  <Text fontSize="sm" color="gray.600">
                    Préstamos Activos
                  </Text>
                  <Text fontSize="xs" color="gray.500">
                    {stats?.loans.last_month || 0} último mes
                  </Text>
                </VStack>
              </Card.Root>

              <Card.Root p={6} borderTopWidth="4px" borderTopColor="red.500">
                <VStack align="start" gap={3}>
                  <HStack justify="space-between" w="full">
                    <Box color="red.500">
                      <LuCircleAlert size={28} />
                    </Box>
                    <Text fontSize="3xl" fontWeight="bold">
                      {stats?.loans.overdue || 0}
                    </Text>
                  </HStack>
                  <Text fontSize="sm" color="gray.600">
                    Préstamos Vencidos
                  </Text>
                  <Text fontSize="xs" color="orange.600">
                    {stats?.reservations.active || 0} reservas activas
                  </Text>
                </VStack>
              </Card.Root>
            </SimpleGrid>
          )}

          {/* Charts - Solo para Administrador */}
          {isAdmin && stats && (
            <SimpleGrid columns={{ base: 1, lg: 2 }} gap={6}>
              <Card.Root p={6}>
                <Heading size="lg" mb={4}>
                  Estado de Colección
                </Heading>
                {collectionChartData && (
                  <Box maxW="400px" mx="auto">
                    <Pie data={collectionChartData} />
                  </Box>
                )}
              </Card.Root>

              <Card.Root p={6}>
                <Heading size="lg" mb={4}>
                  Estadísticas de Préstamos
                </Heading>
                {loansChartData && (
                  <Bar
                    data={loansChartData}
                    options={{
                      responsive: true,
                      plugins: {
                        legend: {
                          display: false,
                        },
                      },
                    }}
                  />
                )}
              </Card.Root>
            </SimpleGrid>
          )}

          {/* Popular Documents - Para ambos roles */}
          <Card.Root p={6}>
            <Heading size="lg" mb={4}>
              Documentos Más Populares (Últimos 30 días)
            </Heading>
            {isLoadingDocs ? (
              <Box textAlign="center" py={8}>
                <Spinner size="lg" color="purple.500" />
              </Box>
            ) : popularDocs.length === 0 ? (
              <Text color="gray.600" textAlign="center" py={4}>
                No hay datos disponibles
              </Text>
            ) : (
              <Table.Root variant="outline">
                <Table.Header>
                  <Table.Row>
                    <Table.ColumnHeader>Título</Table.ColumnHeader>
                    <Table.ColumnHeader>Autor</Table.ColumnHeader>
                    <Table.ColumnHeader>Categoría</Table.ColumnHeader>
                    <Table.ColumnHeader>Tipo</Table.ColumnHeader>
                    <Table.ColumnHeader textAlign="right">Préstamos</Table.ColumnHeader>
                  </Table.Row>
                </Table.Header>
                <Table.Body>
                  {popularDocs.map((doc) => (
                    <Table.Row key={doc.document_id}>
                      <Table.Cell fontWeight="semibold">{doc.titulo}</Table.Cell>
                      <Table.Cell>{doc.autor}</Table.Cell>
                      <Table.Cell>{doc.categoria}</Table.Cell>
                      <Table.Cell>
                        <Text textTransform="capitalize">{doc.tipo}</Text>
                      </Table.Cell>
                      <Table.Cell textAlign="right">
                        <Text fontWeight="bold" color="purple.600">
                          {doc.total_prestamos}
                        </Text>
                      </Table.Cell>
                    </Table.Row>
                  ))}
                </Table.Body>
              </Table.Root>
            )}
          </Card.Root>
        </VStack>
      </Container>
    </Box>
  );
}
