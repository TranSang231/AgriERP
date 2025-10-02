export function getErrorMessage(error: any, defaultMessage?: string) {
    const { data } = error;
    if (data) {
        if (data.route && Array.isArray(data.route)) {
            return data.route.join(', '); 
        }
        const { error: message, error_description, detail } = data
        return error_description 
            ? error_description 
            : detail
                ? detail
                :message;
    }
    return defaultMessage;
}