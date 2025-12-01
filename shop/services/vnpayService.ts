/**
 * VNPay Payment Service
 * Handles VNPay payment integration
 */
import { useApi } from '~/services/api'

export interface VNPayPaymentRequest {
  order_id: number
  bank_code?: string
  language?: 'vn' | 'en'
}

export interface VNPayPaymentResponse {
  payment_url: string
  order_id: number
}

export interface VNPayReturnResponse {
  success: boolean
  order_id: string
  amount: number
  transaction_no: string
  response_code: string
  message: string
  bank_code?: string
  card_type?: string
}

export const useVNPayService = () => {
  const { request } = useApi()

  /**
   * Create VNPay payment URL for an order
   */
  const createPayment = async (data: VNPayPaymentRequest): Promise<VNPayPaymentResponse> => {
    console.log('[VNPay] Creating payment for order:', data.order_id)
    
    const response = await request<VNPayPaymentResponse>('/payment/vnpay/create', {
      method: 'POST',
      body: data
    })
    
    return response
  }

  /**
   * Get payment result from VNPay return URL
   */
  const getPaymentResult = async (queryParams: Record<string, string>): Promise<VNPayReturnResponse> => {
    const query = new URLSearchParams(queryParams).toString()
    
    // Use request method from useApi to get apiBase automatically
    const response = await request<VNPayReturnResponse>(`/payment/vnpay/return?${query}`, {
      method: 'GET'
    })
    
    return response
  }

  /**
   * Get list of supported banks
   */
  const getSupportedBanks = () => {
    return [
      { code: '', name: 'Cổng thanh toán VNPay' },
      { code: 'NCB', name: 'Ngân hàng NCB' },
      { code: 'BIDV', name: 'Ngân hàng BIDV' },
      { code: 'VCB', name: 'Ngân hàng Vietcombank' },
      { code: 'TCB', name: 'Ngân hàng Techcombank' },
      { code: 'MB', name: 'Ngân hàng MB' },
      { code: 'VIB', name: 'Ngân hàng VIB' },
      { code: 'ACB', name: 'Ngân hàng ACB' },
      { code: 'SHB', name: 'Ngân hàng SHB' },
      { code: 'VPB', name: 'Ngân hàng VPBank' },
      { code: 'TPB', name: 'Ngân hàng TPBank' },
    ]
  }

  return {
    createPayment,
    getPaymentResult,
    getSupportedBanks
  }
}
