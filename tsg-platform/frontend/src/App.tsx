import { Routes, Route, Outlet, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

// Layouts
import { MainLayout } from '@/layouts/MainLayout';

// Pages
import { Home } from '@/pages/Home';
import { About } from '@/pages/About';
import { Contact } from '@/pages/Contact';

// Auth Pages
import { Login } from '@/pages/auth/Login';
import { Register } from '@/pages/auth/Register';

// Admin Pages
import AdminPage from '@/app/admin/page';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// App Layout Component
const AppLayout = () => (
  <MainLayout>
    <Outlet />
  </MainLayout>
);

// Simple Route Components
const Dashboard = () => <div className="p-8">Dashboard Page</div>;
const NotFound = () => <div className="p-8">404 - Sayfa Bulunamadı</div>;

// Auth Check Component
const RequireAuth = ({ children }: { children: JSX.Element }) => {
  // Burada gerçek bir auth kontrolü yapılmalı
  const isAuthenticated = true; // Örnek olarak true yapıldı
  
  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  return children;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
        <Toaster position="top-right" />
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/auth/login" element={<Login />} />
            <Route path="/auth/register" element={<Register />} />
            
            {/* Protected Admin Routes */}
            <Route 
              path="/admin" 
              element={
                <RequireAuth>
                  <AdminPage />
                </RequireAuth>
              } 
            />
            
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
    </QueryClientProvider>
  );
}

export default App;
