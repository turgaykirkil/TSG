import { Link } from 'react-router-dom';
import { ArrowLeftIcon } from '@heroicons/react/24/outline';

export function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <h1 className="text-9xl font-extrabold text-primary-600">404</h1>
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">Sayfa Bulunamadı</h2>
          <p className="mt-2 text-lg text-gray-600">
            Üzgünüz, aradığınız sayfayı bulamadık.
          </p>
          <p className="text-gray-500 mt-2">
            Sayfa taşınmış, silinmiş veya hiç var olmamış olabilir.
          </p>
        </div>

        <div className="mt-8 flex justify-center space-x-4">
          <Link
            to="/"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <ArrowLeftIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
            Ana Sayfaya Dön
          </Link>
          <button
            onClick={() => window.history.back()}
            className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Geri Dön
          </button>
        </div>

        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            Yardıma mı ihtiyacınız var?{' '}
            <Link to="/contact" className="font-medium text-primary-600 hover:text-primary-500">
              İletişime geçin
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
