import apiClient from "@/lib/api";

export interface PaymentItem {
  title: string;
  quantity: number;
  unit_price: number;
  currency_id?: string;
}

export interface PaymentPreferenceResponse {
  preferenceId: string;
  init_point: string;
  sandbox_init_point: string;
}

export const PaymentService = {
  createPreference: async (items: PaymentItem[], email: string) => {
    const response = await apiClient.post<PaymentPreferenceResponse>("/payments/create_preference", {
      items,
      email
    });
    return response.data;
  }
};
