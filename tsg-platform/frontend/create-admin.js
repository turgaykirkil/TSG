import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

(async () => {
  const { data, error } = await supabase.auth.admin.createUser({
    email: 'turgaykirkil@me.com',
    password: 'GucluParola123!',
    email_confirm: true,
    user_metadata: { role: 'admin' }
  });

  if (error) {
    console.error('Auth createUser error:', error);
    process.exit(1);
  }

  // public.users tablosuna da rol kaydı
  await supabase.from('users').upsert({
    id: data.user?.id,
    email: data.user?.email,
    role: 'admin',
    name: 'Turgay'
  });

  console.log('Admin user created with id:', data.user?.id);
  process.exit(0);
})();
