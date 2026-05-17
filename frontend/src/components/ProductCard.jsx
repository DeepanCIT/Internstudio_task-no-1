import { Link } from 'react-router-dom'
import { addToCart } from '../services/api'
import toast from 'react-hot-toast'
import { useAuth } from '../context/AuthContext'
import { buildImagePlaceholder } from '../utils/imagePlaceholder'

function StarRating({ rating }) {
  return (
    <div className="flex items-center gap-1">
      {[1,2,3,4,5].map(i => (
        <svg key={i} className={`w-3.5 h-3.5 ${i <= Math.round(rating) ? 'text-amber-400' : 'text-gray-300'}`}
          fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        </svg>
      ))}
      <span className="text-xs text-gray-500 ml-1">{rating?.toFixed(1)}</span>
    </div>
  )
}

export default function ProductCard({ product, badge }) {
  const { user } = useAuth()
  const placeholder = buildImagePlaceholder(product)

  const handleAddToCart = async e => {
    e.preventDefault()
    e.stopPropagation()
    if (!user) { toast.error('Please login to add to cart'); return }
    try {
      await addToCart(product.id)
      toast.success('Added to cart!')
    } catch {
      toast.error('Could not add to cart')
    }
  }

  return (
    <Link to={`/products/${product.id}`} className="card group block overflow-hidden">
      <div className="relative">
        {badge && (
          <span className="absolute top-2 left-2 z-10 bg-indigo-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
            {badge}
          </span>
        )}
        <img
          src={product.image_url || placeholder}
          alt={product.name}
          onError={event => {
            event.currentTarget.onerror = null
            event.currentTarget.src = placeholder
          }}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>

      <div className="p-4">
        <p className="text-xs text-indigo-500 font-medium uppercase tracking-wide mb-1">
          {product.category}
        </p>
        <h3 className="font-semibold text-gray-800 text-sm leading-snug line-clamp-2 mb-2 group-hover:text-indigo-600 transition-colors">
          {product.name}
        </h3>
        <StarRating rating={product.avg_rating} />
        <p className="text-xs text-gray-400 mt-0.5 mb-3">
          {product.reviews_count?.toLocaleString()} reviews
        </p>

        <div className="flex items-center justify-between mt-auto">
          <span className="text-lg font-bold text-gray-900">
            ${product.price?.toFixed(2)}
          </span>
          <button
            onClick={handleAddToCart}
            className="bg-indigo-500 hover:bg-indigo-600 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors"
          >
            + Cart
          </button>
        </div>

        {product.tags?.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-3">
            {product.tags.slice(0, 3).map(tag => (
              <span key={tag} className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </Link>
  )
}
