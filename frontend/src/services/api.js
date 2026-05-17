import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

// Attach JWT token to every request
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auth
export const register = (data)         => api.post('/auth/register', data)
export const login    = (data)         => api.post('/auth/login', data)
export const getMe    = ()             => api.get('/auth/me')

// Products
export const getProducts   = (params)  => api.get('/products', { params })
export const getProduct    = (id)      => api.get(`/products/${id}`)
export const getCategories = ()        => api.get('/products/categories')

// Browsing
export const recordBrowse  = (product_id, duration = 0) =>
  api.post('/browse', { product_id, duration })
export const getBrowseHistory = () => api.get('/browse/history')

// Ratings
export const rateProduct = (product_id, rating, review = '') =>
  api.post('/ratings', { product_id, rating, review })

// Cart
export const getCart        = ()             => api.get('/cart')
export const addToCart      = (product_id, quantity = 1) =>
  api.post('/cart', { product_id, quantity })
export const removeFromCart = (item_id)      => api.delete(`/cart/${item_id}`)
export const checkout       = ()             => api.post('/cart/checkout')

// Recommendations
export const getRecommendations = (method = 'hybrid', n = 12) =>
  api.get('/recommendations', { params: { method, n } })
export const getSimilar         = (product_id, n = 8) =>
  api.get(`/recommendations/similar/${product_id}`, { params: { n } })
export const getTrending        = (n = 10)   => api.get('/recommendations/trending', { params: { n } })
export const getNewArrivals     = (n = 10)   => api.get('/recommendations/new-arrivals', { params: { n } })

export default api
