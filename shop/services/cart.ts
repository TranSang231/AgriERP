import { useApi } from "./api";

export interface CartItem {
  id: number;
  product: {
    id: number;
    name: string;
    price: number;
    sale_price?: number;
    image: string;
    stock: number;
  };
  quantity: number;
  created_at: string;
}

export interface Cart {
  id: number;
  items: CartItem[];
  total_amount: number;
  total_items: number;
}

export interface AddToCartData {
  product_id: number;
  quantity: number;
}

export function useCartService() {
  const { request } = useApi();

  const getCart = () => {
    return request<Cart>("/carts");
  };

  const addToCart = (data: AddToCartData) => {
    return request<CartItem>("/carts", {
      method: "POST",
      body: data,
    });
  };

  const updateCartItem = (itemId: number, quantity: number) => {
    return request<CartItem>(`/carts/${itemId}`, {
      method: "PATCH",
      body: { quantity },
    });
  };

  const removeFromCart = (itemId: number) => {
    return request(`/carts/${itemId}`, {
      method: "DELETE",
    });
  };

  const clearCart = () => {
    return request("/carts/clear", {
      method: "POST",
    });
  };

  return {
    getCart,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
  };
}
