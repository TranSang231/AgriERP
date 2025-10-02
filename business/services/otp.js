import BaseService from "./base";

class OTPService extends BaseService {
  get entity() {
    return "otp";
  }
  sendEmailOTP(email){
    return this.request().post(`${this.entity}/emails/send`, {email:email});
  }

  verifyEmailOTP(email,token){
    return this.request().post(`${this.entity}/emails/verify`,{email:email,token:token});
  }

  sendSMSOTP(phone, country_code=null){
    let data = { phone:phone }
    if (country_code) {
      const code = typeof country_code === 'string' ? country_code : country_code.toString();
      data = { ...data, country_code: code };
    }
    return this.request().post(`${this.entity}/phones/send-sms`, data);
  }

}

export default new OTPService();
