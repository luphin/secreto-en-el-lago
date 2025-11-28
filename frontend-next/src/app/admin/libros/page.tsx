"use client";

import { useState } from "react";
import { Box, Container, VStack, Heading, Tabs } from "@chakra-ui/react";
import { AdminNav } from "@/components/admin/AdminNav";
import { DocumentsTab } from "./components/DocumentsTab";
import { ItemsTab } from "./components/ItemsTab";
import { LoansTab } from "./components/LoansTab";
import { ReservationsTab } from "./components/ReservationsTab";

export default function AdminLibrosPage() {
    const [activeTab, setActiveTab] = useState("documents");

    return (
        <Box minH="100vh" bg="bg.canvas">
            <AdminNav />

            <Container maxW="container.xl" py={8}>
                <VStack align="stretch" gap={6}>
                    <Heading size="2xl">Gestión de Libros</Heading>

                    <Tabs.Root
                        value={activeTab}
                        onValueChange={(e) => setActiveTab(e.value)}
                        variant="enclosed"
                        colorPalette="purple"
                    >
                        <Tabs.List>
                            <Tabs.Trigger value="documents">Documentos</Tabs.Trigger>
                            <Tabs.Trigger value="items">Ejemplares</Tabs.Trigger>
                            <Tabs.Trigger value="loans">Préstamos</Tabs.Trigger>
                            <Tabs.Trigger value="reservations">Reservas</Tabs.Trigger>
                        </Tabs.List>

                        <Tabs.Content value="documents">
                            <DocumentsTab />
                        </Tabs.Content>

                        <Tabs.Content value="items">
                            <ItemsTab />
                        </Tabs.Content>

                        <Tabs.Content value="loans">
                            <LoansTab />
                        </Tabs.Content>

                        <Tabs.Content value="reservations">
                            <ReservationsTab />
                        </Tabs.Content>
                    </Tabs.Root>
                </VStack>
            </Container>
        </Box>
    );
}
