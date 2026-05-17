import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getCart, removeFromCart, checkout } from '../services/api'
import toast from 'react-hot-toast'

export default function Cart() {
  const [items,   setItems]   = useState([])
  const [loading, setLoading] = useState(true)

  const fetchCart = () => {
    setLoading(true)
    getCart()
      .then(r => setItems(r.data))
      .finally(() => setLoading(false))
  }

  useEffect(fetchCart, [])

  const handleRemove = async id => {
    await removeFromCart(id)
    fetchCart()
    toast.success('Removed from cart')
  }

  const handleCheckout = async () => {
    try {
      await checkout()
      setItems([])
      toast.success('🎉 Order placed successfully!')
    } catch {
      toast.error('Checkout failed')
    }
  }

  const total = items.reduce((s, i) => s + i.product.price * i.quantity, 0)

  if (loading) return <div className="text-center py-20 text-gray-400">Loading cart…</div>

  if (!items.length) return (
    <div className="max-w-lg mx-auto text-center py-20">
      <p className="text-6xl mb-4">🛒</p>
      <h2 className="text-xl font-bold text-gray-800 mb-2">Your cart is empty</h2>
      <Link to="/products" className="btn-primary mt-4 inline-block">Start Shopping</Link>
    </div>
  )

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-extrabold text-gray-900 mb-6">Your Cart</h1>
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-4">
          {items.map(item => (
            <div key={item.id} className="card p-4 flex gap-4 items-center">
              <img src={item.product.image_url} alt={item.product.name}
                className="w-20 h-20 object-cover rounded-lg"/>
              <div className="flex-1">
                <Link to={`/products/${item.product.id}`}
                  className="font-semibold text-gray-800 hover:text-indigo-600 text-sm">
                  {item.product.name}
                </Link>
                <p className="text-xs text-gray-400 mt-0.5">{item.product.brand}</p>
                <p className="text-sm font-bold text-gray-900 mt-1">
                  ${item.product.price.toFixed(2)} × {item.quantity}
                </p>
              </div>
              <button onClick={() => handleRemove(item.id)}
                className="text-red-400 hover:text-red-600 transition-colors p-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          ))}
        </div>

        <div className="card p-6 h-fit">
          <h3 className="font-bold text-gray-800 mb-4">Order Summary</h3>
          <div className="space-y-2 text-sm mb-4">
            {items.map(i => (
              <div key={i.id} className="flex justify-between text-gray-600">
                <span className="truncate max-w-[150px]">{i.product.name}</span>
                <span>${(i.product.price * i.quantity).toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="border-t pt-3 flex justify-between font-bold text-gray-900">
            <span>Total</span>
            <span>${total.toFixed(2)}</span>
          </div>
          <button onClick={handleCheckout} className="btn-primary w-full mt-4 py-3">
            Place Order
          </button>
        </div>
      </div>
    </div>
  )
}
