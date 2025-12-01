"""
VNPay Payment Integration for Django
Based on VNPay API v2.1.0
"""
import hashlib
import hmac
import urllib.parse
from datetime import datetime
from typing import Dict, Optional


class VNPayPayment:
    """VNPay payment handler class"""
    
    def __init__(self):
        self.request_data: Dict[str, str] = {}
        self.response_data: Dict[str, str] = {}
    
    def get_payment_url(self, vnpay_payment_url: str, secret_key: str) -> str:
        """
        Generate VNPay payment URL with secure hash
        
        Args:
            vnpay_payment_url: VNPay payment gateway URL
            secret_key: Secret key for HMAC SHA512
            
        Returns:
            Complete payment URL with secure hash
        """
        # Remove empty/null values before sorting
        cleaned_data = {k: v for k, v in self.request_data.items() if v is not None and str(v).strip() != ''}
        
        # Sort request data by key (alphabetically)
        input_data = sorted(cleaned_data.items())
        query_string = ''
        seq = 0
        
        # Build query string
        for key, val in input_data:
            if seq == 1:
                query_string = query_string + "&" + key + '=' + urllib.parse.quote_plus(str(val))
            else:
                seq = 1
                query_string = key + '=' + urllib.parse.quote_plus(str(val))
        
        # Log for debugging - write to file
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f'[VNPAY] Query string before hash: {query_string}')
        
        # Also write to debug file
        try:
            with open('vnpay_debug.log', 'a', encoding='utf-8') as f:
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'\n{"="*80}\n')
                f.write(f'[{timestamp}] VNPay Payment URL Generation\n')
                f.write(f'{"="*80}\n')
                f.write(f'Query string (before hash):\n{query_string}\n\n')
        except Exception as e:
            logger.error(f'Failed to write debug log: {e}')
        
        # Generate secure hash
        hash_value = self._hmacsha512(secret_key, query_string)
        logger.info(f'[VNPAY] Generated hash: {hash_value}')
        
        # Write hash to debug file
        try:
            with open('vnpay_debug.log', 'a', encoding='utf-8') as f:
                f.write(f'Secret Key: {secret_key}\n\n')
                f.write(f'Generated Hash:\n{hash_value}\n')
                f.write(f'{"="*80}\n\n')
        except Exception as e:
            logger.error(f'Failed to write debug log: {e}')
        
        return vnpay_payment_url + "?" + query_string + '&vnp_SecureHash=' + hash_value
    
    def validate_response(self, secret_key: str) -> bool:
        """
        Validate VNPay response secure hash
        
        Args:
            secret_key: Secret key for HMAC SHA512
            
        Returns:
            True if valid, False otherwise
        """
        if 'vnp_SecureHash' not in self.response_data:
            return False
            
        vnp_secure_hash = self.response_data['vnp_SecureHash']
        
        # Create copy to avoid modifying original
        data_to_validate = dict(self.response_data)
        
        # Remove hash params
        if 'vnp_SecureHash' in data_to_validate:
            data_to_validate.pop('vnp_SecureHash')
        if 'vnp_SecureHashType' in data_to_validate:
            data_to_validate.pop('vnp_SecureHashType')
        
        # Sort and build hash data
        input_data = sorted(data_to_validate.items())
        hash_data = ''
        seq = 0
        
        for key, val in input_data:
            if str(key).startswith('vnp_'):
                if seq == 1:
                    hash_data = hash_data + "&" + str(key) + '=' + urllib.parse.quote_plus(str(val))
                else:
                    seq = 1
                    hash_data = str(key) + '=' + urllib.parse.quote_plus(str(val))
        
        # Generate hash and compare
        hash_value = self._hmacsha512(secret_key, hash_data)
        
        return vnp_secure_hash == hash_value
    
    @staticmethod
    def _hmacsha512(key: str, data: str) -> str:
        """Generate HMAC SHA512 hash"""
        byte_key = key.encode('utf-8')
        byte_data = data.encode('utf-8')
        return hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()


class VNPayConfig:
    """VNPay configuration constants"""
    
    # VNPay API URLs
    SANDBOX_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
    PRODUCTION_PAYMENT_URL = 'https://vnpayment.vn/paymentv2/vpcpay.html'
    
    SANDBOX_API_URL = 'https://sandbox.vnpayment.vn/merchant_webapi/api/transaction'
    PRODUCTION_API_URL = 'https://vnpayment.vn/merchant_webapi/api/transaction'
    
    # API Version
    VERSION = '2.1.0'
    
    # Command
    COMMAND_PAY = 'pay'
    
    # Currency
    CURRENCY_VND = 'VND'
    
    # Language
    LANGUAGE_VN = 'vn'
    LANGUAGE_EN = 'en'
    
    # Response codes
    RESPONSE_CODE_SUCCESS = '00'
    RESPONSE_CODE_INVALID_AMOUNT = '04'
    RESPONSE_CODE_MAINTENANCE = '05'
    RESPONSE_CODE_INVALID_CARD = '07'
    RESPONSE_CODE_CARD_LOCKED = '09'
    RESPONSE_CODE_EXPIRED_CARD = '10'
    RESPONSE_CODE_INSUFFICIENT_BALANCE = '11'
    RESPONSE_CODE_INVALID_OTP = '12'
    RESPONSE_CODE_CANCELED = '24'
    RESPONSE_CODE_INVALID_SIGNATURE = '97'
    RESPONSE_CODE_INVALID_REQUEST = '99'
    
    @classmethod
    def get_response_message(cls, code: str) -> str:
        """Get response message by code"""
        messages = {
            '00': 'Giao dịch thành công',
            '04': 'Số tiền không hợp lệ',
            '05': 'Hệ thống đang bảo trì',
            '07': 'Thẻ không hợp lệ',
            '09': 'Thẻ bị khóa',
            '10': 'Thẻ hết hạn',
            '11': 'Số dư không đủ',
            '12': 'OTP không chính xác',
            '24': 'Giao dịch bị hủy',
            '97': 'Chữ ký không hợp lệ',
            '99': 'Yêu cầu không hợp lệ',
        }
        return messages.get(code, 'Lỗi không xác định')
