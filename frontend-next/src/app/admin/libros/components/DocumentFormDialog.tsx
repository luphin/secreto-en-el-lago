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
import DocumentService from "@/services/document.service";
import type { DocumentResponse, DocumentCreate, DocumentUpdate } from "@/types/document.types";
import { DocumentType } from "@/types/document.types";

const documentTypes = createListCollection({
    items: [
        { label: "Libro", value: DocumentType.LIBRO },
        { label: "Audio", value: DocumentType.AUDIO },
        { label: "Video", value: DocumentType.VIDEO },
    ],
});

interface DocumentFormDialogProps {
    isOpen: boolean;
    onClose: () => void;
    document: DocumentResponse | null;
    onSuccess: () => void;
}

export function DocumentFormDialog({ isOpen, onClose, document, onSuccess }: DocumentFormDialogProps) {
    const [formData, setFormData] = useState<DocumentCreate>({
        id_fisico: "",
        titulo: "",
        autor: "",
        editorial: "",
        edicion: "",
        ano_edicion: new Date().getFullYear(),
        tipo: DocumentType.LIBRO,
        categoria: "",
        tipo_medio: "",
    });
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        if (document) {
            setFormData({
                id_fisico: document.id_fisico,
                titulo: document.titulo,
                autor: document.autor,
                editorial: document.editorial,
                edicion: document.edicion,
                ano_edicion: document.ano_edicion,
                tipo: document.tipo,
                categoria: document.categoria,
                tipo_medio: document.tipo_medio || "",
            });
        } else {
            // Reset form
            setFormData({
                id_fisico: "",
                titulo: "",
                autor: "",
                editorial: "",
                edicion: "",
                ano_edicion: new Date().getFullYear(),
                tipo: DocumentType.LIBRO,
                categoria: "",
                tipo_medio: "",
            });
        }
    }, [document, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            if (document) {
                // Update
                await DocumentService.updateDocument(document._id, formData as DocumentUpdate);
                toaster.create({
                    title: "Éxito",
                    description: "Documento actualizado correctamente",
                    type: "success",
                });
            } else {
                // Create
                await DocumentService.createDocument(formData);
                toaster.create({
                    title: "Éxito",
                    description: "Documento creado correctamente",
                    type: "success",
                });
            }
            onSuccess();
        } catch (error: any) {
            console.error("Error saving document:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo guardar el documento",
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
                        <Dialog.Title>{document ? "Editar Documento" : "Nuevo Documento"}</Dialog.Title>
                    </Dialog.Header>

                    <Dialog.Body>
                        <form onSubmit={handleSubmit}>
                            <VStack gap={4}>
                                <Field label="ID Físico" required>
                                    <Input
                                        value={formData.id_fisico}
                                        onChange={(e) => setFormData({ ...formData, id_fisico: e.target.value })}
                                        placeholder="LIB-001-2024"
                                        required
                                    />
                                </Field>

                                <Field label="Título" required>
                                    <Input
                                        value={formData.titulo}
                                        onChange={(e) => setFormData({ ...formData, titulo: e.target.value })}
                                        placeholder="Título del documento"
                                        required
                                    />
                                </Field>

                                <Field label="Autor" required>
                                    <Input
                                        value={formData.autor}
                                        onChange={(e) => setFormData({ ...formData, autor: e.target.value })}
                                        placeholder="Nombre del autor"
                                        required
                                    />
                                </Field>

                                <Field label="Editorial" required>
                                    <Input
                                        value={formData.editorial}
                                        onChange={(e) => setFormData({ ...formData, editorial: e.target.value })}
                                        placeholder="Editorial"
                                        required
                                    />
                                </Field>

                                <Field label="Edición" required>
                                    <Input
                                        value={formData.edicion}
                                        onChange={(e) => setFormData({ ...formData, edicion: e.target.value })}
                                        placeholder="Primera, Segunda, etc."
                                        required
                                    />
                                </Field>

                                <Field label="Año de Edición" required>
                                    <Input
                                        type="number"
                                        value={formData.ano_edicion}
                                        onChange={(e) => setFormData({ ...formData, ano_edicion: parseInt(e.target.value) })}
                                        required
                                    />
                                </Field>

                                <Field label="Tipo" required>
                                    <Select.Root
                                        collection={documentTypes}
                                        value={[formData.tipo]}
                                        onValueChange={(e) => setFormData({ ...formData, tipo: e.value[0] as DocumentType })}
                                    >
                                        <Select.Trigger>
                                            <Select.ValueText placeholder="Seleccionar tipo" />
                                        </Select.Trigger>
                                        <Select.Content>
                                            {documentTypes.items.map((item) => (
                                                <Select.Item key={item.value} item={item}>
                                                    {item.label}
                                                </Select.Item>
                                            ))}
                                        </Select.Content>
                                    </Select.Root>
                                </Field>

                                <Field label="Categoría" required>
                                    <Input
                                        value={formData.categoria}
                                        onChange={(e) => setFormData({ ...formData, categoria: e.target.value })}
                                        placeholder="Novela, Ciencia, etc."
                                        required
                                    />
                                </Field>

                                <Field label="Tipo de Medio (opcional)">
                                    <Input
                                        value={formData.tipo_medio}
                                        onChange={(e) => setFormData({ ...formData, tipo_medio: e.target.value })}
                                        placeholder="DVD, CD, etc."
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
                            {document ? "Actualizar" : "Crear"}
                        </Button>
                    </Dialog.Footer>
                </Dialog.Content>
            </Dialog.Positioner>
        </Dialog.Root>
    );
}
