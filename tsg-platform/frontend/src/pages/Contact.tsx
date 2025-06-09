import { useState } from 'react';
import { EnvelopeIcon, MapPinIcon, PhoneIcon } from '@heroicons/react/24/outline';

type FormData = {
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
};

type ContactInfo = {
  icon: React.ReactNode;
  title: string;
  description: string;
};

export function Contact() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });

  const contactInfo: ContactInfo[] = [
    {
      icon: <MapPinIcon className="h-6 w-6 text-primary-600" />,
      title: 'Adres',
      description: 'İstanbul, Türkiye'
    },
    {
      icon: <PhoneIcon className="h-6 w-6 text-primary-600" />,
      title: 'Telefon',
      description: '+90 (555) 123 45 67'
    },
    {
      icon: <EnvelopeIcon className="h-6 w-6 text-primary-600" />,
      title: 'E-posta',
      description: 'info@tsgplatform.com'
    }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form gönderildi:', formData);
    setFormData({
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: ''
    });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative bg-primary-700">
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gray-900 opacity-50" />
        </div>
        <div className="relative max-w-7xl mx-auto py-24 px-4 sm:py-32 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">
            İletişim
          </h1>
          <p className="mt-6 max-w-3xl mx-auto text-xl text-primary-100">
            Sorularınız veya geri bildirimleriniz için lütfen bizimle iletişime geçin.
          </p>
        </div>
      </div>

      {/* Contact Info */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-12 lg:grid-cols-3">
            {contactInfo.map((item, index) => (
              <div key={index} className="text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-100 text-primary-600 mx-auto">
                  {item.icon}
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900">{item.title}</h3>
                <p className="mt-1 text-base text-gray-500">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Contact Form */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow rounded-lg p-8">
            <div className="max-w-2xl mx-auto">
              <h2 className="text-2xl font-extrabold text-gray-900 sm:text-3xl">Bize Ulaşın</h2>
              <p className="mt-3 text-lg text-gray-500">
                Formu doldurarak bize ulaşabilir veya yukarıdaki iletişim bilgilerimizden bize ulaşabilirsiniz.
              </p>
              
              <form onSubmit={handleSubmit} className="mt-8 space-y-6">
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                      Ad Soyad <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      name="name"
                      id="name"
                      autoComplete="name"
                      required
                      value={formData.name}
                      onChange={handleChange}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                      E-posta <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="email"
                      name="email"
                      id="email"
                      autoComplete="email"
                      required
                      value={formData.email}
                      onChange={handleChange}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                      Telefon
                    </label>
                    <input
                      type="tel"
                      name="phone"
                      id="phone"
                      autoComplete="tel"
                      value={formData.phone}
                      onChange={handleChange}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label htmlFor="subject" className="block text-sm font-medium text-gray-700">
                      Konu <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      name="subject"
                      id="subject"
                      required
                      value={formData.subject}
                      onChange={handleChange}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700">
                    Mesajınız <span className="text-red-500">*</span>
                  </label>
                  <div className="mt-1">
                    <textarea
                      id="message"
                      name="message"
                      rows={4}
                      required
                      value={formData.message}
                      onChange={handleChange}
                      className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                </div>

                <div className="flex justify-end">
                  <button
                    type="submit"
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Gönder
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      {/* Map Section */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
          <div className="bg-gray-200 rounded-lg overflow-hidden h-96">
            <iframe
              width="100%"
              height="100%"
              frameBorder="0"
              scrolling="no"
              marginHeight={0}
              marginWidth={0}
              src="https://maps.google.com/maps?q=Istanbul&t=&z=13&ie=UTF8&iwloc=&output=embed"
              title="Haritada Konumumuz"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
