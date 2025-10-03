# E-commerce Dashboard Components

This directory contains Vue.js components for the AgriERP E-commerce Dashboard.

## Components

### InventoryAlerts.vue
A component that displays inventory alerts for products with low stock or out of stock status.

**Features:**
- Real-time inventory monitoring
- Color-coded alerts (red for out of stock, yellow for low stock)
- Expandable lists for better UX
- Direct navigation to inventory management
- Loading states and error handling

**Props:**
- None (self-contained component)

**Exposed Methods:**
- `refresh()` - Manually refresh inventory alerts

**Usage:**
```vue
<template>
  <InventoryAlerts ref="inventoryRef" />
</template>

<script setup>
import InventoryAlerts from '@/components/ecommerce/InventoryAlerts.vue';

const inventoryRef = ref(null);

// Manually refresh alerts
const refreshAlerts = () => {
  inventoryRef.value?.refresh();
};
</script>
```

## API Integration

The components integrate with the following backend endpoints:

- `GET /api/v1/ecommerce/statistics/general` - General statistics
- `GET /api/v1/ecommerce/statistics/sales` - Sales data for charts
- `GET /api/v1/ecommerce/statistics/order-status` - Order status distribution
- `GET /api/v1/ecommerce/statistics/recent-orders` - Recent orders list
- `GET /api/v1/ecommerce/statistics/top-products` - Top selling products
- `GET /api/v1/ecommerce/statistics/inventory-alerts` - Inventory alerts

## Styling

Components use:
- Tailwind CSS for utility classes
- Element Plus components and theming
- Custom CSS for animations and transitions
- Responsive design patterns

## Internationalization

All text content supports i18n through Vue I18n:
- English translations in `locales/en.ts`
- Vietnamese translations can be added to `locales/vi.ts`
- Use `t('translation_key')` for all user-facing text

## Error Handling

Components include:
- Graceful API error handling
- Fallback to mock data when API fails
- Loading states during data fetching
- Empty states when no data available

