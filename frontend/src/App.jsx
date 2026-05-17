import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider, useAuth } from './context/AuthContext'
import Navbar from './components/Navbar'
import Home          from './pages/Home'
import Products      from './pages/Products'
import ProductDetail from './pages/ProductDetail'
import Login         from './pages/Login'
import Register      from './pages/Register'
import Cart          from './pages/Cart'
import Profile       from './pages/Profile'

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="text-center py-20 text-gray-400">Loading…</div>
  return user ? children : <Navigate to="/login" replace/>
}

function AppRoutes() {
  return (
    <>
      <Navbar/>
      <main>
        <Routes>
          <Route path="/"               element={<Home/>}/>
          <Route path="/products"       element={<Products/>}/>
          <Route path="/products/:id"   element={<ProductDetail/>}/>
          <Route path="/login"          element={<Login/>}/>
          <Route path="/register"       element={<Register/>}/>
          <Route path="/cart"           element={<ProtectedRoute><Cart/></ProtectedRoute>}/>
          <Route path="/profile"        element={<ProtectedRoute><Profile/></ProtectedRoute>}/>
          <Route path="*"               element={<Navigate to="/" replace/>}/>
        </Routes>
      </main>
      <Toaster position="top-right" toastOptions={{ style: { borderRadius: '10px' } }}/>
    </>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes/>
      </BrowserRouter>
    </AuthProvider>
  )
}
