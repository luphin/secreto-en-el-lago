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
} from "@chakra-ui/react";
import { LuPlus, LuPencil, LuTrash2, LuSearch, LuBookOpen } from "react-icons/lu";
import { toaster } from "@/components/ui/toaster";
import ItemService from "@/services/item.service";
import DocumentService from "@/services/document.service";
import type { ItemResponse } from "@/types/item.types";
import type { DocumentResponse } from "@/types/document.types";
import { ItemFormDialog } from "./ItemFormDialog";
import { DeleteConfirmDialog } from "./DeleteConfirmDialog";
import { QuickLoanDialog } from "./QuickLoanDialog";
import { ItemStatus } from "@/types/item.types";

interface ItemsTabProps {
    isActive: boolean;
}

export function ItemsTab({ isActive }: ItemsTabProps) {
    const [items, setItems] = useState<ItemResponse[]>([]);
    const [documents, setDocuments] = useState<Map<string, DocumentResponse>>(new Map());
    const [isLoading, setIsLoading] = useState(true);
    const [searchDocId, setSearchDocId] = useState("");
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [isDeleteOpen, setIsDeleteOpen] = useState(false);
    const [isQuickLoanOpen, setIsQuickLoanOpen] = useState(false);
    const [selectedItem, setSelectedItem] = useState<ItemResponse | null>(null);
    const [selectedItemForLoan, setSelectedItemForLoan] = useState<string>("");

    useEffect(() => {
        if (isActive && items.length === 0) {
            loadItems();
        }
    }, [isActive]);

    const loadItems = async () => {
        setIsLoading(true);
        try {
            const data = await ItemService.getItems({ limit: 100 });
            setItems(data);

            // Load document info for each item
            const docMap = new Map<string, DocumentResponse>();
            for (const item of data) {
                if (!docMap.has(item.document_id)) {
                    try {
                        const doc = await DocumentService.getDocumentById(item.document_id);
                        docMap.set(item.document_id, doc);
                    } catch (error) {
                        console.error(`Error loading document ${item.document_id}:`, error);
                    }
                }
            }
            setDocuments(docMap);
        } catch (error) {
            console.error("Error loading items:", error);
            toaster.create({
                title: "Error",
                description: "No se pudieron cargar los ejemplares",
                type: "error",
            });
        } finally {
            setIsLoading(false);
        }
    };

    // Filtrar ejemplares localmente por ID físico, ubicación o ID de documento
    const filteredItems = searchDocId.trim() === ""
        ? items
        : items.filter(item => {
            const doc = documents.get(item.document_id);
            const searchLower = searchDocId.toLowerCase();
            return (
                item.document_id.toLowerCase().includes(searchLower) ||
                item.ubicacion.toLowerCase().includes(searchLower) ||
                doc?.id_fisico.toLowerCase().includes(searchLower)
            );
        });

    const handleCreate = () => {
        setSelectedItem(null);
        setIsFormOpen(true);
    };

    const handleEdit = (item: ItemResponse) => {
        setSelectedItem(item);
        setIsFormOpen(true);
    };

    const handleDeleteClick = (item: ItemResponse) => {
        setSelectedItem(item);
        setIsDeleteOpen(true);
    };

    const handleDeleteConfirm = async () => {
        if (!selectedItem) return;

        try {
            await ItemService.deleteItem(selectedItem._id);
            toaster.create({
                title: "Éxito",
                description: "Ejemplar eliminado correctamente",
                type: "success",
            });
            loadItems();
        } catch (error: any) {
            console.error("Error deleting item:", error);
            toaster.create({
                title: "Error",
                description: error.response?.data?.detail || "No se pudo eliminar el ejemplar",
                type: "error",
            });
        } finally {
            setIsDeleteOpen(false);
            setSelectedItem(null);
        }
    };

    const handleLoanClick = (item: ItemResponse) => {
        setSelectedItemForLoan(item._id);
        setIsQuickLoanOpen(true);
    };

    const handleLoanSuccess = () => {
        setIsQuickLoanOpen(false);
        setSelectedItemForLoan("");
        loadItems();
    };

    const handleFormSuccess = () => {
        setIsFormOpen(false);
        setSelectedItem(null);
        loadItems();
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case "disponible":
                return "green";
            case "prestado":
                return "blue";
            case "en_restauracion":
                return "orange";
            case "reservado":
                return "purple";
            default:
                return "gray";
        }
    };

    if (isLoading && items.length === 0) {
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
                            placeholder="Buscar por ID físico, ubicación o ID de documento..."
                            value={searchDocId}
                            onChange={(e) => setSearchDocId(e.target.value)}
                        />
                    </HStack>
                    <Button onClick={handleCreate} colorPalette="purple">
                        <LuPlus />
                        Nuevo Ejemplar
                    </Button>
                </HStack>
            </Card.Root>

            {/* Items table */}
            <Card.Root>
                {filteredItems.length === 0 ? (
                    <Box textAlign="center" py={8}>
                        <Text color="gray.600">No se encontraron ejemplares</Text>
                    </Box>
                ) : (
                    <Table.Root variant="outline">
                        <Table.Header>
                            <Table.Row>
                                <Table.ColumnHeader>Id</Table.ColumnHeader>
                                <Table.ColumnHeader>Documento</Table.ColumnHeader>
                                <Table.ColumnHeader>Ubicación</Table.ColumnHeader>
                                <Table.ColumnHeader>Estado</Table.ColumnHeader>
                                <Table.ColumnHeader>Acciones</Table.ColumnHeader>
                            </Table.Row>
                        </Table.Header>
                        <Table.Body>
                            {filteredItems.map((item) => {
                                const doc = documents.get(item.document_id);
                                return (
                                    <Table.Row key={item._id}>
                                        <Table.Cell>{item._id}</Table.Cell>
                                        <Table.Cell>
                                            {doc ? (
                                                <Box>
                                                    <Text fontWeight="semibold">{doc.titulo}</Text>
                                                    <Text fontSize="sm" color="gray.600">{doc.autor}</Text>
                                                </Box>
                                            ) : (
                                                <Text color="gray.500">ID: {item.document_id}</Text>
                                            )}
                                        </Table.Cell>
                                        <Table.Cell>{item.ubicacion}</Table.Cell>
                                        <Table.Cell>
                                            <Badge colorPalette={getStatusColor(item.estado)}>
                                                {item.estado.replace("_", " ")}
                                            </Badge>
                                        </Table.Cell>
                                        <Table.Cell>
                                            <HStack gap={2}>
                                                {item.estado === ItemStatus.DISPONIBLE && (
                                                    <IconButton
                                                        size="sm"
                                                        onClick={() => handleLoanClick(item)}
                                                        aria-label="Prestar"
                                                        colorPalette="green"
                                                    >
                                                        <LuBookOpen />
                                                    </IconButton>
                                                )}
                                                <IconButton
                                                    size="sm"
                                                    onClick={() => handleEdit(item)}
                                                    aria-label="Editar"
                                                    colorPalette="blue"
                                                >
                                                    <LuPencil />
                                                </IconButton>
                                                <IconButton
                                                    size="sm"
                                                    onClick={() => handleDeleteClick(item)}
                                                    aria-label="Eliminar"
                                                    colorPalette="red"
                                                >
                                                    <LuTrash2 />
                                                </IconButton>
                                            </HStack>
                                        </Table.Cell>
                                    </Table.Row>
                                );
                            })}
                        </Table.Body>
                    </Table.Root>
                )}
            </Card.Root>

            {/* Form Dialog */}
            <ItemFormDialog
                isOpen={isFormOpen}
                onClose={() => {
                    setIsFormOpen(false);
                    setSelectedItem(null);
                }}
                item={selectedItem}
                onSuccess={handleFormSuccess}
            />

            {/* Delete Confirmation Dialog */}
            <DeleteConfirmDialog
                isOpen={isDeleteOpen}
                onClose={() => {
                    setIsDeleteOpen(false);
                    setSelectedItem(null);
                }}
                onConfirm={handleDeleteConfirm}
                title="Eliminar Ejemplar"
                message="¿Está seguro que desea eliminar este ejemplar?"
            />

            {/* Quick Loan Dialog */}
            <QuickLoanDialog
                isOpen={isQuickLoanOpen}
                onClose={() => {
                    setIsQuickLoanOpen(false);
                    setSelectedItemForLoan("");
                }}
                itemId={selectedItemForLoan}
                onSuccess={handleLoanSuccess}
            />
        </VStack>
    );
}
