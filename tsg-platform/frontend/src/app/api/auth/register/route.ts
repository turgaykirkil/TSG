import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { User } from '@supabase/supabase-js';
import { supabaseAdmin } from '@/lib/supabase-admin';


// Define a more specific type for user profile that matches our database schema
type UserProfile = {
  id: string;
  email: string;
  name?: string | null;
  full_name?: string;
  role: string;
  created_at: string;
  updated_at: string | null;
};



export async function POST(request: NextRequest) {
  let authData: { user: User } | null = null;
  
  try {
    const { email, password, name } = await request.json();

    // Input validation
    if (!email || !password || !name) {
      return NextResponse.json(
        { error: 'E-posta, şifre ve isim alanları zorunludur' },
        { status: 400 }
      );
    }

    // Check if user already exists in public.users
    console.log('Checking for existing user...');
    
    const { data: existingUser, error: userCheckError } = await supabaseAdmin
      .from('users')
      .select('id')
      .eq('email', email)
      .maybeSingle();
    
    if (userCheckError) {
      console.error('Error checking existing user:', userCheckError);
      throw new Error('Kullanıcı kontrolü sırasında hata oluştu');
    }
    
    if (existingUser) {
      console.log('User with this email already exists in public.users');
      return NextResponse.json(
        { error: 'Bu e-posta adresi zaten kullanımda' },
        { status: 400 }
      );
    }

    // Create user in auth.users
    console.log('Creating user in auth.users table...');
    const { data: authResponse, error: authError } = await supabaseAdmin.auth.admin.createUser({
      email,
      password,
      email_confirm: true, // Skip email confirmation for now
      user_metadata: { full_name: name },
    });
    
    if (authError) {
      console.error('Auth user creation error:', authError);
      throw new Error('Kullanıcı oluşturulurken hata oluştu');
    }
    
    if (!authResponse?.user) {
      console.error('No user data returned from auth create');
      throw new Error('Kullanıcı oluşturulurken bilinmeyen bir hata oluştu');
    }
    
    authData = { user: authResponse.user };
    
    console.log('Auth user created successfully:', {
      id: authData.user.id,
      email: authData.user.email,
      email_confirmed: authData.user.email_confirmed_at !== null,
    });
    
    // Create user profile in public.users using RLS bypass
    console.log('Creating user profile in public.users...');
    if (!authData?.user) {
      throw new Error('Kullanıcı bilgileri alınamadı');
    }

    const userProfile: UserProfile = {
      id: authData.user.id,
      email: authData.user.email || email,
      name: name, // Some databases use 'name' instead of 'full_name'
      full_name: name, // We'll store in both fields for compatibility
      role: 'user',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    // Use RLS bypass with explicit schema
    const { data: profileData, error: profileError } = await supabaseAdmin
      .schema('public')
      .from('users')
      .insert(userProfile)
      .select()
      .single();
      
    if (profileError) {
      console.error('Profile creation error:', profileError);
      
      // Attempt to clean up the auth user if profile creation fails
      try {
        await supabaseAdmin.auth.admin.deleteUser(authData.user.id);
        console.log('Cleaned up auth user after profile creation failure');
      } catch (cleanupError) {
        console.error('Error cleaning up auth user:', cleanupError);
      }
      
      throw new Error('Profil oluşturulurken hata oluştu');
    }
    
    if (!profileData) {
      console.error('No profile data returned after creation');
      throw new Error('Profil oluşturulurken bilinmeyen bir hata oluştu');
    }

    console.log('User profile created successfully:', profileData);
    
    // If we get here, both auth and profile creation were successful
    return NextResponse.json(
      { 
        message: 'Kayıt başarılı', 
        user: {
          id: profileData.id,
          email: profileData.email,
          name: profileData.full_name,
          role: profileData.role,
        } 
      },
      { status: 201 }
    );
    
  } catch (error) {
    console.error('Registration error:', error);
    
    // Attempt to clean up any created resources
    if (authData?.user?.id) {
      try {
        await supabaseAdmin.auth.admin.deleteUser(authData.user.id);
        console.log('Cleaned up auth user after registration failure');
      } catch (cleanupError) {
        console.error('Error cleaning up auth user:', cleanupError);
      }
    }
    
    return NextResponse.json(
      { 
        error: 'Kayıt işlemi sırasında bir hata oluştu',
        details: error instanceof Error ? error.message : 'Bilinmeyen hata'
      },
      { status: 500 }
    );
  }
}

// POST fonksiyonu zaten yukarıda export edilmiş durumda
