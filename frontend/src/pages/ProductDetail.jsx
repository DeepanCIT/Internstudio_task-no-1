import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getProduct, getSimilar, addToCart, rateProduct, recordBrowse } from '../services/api'
import { useAuth } from '../context/AuthContext'
import ProductCard from '../components/ProductCard'
import { buildImagePlaceholder } from '../utils/imagePlaceholder'
import toast from 'react-hot-toast'

function Stars({ value, onChange }) {
  const [hover, setHover] = useState(0)
  return (
    <div className="flex gap-1">
      {[1,2,3,4,5].map(i => (
        <button key={i}
          onMouseEnter={() => setHover(i)} onMouseLeave={() => setHover(0)}
          onClick={() => onChange(i)}
          className={`text-2xl ${i <= (hover || value) ? 'text-amber-400' : 'text-gray-300'} transition-colors`}>
          ★
        </button>
      ))}
    </div>
  )
}

export default function ProductDetail() {
  const { id } = useParams()
  const { user } = useAuth()

  const [product, setProduct]   = useState(null)
  const [similar, setSimilar]   = useState([])
  const [loading, setLoading]   = useState(true)
  const [qty,     setQty]       = useState(1)
  const [userRating, setUserRating] = useState(0)
  const [review,  setReview]    = useState('')
  const [ratingSubmitting, setRatingSubmitting] = useState(false)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      getProduct(id),
      getSimilar(id, 8)
    ]).then(([prodRes, simRes]) => {
      setProduct(prodRes.data)
      setSimilar(simRes.data)
    }).finally(() => setLoading(false))

    // Record browse event (fire & forget)
    if (user) {
      setTimeout(() => recordBrowse(parseInt(id), 30).catch(() => {}), 2000)
    }
  }, [id])

  const handleAddToCart = async () => {
    if (!user) { toast.error('Please login'); return }
    try {
      await addToCart(parseInt(id), qty)
      toast.success('Added to cart!')
    } catch {
      toast.error('Could not add to cart')
    }
  }

  const handleRating = async () => {
    if (!user) { toast.error('Please login to rate'); return }
    if (!userRating) { toast.error('Select a star rating'); return }
    setRatingSubmitting(true)
    try {
      await rateProduct(parseInt(id), userRating, review)
      toast.success('Rating submitted! Recommendations updated.')
      const refreshed = await getProduct(id)
      setProduct(refreshed.data)
    } catch {
      toast.error('Could not submit rating')
    } finally {
      setRatingSubmitting(false)
    }
  }

  if (loading) return (
    <div className="max-w-5xl mx-auto px-4 py-10 animate-pulse">
      <div className="flex gap-8">
        <div className="w-96 h-96 bg-gray-200 rounded-xl"/>
        <div className="flex-1 space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3"/>
          <div className="h-10 bg-gray-200 rounded w-2/3"/>
          <div className="h-4 bg-gray-200 rounded w-full"/>
          <div className="h-4 bg-gray-200 rounded w-5/6"/>
        </div>
      </div>
    </div>
  )

  if (!product) return <div className="text-center py-20 text-gray-400">Product not found</div>

  const placeholder = buildImagePlaceholder(product)

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Main product */}
      <div className="card p-6 flex flex-col md:flex-row gap-8 mb-12">
        <img src={product.image_url || placeholder} alt={product.name}
          onError={event => {
            event.currentTarget.onerror = null
            event.currentTarget.src = placeholder
          }}
          className="w-full md:w-80 h-80 object-cover rounded-xl"/>

        <div className="flex-1">
          <p className="text-indigo-500 text-sm font-semibold uppercase mb-1">
            {product.category} › {product.subcategory}
          </p>
          <h1 className="text-2xl font-extrabold text-gray-900 mb-2">{product.name}</h1>
          <div className="flex items-center gap-3 mb-4">
            <div className="flex">
              {[1,2,3,4,5].map(i => (
                <span key={i} className={`text-xl ${i <= Math.round(product.avg_rating) ? 'text-amber-400' : 'text-gray-300'}`}>★</span>
              ))}
            </div>
            <span className="text-sm text-gray-500">
              {product.avg_rating?.toFixed(1)} ({product.reviews_count?.toLocaleString()} reviews)
            </span>
          </div>

          <p className="text-gray-600 leading-relaxed mb-6">{product.description}</p>

          <p className="text-3xl font-bold text-gray-900 mb-6">${product.price?.toFixed(2)}</p>

          <div className="flex items-center gap-4 mb-6">
            <div className="flex items-center border border-gray-200 rounded-lg overflow-hidden">
              <button onClick={() => setQty(q => Math.max(1, q-1))} className="px-3 py-2 hover:bg-gray-100">−</button>
              <span className="px-4 py-2 font-semibold">{qty}</span>
              <button onClick={() => setQty(q => q+1)} className="px-3 py-2 hover:bg-gray-100">+</button>
            </div>
            <button onClick={handleAddToCart} className="btn-primary flex-1">
              🛒 Add to Cart
            </button>
          </div>

          <div className="flex flex-wrap gap-2">
            {product.tags?.map(t => (
              <span key={t} className="text-xs bg-gray-100 text-gray-600 px-3 py-1 rounded-full">{t}</span>
            ))}
          </div>
        </div>
      </div>

      {/* Rate this product */}
      {user && (
        <div className="card p-6 mb-12">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Rate This Product</h2>
          <Stars value={userRating} onChange={setUserRating}/>
          <textarea
            value={review} onChange={e => setReview(e.target.value)}
            placeholder="Write a short review (optional)…"
            className="input mt-3 h-24 resize-none"
          />
          <button onClick={handleRating} disabled={ratingSubmitting}
            className="btn-primary mt-3">
            {ratingSubmitting ? 'Submitting…' : 'Submit Rating'}
          </button>
          <p className="text-xs text-gray-400 mt-2">
            Your rating helps personalise future suggestions.
          </p>
        </div>
      )}

      {/* Similar products */}
      {similar.length > 0 && (
        <section>
          <h2 className="text-xl font-bold text-gray-800 mb-4">Similar Products</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {similar.map(p => <ProductCard key={p.id} product={p} badge="Similar"/>)}
          </div>
        </section>
      )}
    </div>
  )
}
