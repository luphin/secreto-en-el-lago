"use client";
import { initMercadoPago, Wallet } from '@mercadopago/sdk-react';
import { useState } from 'react';
import { PaymentService, PaymentItem } from '@/services/payment.service';

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
        <div className="payment-container">
            {!preferenceId ? (
                <button 
                    onClick={handleBuy}
                    disabled={isLoading}
                    className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    {isLoading ? "Procesando..." : buttonText}
                </button>
            ) : (
                <div className="mt-4">
                    <Wallet initialization={{ preferenceId: preferenceId }} customization={{ texts: { valueProp: 'smart_option' } }} />
                </div>
            )}
        </div>
    );
}
