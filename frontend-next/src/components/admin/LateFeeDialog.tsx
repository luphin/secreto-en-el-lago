"use client";

import { useState } from "react";
import {
    Dialog,
    VStack,
    HStack,
    Input,
    Button,
    Text,
    Box,
    Badge,
    Separator,
} from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { toaster } from "@/components/ui/toaster";
import { LuCircleAlert, LuDollarSign, LuCreditCard, LuBanknote } from "react-icons/lu";

interface LateFeeDialogProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: () => void;
    loanId: string;
    daysLate: number;
    feeAmount: number;
}

const PAYMENT_METHODS = [
    { value: "efectivo", label: "Efectivo", icon: LuBanknote },
    { value: "tarjeta", label: "Tarjeta", icon: LuCreditCard },
];

export function LateFeeDialog({
    isOpen,
    onClose,
    onConfirm,
    loanId,
    daysLate,
    feeAmount
}: LateFeeDialogProps) {
    const [paymentMethod, setPaymentMethod] = useState<string>("");
    const [amountReceived, setAmountReceived] = useState<string>("");
    const [isProcessing, setIsProcessing] = useState(false);

    const handlePayment = async () => {
        if (!paymentMethod) {
            toaster.create({
                title: "Error",
                description: "Por favor selecciona un método de pago",
                type: "error",
            });
            return;
        }

        if (paymentMethod === "efectivo") {
            const received = parseFloat(amountReceived);
            if (isNaN(received) || received < feeAmount) {
                toaster.create({
                    title: "Error",
                    description: `El monto recibido debe ser al menos $${feeAmount.toLocaleString('es-CL')}`,
                    type: "error",
                });
                return;
            }
        }

        setIsProcessing(true);

        // Simular procesamiento de pago
        setTimeout(() => {
            const change = paymentMethod === "efectivo"
                ? parseFloat(amountReceived) - feeAmount
                : 0;

            toaster.create({
                title: "¡Pago procesado exitosamente!",
                description: paymentMethod === "efectivo" && change > 0
                    ? `Vuelto: $${change.toLocaleString('es-CL')}`
                    : `Multa de $${feeAmount.toLocaleString('es-CL')} pagada con ${paymentMethod}`,
                type: "success",
                duration: 5000,
            });

            setIsProcessing(false);
            onConfirm();
        }, 1500);
    };

    const handleClose = () => {
        setPaymentMethod("");
        setAmountReceived("");
        onClose();
    };

    const change = paymentMethod === "efectivo" && amountReceived
        ? Math.max(0, parseFloat(amountReceived) - feeAmount)
        : 0;

    return (
        <Dialog.Root open={isOpen} onOpenChange={(e) => !e.open && handleClose()} size="lg">
            <Dialog.Backdrop />
            <Dialog.Positioner>
                <Dialog.Content>
                    <Dialog.Header>
                        <Dialog.Title>
                            <HStack>
                                <LuCircleAlert color="red" />
                                <Text>Multa por Atraso en Devolución</Text>
                            </HStack>
                        </Dialog.Title>
                    </Dialog.Header>

                    <Dialog.Body>
                        <VStack align="stretch" gap={6}>
                            {/* Información de la multa */}
                            <Box p={4} bg="red.50" borderRadius="md" borderWidth="1px" borderColor="red.200">
                                <VStack align="stretch" gap={2}>
                                    <HStack justify="space-between">
                                        <Text fontWeight="semibold" color="red.700">
                                            Días de atraso:
                                        </Text>
                                        <Badge colorPalette="red" size="lg">
                                            {daysLate} {daysLate === 1 ? 'día' : 'días'}
                                        </Badge>
                                    </HStack>
                                    <HStack justify="space-between">
                                        <Text fontWeight="semibold" color="red.700">
                                            Tarifa por día:
                                        </Text>
                                        <Text fontWeight="bold">$500</Text>
                                    </HStack>
                                    <Separator />
                                    <HStack justify="space-between">
                                        <Text fontSize="lg" fontWeight="bold" color="red.700">
                                            Total a pagar:
                                        </Text>
                                        <HStack>
                                            <LuDollarSign size={24} color="red" />
                                            <Text fontSize="2xl" fontWeight="bold" color="red.600">
                                                ${feeAmount.toLocaleString('es-CL')}
                                            </Text>
                                        </HStack>
                                    </HStack>
                                </VStack>
                            </Box>

                            {/* Método de pago */}
                            <Field label="Método de Pago" required>
                                <VStack align="stretch" gap={2}>
                                    {PAYMENT_METHODS.map((method) => {
                                        const Icon = method.icon;
                                        return (
                                            <Button
                                                key={method.value}
                                                variant={paymentMethod === method.value ? "solid" : "outline"}
                                                colorPalette={paymentMethod === method.value ? "blue" : "gray"}
                                                onClick={() => setPaymentMethod(method.value)}
                                                size="lg"
                                                justifyContent="start"
                                            >
                                                <HStack>
                                                    <Icon size={20} />
                                                    <Text>{method.label}</Text>
                                                </HStack>
                                            </Button>
                                        );
                                    })}
                                </VStack>
                            </Field>

                            {/* Campo de monto recibido (solo para efectivo) */}
                            {paymentMethod === "efectivo" && (
                                <Field label="Monto Recibido" required>
                                    <Input
                                        type="number"
                                        value={amountReceived}
                                        onChange={(e) => setAmountReceived(e.target.value)}
                                        placeholder="Ingrese el monto recibido"
                                        min={feeAmount}
                                    />
                                    {change > 0 && (
                                        <Box mt={2} p={2} bg="green.50" borderRadius="md">
                                            <Text fontSize="sm" color="green.700" fontWeight="semibold">
                                                Vuelto: ${change.toLocaleString('es-CL')}
                                            </Text>
                                        </Box>
                                    )}
                                </Field>
                            )}

                            {/* Simulación de tarjeta */}
                            {paymentMethod === "tarjeta" && (
                                <Box p={4} bg="blue.50" borderRadius="md" borderWidth="1px" borderColor="blue.200">
                                    <VStack align="center" gap={2}>
                                        <LuCreditCard size={48} color="blue" />
                                        <Text fontSize="sm" color="blue.700" textAlign="center">
                                            Simulación: Pase la tarjeta por el lector
                                        </Text>
                                        <Text fontSize="xs" color="gray.600" textAlign="center">
                                            (En producción, aquí se integraría con el terminal de pago)
                                        </Text>
                                    </VStack>
                                </Box>
                            )}
                        </VStack>
                    </Dialog.Body>

                    <Dialog.Footer>
                        <Dialog.CloseTrigger asChild>
                            <Button variant="outline" onClick={handleClose} disabled={isProcessing}>
                                Cancelar
                            </Button>
                        </Dialog.CloseTrigger>
                        <Button
                            colorPalette="green"
                            onClick={handlePayment}
                            loading={isProcessing}
                            disabled={!paymentMethod}
                        >
                            {isProcessing ? "Procesando..." : "Confirmar Pago"}
                        </Button>
                    </Dialog.Footer>
                </Dialog.Content>
            </Dialog.Positioner>
        </Dialog.Root>
    );
}
