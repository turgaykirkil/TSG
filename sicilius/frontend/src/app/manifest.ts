import { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
    return {
        name: 'Sicilius | Kurumsal Veri Analizi',
        short_name: 'Sicilius',
        description: 'Halka açık kayıtları modernize ederek hızlı arama ve analiz sunan profesyonel veri platformu.',
        start_url: '/',
        display: 'standalone',
        background_color: '#0f172a',
        theme_color: '#0f172a',
        icons: [
            {
                src: '/favicon.ico',
                sizes: 'any',
                type: 'image/x-icon',
            },
        ],
    };
}
