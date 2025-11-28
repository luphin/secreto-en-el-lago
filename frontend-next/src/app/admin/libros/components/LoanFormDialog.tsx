"use client";

import { useState } from "react";
import {
    Dialog,
    VStack,
    Input,
    Button,
    Select,
    createListCollection,
} from "@chakra-ui/react";
import { toaster } from "@/components/ui/toaster";
import { Field } from "@/components/ui/field";
import LoanService from "@/services/loan.service";
import type { LoanCreate } from "@/types/loan.types";
import { LoanType } from "@/types/loan.types";

const loanTypes = createListCollection({
    items: [
        { label: "Sala", value: LoanType.SALA },
        { label: "Domicilio", value: LoanType.DOMICILIO },
    ],
});

interface LoanFormDialogProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export function LoanFormDialog({ isOpen, onClose, onSuccess }: LoanFormDialogProps) {
    const [formData, setFormData] = useState<LoanCreate>({
        item_id: "",
        user_id: "",
        tipo_prestamo: LoanType.DOMICILIO,
    });
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            await LoanService.createLoan(formData);
            toaster.create({
                title: "Éxito",
                description: "Préstamo creado correctamente",
                type: "success",
            });
            onSuccess();
            // Reset form
            setFormData({
                item_id: "",
                user_id: "",
                tipo_prestamo: LoanType.DOMICILIO,
            });
        } catch (error: any) {
            console.error("Error creating loan:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo crear el préstamo",
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
                        <Dialog.Title>Nuevo Préstamo</Dialog.Title>
                    </Dialog.Header>

                    <Dialog.Body>
                        <form onSubmit={handleSubmit}>
                            <VStack gap={4}>
                                <Field label="ID del Ejemplar" required>
                                    <Input
                                        value={formData.item_id}
                                        onChange={(e) => setFormData({ ...formData, item_id: e.target.value })}
                                        placeholder="ID del ejemplar"
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

                                <Field label="Tipo de Préstamo" required>
                                    <Select.Root
                                        collection={loanTypes}
                                        value={[formData.tipo_prestamo]}
                                        onValueChange={(e) => setFormData({ ...formData, tipo_prestamo: e.value[0] as LoanType })}
                                    >
                                        <Select.Trigger>
                                            <Select.ValueText placeholder="Seleccionar tipo" />
                                        </Select.Trigger>
                                        <Select.Content>
                                            {loanTypes.items.map((item) => (
                                                <Select.Item key={item.value} item={item}>
                                                    {item.label}
                                                </Select.Item>
                                            ))}
                                        </Select.Content>
                                    </Select.Root>
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
