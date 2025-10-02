import { defineStore } from "pinia";

type Promotion = {
  id: number;
  type?: string;
  discount?: number;
  promotion_items?: Array<{
    product_id: number;
    discount: number;
  }>;
};

export const usePromotionsStore = defineStore("promotions", {
  state: () => ({
    productIdToDiscountPercent: {} as Record<number, number>,
    loadedAt: null as Date | null,
    isLoading: false as boolean,
  }),
  actions: {
    /**
     * Derive highest product-level discount percent from a product object's embedded promotions
     */
    getDiscountPercentFromProductObject(product: any): number {
      try {
        if (!product || !Array.isArray((product as any).promotions)) return 0;
        const nowMs = Date.now();
        const productId = (product as any)?.id;
        let maxPercent = 0;
        for (const promo of (product as any).promotions as any[]) {
          if (!promo) continue;
          const type = (promo as any)?.type || "discount";
          if (type !== "discount") continue;
          const start = (promo as any)?.start;
          const end = (promo as any)?.end;
          const startMs = start ? Date.parse(start) : NaN;
          const endMs = end ? Date.parse(end) : NaN;
          // active if now in [start, end]
          if (Number.isFinite(startMs) && nowMs < startMs) continue;
          if (Number.isFinite(endMs) && nowMs > endMs) continue;
          const items = Array.isArray((promo as any)?.promotion_items)
            ? (promo as any).promotion_items
            : [];
          for (const item of items) {
            const pid = (item as any)?.product_id;
            if (!pid || !productId || String(pid) !== String(productId)) continue;
            const d = Number((item as any)?.discount) || 0;
            if (d > maxPercent) maxPercent = d;
          }
        }
        return maxPercent;
      } catch (_) {
        return 0;
      }
    },
    async loadActiveDiscounts() {
      if (this.isLoading) return;
      this.isLoading = true;
      try {
        const now = new Date().toISOString();
        const query = new URLSearchParams({
          "start__lte": now,
          "end__gte": now,
          // fetch all active promotions; server will return both types
          // we'll only use product-level discounts
        });
        const res = await fetch(`/api/ecommerce/promotions?${query.toString()}`);
        if (!res.ok) return;
        const data: Promotion[] = await res.json();
        const map: Record<number, number> = {};
        for (const promo of data) {
          if (promo.type && promo.type !== "discount") continue;
          const items = promo.promotion_items || [];
          for (const item of items) {
            const current = map[item.product_id] ?? 0;
            if (item.discount > current) map[item.product_id] = item.discount;
          }
        }
        this.productIdToDiscountPercent = map;
        this.loadedAt = new Date();
      } catch (e) {
        // swallow errors for storefront
      } finally {
        this.isLoading = false;
      }
    },
    getProductDiscountPercent(productId: number): number {
      return this.productIdToDiscountPercent[productId] ?? 0;
    },
  },
});


