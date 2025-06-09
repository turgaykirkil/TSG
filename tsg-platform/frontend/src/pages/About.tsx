import { Link } from 'react-router-dom';

type TeamMember = {
  name: string;
  role: string;
  image: string;
  bio: string;
};

const teamMembers: TeamMember[] = [
  {
    name: 'Turgay Kırkıl',
    role: 'Kurucu & Geliştirici',
    image: 'https://via.placeholder.com/150',
    bio: '10+ yıllık yazılım geliştirme deneyimi ile projenin teknik liderliğini yapmaktadır.'
  },
  {
    name: 'Ahmet Yılmaz',
    role: 'UI/UX Tasarımcı',
    image: 'https://via.placeholder.com/150',
    bio: 'Kullanıcı deneyimi ve arayüz tasarımı konusunda uzmanlaşmıştır.'
  },
  {
    name: 'Mehmet Demir',
    role: 'İş Analisti',
    image: 'https://via.placeholder.com/150',
    bio: 'İş gereksinimlerinin analizi ve çözüm önerileri konusunda uzmandır.'
  }
];

export function About() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative bg-primary-700">
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gray-900 opacity-50" />
        </div>
        <div className="relative max-w-7xl mx-auto py-24 px-4 sm:py-32 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">Hakkımızda</h1>
          <p className="mt-6 max-w-3xl text-xl text-primary-100">
            TSG Platform olarak amacımız, modern teknolojiler kullanarak iş süreçlerinizi kolaylaştırmak ve verimliliğinizi artırmaktır.
          </p>
        </div>
      </div>

      {/* Mission Section */}
      <div className="py-16 bg-white overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 space-y-12 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-3 lg:gap-8 lg:items-start">
            <div className="relative">
              <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">Misyonumuz</h2>
              <p className="mt-4 text-lg text-gray-500">
                Müşterilerimize en iyi çözümleri sunarak iş süreçlerini daha verimli hale getirmek ve onların başarısına katkıda bulunmak için buradayız.
              </p>
            </div>
            <div className="mt-12 lg:mt-0 lg:col-span-2">
              <dl className="space-y-10 sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-x-6 sm:gap-y-10 lg:gap-x-8">
                <div className="relative">
                  <dt>
                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Hızlı ve Güvenilir</p>
                  </dt>
                  <dd className="mt-2 ml-16 text-base text-gray-500">
                    En son teknolojileri kullanarak hızlı ve güvenilir çözümler sunuyoruz.
                  </dd>
                </div>
                <div className="relative">
                  <dt>
                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Güvenlik Önceliği</p>
                  </dt>
                  <dd className="mt-2 ml-16 text-base text-gray-500">
                    Veri güvenliği bizim için en öncelikli konulardan biridir.
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>

      {/* Team Section */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">Ekibimiz</h2>
            <p className="mt-4 text-xl text-gray-500">
              Deneyimli ve uzman ekibimizle yanınızdayız.
            </p>
          </div>

          <div className="mt-12 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {teamMembers.map((member) => (
              <div key={member.name} className="pt-6">
                <div className="flow-root bg-white rounded-lg px-6 pb-8">
                  <div className="-mt-6">
                    <div className="flex items-center justify-center">
                      <img
                        className="h-32 w-32 rounded-full ring-4 ring-white"
                        src={member.image}
                        alt={member.name}
                      />
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 text-center">
                      {member.name}
                    </h3>
                    <p className="mt-1 text-base text-primary-600 text-center">{member.role}</p>
                    <p className="mt-3 text-base text-gray-500 text-center">{member.bio}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
          <h2 className="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            <span className="block">Hazır mısınız?</span>
            <span className="block text-primary-600">Hemen başlayın.</span>
          </h2>
          <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
            <div className="inline-flex rounded-md shadow">
              <Link
                to="/contact"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                İletişime Geçin
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
