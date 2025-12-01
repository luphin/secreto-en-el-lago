"use client";

import MercadoPagoButton from '@/components/checkout/MercadoPagoButton';
import { useState } from 'react';

export default function TestPaymentPage() {
  const [email, setEmail] = useState("test_user_123456@testuser.com");
  
  // Items de prueba
  const items = [
    {
      title: "Libro: Secreto en el Lago (Edición Especial)",
      quantity: 1,
      unit_price: 15000
    },
    {
      title: "Marcapáginas coleccionable",
      quantity: 2,
      unit_price: 2500
    }
  ];

  const total = items.reduce((acc, item) => acc + (item.unit_price * item.quantity), 0);

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Prueba de Integración Mercado Pago</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Resumen de Compra */}
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <h2 className="text-xl font-semibold mb-4">Resumen del Pedido</h2>
          <div className="space-y-4">
            {items.map((item, index) => (
              <div key={index} className="flex justify-between border-b pb-2">
                <div>
                  <p className="font-medium">{item.title}</p>
                  <p className="text-sm text-gray-500">Cant: {item.quantity}</p>
                </div>
                <p>${(item.unit_price * item.quantity).toLocaleString('es-CL')}</p>
              </div>
            ))}
            
            <div className="flex justify-between pt-2 font-bold text-lg">
              <span>Total</span>
              <span>${total.toLocaleString('es-CL')}</span>
            </div>
          </div>
        </div>

        {/* Configuración y Pago */}
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <h2 className="text-xl font-semibold mb-4">Datos del Comprador</h2>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email del Pagador (Test User)
            </label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="email@ejemplo.com"
            />
            <p className="text-xs text-gray-500 mt-1">
              Usa un email de prueba de Sandbox de Mercado Pago para probar.
            </p>
          </div>

          <div className="mt-6">
            <MercadoPagoButton 
              items={items} 
              userEmail={email} 
              buttonText="Pagar Ahora"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
