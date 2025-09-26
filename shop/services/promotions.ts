import { useApi } from "./api";

export interface PromotionItem {
  id: string;
  product_id: string;
  product: {
    id: string;
    name: any;
    price: number;
  };
  quantity_limit: number;
  quantity_limit_by_customer: number;
  discount: number;
}

export interface Promotion {
  id: string;
  name: string;
  start: string;
  end: string;
  promotion_items: PromotionItem[];
  created_at: string;
  updated_at: string;
}

export function usePromotionService() {
  const { request } = useApi();

  const getPromotions = () => {
    return request<Promotion[]>("/promotions");
  };

  const getActivePromotions = () => {
    const now = new Date().toISOString();
    return request<Promotion[]>(`/promotions?start__lte=${now}&end__gte=${now}`);
  };

  const validatePromotion = (promotionId: string, productIds: string[], quantities: number[]) => {
    return request<{ valid: boolean; discount: number; message?: string }>("/promotions/validate", {
      method: "POST",
      body: {
        promotion_id: promotionId,
        product_ids: productIds,
        quantities: quantities
      }
    });
  };

  return {
    getPromotions,
    getActivePromotions,
    validatePromotion,
  };
}
