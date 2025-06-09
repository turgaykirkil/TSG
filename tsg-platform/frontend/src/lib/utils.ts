import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Tailwind CSS sınıflarını birleştirmek için kullanılır
 * @param inputs - Birleştirilecek sınıflar
 * @returns Birleştirilmiş sınıf isimleri
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * URL'den dosya adını çıkarır
 * @param url - Dosya URL'si
 * @returns Dosya adı
 */
export function getFilenameFromUrl(url: string): string {
  try {
    const urlObj = new URL(url);
    const pathname = urlObj.pathname;
    return pathname.split('/').pop() || '';
  } catch (e) {
    return url.split('/').pop() || '';
  }
}

/**
 * Dosya boyutunu okunabilir formata dönüştürür
 * @param bytes - Bayt cinsinden dosya boyutu
 * @param decimals - Ondalık basamak sayısı
 * @returns İnsan tarafından okunabilir dosya boyutu
 */
export function formatFileSize(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}

/**
 * Tarihi okunabilir formata dönüştürür
 * @param date - Tarih nesnesi veya string
 * @returns Biçimlendirilmiş tarih
 */
export function formatDate(
  date: Date | string | number,
  options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }
): string {
  const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
  return new Intl.DateTimeFormat('tr-TR', options).format(d);
}

/**
 * Dizeyi belirtilen uzunlukta kısaltır
 * @param str - Kısaltılacak dize
 * @param length - İzin verilen maksimum uzunluk
 * @returns Kısaltılmış dize
 */
export function truncateString(str: string, length: number): string {
  if (!str || str.length <= length) return str;
  return `${str.substring(0, length)}...`;
}

/**
 * Dizeyi baş harfleri büyük olacak şekilde düzenler
 * @param str - Düzenlenecek dize
 * @returns Baş harfleri büyük dize
 */
export function toTitleCase(str: string): string {
  return str.replace(
    /\w\S*/g,
    (txt) => txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase()
  );
}

/**
 * Dizeyi kabak durumuna (camelCase) dönüştürür
 * @param str - Dönüştürülecek dize
 * @returns camelCase formatında dize
 */
export function toCamelCase(str: string): string {
  return str
    .replace(/(?:^\w|[A-Z]|\b\w)/g, (letter, index) => {
      return index === 0 ? letter.toLowerCase() : letter.toUpperCase();
    })
    .replace(/[\s-]+/g, '');
}
