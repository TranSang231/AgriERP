# Hướng dẫn sử dụng hệ thống đa ngôn ngữ trong Shop

## Tổng quan

Hệ thống đa ngôn ngữ trong shop được thiết kế để tự động xử lý việc hiển thị nội dung theo ngôn ngữ người dùng chọn, với fallback về ngôn ngữ gốc (origin) khi không có bản dịch.

## Cấu trúc dữ liệu

### Backend trả về
```typescript
{
  "origin": "Nội dung gốc",
  "translates": [
    {
      "language": "vi",
      "value": "Nội dung tiếng Việt"
    },
    {
      "language": "en", 
      "value": "English content"
    }
  ]
}
```

### Frontend xử lý
- **Tự động chọn ngôn ngữ** dựa trên `Accept-Language` header
- **Fallback logic**: Nếu không có bản dịch → dùng `origin`
- **Không cần lo lắng** về việc chọn `origin` hay `translates.value`

## Cách sử dụng

### 1. Sử dụng Composable (Khuyến nghị)

```vue
<template>
  <div>
    <h1>{{ localize(product.name) }}</h1>
    <p>{{ localize(product.description) }}</p>
  </div>
</template>

<script setup>
import { useLocalize } from '~/composables/useLocalize'

const { localize } = useLocalize()
</script>
```

### 2. Sử dụng Component

```vue
<template>
  <div>
    <MultilingualText :content="product.name" />
    <MultilingualText :content="product.description" />
  </div>
</template>
```

### 3. Sử dụng Store trực tiếp

```vue
<template>
  <div>
    <h1>{{ localeStore.localize(product.name) }}</h1>
  </div>
</template>

<script setup>
import { useLocaleStore } from '~/stores/locale'

const localeStore = useLocaleStore()
</script>
```

## Các thành phần chính

### 1. Locale Store (`stores/locale.ts`)
- Quản lý ngôn ngữ hiện tại
- Cung cấp hàm `localize()` để xử lý nội dung đa ngôn ngữ
- Lưu trữ persistent trong localStorage

### 2. API Plugin (`plugins/api.ts`)
- Tự động thêm `Accept-Language` header vào mọi API request
- Sử dụng ngôn ngữ từ locale store

### 3. Language Switcher (`components/LanguageSwitcher.vue`)
- Component để chuyển đổi ngôn ngữ
- Tự động sync với i18n và locale store

### 4. Multilingual Text (`components/MultilingualText.vue`)
- Component wrapper để hiển thị nội dung đa ngôn ngữ
- Tự động xử lý fallback logic

## Cấu hình

### 1. i18n Config (`i18n.config.ts`)
```typescript
locales: [
  { code: 'en', name: 'English' },
  { code: 'vi', name: 'Tiếng Việt' }
],
defaultLocale: 'en'
```

### 2. Locale Store
```typescript
supported_languages: [
  { code: 'en', name: 'English', flag: 'us' },
  { code: 'vi', name: 'Tiếng Việt', flag: 'vn' }
]
```

## Ví dụ thực tế

### ProductCard.vue
```vue
<template>
  <div class="product-card">
    <img :alt="localize(product.name)" />
    <h3>{{ localize(product.name) }}</h3>
    <p>{{ localize(product.category?.name) }}</p>
  </div>
</template>

<script setup>
import { useLocalize } from '~/composables/useLocalize'

const { localize } = useLocalize()
</script>
```

### CategoryMenu.vue
```vue
<template>
  <div>
    <h3>{{ $t('categories.title') }}</h3>
    <button v-for="category in categories" :key="category.id">
      {{ localize(category.name) }}
    </button>
  </div>
</template>

<script setup>
import { useLocalize } from '~/composables/useLocalize'

const { localize } = useLocalize()
</script>
```

## Lưu ý quan trọng

1. **Backend luôn trả về cả `origin` và `translates`**
2. **Frontend tự động chọn ngôn ngữ** dựa trên locale hiện tại
3. **Fallback logic**: Nếu không có bản dịch → dùng `origin`
4. **Accept-Language header**: Tự động được thêm vào API requests
5. **Persistent language**: Ngôn ngữ được lưu trong localStorage

## Troubleshooting

### Lỗi thường gặp
1. **TypeScript errors**: Đảm bảo interface có cấu trúc `{ origin: string, translates?: Array<{language: string, value: string}> }`
2. **Không hiển thị nội dung**: Kiểm tra xem có sử dụng `localize()` function không
3. **Ngôn ngữ không đổi**: Kiểm tra LanguageSwitcher có sync với locale store không

### Debug
```javascript
// Kiểm tra ngôn ngữ hiện tại
console.log(localeStore.currentLangue)

// Kiểm tra nội dung đa ngôn ngữ
console.log(localize(product.name))
```
