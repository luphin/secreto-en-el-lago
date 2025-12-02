"use client";

import { useState } from "react";
import {
    Dialog,
    VStack,
    Input,
    Button,
} from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { toaster } from "@/components/ui/toaster";
import ReservationService from "@/services/reservation.service";
import DocumentService from "@/services/document.service";
import type { ReservationCreate } from "@/types/reservation.types";

interface ReservationFormDialogProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export function ReservationFormDialog({ isOpen, onClose, onSuccess }: ReservationFormDialogProps) {
    const [physicalId, setPhysicalId] = useState("");
    const [userId, setUserId] = useState("");
    const [reservationDate, setReservationDate] = useState("");
    const [formData, setFormData] = useState<ReservationCreate>({
        document_id: "",
        user_id: "",
        fecha_reserva: "",
    });
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!physicalId.trim() || !userId.trim() || !reservationDate) {
            toaster.create({
                title: "Error de validación",
                description: "Por favor completa todos los campos",
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
                description: `Reserva para el libro ${physicalId} registrada correctamente`,
                type: "success",
                duration: 5000,
            });
            onSuccess();
            // Reset form
            setPhysicalId("");
            setUserId("");
            setReservationDate("");
            setFormData({
                document_id: "",
                user_id: "",
                fecha_reserva: "",
            });
        } catch (error: any) {
            console.error("Error creating reservation:", error);
            const errorMessage = error.response?.data?.detail || "No se pudo crear la reserva. Verifica que el ID físico sea correcto.";
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
                                <Field label="ID Físico del Libro" required helperText="Ejemplo: LIB-015-2024">
                                    <Input
                                        value={physicalId}
                                        onChange={(e) => setPhysicalId(e.target.value)}
                                        placeholder="LIB-XXX-XXXX"
                                        required
                                    />
                                </Field>

                                <Field label="ID del Usuario" required>
                                    <Input
                                        value={userId}
                                        onChange={(e) => setUserId(e.target.value)}
                                        placeholder="ID del usuario"
                                        required
                                    />
                                </Field>

                                <Field label="Fecha de Reserva" required helperText="Selecciona cuándo recogerá el libro">
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
                            colorPalette="purple"
                            onClick={handleSubmit}
                            loading={isSubmitting}
                        >
                            Crear
                        </Button>
                    </Dialog.Footer>
                </Dialog.Content>
            </Dialog.Positioner>
        </Dialog.Root>
    );
}
