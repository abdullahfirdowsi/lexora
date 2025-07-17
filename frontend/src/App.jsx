import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/layout/Layout';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import Dashboard from './pages/Dashboard';
import './App.css';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Public Route Component (redirect to dashboard if authenticated)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  return isAuthenticated ? <Navigate to="/dashboard" /> : children;
};

// Landing Page Component
const LandingPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-center min-h-screen text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6">
            Welcome to <span className="text-primary">Lexora</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl">
            AI-Powered Learning Platform with Personalized Narrated Lessons.
            Create structured learning paths and generate lifelike video content.
          </p>
          <div className="space-x-4">
            <button className="bg-primary text-primary-foreground px-6 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors">
              Get Started
            </button>
            <button className="border border-border text-foreground px-6 py-3 rounded-lg font-medium hover:bg-accent transition-colors">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

function AppContent() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route 
          path="/" 
          element={
            <PublicRoute>
              <Layout>
                <LandingPage />
              </Layout>
            </PublicRoute>
          } 
        />
        <Route 
          path="/login" 
          element={
            <PublicRoute>
              <LoginForm />
            </PublicRoute>
          } 
        />
        <Route 
          path="/register" 
          element={
            <PublicRoute>
              <RegisterForm />
            </PublicRoute>
          } 
        />

        {/* Protected Routes */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          } 
        />
        
        {/* Placeholder routes for future pages */}
        <Route 
          path="/topics" 
          element={
            <ProtectedRoute>
              <Layout>
                <div className="p-6">
                  <h1 className="text-2xl font-bold">Topics</h1>
                  <p className="text-muted-foreground">Topics page coming soon...</p>
                </div>
              </Layout>
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/learning-paths" 
          element={
            <ProtectedRoute>
              <Layout>
                <div className="p-6">
                  <h1 className="text-2xl font-bold">Learning Paths</h1>
                  <p className="text-muted-foreground">Learning paths page coming soon...</p>
                </div>
              </Layout>
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/videos" 
          element={
            <ProtectedRoute>
              <Layout>
                <div className="p-6">
                  <h1 className="text-2xl font-bold">Videos</h1>
                  <p className="text-muted-foreground">Videos page coming soon...</p>
                </div>
              </Layout>
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/settings" 
          element={
            <ProtectedRoute>
              <Layout>
                <div className="p-6">
                  <h1 className="text-2xl font-bold">Settings</h1>
                  <p className="text-muted-foreground">Settings page coming soon...</p>
                </div>
              </Layout>
            </ProtectedRoute>
          } 
        />

        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
