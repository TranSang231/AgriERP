export function useCurrency(locale = 'vi-VN', currency = 'VND') {
  const formatter = new Intl.NumberFormat(locale, { style: 'currency', currency })
  function format(amount: number) { return formatter.format(amount || 0) }
  return { format }
}


