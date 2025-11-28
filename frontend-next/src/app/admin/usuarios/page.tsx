"use client";

import { useState, useEffect } from "react";
import {
    Box,
    Container,
    VStack,
    Heading,
    Table,
    Spinner,
    Card,
    Text,
    Badge,
} from "@chakra-ui/react";
import { AdminNav } from "@/components/admin/AdminNav";
import { toaster } from "@/components/ui/toaster";
import UserService from "@/services/user.service";
import type { UserResponse } from "@/types/auth.types";
import { UserRole } from "@/types/auth.types";

export default function AdminUsuariosPage() {
    const [users, setUsers] = useState<UserResponse[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadUsers();
    }, []);

    const loadUsers = async () => {
        setIsLoading(true);
        try {
            const data = await UserService.getUsers(0, 100, UserRole.LECTOR);
            setUsers(data);
        } catch (error) {
            console.error("Error loading users:", error);
            toaster.create({
                title: "Error",
                description: "No se pudieron cargar los usuarios",
                type: "error",
            });
        } finally {
            setIsLoading(false);
        }
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("es-ES", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    };

    if (isLoading && users.length === 0) {
        return (
            <Box minH="100vh" bg="bg.canvas">
                <AdminNav />
                <Box textAlign="center" py={12}>
                    <Spinner size="xl" color="purple.500" />
                </Box>
            </Box>
        );
    }

    return (
        <Box minH="100vh" bg="bg.canvas">
            <AdminNav />

            <Container maxW="container.xl" py={8}>
                <VStack align="stretch" gap={6}>
                    <Heading size="2xl">Gestión de Usuarios</Heading>

                    <Card.Root>
                        {users.length === 0 ? (
                            <Box textAlign="center" py={8}>
                                <Text color="gray.600">No se encontraron usuarios</Text>
                            </Box>
                        ) : (
                            <Table.Root variant="outline">
                                <Table.Header>
                                    <Table.Row>
                                        <Table.ColumnHeader>ID</Table.ColumnHeader>
                                        <Table.ColumnHeader>RUT</Table.ColumnHeader>
                                        <Table.ColumnHeader>Nombres</Table.ColumnHeader>
                                        <Table.ColumnHeader>Apellidos</Table.ColumnHeader>
                                        <Table.ColumnHeader>Email</Table.ColumnHeader>
                                        <Table.ColumnHeader>Teléfono</Table.ColumnHeader>
                                        <Table.ColumnHeader>Estado</Table.ColumnHeader>
                                    </Table.Row>
                                </Table.Header>
                                <Table.Body>
                                    {users.map((user) => (
                                        <Table.Row key={user._id}>
                                            <Table.Cell>{user._id}</Table.Cell>
                                            <Table.Cell fontFamily="mono">{user.rut}</Table.Cell>
                                            <Table.Cell>{user.nombres}</Table.Cell>
                                            <Table.Cell>{user.apellidos}</Table.Cell>
                                            <Table.Cell>{user.email}</Table.Cell>
                                            <Table.Cell>{user.telefono}</Table.Cell>
                                            <Table.Cell>
                                                <Badge colorPalette={user.activo ? "green" : "red"}>
                                                    {user.activo ? "Activo" : "Inactivo"}
                                                </Badge>
                                            </Table.Cell>
                                        </Table.Row>
                                    ))}
                                </Table.Body>
                            </Table.Root>
                        )}
                    </Card.Root>
                </VStack>
            </Container>
        </Box>
    );
}
