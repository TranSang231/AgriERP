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
           // NEW: For the orders list page
        orders: {
          title: 'My Orders',
          subtitle: 'Review your past and current orders.',
          loading: 'Loading your orders...',
          unknownStatus: 'Unknown Status',
          paymentMethods: {
            bank_transfer: 'Bank Transfer',
            cod: 'Cash on Delivery'
          },
          empty: {
            title: 'No Orders Yet',
            subtitle: 'Start shopping to see your orders here.',
            shopNow: 'Shop Now'
          },
          error: {
            title: 'Error Loading Orders',
            loadFailed: 'Failed to load the order list. Please try again later.',
            retryButton: 'Retry'
          },
          orderCard: {
            orderId: 'Order #{id}',
            placedOn: 'Placed on {date}',
            customerInfo: 'Customer Information',
            name: 'Name:',
            company: 'Company:',
            taxCode: 'Tax Code:',
            paymentMethod: 'Payment Method:',
            products: 'Products ({count})',
            moreProducts: 'and {count} more products',
            summary: 'Order Summary',
            subtotal: 'Subtotal',
            tax: 'Tax ({rate}%)',
            shippingFee: 'Shipping Fee',
            total: 'Total',
            viewDetails: 'View Details',
            payNow: 'Pay Now',
            cancelOrder: 'Cancel Order',
            continueShopping: '← Continue Shopping'
          },
          meta: {
            title: 'My Orders - AgriShop',
            description: 'View your order history at AgriShop.'
          }
        },

        // UPDATED: For the single order detail page
        order: {
          title: 'Order',
          title_plural: 'Orders', // For breadcrumb
          details: 'Order Details',
          customerInfo: 'Customer Information',
          customerName: 'Customer Name',
          company: 'Company Name',
          taxCode: 'Tax Code',
          paymentMethod: 'Payment Method',
          productList: 'Ordered Products',
          quantity: 'Quantity',
          unitPrice: 'Unit Price',
          paymentInfo: 'Payment Information',
          paymentWaiting: 'Please complete the payment via bank transfer to process the order.',
          qrCode: 'Payment QR Code',
          qrInstruction: 'Scan the QR code with your banking app to complete the payment.',
          paymentSuccess: 'Payment successful! Your order is being processed.',
          orderSummary: 'Order Summary',
          subtotal: 'Subtotal',
          tax: 'Tax',
          shippingFee: 'Shipping Fee',
          total: 'Total',
          actions: 'Actions',
          timeline: 'Order Status',
          timelineEvents: {
            created: 'Order has been placed',
            confirmed: 'The order is being processed',
            packing: 'Your order is being packed',
            shipped: 'The order has been shipped',
            completed: 'Order completed successfully'
          },
          back: 'Back to List',
          retry: 'Retry',
          pay: 'Pay Now',
          cancel: 'Cancel Order',
          print: 'Print Order',
          loading: 'Loading order information...',
          error: 'An error occurred',
          placedOn: 'Placed on',
          errorMessages: {
            noId: 'Order ID not found.',
            notFound: 'Order not found.',
            loadFailed: 'Failed to load order details.'
          },
          // Shared Statuses (reused by both pages)
          statuses: {
            new: 'New',
            confirmed: 'Confirmed',
            packing: 'Packing',
            shipped: 'Shipped',
            completed: 'Completed',
            canceled: 'Canceled',
            unknown: 'Unknown'
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
            returnRequested: 'Return Requested',
            returning: 'Returning',
            returned: 'Returned'
          }
        },
          // NEW: For the detailed profile page
        profile: {
          guest: 'Customer',
          // Sidebar
          sidebar: {
            navTitle: 'Navigate',
            home: 'Home',
            products: 'Products',
            cart: 'Cart'
          },
          // Main Content Header
          header: {
            title: 'Personal Profile',
            subtitle: 'Manage your account information',
            settings: 'Settings'
          },
          // Avatar Section
          avatar: {
            upload: 'Upload Photo'
          },
          // Password Section
          password: {
            title: 'Change Password',
            changeButton: 'Change Password',
            currentLabel: 'Current Password',
            currentPlaceholder: 'Enter current password',
            newLabel: 'New Password',
            newPlaceholder: 'Enter new password (min. 6 characters)',
            confirmLabel: 'Confirm New Password',
            confirmPlaceholder: 'Re-enter new password',
            updateButton: 'Update Password',
            cancelButton: 'Cancel'
          },
          // Profile Info Section
          info: {
            title: 'Personal Information',
            emailLabel: 'Email',
            firstNameLabel: 'First Name',
            firstNamePlaceholder: 'Your first name',
            lastNameLabel: 'Last Name',
            lastNamePlaceholder: 'Your last name'
          },
          // Contact Info Section
          contact: {
            title: 'Contact Information',
            addressLabel: 'Home Address',
            addressPlaceholder: 'Street, building, etc.',
            locationLabel: 'Region (Province/District/Ward)',
            provinceLabel: 'Province/City',
            provincePlaceholder: '-- Select province/city --',
            districtLabel: 'District',
            districtPlaceholder: '-- Select district --',
            wardLabel: 'Ward/Commune',
            wardPlaceholder: '-- Select ward/commune --',
            phoneLabel: 'Phone Number',
            phonePlaceholder: '0123456789'
          },
          // Actions
          actions: {
            save: 'Save',
            saving: 'Saving...',
            cancel: 'Cancel',
            processing: 'Processing...'
          },
          // Footer
          footer: {
            copyright: '© 2024 AgriShop - Smart Agriculture',
            language: {
              vietnamese: 'Tiếng Việt',
              english: 'English'
            }
          },
          // Notifications (Toasts)
          notifications: {
            loadProfileError: 'Could not load profile information.',
            updateProfileSuccess: 'Profile updated successfully!',
            updateProfileError: 'Could not update profile.',
            fieldUpdateSuccess: 'Update successful!',
            fieldUpdateError: 'Could not update information.',
            avatarUpdateSuccess: 'Avatar updated.',
            avatarUpdateError: 'Could not update avatar.',
            passwordUpdateSuccess: 'Password changed successfully!',
            passwordUpdateError: 'Could not change password.',
            currentPasswordRequired: 'Please enter your current password.',
            newPasswordRequired: 'Please enter a new password.',
            newPasswordMinLength: 'New password must be at least 6 characters.',
            passwordMismatch: 'Confirmation password does not match.',
            sessionExpired: 'Session has expired. Please log in again.'
          }
        },
                thanks: {
          loading: 'Loading order information...',
          errorTitle: 'An error occurred',
          backToHome: 'Back to Home',
          successTitle: 'Order placed successfully!',
          successSubtitle: 'Thank you for your purchase. We will process your order shortly.',
          orderInfoTitle: 'Order Information',
          orderId: 'Order ID',
          orderDate: 'Order Date',
          paymentMethod: 'Payment Method',
          status: 'Status',
          customerInfoTitle: 'Customer Information',
          customerName: 'Customer Name',
          company: 'Company',
          taxCode: 'Tax Code',
          itemsTitle: 'Ordered Products',
          quantity: 'Quantity:',
          summaryTitle: 'Order Summary',
          subtotal: 'Subtotal',
          tax: 'Tax',
          shippingFee: 'Shipping Fee',
          total: 'Total',
          paymentInfoTitle: 'Payment Information',
          paymentPending: 'Your order is awaiting payment confirmation.',
          paymentConfirmation: 'We will check and confirm the transaction within 24 hours.',
          continueShopping: 'Continue Shopping',
          printOrder: 'Print Order',
          errorMessages: {
            notFound: 'Order information not found.',
            loadFailed: 'Could not load order information.'
          }
        },
                // NEW: For the products list page
        products: {
          breadcrumb: {
            products: 'Products'
          },
          title: 'Products',
          productsFound: '{count} products found',
          filters: 'Filters',
          showingCount: 'Showing {shown} of {total} products',
          sortBy: 'Sort by:',
          sortOptions: {
            default: 'Default',
            nameAsc: 'Name (A-Z)',
            nameDesc: 'Name (Z-A)',
            priceAsc: 'Price (Low to High)',
            priceDesc: 'Price (High to Low)',
            newest: 'Newest'
          },
          meta: {
            title: 'Products - AgriShop',
            description: 'Browse our wide selection of agricultural products and farming supplies.'
          }
        },
                // NEW: For the product detail page
        productDetail: {
          loading: 'Loading product details...',
          noName: 'Untitled Product',
          defaultUnit: 'item',
          unknownCategory: 'Uncategorized',
          unitLabel: 'Unit:',
          categoriesLabel: 'Categories:',
          quantityLabel: 'Quantity:',
          descriptionTitle: 'Product Description',
          specificationsTitle: 'Technical Specifications',
          stock: {
            outOfStock: 'Out of Stock',
            inStock: 'In stock ({count} {unit})'
          },
          actions: {
            back: 'Go Back',
            addToCart: 'Add to Cart',
          },
          error: {
            title: 'An error occurred',
            notFound: 'Product not found.',
            loadFailed: 'Could not load product details.',
          },
          specs: {
            price: 'Price',
            unit: 'Unit',
            stock: 'In Stock',
            dimensions: 'Dimensions',
            weight: 'Weight',
            vat: 'VAT Rate',
          },
          notifications: {
            addedToCart: 'Added {count} {unit} of {productName} to your cart!',
          },
          meta: {
            title: '{productName} - AgriShop',
            description: 'View details for {productName}. Find high-quality agricultural supplies at AgriShop.'
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
          // NEW: Dành cho trang danh sách đơn hàng
        orders: {
          title: 'Đơn hàng của tôi',
          subtitle: 'Xem lại các đơn hàng đã đặt và hiện tại của bạn.',
          loading: 'Đang tải danh sách đơn hàng...',
          unknownStatus: 'Trạng thái không xác định',
          paymentMethods: {
            bank_transfer: 'Chuyển khoản ngân hàng',
            cod: 'Thanh toán khi nhận hàng'
          },
          empty: {
            title: 'Chưa có đơn hàng nào',
            subtitle: 'Hãy bắt đầu mua sắm để xem đơn hàng của bạn ở đây.',
            shopNow: 'Mua sắm ngay'
          },
          error: {
            title: 'Lỗi khi tải đơn hàng',
            loadFailed: 'Không thể tải danh sách đơn hàng. Vui lòng thử lại sau.',
            retryButton: 'Thử lại'
          },
          orderCard: {
            orderId: 'Đơn hàng #{id}',
            placedOn: 'Đặt ngày {date}',
            customerInfo: 'Thông tin khách hàng',
            name: 'Tên:',
            company: 'Công ty:',
            taxCode: 'Mã số thuế:',
            paymentMethod: 'Phương thức thanh toán:',
            products: 'Sản phẩm ({count})',
            moreProducts: 'và {count} sản phẩm khác',
            summary: 'Tóm tắt đơn hàng',
            subtotal: 'Tạm tính',
            tax: 'Thuế ({rate}%)',
            shippingFee: 'Phí vận chuyển',
            total: 'Tổng cộng',
            viewDetails: 'Xem chi tiết',
            payNow: 'Thanh toán ngay',
            cancelOrder: 'Hủy đơn hàng',
            continueShopping: '← Tiếp tục mua sắm'
          },
          meta: {
            title: 'Đơn hàng của tôi - AgriShop',
            description: 'Xem lịch sử đơn hàng của bạn tại AgriShop.'
          }
        },

        // UPDATED: Dành cho trang chi tiết đơn hàng
        order: {
          title: 'Đơn hàng',
          title_plural: 'Đơn hàng', // Dùng cho breadcrumb
          details: 'Chi tiết đơn hàng',
          customerInfo: 'Thông tin khách hàng',
          customerName: 'Tên khách hàng',
          company: 'Tên công ty',
          taxCode: 'Mã số thuế',
          paymentMethod: 'Phương thức thanh toán',
          productList: 'Sản phẩm đã đặt',
          quantity: 'Số lượng',
          unitPrice: 'Đơn giá',
          paymentInfo: 'Thông tin thanh toán',
          paymentWaiting: 'Vui lòng hoàn tất thanh toán qua chuyển khoản để đơn hàng được xử lý.',
          qrCode: 'Mã QR thanh toán',
          qrInstruction: 'Quét mã QR bằng ứng dụng ngân hàng của bạn để hoàn tất thanh toán.',
          paymentSuccess: 'Thanh toán thành công! Đơn hàng của bạn đang được xử lý.',
          orderSummary: 'Tóm tắt đơn hàng',
          subtotal: 'Tạm tính',
          tax: 'Thuế',
          shippingFee: 'Phí vận chuyển',
          total: 'Tổng cộng',
          actions: 'Thao tác',
          timeline: 'Trạng thái đơn hàng',
          timelineEvents: {
            created: 'Đơn hàng đã được đặt',
            confirmed: 'Đơn hàng đang được xử lý',
            packing: 'Đơn hàng của bạn đang được đóng gói',
            shipped: 'Đơn hàng đã được vận chuyển',
            completed: 'Đơn hàng đã hoàn thành'
          },
          back: 'Quay lại danh sách',
          retry: 'Thử lại',
          pay: 'Thanh toán',
          cancel: 'Hủy đơn hàng',
          print: 'In đơn hàng',
          loading: 'Đang tải thông tin đơn hàng...',
          error: 'Có lỗi xảy ra',
          placedOn: 'Đặt ngày',
          errorMessages: {
            noId: 'Không tìm thấy ID đơn hàng.',
            notFound: 'Không tìm thấy đơn hàng.',
            loadFailed: 'Tải chi tiết đơn hàng thất bại.'
          },
          // Trạng thái dùng chung (cả 2 trang đều tái sử dụng)
          statuses: {
            new: 'Mới',
            confirmed: 'Đã xác nhận',
            packing: 'Đang đóng gói',
            shipped: 'Đã giao hàng',
            completed: 'Hoàn thành',
            canceled: 'Đã hủy',
            unknown: 'Không xác định'
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
        },
          // NEW: Dành cho trang hồ sơ chi tiết
        profile: {
          guest: 'Khách hàng',
          // Sidebar
          sidebar: {
            navTitle: 'Điều hướng',
            home: 'Trang chủ',
            products: 'Sản phẩm',
            cart: 'Giỏ hàng'
          },
          // Main Content Header
          header: {
            title: 'Hồ sơ cá nhân',
            subtitle: 'Quản lý thông tin tài khoản',
            settings: 'Cài đặt'
          },
          // Avatar Section
          avatar: {
            upload: 'Tải lên ảnh'
          },
          // Password Section
          password: {
            title: 'Đổi mật khẩu',
            changeButton: 'Đổi mật khẩu',
            currentLabel: 'Mật khẩu hiện tại',
            currentPlaceholder: 'Nhập mật khẩu hiện tại',
            newLabel: 'Mật khẩu mới',
            newPlaceholder: 'Nhập mật khẩu mới (ít nhất 6 ký tự)',
            confirmLabel: 'Xác nhận mật khẩu mới',
            confirmPlaceholder: 'Nhập lại mật khẩu mới',
            updateButton: 'Cập nhật mật khẩu',
            cancelButton: 'Hủy'
          },
          // Profile Info Section
          info: {
            title: 'Thông tin cá nhân',
            emailLabel: 'Email',
            firstNameLabel: 'Tên',
            firstNamePlaceholder: 'Tên của bạn',
            lastNameLabel: 'Họ',
            lastNamePlaceholder: 'Họ của bạn'
          },
          // Contact Info Section
          contact: {
            title: 'Thông tin liên hệ',
            addressLabel: 'Địa chỉ nhà',
            addressPlaceholder: 'Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành phố',
            locationLabel: 'Khu vực (Tỉnh/Quận/Phường)',
            provinceLabel: 'Tỉnh/Thành phố',
            provincePlaceholder: '-- Chọn tỉnh/thành phố --',
            districtLabel: 'Quận/Huyện',
            districtPlaceholder: '-- Chọn quận/huyện --',
            wardLabel: 'Phường/Xã',
            wardPlaceholder: '-- Chọn phường/xã --',
            phoneLabel: 'Số điện thoại',
            phonePlaceholder: '0123456789'
          },
          // Actions
          actions: {
            save: 'Lưu',
            saving: 'Đang lưu...',
            cancel: 'Hủy',
            processing: 'Đang xử lý...'
          },
          // Footer
          footer: {
            copyright: '© 2024 AgriShop - Nông nghiệp thông minh',
            language: {
              vietnamese: 'Tiếng Việt',
              english: 'English'
            }
          },
          // Notifications (Toasts)
          notifications: {
            loadProfileError: 'Không thể tải thông tin hồ sơ.',
            updateProfileSuccess: 'Cập nhật hồ sơ thành công!',
            updateProfileError: 'Không thể cập nhật hồ sơ.',
            fieldUpdateSuccess: 'Cập nhật thành công!',
            fieldUpdateError: 'Không thể cập nhật thông tin.',
            avatarUpdateSuccess: 'Ảnh đại diện đã được cập nhật.',
            avatarUpdateError: 'Không thể cập nhật ảnh.',
            passwordUpdateSuccess: 'Đổi mật khẩu thành công!',
            passwordUpdateError: 'Không thể đổi mật khẩu.',
            currentPasswordRequired: 'Vui lòng nhập mật khẩu hiện tại.',
            newPasswordRequired: 'Vui lòng nhập mật khẩu mới.',
            newPasswordMinLength: 'Mật khẩu mới phải có ít nhất 6 ký tự.',
            passwordMismatch: 'Mật khẩu xác nhận không khớp.',
            sessionExpired: 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.'
          }
        },
                thanks: {
          loading: 'Đang tải thông tin đơn hàng...',
          errorTitle: 'Có lỗi xảy ra',
          backToHome: 'Về trang chủ',
          successTitle: 'Đặt hàng thành công!',
          successSubtitle: 'Cảm ơn bạn đã mua hàng. Chúng tôi sẽ xử lý đơn hàng của bạn sớm nhất.',
          orderInfoTitle: 'Thông tin đơn hàng',
          orderId: 'Mã đơn hàng',
          orderDate: 'Ngày đặt hàng',
          paymentMethod: 'Phương thức thanh toán',
          status: 'Trạng thái',
          customerInfoTitle: 'Thông tin khách hàng',
          customerName: 'Tên khách hàng',
          company: 'Công ty',
          taxCode: 'Mã số thuế',
          itemsTitle: 'Sản phẩm đã đặt',
          quantity: 'Số lượng:',
          summaryTitle: 'Tóm tắt đơn hàng',
          subtotal: 'Tạm tính',
          tax: 'Thuế',
          shippingFee: 'Phí vận chuyển',
          total: 'Tổng cộng',
          paymentInfoTitle: 'Thông tin thanh toán',
          paymentPending: 'Đơn hàng của bạn đang chờ xác nhận thanh toán.',
          paymentConfirmation: 'Chúng tôi sẽ kiểm tra và xác nhận giao dịch trong vòng 24 giờ.',
          continueShopping: 'Tiếp tục mua sắm',
          printOrder: 'In đơn hàng',
          errorMessages: {
            notFound: 'Không tìm thấy thông tin đơn hàng.',
            loadFailed: 'Không thể tải thông tin đơn hàng.'
          }
        },
                // NEW: Dành cho trang danh sách sản phẩm
        products: {
          breadcrumb: {
            products: 'Sản phẩm'
          },
          title: 'Sản phẩm',
          productsFound: 'Tìm thấy {count} sản phẩm',
          filters: 'Bộ lọc',
          showingCount: 'Hiển thị {shown} trên {total} sản phẩm',
          sortBy: 'Sắp xếp theo:',
          sortOptions: {
            default: 'Mặc định',
            nameAsc: 'Tên (A-Z)',
            nameDesc: 'Tên (Z-A)',
            priceAsc: 'Giá (Thấp đến Cao)',
            priceDesc: 'Giá (Cao đến Thấp)',
            newest: 'Mới nhất'
          },
          meta: {
            title: 'Sản phẩm - AgriShop',
            description: 'Duyệt qua danh sách đa dạng các sản phẩm nông nghiệp và vật tư canh tác của chúng tôi.'
          }
        },
                // NEW: Dành cho trang chi tiết sản phẩm
        productDetail: {
          loading: 'Đang tải thông tin sản phẩm...',
          noName: 'Không có tên',
          defaultUnit: 'Cái',
          unknownCategory: 'Không xác định',
          unitLabel: 'Đơn vị:',
          categoriesLabel: 'Danh mục:',
          quantityLabel: 'Số lượng:',
          descriptionTitle: 'Mô tả sản phẩm',
          specificationsTitle: 'Thông số kỹ thuật',
          stock: {
            outOfStock: 'Hết hàng',
            inStock: 'Còn {count} {unit}'
          },
          actions: {
            back: 'Quay lại',
            addToCart: 'Thêm vào giỏ hàng',
          },
          error: {
            title: 'Có lỗi xảy ra',
            notFound: 'Không tìm thấy sản phẩm.',
            loadFailed: 'Không thể tải thông tin sản phẩm.',
          },
          specs: {
            price: 'Giá bán',
            unit: 'Đơn vị',
            stock: 'Tồn kho',
            dimensions: 'Kích thước',
            weight: 'Trọng lượng',
            vat: 'Thuế VAT',
          },
          notifications: {
            addedToCart: 'Đã thêm {count} {unit} sản phẩm {productName} vào giỏ hàng!',
          },
          meta: {
            title: '{productName} - AgriShop',
            description: 'Xem chi tiết sản phẩm {productName}. Tìm các vật tư nông nghiệp chất lượng cao tại AgriShop.'
          }
        }
      }
    }
  }
}