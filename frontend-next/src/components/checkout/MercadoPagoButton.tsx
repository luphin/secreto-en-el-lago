"use client";
import { initMercadoPago, Wallet } from '@mercadopago/sdk-react';
import { useState } from 'react';
import { PaymentService, PaymentItem } from '@/services/payment.service';
import { Button, Box, HStack, Text, Spinner } from '@chakra-ui/react';
import { LuCreditCard, LuShieldCheck } from 'react-icons/lu';

// Inicializar Mercado Pago
const PUBLIC_KEY = process.env.NEXT_PUBLIC_MP_PUBLIC_KEY || "TEST-00000000-0000-0000-0000-000000000000";

initMercadoPago(PUBLIC_KEY, {
    locale: 'es-CL'
});

interface MercadoPagoButtonProps {
    items: PaymentItem[];
    userEmail: string;
    buttonText?: string;
}

export default function MercadoPagoButton({ items, userEmail, buttonText = "Pagar con Mercado Pago" }: MercadoPagoButtonProps) {
    const [preferenceId, setPreferenceId] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleBuy = async () => {
        setIsLoading(true);
        try {
            const data = await PaymentService.createPreference(items, userEmail);
            setPreferenceId(data.preferenceId);
        } catch (error) {
            console.error("Error al crear preferencia de pago:", error);
            alert("Hubo un error al iniciar el pago. Por favor intenta nuevamente.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box width="100%">
            {!preferenceId ? (
                <Button
                    onClick={handleBuy}
                    disabled={isLoading}
                    width="100%"
                    size="lg"
                    colorPalette="blue"
                    variant="solid"
                    _hover={{
                        transform: "translateY(-2px)",
                        shadow: "lg",
                    }}
                    transition="all 0.2s"
                >
                    {isLoading ? (
                        <HStack gap={2}>
                            <Spinner size="sm" />
                            <Text>Procesando...</Text>
                        </HStack>
                    ) : (
                        <HStack gap={2}>
                            <LuCreditCard size={20} />
                            <Text fontWeight="semibold">{buttonText}</Text>
                        </HStack>
                    )}
                </Button>
            ) : (
                <Box mt={4}>
                    <Box
                        p={4}
                        bg="blue.50"
                        borderRadius="md"
                        borderWidth="1px"
                        borderColor="blue.200"
                        mb={3}
                    >
                        <HStack gap={2} justify="center">
                            <LuShieldCheck color="var(--chakra-colors-blue-600)" size={18} />
                            <Text fontSize="sm" color="blue.700" fontWeight="medium">
                                Pago seguro con Mercado Pago
                            </Text>
                        </HStack>
                    </Box>
                    <Wallet
                        initialization={{ preferenceId: preferenceId }}
                    />
                </Box>
            )}
        </Box>
    );
}
