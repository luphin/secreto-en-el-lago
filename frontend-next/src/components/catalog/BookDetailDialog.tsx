"use client";

import {
    Dialog,
    Box,
    VStack,
    HStack,
    Text,
    Image,
    Tag,
    Heading,
} from "@chakra-ui/react";
import { LuMapPin, LuBook, LuCalendar, LuBuilding } from "react-icons/lu";

interface BookDetailDialogProps {
    isOpen: boolean;
    onClose: () => void;
    book: {
        title: string;
        author: string;
        imageUrl?: string;
        available: boolean;
        description?: string;
        location?: string;
        editorial?: string;
        year?: number;
        category?: string;
    };
}

export function BookDetailDialog({ isOpen, onClose, book }: BookDetailDialogProps) {
    return (
        <Dialog.Root open={isOpen} onOpenChange={(e) => !e.open && onClose()} size="lg">
            <Dialog.Backdrop />
            <Dialog.Positioner>
                <Dialog.Content maxW="800px">
                    <Dialog.Header>
                        <Dialog.Title>{book.title}</Dialog.Title>
                        <Dialog.CloseTrigger />
                    </Dialog.Header>

                    <Dialog.Body>
                        <HStack align="start" gap={6}>
                            {/* Imagen del libro */}
                            <Box
                                flexShrink={0}
                                w="250px"
                                h="350px"
                                bg="gray.200"
                                borderRadius="md"
                                overflow="hidden"
                                display="flex"
                                alignItems="center"
                                justifyContent="center"
                            >
                                {book.imageUrl ? (
                                    <Image
                                        src={book.imageUrl}
                                        alt={book.title}
                                        objectFit="cover"
                                        w="full"
                                        h="full"
                                    />
                                ) : (
                                    <Text color="gray.500">Sin imagen</Text>
                                )}
                            </Box>

                            {/* Información del libro */}
                            <VStack align="stretch" flex={1} gap={4}>
                                {/* Autor */}
                                <Box>
                                    <Text fontSize="sm" color="gray.600" mb={1}>
                                        Autor
                                    </Text>
                                    <Text fontSize="lg" fontWeight="semibold">
                                        {book.author}
                                    </Text>
                                </Box>

                                {/* Disponibilidad */}
                                <Box>
                                    <Text fontSize="sm" color="gray.600" mb={2}>
                                        Disponibilidad
                                    </Text>
                                    <Tag.Root
                                        size="lg"
                                        colorPalette={book.available ? "green" : "red"}
                                        variant="solid"
                                    >
                                        {book.available ? "Disponible" : "No disponible"}
                                    </Tag.Root>
                                </Box>

                                {/* Ubicación */}
                                {book.location && (
                                    <Box>
                                        <HStack gap={2} mb={1}>
                                            <LuMapPin size={16} />
                                            <Text fontSize="sm" color="gray.600">
                                                Ubicación
                                            </Text>
                                        </HStack>
                                        <Text>{book.location}</Text>
                                    </Box>
                                )}

                                {/* Editorial */}
                                {book.editorial && (
                                    <Box>
                                        <HStack gap={2} mb={1}>
                                            <LuBuilding size={16} />
                                            <Text fontSize="sm" color="gray.600">
                                                Editorial
                                            </Text>
                                        </HStack>
                                        <Text>{book.editorial}</Text>
                                    </Box>
                                )}

                                {/* Año */}
                                {book.year && (
                                    <Box>
                                        <HStack gap={2} mb={1}>
                                            <LuCalendar size={16} />
                                            <Text fontSize="sm" color="gray.600">
                                                Año de edición
                                            </Text>
                                        </HStack>
                                        <Text>{book.year}</Text>
                                    </Box>
                                )}

                                {/* Categoría */}
                                {book.category && (
                                    <Box>
                                        <HStack gap={2} mb={1}>
                                            <LuBook size={16} />
                                            <Text fontSize="sm" color="gray.600">
                                                Categoría
                                            </Text>
                                        </HStack>
                                        <Text>{book.category}</Text>
                                    </Box>
                                )}

                                {/* Descripción */}
                                {book.description && (
                                    <Box>
                                        <Text fontSize="sm" color="gray.600" mb={2}>
                                            Descripción
                                        </Text>
                                        <Text fontSize="sm" lineHeight="1.6">
                                            {book.description}
                                        </Text>
                                    </Box>
                                )}
                            </VStack>
                        </HStack>
                    </Dialog.Body>
                </Dialog.Content>
            </Dialog.Positioner>
        </Dialog.Root>
    );
}
