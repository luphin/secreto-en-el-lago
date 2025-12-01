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
import type { ReservationCreate } from "@/types/reservation.types";

interface ReservationFormDialogProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export function ReservationFormDialog({ isOpen, onClose, onSuccess }: ReservationFormDialogProps) {
    const [formData, setFormData] = useState<ReservationCreate>({
        document_id: "",
        user_id: "",
        fecha_reserva: "",
    });
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            await ReservationService.createReservation(formData);
            toaster.create({
                title: "Éxito",
                description: "Reserva creada correctamente",
                type: "success",
            });
            onSuccess();
            // Reset form
            setFormData({
                document_id: "",
                user_id: "",
                fecha_reserva: "",
            });
        } catch (error: any) {
            console.error("Error creating reservation:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo crear la reserva",
                type: "error",
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
                                <Field label="ID del Documento" required>
                                    <Input
                                        value={formData.document_id}
                                        onChange={(e) => setFormData({ ...formData, document_id: e.target.value })}
                                        placeholder="ID del documento"
                                        required
                                    />
                                </Field>

                                <Field label="ID del Usuario" required>
                                    <Input
                                        value={formData.user_id}
                                        onChange={(e) => setFormData({ ...formData, user_id: e.target.value })}
                                        placeholder="ID del usuario"
                                        required
                                    />
                                </Field>

                                <Field label="Fecha de Reserva" required>
                                    <Input
                                        type="datetime-local"
                                        value={formData.fecha_reserva}
                                        onChange={(e) => setFormData({ ...formData, fecha_reserva: e.target.value })}
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
