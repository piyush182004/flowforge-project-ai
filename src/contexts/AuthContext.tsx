import { createContext, useContext, useEffect, useState } from 'react';
import { CivicAuthProvider as CivicProvider, useUser } from '@civic/auth/react';
import { useNavigate } from 'react-router-dom';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: any; // Using any for now, update to proper Civic user type if available
  signIn: () => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const { user, isLoading: authLoading, signIn: civicSignIn, signOut: civicSignOut } = useUser();
  const [isInitialized, setIsInitialized] = useState(false);

  // Handle auth state changes
  useEffect(() => {
    if (!authLoading) {
      setIsInitialized(true);
      
      // Redirect if needed based on auth state
      if (user && window.location.pathname === '/login') {
        navigate('/');
      }
    }
  }, [user, authLoading, navigate]);

  const value: AuthContextType = {
    isAuthenticated: !!user,
    isLoading: authLoading || !isInitialized,
    user,
    signIn: civicSignIn,
    signOut: async () => {
      await civicSignOut();
      navigate('/login');
    }
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Export the Civic provider with a different name to avoid conflicts
export const CivicAuthProvider = CivicProvider;
