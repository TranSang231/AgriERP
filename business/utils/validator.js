import { REGION_CODES } from '@/constants/countries';
export function isValidEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return email && typeof email === 'string' && pattern.test(email);
}

export function isValidPhoneNumber(phone) {
    const pattern = /^(0|[\+]?[0-9]{1,3})\W*[0-9]{9,11}$/i;
    // const pattern = /^[\+]?[0-9]{0,3}\W?+[(]?[0-9]{1,3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/i;
    return phone && pattern.test(phone);
}

export function isValidWebsite(url) {
    const pattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
    return url && typeof url === 'string' && pattern.test(url);
}

export function isValidDomain(domain) {
    if (!domain || typeof domain !== 'string') {
        return false;
    }
    const domainPattern = /^([a-z0-9|-]+[a-z0-9]{1,}\.)*[a-z0-9|-]+[a-z0-9]{1,}\.[a-z]{2,}(:[0-9]+)?$/;
    const localhostPattern = /localhost(:[0-9]{1,5})*/;
    return  domainPattern.test(domain) || localhostPattern.test(domain);
}

export function isValidSlug(slug) {
    const pattern = /^[a-zA-Z\-\_0-9]{1,60}$/;
    return slug && typeof slug === 'string' && pattern.test(slug);
}

function extractPhoneNumber(phone) {
    if (phone.startsWith('+')) {
        const n = phone.substring(1).trim();
        const region_code = REGION_CODES.find(o => n.startsWith(o));
        const phone_number = !!region_code ? n.substring(region_code.length) : n;
        return { region_code, phone_number };
    }
    const phone_number = phone.startsWith('0') ? phone.substring(1).trim() : phone;
    return { region_code: null, phone_number };
}

export function isTheSamePhoneNumber(phone1, phone2) {
    const { region_code: r1, phone_number: n1 } = extractPhoneNumber(phone1);
    const { region_code: r2, phone_number: n2 } = extractPhoneNumber(phone2);
    return n1 === n2 && (!r1 || !r2 || r1 === r2);;
}

function extractTextFromHTML(htmlString) {
    return htmlString.replace(/<[^>]*(>|$)| |‌|»|«|>/g, ' ');
}

export function requireShortTranslate(value, callback, t, localeStore) {
    if (!value || !value.origin || value.origin.length === 0) {
        callback(new Error(t('validate_error_required')));
    }
    
    if (value.translates && value.translates.length > 0) {
        const requiredError = value.translates.some((translate) => {
            let language = localeStore && localeStore.supported_languages
                ? localeStore.supported_languages.find((l) => l.code == translate.language)
                : null;
            language = language ? language.name: translate.language;
            if (!translate.value || translate.value.length === 0) {  
                callback(new Error(t('validate_error_translation_required', {language: language})));
                return true;
            }
            return false;
        })
        if (requiredError) {
            return;
        }
    }
    callback();
}

export function requireLongTranslate(value, callback, t, localeStore) {
    if (!value || !value.origin || value.origin.length === 0) {
        callback(new Error(t('validate_error_required')));
    }
    const originText = extractTextFromHTML(value.origin).trim();
    if (!originText || originText.length === 0) {
        callback(new Error(t('validate_error_required')));
    }
    
    if (value.translates && value.translates.length > 0) {
        const requiredError = value.translates.some((translate) => {
            let language = localeStore && localeStore.supported_languages
                ? localeStore.supported_languages.find((l) => l.code == translate.language)
                : null;
            language = language ? language.name: translate.language;
            if (!translate.value || translate.value.length === 0) {  
                callback(new Error(t('validate_error_translation_required', {language: language})));
                return true;
            }
            const translateText = extractTextFromHTML(translate.value).trim();
            if (!translateText || translateText.length === 0) {
                callback(new Error(t('validate_error_translation_required', {language: language})));
                return true;
            }
            return false;
        })
        if (requiredError) {
            return;
        }
    }
    callback();
}