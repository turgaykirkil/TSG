export class CacheService {
  private static instance: CacheService;
  private cache: Map<string, { data: any; timestamp: number }> = new Map();
  private CACHE_DURATION = 15 * 60 * 1000; // 15 dakika

  private constructor() {}

  public static getInstance(): CacheService {
    if (!CacheService.instance) {
      CacheService.instance = new CacheService();
    }
    return CacheService.instance;
  }

  set(key: string, data: any): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }

  get(key: string): any {
    const cachedItem = this.cache.get(key);
    
    if (cachedItem) {
      // Önbellek süresi dolmamışsa veriyi döndür
      if (Date.now() - cachedItem.timestamp < this.CACHE_DURATION) {
        return cachedItem.data;
      }
      
      // Süresi dolmuşsa önbellekten sil
      this.cache.delete(key);
    }
    
    return null;
  }

  has(key: string): boolean {
    const cachedItem = this.cache.get(key);
    return !!cachedItem && (Date.now() - cachedItem.timestamp < this.CACHE_DURATION);
  }

  delete(key: string): void {
    this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }

  getCacheStats() {
    return {
      totalItems: this.cache.size,
      cacheSize: Array.from(this.cache.values()).reduce((total, item) => total + JSON.stringify(item.data).length, 0)
    };
  }
}
