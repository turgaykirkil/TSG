import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-xl shadow-lg text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">TSG Platform</h1>
        <p className="text-gray-600 mb-8">Lütfen giriş yapın veya admin paneline gitmek için aşağıdaki butonu kullanın</p>
        
        <Link 
          href="/admin" 
          className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-lg"
        >
          Admin Paneline Git (Geliştirme Aşamasında)
        </Link>
      </div>
    </div>
  );
}
