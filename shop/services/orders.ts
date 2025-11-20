import { useApi } from "./api";

export interface OrderItem {
  id?: string;
  order_id?: string;
  product_id: string;
  product_name: string;
  unit: string;
  quantity: number;
  price: number;
  amount: number;
  created_at?: string;
  updated_at?: string;
}

export interface Order {
  id?: string;
  customer_id?: string;
  customer_name: string;
  company_name?: string;
  tax_code?: string;
  payment_method: number; // 0 = BANK_TRANSFER, 1 = CASH_ON_DELIVERY
  payment_status?: number;
  account_number?: string;
  vat_rate: number;
  shipping_fee: number;
  shipping_status?: number;
  order_status?: number;
  date: string;
  items: OrderItem[];
  created_at?: string;
  updated_at?: string;
}

export interface CreateOrderData {
  customer_id?: string;
  customer_name: string;
  company_name?: string;
  tax_code?: string;
  payment_method: number;
  account_number?: string;
  vat_rate: number;
  shipping_fee: number;
  date: string;
  items: {
    product_id: number;
    product_name: string;
    unit: string;
    quantity: number;
    price: number;
    amount: number;
  }[];
}

export function useOrderService() {
  const { request } = useApi();

  const createOrder = (orderData: CreateOrderData) => {
    return request<Order>("/orders", {
      method: "POST",
      body: orderData,
    });
  };

  const getOrders = (params?: any) => {
    return request<Order[]>("/orders", {
      method: 'GET',
      params,
    });
  };

  const getOrder = (orderId: string) => {
    return request<Order>(`/orders/${orderId}`, {
      method: 'GET'
    });
  };

  return {
    createOrder,
    getOrders,
    getOrder,
  };
}
