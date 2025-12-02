"use client";

import { useState, useEffect } from "react";
import {
    Dialog,
    VStack,
    Input,
    Button,
    Select,
    createListCollection,
} from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { toaster } from "@/components/ui/toaster";
import ItemService from "@/services/item.service";
import DocumentService from "@/services/document.service";
import type { ItemResponse, ItemCreate, ItemUpdate } from "@/types/item.types";
import { ItemStatus } from "@/types/item.types";

const itemStatuses = createListCollection({
    items: [
        { label: "Disponible", value: ItemStatus.DISPONIBLE },
        { label: "Prestado", value: ItemStatus.PRESTADO },
        { label: "En Restauración", value: ItemStatus.EN_RESTAURACION },
        { label: "Reservado", value: ItemStatus.RESERVADO },
    ],
});

interface ItemFormDialogProps {
    isOpen: boolean;
    onClose: () => void;
    item: ItemResponse | null;
    onSuccess: () => void;
}

export function ItemFormDialog({ isOpen, onClose, item, onSuccess }: ItemFormDialogProps) {
    const [physicalId, setPhysicalId] = useState("");
    const [ubicacion, setUbicacion] = useState("");
    const [estado, setEstado] = useState<ItemStatus>(ItemStatus.DISPONIBLE);
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        if (item) {
            setPhysicalId("");
            setUbicacion(item.ubicacion);
            setEstado(item.estado);
        } else {
            setPhysicalId("");
            setUbicacion("");
            setEstado(ItemStatus.DISPONIBLE);
        }
    }, [item, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            if (item) {
                // Update
                const updateData: ItemUpdate = {
                    ubicacion,
                    estado,
                };
                await ItemService.updateItem(item._id, updateData);
                toaster.create({
                    title: "Éxito",
                    description: "Ejemplar actualizado correctamente",
                    type: "success",
                });
            } else {
                // Create - primero buscar el documento por ID físico
                const documentData = await DocumentService.getDocumentByPhysicalId(physicalId);

                const formData: ItemCreate = {
                    document_id: documentData.document_id,
                    ubicacion,
                    estado,
                };

                await ItemService.createItem(formData);
                toaster.create({
                    title: "Éxito",
                    description: "Ejemplar creado correctamente",
                    type: "success",
                });
            }
            onSuccess();
        } catch (error: any) {
            console.error("Error saving item:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo guardar el ejemplar",
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
                        <Dialog.Title>{item ? "Editar Ejemplar" : "Nuevo Ejemplar"}</Dialog.Title>
                    </Dialog.Header>

                    <Dialog.Body>
                        <form onSubmit={handleSubmit}>
                            <VStack gap={4}>
                                {!item && (
                                    <Field label="ID Físico del Documento" required>
                                        <Input
                                            value={physicalId}
                                            onChange={(e) => setPhysicalId(e.target.value)}
                                            placeholder="LIB-006-2024"
                                            required
                                        />
                                    </Field>
                                )}

                                <Field label="Ubicación" required>
                                    <Input
                                        value={ubicacion}
                                        onChange={(e) => setUbicacion(e.target.value)}
                                        placeholder="Estantería 5, Nivel 3"
                                        required
                                    />
                                </Field>

                                <Field label="Estado" required>
                                    <Select.Root
                                        collection={itemStatuses}
                                        value={[estado ?? ItemStatus.DISPONIBLE]}
                                        onValueChange={(e) => setEstado(e.value[0] as ItemStatus)}
                                    >
                                        <Select.Trigger>
                                            <Select.ValueText placeholder="Seleccionar estado" />
                                        </Select.Trigger>
                                        <Select.Content>
                                            {itemStatuses.items.map((item) => (
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
                        <Button variant="outline" onClick={onClose} disabled={isSubmitting}>
                            Cancelar
                        </Button>
                        <Button
                            colorPalette="blue"
                            onClick={handleSubmit}
                            loading={isSubmitting}
                        >
                            {item ? "Actualizar" : "Crear"}
                        </Button>
                    </Dialog.Footer>

                    <Dialog.CloseTrigger />
                </Dialog.Content>
            </Dialog.Positioner>
        </Dialog.Root>
    );
}
