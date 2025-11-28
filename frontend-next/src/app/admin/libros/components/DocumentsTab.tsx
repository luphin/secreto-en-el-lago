"use client";

import { useState, useEffect } from "react";
import {
    Box,
    VStack,
    HStack,
    Input,
    Button,
    Table,
    Spinner,
    Card,
    Text,
    Badge,
    IconButton,
    Heading,
} from "@chakra-ui/react";
import { LuPlus, LuPencil, LuTrash2, LuSearch } from "react-icons/lu";
import { toaster } from "@/components/ui/toaster";
import DocumentService from "@/services/document.service";
import type { DocumentResponse } from "@/types/document.types";
import { DocumentFormDialog } from "./DocumentFormDialog";
import { DeleteConfirmDialog } from "./DeleteConfirmDialog";

export function DocumentsTab() {
    const [documents, setDocuments] = useState<DocumentResponse[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [isDeleteOpen, setIsDeleteOpen] = useState(false);
    const [selectedDocument, setSelectedDocument] = useState<DocumentResponse | null>(null);

    useEffect(() => {
        loadDocuments();
    }, []);

    const loadDocuments = async () => {
        setIsLoading(true);
        try {
            const data = await DocumentService.getDocuments({ limit: 100 });
            setDocuments(data);
        } catch (error) {
            console.error("Error loading documents:", error);
            toaster.create({
                title: "Error",
                description: "No se pudieron cargar los documentos",
                type: "error",
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleSearch = async () => {
        if (!searchTerm.trim()) {
            loadDocuments();
            return;
        }

        setIsLoading(true);
        try {
            const data = await DocumentService.getDocuments({ search: searchTerm });
            setDocuments(data);
        } catch (error) {
            console.error("Error searching documents:", error);
            toaster.create({
                title: "Error",
                description: "Error al buscar documentos",
                type: "error",
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreate = () => {
        setSelectedDocument(null);
        setIsFormOpen(true);
    };

    const handleEdit = (document: DocumentResponse) => {
        setSelectedDocument(document);
        setIsFormOpen(true);
    };

    const handleDeleteClick = (document: DocumentResponse) => {
        setSelectedDocument(document);
        setIsDeleteOpen(true);
    };

    const handleDeleteConfirm = async () => {
        if (!selectedDocument) return;

        try {
            await DocumentService.deleteDocument(selectedDocument._id);
            toaster.create({
                title: "Éxito",
                description: "Documento eliminado correctamente",
                type: "success",
            });
            loadDocuments();
        } catch (error: any) {
            console.error("Error deleting document:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo eliminar el documento",
                type: "error",
            });
        } finally {
            setIsDeleteOpen(false);
            setSelectedDocument(null);
        }
    };

    const handleFormSuccess = () => {
        setIsFormOpen(false);
        setSelectedDocument(null);
        loadDocuments();
    };

    const getTypeColor = (type: string) => {
        switch (type) {
            case "libro":
                return "blue";
            case "audio":
                return "purple";
            case "video":
                return "orange";
            default:
                return "gray";
        }
    };

    if (isLoading && documents.length === 0) {
        return (
            <Box textAlign="center" py={12}>
                <Spinner size="xl" color="purple.500" />
            </Box>
        );
    }

    return (
        <VStack align="stretch" gap={6}>
            {/* Header with search and create button */}
            <Card.Root p={4}>
                <HStack justify="space-between">
                    <HStack flex={1} maxW="600px">
                        <Input
                            placeholder="Buscar por título, autor o categoría..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
                        />
                        <Button onClick={handleSearch} colorPalette="purple">
                            <LuSearch />
                            Buscar
                        </Button>
                    </HStack>
                    <Button onClick={handleCreate} colorPalette="purple">
                        <LuPlus />
                        Nuevo Documento
                    </Button>
                </HStack>
            </Card.Root>

            {/* Documents table */}
            <Card.Root>
                {documents.length === 0 ? (
                    <Box textAlign="center" py={8}>
                        <Text color="gray.600">No se encontraron documentos</Text>
                    </Box>
                ) : (
                    <Table.Root variant="outline">
                        <Table.Header>
                            <Table.Row>
                                <Table.ColumnHeader>ID Físico</Table.ColumnHeader>
                                <Table.ColumnHeader>Título</Table.ColumnHeader>
                                <Table.ColumnHeader>Autor</Table.ColumnHeader>
                                <Table.ColumnHeader>Categoría</Table.ColumnHeader>
                                <Table.ColumnHeader>Tipo</Table.ColumnHeader>
                                <Table.ColumnHeader>Disponibles</Table.ColumnHeader>
                                <Table.ColumnHeader>Acciones</Table.ColumnHeader>
                            </Table.Row>
                        </Table.Header>
                        <Table.Body>
                            {documents.map((doc) => (
                                <Table.Row key={doc._id}>
                                    <Table.Cell fontWeight="semibold">{doc.id_fisico}</Table.Cell>
                                    <Table.Cell>{doc.titulo}</Table.Cell>
                                    <Table.Cell>{doc.autor}</Table.Cell>
                                    <Table.Cell>{doc.categoria}</Table.Cell>
                                    <Table.Cell>
                                        <Badge colorPalette={getTypeColor(doc.tipo)}>
                                            {doc.tipo}
                                        </Badge>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <Badge colorPalette={doc.items_disponibles > 0 ? "green" : "red"}>
                                            {doc.items_disponibles}
                                        </Badge>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <HStack gap={2}>
                                            <IconButton
                                                size="sm"
                                                onClick={() => handleEdit(doc)}
                                                aria-label="Editar"
                                                colorPalette="blue"
                                            >
                                                <LuPencil />
                                            </IconButton>
                                            <IconButton
                                                size="sm"
                                                onClick={() => handleDeleteClick(doc)}
                                                aria-label="Eliminar"
                                                colorPalette="red"
                                            >
                                                <LuTrash2 />
                                            </IconButton>
                                        </HStack>
                                    </Table.Cell>
                                </Table.Row>
                            ))}
                        </Table.Body>
                    </Table.Root>
                )}
            </Card.Root>

            {/* Form Dialog */}
            <DocumentFormDialog
                isOpen={isFormOpen}
                onClose={() => {
                    setIsFormOpen(false);
                    setSelectedDocument(null);
                }}
                document={selectedDocument}
                onSuccess={handleFormSuccess}
            />

            {/* Delete Confirmation Dialog */}
            <DeleteConfirmDialog
                isOpen={isDeleteOpen}
                onClose={() => {
                    setIsDeleteOpen(false);
                    setSelectedDocument(null);
                }}
                onConfirm={handleDeleteConfirm}
                title="Eliminar Documento"
                message={`¿Está seguro que desea eliminar el documento "${selectedDocument?.titulo}"?`}
            />
        </VStack>
    );
}
