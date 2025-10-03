// D:\nam5ky1\ERP\AgriERP\shop\i18n.config.ts
   // KHÔNG CẦN IMPORT GÌ CẢ - Module i18n tự handle

   export default () => {
     console.log('i18n.config.ts loaded');
     return {
       legacy: false,
       fallbackLocale: 'en',
       locale: 'en',
       // Detect browser language và persist qua cookie (giữ locale sau refresh)
       detectBrowserLanguage: {
         useCookie: true,
         cookieKey: 'i18n_redirect',
         redirectOn: 'root'  // Chỉ detect trên root, phù hợp no_prefix
       },
       messages: {
         // English translations (giữ nguyên)
         en: {
           header: {
             searchPlaceholder: 'Search products...',
             orders: 'Orders',
             cart: 'Cart',
             profile: 'Profile',
             myOrders: 'My Orders',
             logout: 'Logout',
             login: 'Login',
             register: 'Register',
           },
           footer: {
             tagline: 'Your trusted partner for agricultural products and supplies.',
             quickLinks: 'Quick Links',
             products: 'Products',
             categories: 'Categories',
             aboutUs: 'About Us',
             contact: 'Contact',
             customerService: 'Customer Service',
             helpCenter: 'Help Center',
             shippingInfo: 'Shipping Info',
             returns: 'Returns',
             faq: 'FAQ',
             contactInfo: 'Contact Info',
             copyright: '© 2024 AgriShop. All rights reserved.',
           },
         home: {
          heroTitle: 'Quality Agricultural Products',
          heroSubtitle: 'Discover premium farming supplies, seeds, tools, and equipment for modern agriculture.',
          shopNow: 'Shop Now',
          browseCategories: 'Browse Categories',
          premiumAgriculture: 'Premium Agriculture',
          qualityProducts: 'Quality Products & Equipment',
          whyChoose: 'Why Choose AgriShop?',
          whyChooseSubtitle: 'We provide everything you need for successful farming with quality products and expert support.',
          features: {
            quality: {
              title: 'Quality Guaranteed',
              description: 'Premium products tested and verified for optimal performance in agricultural applications.'
            },
            delivery: {
              title: 'Fast Delivery',
              description: 'Quick and reliable shipping to get your agricultural supplies when you need them most.'
            },
            support: {
              title: 'Expert Support',
              description: 'Professional guidance from agricultural experts to help you make the right choices.'
            }
          },
          shopByCategory: {
            title: 'Shop by Category',
            subtitle: 'Find exactly what you need for your farming operation'
          },
          viewAllCategories: 'View All Categories',
          featuredProducts: {
            title: 'Featured Products',
            subtitle: 'Popular items trusted by farmers worldwide'
          },
          viewAllProducts: 'View All Products',
          newsletter: {
            title: 'Stay Updated',
            subtitle: 'Get the latest news about agricultural products and farming tips',
            placeholder: 'Enter your email',
            subscribeButton: 'Subscribe'
          },
          meta: {
            title: 'AgriShop - Quality Agricultural Products',
            description: 'Discover premium farming supplies, seeds, tools, and equipment for modern agriculture at AgriShop.'
          }
        },
          cart: {
          title: 'Shopping Cart',
          breadcrumb: {
            home: 'Home',
            cart: 'Shopping Cart'
          },
          empty: {
            title: 'Your cart is empty',
            subtitle: 'Add some products to get started',
            continueShopping: 'Continue Shopping'
          },
          items: {
            title: 'Cart Items ({count})',
            selectAll: 'Select All'
          },
          summary: {
            title: 'Order Summary',
            subtotal: 'Subtotal ({count} items)',
            discounts: 'Product discounts',
            shipping: 'Shipping',
            shippingFree: 'Free',
            tax: 'Tax',
            total: 'Total',
            checkoutButton: 'Proceed to Checkout',
            clearButton: 'Clear Cart'
          },
          actions: {
            continueShopping: 'Continue Shopping',
            clearConfirm: 'Are you sure you want to clear your cart?',
            selectItemWarning: 'Please select at least one item to proceed to checkout.'
          },
          meta: {
            title: 'Shopping Cart - AgriShop',
            description: 'Review your cart and proceed to checkout for your agricultural supplies.'
          }
        },
          categories: {
          title: 'Product Categories',
          subtitle: 'Select a category to view related products',
          loading: 'Loading categories...',
          error: {
            title: 'An error occurred',
            loadFailed: 'Failed to load categories',
            retryButton: 'Retry'
          },
          empty: {
            title: 'No Categories Found',
            viewAllProducts: 'View All Products'
          },
          defaultName: 'Category',
          meta: {
            title: 'Product Categories - AgriShop',
            description: 'Browse all product categories available at AgriShop.'
          }
        },
       checkout: {
          title: 'Checkout',
          empty: {
            title: 'There are no products to checkout',
            backToCart: 'Back to Cart'
          },
          customerInfo: {
            title: 'Customer Information',
            nameLabel: 'Customer Name *',
            namePlaceholder: 'Enter customer name',
            companyLabel: 'Company Name',
            companyPlaceholder: 'Enter company name (if any)',
            taxCodeLabel: 'Tax Code',
            taxCodePlaceholder: 'Enter tax code (if any)'
          },
          shippingInfo: {
            title: 'Shipping Information',
            addressLabel: 'Detailed Address',
            addressPlaceholder: 'House number, street name, building...',
            provinceLabel: 'Province/City',
            provincePlaceholder: '-- Select province/city --',
            districtLabel: 'District',
            districtPlaceholder: '-- Select district --',
            wardLabel: 'Ward/Commune',
            wardPlaceholder: '-- Select ward/commune --',
            loading: 'Loading...'
          },
          payment: {
            title: 'Payment Method',
            bankTransfer: 'Bank Transfer',
            bankTransferDesc: 'Scan QR code to pay',
            cod: 'Cash on Delivery (COD)',
            codDesc: 'Pay with cash upon delivery',
            bankTransferInfo: {
              title: 'Bank Transfer Information',
              qrPlaceholder: 'QR Code will be displayed here',
              qrCode: 'QR Code',
              qrScanPrompt: 'Scan the QR code with your banking app to pay',
              amountLabel: 'Amount:',
              confirmCheckbox: 'I have successfully transferred the amount',
              confirmNote: 'The order will be processed after the transaction is confirmed'
            }
          },
          products: {
            title: 'Products for Checkout',
            quantity: 'Quantity:'
          },
          summary: {
            title: 'Order Summary',
            voucherLabel: 'Select Voucher',
            voucherPlaceholder: '-- Select voucher --',
            voucherLoading: 'Loading vouchers...',
            voucherApplied: '✅ Applied:',
            subtotal: 'Subtotal',
            tax: 'Tax (8%)',
            discount: 'Discount',
            total: 'Total'
          },
          actions: {
            placeOrder: 'Place Order',
            processing: 'Processing...'
          },
          errors: {
            invalidVoucher: 'This voucher code cannot be applied to these products.',
            applyVoucherFailed: 'Error applying voucher.',
            voucherNotFound: 'Voucher does not exist or has expired.',
            fillRequiredFields: 'Please fill in all required information.',
            noServerResponse: 'No response received from the server.',
            orderFailed: 'Order placement failed, please try again.',
            validation: {
              nameRequired: 'Customer name is required',
              addressRequired: 'Detailed address is required',
              provinceRequired: 'Province/City is required',
              districtRequired: 'District is required',
              wardRequired: 'Ward/Commune is required',
              transferConfirmRequired: 'Please confirm that you have made the transfer'
            }
          },
          meta: {
            title: 'Checkout - AgriShop',
            description: 'Complete your purchase by providing your shipping and payment details.'
          }
        },
        order: {
          title: 'Order',
          details: 'Order details',
          customerInfo: 'Customer information',
          productList: 'Ordered products',
          paymentInfo: 'Payment information',
          orderSummary: 'Order summary',
          actions: 'Actions',
          timeline: 'Order status',
          back: 'Back to list',
          pay: 'Pay now',
          cancel: 'Cancel order',
          print: 'Print order',
          loading: 'Loading order information...',
          error: 'An error occurred',
          statuses: {
            new: 'New',
            confirmed: 'Confirmed',
            packing: 'Packing',
            shipped: 'Shipped',
            completed: 'Completed',
            canceled: 'Canceled'
          },
          paymentStatuses: {
            init: 'Initialized',
            pending: 'Pending',
            authorized: 'Authorized',
            captured: 'Captured',
            completed: 'Completed',
            rejected: 'Rejected',
            error: 'Error',
            canceled: 'Canceled',
            paid: 'Paid'
          },
          shippingStatuses: {
            placed: 'Placed',
            packing: 'Packing',
            delivering: 'Delivering',
            delivered: 'Delivered',
            returnRequested: 'Return requested',
            returning: 'Returning',
            returned: 'Returned'
          }
        }
      },
         // Vietnamese translations (giữ nguyên)
         vi: {
           header: {
             searchPlaceholder: 'Tìm kiếm sản phẩm...',
             orders: 'Đơn hàng',
             cart: 'Giỏ hàng',
             profile: 'Hồ sơ',
             myOrders: 'Đơn hàng của tôi',
             logout: 'Đăng xuất',
             login: 'Đăng nhập',
             register: 'Đăng ký',
           },
           footer: {
             tagline: 'Đối tác tin cậy của bạn cho các sản phẩm và vật tư nông nghiệp.',
             quickLinks: 'Liên kết nhanh',
             products: 'Sản phẩm',
             categories: 'Danh mục',
             aboutUs: 'Về chúng tôi',
             contact: 'Liên hệ',
             customerService: 'Chăm sóc khách hàng',
             helpCenter: 'Trung tâm trợ giúp',
             shippingInfo: 'Thông tin giao hàng',
             returns: 'Đổi trả',
             faq: 'Câu hỏi thường gặp',
             contactInfo: 'Thông tin liên hệ',
             copyright: '© 2024 AgriShop. Bảo lưu mọi quyền.',
           },
            home: {
          heroTitle: 'Sản phẩm nông nghiệp chất lượng',
          heroSubtitle: 'Khám phá vật tư, hạt giống, công cụ và thiết bị nông nghiệp cao cấp cho nền nông nghiệp hiện đại.',
          shopNow: 'Mua ngay',
          browseCategories: 'Xem danh mục',
          premiumAgriculture: 'Nông nghiệp cao cấp',
          qualityProducts: 'Sản phẩm & Thiết bị chất lượng',
          whyChoose: 'Tại sao chọn AgriShop?',
          whyChooseSubtitle: 'Chúng tôi cung cấp mọi thứ bạn cần để canh tác thành công với các sản phẩm chất lượng và sự hỗ trợ từ chuyên gia.',
          features: {
            quality: {
              title: 'Đảm bảo chất lượng',
              description: 'Sản phẩm cao cấp được kiểm tra và xác minh để đạt hiệu suất tối ưu trong các ứng dụng nông nghiệp.'
            },
            delivery: {
              title: 'Giao hàng nhanh',
              description: 'Vận chuyển nhanh chóng và đáng tin cậy để bạn nhận được vật tư nông nghiệp của mình khi cần nhất.'
            },
            support: {
              title: 'Hỗ trợ chuyên môn',
              description: 'Hướng dẫn chuyên nghiệp từ các chuyên gia nông nghiệp để giúp bạn đưa ra lựa chọn đúng đắn.'
            }
          },
          shopByCategory: {
            title: 'Mua sắm theo danh mục',
            subtitle: 'Tìm chính xác những gì bạn cần cho hoạt động canh tác của mình'
          },
          viewAllCategories: 'Xem tất cả danh mục',
          featuredProducts: {
            title: 'Sản phẩm nổi bật',
            subtitle: 'Các mặt hàng phổ biến được nông dân trên toàn thế giới tin dùng'
          },
          viewAllProducts: 'Xem tất cả sản phẩm',
          newsletter: {
            title: 'Luôn cập nhật',
            subtitle: 'Nhận tin tức mới nhất về các sản phẩm nông nghiệp và mẹo canh tác',
            placeholder: 'Nhập email của bạn',
            subscribeButton: 'Đăng ký'
          },
          meta: {
            title: 'AgriShop - Sản phẩm nông nghiệp chất lượng',
            description: 'Khám phá vật tư, hạt giống, công cụ và thiết bị nông nghiệp cao cấp cho nền nông nghiệp hiện đại tại AgriShop.'
          }
        },
         cart: {
          title: 'Giỏ hàng',
          breadcrumb: {
            home: 'Trang chủ',
            cart: 'Giỏ hàng'
          },
          empty: {
            title: 'Giỏ hàng của bạn đang trống',
            subtitle: 'Hãy thêm sản phẩm vào giỏ để bắt đầu mua sắm',
            continueShopping: 'Tiếp tục mua sắm'
          },
          items: {
            title: 'Sản phẩm trong giỏ ({count})',
            selectAll: 'Chọn tất cả'
          },
          summary: {
            title: 'Tóm tắt đơn hàng',
            subtotal: 'Tạm tính ({count} sản phẩm)',
            discounts: 'Giảm giá sản phẩm',
            shipping: 'Phí vận chuyển',
            shippingFree: 'Miễn phí',
            tax: 'Thuế',
            total: 'Tổng cộng',
            checkoutButton: 'Tiến hành thanh toán',
            clearButton: 'Xóa giỏ hàng'
          },
          actions: {
            continueShopping: 'Tiếp tục mua sắm',
            clearConfirm: 'Bạn có chắc chắn muốn xóa toàn bộ giỏ hàng không?',
            selectItemWarning: 'Vui lòng chọn ít nhất một sản phẩm để tiến hành thanh toán.'
          },
          meta: {
            title: 'Giỏ hàng - AgriShop',
            description: 'Kiểm tra giỏ hàng của bạn và tiến hành thanh toán các mặt hàng nông nghiệp.'
          }
        },
        categories: {
          title: 'Danh mục sản phẩm',
          subtitle: 'Chọn danh mục để xem các sản phẩm liên quan',
          loading: 'Đang tải danh mục...',
          error: {
            title: 'Có lỗi xảy ra',
            loadFailed: 'Không thể tải danh mục',
            retryButton: 'Thử lại'
          },
          empty: {
            title: 'Chưa có danh mục',
            viewAllProducts: 'Xem tất cả sản phẩm'
          },
          defaultName: 'Danh mục',
          meta: {
            title: 'Danh mục Sản phẩm - AgriShop',
            description: 'Duyệt qua tất cả các danh mục sản phẩm có sẵn tại AgriShop.'
          }
        },
            checkout: {
          title: 'Thanh toán',
          empty: {
            title: 'Không có sản phẩm nào để thanh toán',
            backToCart: 'Quay lại giỏ hàng'
          },
          customerInfo: {
            title: 'Thông tin khách hàng',
            nameLabel: 'Tên khách hàng *',
            namePlaceholder: 'Nhập tên khách hàng',
            companyLabel: 'Tên công ty',
            companyPlaceholder: 'Nhập tên công ty (nếu có)',
            taxCodeLabel: 'Mã số thuế',
            taxCodePlaceholder: 'Nhập mã số thuế (nếu có)'
          },
          shippingInfo: {
            title: 'Thông tin giao hàng',
            addressLabel: 'Địa chỉ chi tiết',
            addressPlaceholder: 'Số nhà, tên đường, tòa nhà...',
            provinceLabel: 'Tỉnh/Thành phố',
            provincePlaceholder: '-- Chọn tỉnh/thành phố --',
            districtLabel: 'Quận/Huyện',
            districtPlaceholder: '-- Chọn quận/huyện --',
            wardLabel: 'Phường/Xã',
            wardPlaceholder: '-- Chọn phường/xã --',
            loading: 'Đang tải...'
          },
          payment: {
            title: 'Phương thức thanh toán',
            bankTransfer: 'Chuyển khoản ngân hàng',
            bankTransferDesc: 'Quét QR code để thanh toán',
            cod: 'Thanh toán khi nhận hàng (COD)',
            codDesc: 'Thanh toán bằng tiền mặt khi nhận hàng',
            bankTransferInfo: {
              title: 'Thông tin chuyển khoản',
              qrPlaceholder: 'QR Code sẽ hiển thị ở đây',
              qrCode: 'QR Code',
              qrScanPrompt: 'Quét QR code bằng ứng dụng ngân hàng để thanh toán',
              amountLabel: 'Số tiền:',
              confirmCheckbox: 'Tôi đã chuyển khoản thành công',
              confirmNote: 'Đơn hàng sẽ được xử lý sau khi admin xác nhận giao dịch'
            }
          },
          products: {
            title: 'Sản phẩm thanh toán',
            quantity: 'Số lượng:'
          },
          summary: {
            title: 'Tóm tắt đơn hàng',
            voucherLabel: 'Chọn Voucher',
            voucherPlaceholder: '-- Chọn voucher --',
            voucherLoading: 'Đang tải voucher...',
            voucherApplied: '✅ Đã áp dụng:',
            subtotal: 'Tạm tính',
            tax: 'Thuế (8%)',
            discount: 'Giảm giá',
            total: 'Tổng cộng'
          },
          actions: {
            placeOrder: 'Đặt hàng',
            processing: 'Đang xử lý...'
          },
          errors: {
            invalidVoucher: 'Mã giảm giá không áp dụng được cho sản phẩm này.',
            applyVoucherFailed: 'Lỗi khi áp dụng mã giảm giá.',
            voucherNotFound: 'Mã giảm giá không tồn tại hoặc đã hết hạn.',
            fillRequiredFields: 'Vui lòng điền đầy đủ thông tin bắt buộc.',
            noServerResponse: 'Không nhận được phản hồi từ server.',
            orderFailed: 'Đặt hàng thất bại, vui lòng thử lại.',
            validation: {
              nameRequired: 'Tên khách hàng là bắt buộc',
              addressRequired: 'Địa chỉ chi tiết là bắt buộc',
              provinceRequired: 'Tỉnh/Thành phố là bắt buộc',
              districtRequired: 'Quận/Huyện là bắt buộc',
              wardRequired: 'Phường/Xã là bắt buộc',
              transferConfirmRequired: 'Vui lòng xác nhận đã chuyển khoản'
            }
          },
          meta: {
            title: 'Thanh toán - AgriShop',
            description: 'Hoàn tất việc mua hàng của bạn bằng cách cung cấp thông tin giao hàng và thanh toán.'
          }
        },
        order: {
          title: 'Đơn hàng',
          details: 'Chi tiết đơn hàng',
          customerInfo: 'Thông tin khách hàng',
          productList: 'Sản phẩm đã đặt',
          paymentInfo: 'Thông tin thanh toán',
          orderSummary: 'Tóm tắt đơn hàng',
          actions: 'Thao tác',
          timeline: 'Trạng thái đơn hàng',
          back: 'Quay lại danh sách',
          pay: 'Thanh toán',
          cancel: 'Hủy đơn hàng',
          print: 'In đơn hàng',
          loading: 'Đang tải thông tin đơn hàng...',
          error: 'Có lỗi xảy ra',
          statuses: {
            new: 'Mới',
            confirmed: 'Đã xác nhận',
            packing: 'Đang đóng gói',
            shipped: 'Đã giao hàng',
            completed: 'Hoàn thành',
            canceled: 'Đã hủy'
          },
          paymentStatuses: {
            init: 'Đã khởi tạo',
            pending: 'Đang chờ',
            authorized: 'Đã ủy quyền',
            captured: 'Đã thu tiền',
            completed: 'Hoàn thành',
            rejected: 'Từ chối',
            error: 'Lỗi',
            canceled: 'Đã hủy',
            paid: 'Đã thanh toán'
          },
          shippingStatuses: {
            placed: 'Đã đặt hàng',
            packing: 'Đang đóng gói',
            delivering: 'Đang giao hàng',
            delivered: 'Đã giao hàng',
            returnRequested: 'Yêu cầu trả hàng',
            returning: 'Đang trả hàng',
            returned: 'Đã trả hàng'
          }
        }
      }
    }
  }
}