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