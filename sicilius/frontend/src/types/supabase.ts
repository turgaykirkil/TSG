export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string | null
          name: string | null
          role: string
          created_at: string
          updated_at: string | null
        }
        Insert: {
          id?: string
          email?: string | null
          name?: string | null
          role?: string
          created_at?: string
          updated_at?: string | null
        }
        Update: {
          id?: string
          email?: string | null
          name?: string | null
          role?: string
          created_at?: string
          updated_at?: string | null
        }
      }
      // Diğer tabloları buraya ekleyebilirsiniz
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

// Auth user tipi
export type User = {
  id: string
  email?: string | null
  name?: string | null
  image?: string | null
  user_metadata?: {
    full_name?: string | null
    avatar_url?: string | null
  }
  app_metadata?: {
    provider?: string
    [key: string]: unknown
  }
  created_at?: string
  updated_at?: string | null
  role?: string
}

export type UserProfile = Database['public']['Tables']['users']['Row']
