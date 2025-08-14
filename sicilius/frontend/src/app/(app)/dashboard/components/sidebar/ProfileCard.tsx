'use client';

import { useAuth } from '@/contexts/AuthContext';

export default function ProfileCard() {
  const { session, logout } = useAuth();
  const user = session.user;

  return (
    <div className="flex items-center gap-3">
      <div className="h-9 w-9 shrink-0 rounded-full bg-gradient-to-br from-blue-600 to-cyan-500 text-white grid place-content-center font-semibold">
        {user?.name?.charAt(0)?.toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || 'U'}
      </div>
      <div className="min-w-0">
        <div className="text-sm font-medium text-slate-800 truncate">{user?.name || 'Kullanıcı'}</div>
        <div className="text-xs text-slate-500 truncate">{user?.email || '—'}</div>
      </div>
      <div className="ml-auto">
        <button
          type="button"
          onClick={logout}
          className="text-xs rounded-full px-3 py-1 bg-slate-800 text-white hover:opacity-90"
        >
          Çıkış
        </button>
      </div>
    </div>
  );
}
