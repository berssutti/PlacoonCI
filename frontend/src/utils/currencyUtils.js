export const formatCurrency = (value) => {
  if (!value) return '';
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
};

export const parseCurrency = (formattedValue) => {
  if (!formattedValue) return null;
  const numericValue = formattedValue.replace(/[^\d]/g, '');
  return numericValue ? parseFloat(numericValue) / 100 : null;
};

export const isValidCurrency = (value) => {
  return value !== null &&
    value !== undefined &&
    !isNaN(value) &&
    typeof value === 'number';
};