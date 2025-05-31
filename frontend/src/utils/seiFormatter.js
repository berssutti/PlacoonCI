export const formatSeiProcess = (value) => {
    if (!value) return value

    const cleanedValue = value.replace(/\D/g, '')

    if (cleanedValue.length <= 5) {
        return cleanedValue
    } else if (cleanedValue.length <= 11) {
        return `${cleanedValue.slice(0, 5)}.${cleanedValue.slice(5)}`
    } else if (cleanedValue.length <= 15) {
        return `${cleanedValue.slice(0, 5)}.${cleanedValue.slice(5, 11)}/${cleanedValue.slice(11, 15)}`
    } else {
        return `${cleanedValue.slice(0, 5)}.${cleanedValue.slice(5, 11)}/${cleanedValue.slice(11, 15)}-${cleanedValue.slice(15, 17)}`
    }
}
