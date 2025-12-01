"use client";

import { useState } from "react";
import {
    Dialog,
    VStack,
    Input,
    Button,
} from "@chakra-ui/react";
import { toaster } from "@/components/ui/toaster";
import { Field } from "@/components/ui/field";
import ReservationService from "@/services/reservation.service";
import DocumentService from "@/services/document.service";
import type { ReservationCreate } from "@/types/reservation.types";

interface QuickReservationDialogProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
    userId: string;
}

export function QuickReservationDialog({ isOpen, onClose, onSuccess, userId }: QuickReservationDialogProps) {
    const [physicalId, setPhysicalId] = useState("");
    const [reservationDate, setReservationDate] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!physicalId.trim()) {
            toaster.create({
                title: "Error de validación",
                description: "Por favor ingresa el ID físico del documento",
                type: "error",
            });
            return;
        }

        if (!reservationDate) {
            toaster.create({
                title: "Error de validación",
                description: "Por favor selecciona una fecha de reserva",
                type: "error",
            });
            return;
        }

        setIsSubmitting(true);

        try {
            // 1. Obtener document_id usando el ID físico
            const { document_id } = await DocumentService.getDocumentByPhysicalId(physicalId);

            // 2. Crear la reserva
            const reservationData: ReservationCreate = {
                document_id,
                user_id: userId,
                fecha_reserva: new Date(reservationDate).toISOString(),
            };

            await ReservationService.createReservation(reservationData);

            toaster.create({
                title: "¡Reserva creada exitosamente!",
                description: `Tu reserva para el ${new Date(reservationDate).toLocaleDateString('es-ES')} ha sido registrada`,
                type: "success",
                duration: 5000,
            });

            onSuccess();
            setPhysicalId(""); // Reset form
            setReservationDate("");
        } catch (error: any) {
            console.error("Error creating reservation:", error);

            const errorMessage = error.response?.data?.detail || "No se pudo crear la reserva. Por favor intenta nuevamente.";

            toaster.create({
                title: "Error al crear reserva",
                description: errorMessage,
                type: "error",
                duration: 5000,
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Dialog.Root open={isOpen} onOpenChange={(e) => !e.open && onClose()}>
            <Dialog.Backdrop />
            <Dialog.Positioner>
                <Dialog.Content>
                    <Dialog.Header>
                        <Dialog.Title>Nueva Reserva</Dialog.Title>
                    </Dialog.Header>

                    <Dialog.Body>
                        <form onSubmit={handleSubmit}>
                            <VStack gap={4}>
                                <Field label="ID Físico del Documento" required helperText="Ejemplo: LIB-015-2024 (Esto se encuentra dentro del libro, en caso de no estar, dirigirse al mesón por favor.)">
                                    <Input
                                        value={physicalId}
                                        onChange={(e) => setPhysicalId(e.target.value)}
                                        placeholder="LIB-XXX-XXXX"
                                        required
                                    />
                                </Field>

                                <Field label="Fecha de Reserva" required helperText="Selecciona cuándo recogerás el libro">
                                    <Input
                                        type="date"
                                        value={reservationDate}
                                        onChange={(e) => setReservationDate(e.target.value)}
                                        min={new Date().toISOString().split('T')[0]}
                                        required
                                    />
                                </Field>
                            </VStack>
                        </form>
                    </Dialog.Body>

                    <Dialog.Footer>
                        <Dialog.CloseTrigger asChild>
                            <Button variant="outline" onClick={onClose}>
                                Cancelar
                            </Button>
                        </Dialog.CloseTrigger>
                        <Button
                            colorPalette="blue"
                            onClick={handleSubmit}
                            loading={isSubmitting}
                        >
                            Crear Reserva
                        </Button>
                    </Dialog.Footer>
                </Dialog.Content>
            </Dialog.Positioner>
        </Dialog.Root>
    );
}
