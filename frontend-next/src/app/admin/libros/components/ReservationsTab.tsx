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
import { LuPlus, LuCircleX, LuCircleCheck, LuFilter } from "react-icons/lu";
import { toaster } from "@/components/ui/toaster";
import ReservationService from "@/services/reservation.service";
import type { ReservationResponse } from "@/types/reservation.types";
import { ReservationStatus } from "@/types/reservation.types";
import { ReservationFormDialog } from "./ReservationFormDialog";

const reservationStatusFilters = createListCollection({
    items: [
        { label: "Todos", value: "all" },
        { label: "Activas", value: ReservationStatus.ACTIVA },
        { label: "Completadas", value: ReservationStatus.COMPLETADA },
        { label: "Expiradas", value: ReservationStatus.EXPIRADA },
    ],
});

interface ReservationsTabProps {
    isActive: boolean;
}

export function ReservationsTab({ isActive }: ReservationsTabProps) {
    const [reservations, setReservations] = useState<ReservationResponse[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState<ReservationStatus | "all">("all");
    const [isFormOpen, setIsFormOpen] = useState(false);

    useEffect(() => {
        if (isActive && reservations.length === 0) {
            loadReservations();
        }
    }, [isActive]);

    const loadReservations = async () => {
        setIsLoading(true);
        try {
            const data = await ReservationService.getReservations({ limit: 100 });
            setReservations(data);
        } catch (error) {
            console.error("Error loading reservations:", error);
            toaster.create({
                title: "Error",
                description: "No se pudieron cargar las reservas",
                type: "error",
            });
        } finally {
            setIsLoading(false);
        }
    };

    // Filtrar reservas localmente
    const filteredReservations = statusFilter === "all"
        ? reservations
        : reservations.filter(reservation => reservation.estado === statusFilter);

    const handleCancel = async (reservationId: string) => {
        try {
            await ReservationService.cancelReservation(reservationId);
            toaster.create({
                title: "Éxito",
                description: "Reserva cancelada correctamente",
                type: "success",
            });
            loadReservations();
        } catch (error: any) {
            console.error("Error canceling reservation:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo cancelar la reserva",
                type: "error",
            });
        }
    };

    const handleComplete = async (reservationId: string) => {
        try {
            await ReservationService.completeReservation(reservationId);
            toaster.create({
                title: "Éxito",
                description: "Reserva completada correctamente",
                type: "success",
            });
            loadReservations();
        } catch (error: any) {
            console.error("Error completing reservation:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo completar la reserva",
                type: "error",
            });
        }
    };

    const handleFormSuccess = () => {
        setIsFormOpen(false);
        loadReservations();
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case "activa":
                return "blue";
            case "completada":
                return "green";
            case "expirada":
                return "red";
            default:
                return "gray";
        }
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("es-ES");
    };

    if (isLoading && reservations.length === 0) {
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
                            collection={reservationStatusFilters}
                            value={[statusFilter]}
                            onValueChange={(e) => setStatusFilter(e.value[0] as ReservationStatus | "all")}
                            width="200px"
                        >
                            <Select.Trigger>
                                <Select.ValueText />
                            </Select.Trigger>
                            <Select.Content>
                                {reservationStatusFilters.items.map((item) => (
                                    <Select.Item key={item.value} item={item}>
                                        {item.label}
                                    </Select.Item>
                                ))}
                            </Select.Content>
                        </Select.Root>
                    </HStack>
                    <Button onClick={() => setIsFormOpen(true)} colorPalette="purple">
                        <LuPlus />
                        Nueva Reserva
                    </Button>
                </HStack>
            </Card.Root>

            {/* Reservations table */}
            <Card.Root>
                {filteredReservations.length === 0 ? (
                    <Box textAlign="center" py={8}>
                        <Text color="gray.600">No se encontraron reservas</Text>
                    </Box>
                ) : (
                    <Table.Root variant="outline">
                        <Table.Header>
                            <Table.Row>
                                <Table.ColumnHeader>ID Documento</Table.ColumnHeader>
                                <Table.ColumnHeader>Usuario</Table.ColumnHeader>
                                <Table.ColumnHeader>Fecha Reserva</Table.ColumnHeader>
                                <Table.ColumnHeader>Fecha Creación</Table.ColumnHeader>
                                <Table.ColumnHeader>Estado</Table.ColumnHeader>
                                <Table.ColumnHeader>Acciones</Table.ColumnHeader>
                            </Table.Row>
                        </Table.Header>
                        <Table.Body>
                            {filteredReservations.map((reservation) => (
                                <Table.Row key={reservation._id}>
                                    <Table.Cell fontFamily="mono">{reservation.document_id}</Table.Cell>
                                    <Table.Cell fontFamily="mono">{reservation.user_id}</Table.Cell>
                                    <Table.Cell>{formatDate(reservation.fecha_reserva)}</Table.Cell>
                                    <Table.Cell>{formatDate(reservation.fecha_creacion)}</Table.Cell>
                                    <Table.Cell>
                                        <Badge colorPalette={getStatusColor(reservation.estado)}>
                                            {reservation.estado}
                                        </Badge>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <HStack gap={2}>
                                            {reservation.estado === ReservationStatus.ACTIVA && (
                                                <>
                                                    <Button
                                                        size="sm"
                                                        onClick={() => handleComplete(reservation._id)}
                                                        colorPalette="green"
                                                    >
                                                        <LuCircleCheck />
                                                        Completar
                                                    </Button>
                                                    <Button
                                                        size="sm"
                                                        onClick={() => handleCancel(reservation._id)}
                                                        colorPalette="red"
                                                    >
                                                        <LuCircleX />
                                                        Cancelar
                                                    </Button>
                                                </>
                                            )}
                                        </HStack>
                                    </Table.Cell>
                                </Table.Row>
                            ))}
                        </Table.Body>
                    </Table.Root>
                )}
            </Card.Root>

            {/* Form Dialog */}
            <ReservationFormDialog
                isOpen={isFormOpen}
                onClose={() => setIsFormOpen(false)}
                onSuccess={handleFormSuccess}
            />
        </VStack>
    );
}
