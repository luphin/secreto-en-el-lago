"use client";

import { useState, useEffect } from "react";
import {
    Box,
    VStack,
    HStack,
    Button,
    Table,
    Spinner,
    Card,
    Text,
    Badge,
    Select,
    createListCollection,
} from "@chakra-ui/react";
import { LuPlus, LuCircleCheck, LuFilter } from "react-icons/lu";
import { toaster } from "@/components/ui/toaster";
import LoanService from "@/services/loan.service";
import type { LoanResponse } from "@/types/loan.types";
import { LoanStatus } from "@/types/loan.types";
import { LoanFormDialog } from "./LoanFormDialog";

const LoanStatuses = createListCollection({
    items: [
        { label: "Activo", value: LoanStatus.ACTIVO },
        { label: "Devuelto", value: LoanStatus.DEVUELTO },
        { label: "Vencido", value: LoanStatus.VENCIDO }
    ],
});

export function LoansTab() {
    const [loans, setLoans] = useState<LoanResponse[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState<LoanStatus | "all">("all");
    const [isFormOpen, setIsFormOpen] = useState(false);

    useEffect(() => {
        loadLoans();
    }, [statusFilter]);

    const loadLoans = async () => {
        setIsLoading(true);
        try {
            const params = statusFilter !== "all" ? { estado: statusFilter, limit: 100 } : { limit: 100 };
            const data = await LoanService.getUserLoans(0, 100);
            setLoans(data);
        } catch (error) {
            console.error("Error loading loans:", error);
            toaster.create({
                title: "Error",
                description: "No se pudieron cargar los préstamos",
                type: "error",
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleReturn = async (loanId: string) => {
        try {
            await LoanService.returnLoan(loanId);
            toaster.create({
                title: "Éxito",
                description: "Préstamo devuelto correctamente",
                type: "success",
            });
            loadLoans();
        } catch (error: any) {
            console.error("Error returning loan:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo procesar la devolución",
                type: "error",
            });
        }
    };

    const handleFormSuccess = () => {
        setIsFormOpen(false);
        loadLoans();
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case "activo":
                return "blue";
            case "devuelto":
                return "green";
            case "vencido":
                return "red";
            default:
                return "gray";
        }
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("es-ES");
    };

    if (isLoading && loans.length === 0) {
        return (
            <Box textAlign="center" py={12}>
                <Spinner size="xl" color="purple.500" />
            </Box>
        );
    }

    return (
        <VStack align="stretch" gap={6}>
            {/* Header with filter and create button */}
            <Card.Root p={4}>
                <HStack justify="space-between">
                    <HStack>
                        <LuFilter />
                        <Text fontWeight="semibold">Filtrar por estado:</Text>
                        <Select.Root
                            collection={LoanStatuses}
                            value={[statusFilter]}
                            onValueChange={(e) => setStatusFilter(e.value[0] as LoanStatus | "all")}
                            width="200px"
                        >
                            <Select.Trigger>
                                <Select.ValueText />
                            </Select.Trigger>
                            <Select.Content>
                                {LoanStatuses.items.map((item) => (
                                    <Select.Item key={item.value} item={item}>
                                        {item.label}
                                    </Select.Item>
                                ))}
                            </Select.Content>
                        </Select.Root>
                    </HStack>
                    <Button onClick={() => setIsFormOpen(true)} colorPalette="purple">
                        <LuPlus />
                        Nuevo Préstamo
                    </Button>
                </HStack>
            </Card.Root>

            {/* Loans table */}
            <Card.Root>
                {loans.length === 0 ? (
                    <Box textAlign="center" py={8}>
                        <Text color="gray.600">No se encontraron préstamos</Text>
                    </Box>
                ) : (
                    <Table.Root variant="outline">
                        <Table.Header>
                            <Table.Row>
                                <Table.ColumnHeader>ID Ejemplar</Table.ColumnHeader>
                                <Table.ColumnHeader>Usuario</Table.ColumnHeader>
                                <Table.ColumnHeader>Tipo</Table.ColumnHeader>
                                <Table.ColumnHeader>Fecha Préstamo</Table.ColumnHeader>
                                <Table.ColumnHeader>Fecha Devolución</Table.ColumnHeader>
                                <Table.ColumnHeader>Estado</Table.ColumnHeader>
                                <Table.ColumnHeader>Acciones</Table.ColumnHeader>
                            </Table.Row>
                        </Table.Header>
                        <Table.Body>
                            {loans.map((loan) => (
                                <Table.Row key={loan._id}>
                                    <Table.Cell fontFamily="mono">{loan.item_id}</Table.Cell>
                                    <Table.Cell fontFamily="mono">{loan.user_id}</Table.Cell>
                                    <Table.Cell>
                                        <Badge colorPalette={loan.tipo_prestamo === "sala" ? "purple" : "blue"}>
                                            {loan.tipo_prestamo}
                                        </Badge>
                                    </Table.Cell>
                                    <Table.Cell>{formatDate(loan.fecha_prestamo)}</Table.Cell>
                                    <Table.Cell>
                                        {loan.fecha_devolucion_real
                                            ? formatDate(loan.fecha_devolucion_real)
                                            : formatDate(loan.fecha_devolucion_pactada)}
                                    </Table.Cell>
                                    <Table.Cell>
                                        <Badge colorPalette={getStatusColor(loan.estado)}>
                                            {loan.estado}
                                        </Badge>
                                    </Table.Cell>
                                    <Table.Cell>
                                        {loan.estado === LoanStatus.ACTIVO && (
                                            <Button
                                                size="sm"
                                                onClick={() => handleReturn(loan._id)}
                                                colorPalette="green"
                                            >
                                                <LuCircleCheck />
                                                Devolver
                                            </Button>
                                        )}
                                    </Table.Cell>
                                </Table.Row>
                            ))}
                        </Table.Body>
                    </Table.Root>
                )}
            </Card.Root>

            {/* Form Dialog */}
            <LoanFormDialog
                isOpen={isFormOpen}
                onClose={() => setIsFormOpen(false)}
                onSuccess={handleFormSuccess}
            />
        </VStack>
    );
}
