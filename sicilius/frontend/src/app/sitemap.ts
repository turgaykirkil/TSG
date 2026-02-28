import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
    const baseUrl = 'https://sicilius.com.tr';

    // Halka açık sayfalar (Sadece bunlar indekslenebilir)
    const routes = [
        '',
        '/home',
        '/about',
        '/contact',
        '/sss',
        '/gizlilik-politikasi',
        '/kvkk-aydinlatma',
        '/kullanici-sozlesmesi',
        '/cerez-politikasi',
    ];

    return routes.map((route) => ({
        url: `${baseUrl}${route}`,
        lastModified: new Date(),
        changeFrequency: 'monthly',
        priority: route === '' ? 1 : 0.8,
    }));
}
