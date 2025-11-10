# Inventory Management System

## Tổng quan
Hệ thống quản lý tồn kho được tích hợp vào trang e-commerce, cung cấp các tính năng quản lý hàng tồn kho một cách hiệu quả.

## Cấu trúc Files

### 1. Service Layer
- `business/services/e-commerce/inventory.js` - Service API để tương tác với backend

### 2. Pages
- `business/pages/e-commerce/inventory/index.vue` - Trang danh sách tồn kho
- `business/pages/e-commerce/inventory/[id].vue` - Trang chi tiết sản phẩm và lịch sử giao dịch

## Tính năng chính

### Trang Danh sách Tồn kho (`/e-commerce/inventory`)

#### Thống kê tổng quan
- Tổng số sản phẩm
- Tổng giá trị tồn kho
- Số sản phẩm sắp hết hàng
- Số sản phẩm hết hàng

#### Bảng danh sách sản phẩm
- Hiển thị hình ảnh sản phẩm
- Tên sản phẩm và SKU
- Đơn vị tính
- Số lượng tồn kho hiện tại
- Số lượng tối thiểu
- Số lượng tối đa
- Giá đơn vị
- Giá trị tồn kho
- Trạng thái tồn kho (Còn hàng/Sắp hết/Hết hàng)
- Ngày cập nhật cuối

#### Tính năng lọc và tìm kiếm
- Tìm kiếm theo tên sản phẩm hoặc SKU
- Lọc theo danh mục sản phẩm
- Lọc theo trạng thái tồn kho
- Hiển thị chỉ sản phẩm sắp hết hàng
- Phân trang

#### Tính năng quản lý
- Điều chỉnh số lượng tồn kho
- Xem chi tiết sản phẩm
- Xuất dữ liệu Excel
- Làm mới dữ liệu

### Trang Chi tiết Sản phẩm (`/e-commerce/inventory/[id]`)

#### Thông tin sản phẩm
- Hình ảnh sản phẩm
- Tên sản phẩm và SKU
- Đơn vị tính và giá
- Danh mục sản phẩm

#### Thống kê tồn kho
- Số lượng hiện tại
- Số lượng tối thiểu
- Giá trị tồn kho

#### Lịch sử giao dịch
- Bảng lịch sử nhập/xuất kho
- Lọc theo khoảng thời gian
- Lọc theo loại giao dịch (Nhập/Xuất/Điều chỉnh)
- Thông tin chi tiết từng giao dịch:
  - Ngày giờ
  - Loại giao dịch
  - Số lượng
  - Số dư sau giao dịch
  - Tham chiếu (Đơn hàng, Phiếu nhập...)
  - Lý do
  - Người thực hiện

#### Tính năng quản lý
- Điều chỉnh tồn kho
- Thêm tồn kho mới
- Làm mới dữ liệu

## API Endpoints

Service `InventoryService` cung cấp các phương thức:

- `getInventoryItems(params)` - Lấy danh sách tồn kho
- `getInventoryItem(itemId)` - Lấy thông tin chi tiết sản phẩm
- `getInventoryHistory(productId, params)` - Lấy lịch sử giao dịch
- `updateInventoryQuantity(itemId, quantity, type)` - Cập nhật số lượng tồn kho
- `getLowStockItems(threshold)` - Lấy sản phẩm sắp hết hàng
- `getInventoryStats()` - Lấy thống kê tồn kho

## Cách sử dụng

1. Truy cập `/e-commerce/inventory` để xem danh sách tồn kho
2. Sử dụng các bộ lọc để tìm kiếm sản phẩm cụ thể
3. Click vào sản phẩm để xem chi tiết và lịch sử giao dịch
4. Sử dụng các nút "Điều chỉnh tồn kho" hoặc "Thêm tồn kho" để quản lý số lượng

## Mock Data

Hệ thống bao gồm mock data để demo khi API chưa sẵn sàng:
- Dữ liệu sản phẩm mẫu
- Lịch sử giao dịch mẫu
- Thống kê tổng quan

## Responsive Design

Giao diện được thiết kế responsive, tương thích với:
- Desktop
- Tablet
- Mobile

## Internationalization

Tất cả text đều sử dụng i18n, hỗ trợ đa ngôn ngữ thông qua `useI18n()`.
