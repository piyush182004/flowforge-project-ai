import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { AuthProvider, CivicAuthProvider } from './contexts/AuthContext'
import { BrowserRouter as Router } from 'react-router-dom'

// Using VITE_CIVIC_CLIENT_ID from environment variables
// Make sure to set this in your .env file
const CIVIC_CLIENT_ID = import.meta.env.VITE_CIVIC_CLIENT_ID || 
  'd9cf379d-36a6-4a2a-a347-cd9940e5589d' // Fallback ID from current implementation

createRoot(document.getElementById("root")!).render(
  <CivicAuthProvider clientId={CIVIC_CLIENT_ID}>
    <Router>
      <AuthProvider>
        <App />
      </AuthProvider>
    </Router>
  </CivicAuthProvider>
);
