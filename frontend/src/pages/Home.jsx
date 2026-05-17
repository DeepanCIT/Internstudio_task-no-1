import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'
import RecommendationSection from '../components/RecommendationSection'
import { getRecommendations, getTrending, getNewArrivals } from '../services/api'

export default function Home() {
  const { user } = useAuth()

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">

      {/* Hero */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 md:p-12 text-white mb-10">
        <p className="text-indigo-200 text-sm font-medium mb-2 uppercase tracking-widest">
          AI-Powered Shopping
        </p>
        <h1 className="text-3xl md:text-5xl font-extrabold mb-4 leading-tight">
          Products Picked<br />Just For You
        </h1>
        <p className="text-indigo-100 max-w-lg mb-6">
          Personalised picks adapt to what you browse and buy, helping you discover
          products you'll love.
        </p>
        <Link to="/products" className="bg-white text-indigo-600 font-bold px-6 py-3 rounded-xl hover:bg-indigo-50 transition-colors inline-block">
          Explore Products →
        </Link>
      </div>

      {/* Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
        {[
          { icon: '🤝', title: 'Personalised Picks', desc: 'Suggestions that adapt to your activity' },
          { icon: '📄', title: 'Smart Discovery', desc: 'Find relevant products faster' },
          { icon: '⚡', title: 'Fresh Finds', desc: 'New and trending items in one place' }
        ].map(a => (
          <div key={a.title} className="card p-5 flex gap-4 items-start">
            <span className="text-3xl">{a.icon}</span>
            <div>
              <h3 className="font-semibold text-gray-800 mb-1">{a.title}</h3>
              <p className="text-sm text-gray-500">{a.desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Personalised section (only when logged in) */}
      {user ? (
        <>
          <RecommendationSection
            title="Recommended For You"
            icon="✨"
            badge="For You"
            fetchFn={() => getRecommendations('hybrid', 10)}
            emptyMsg="Browse more products to get personalised recommendations!"
          />
          <RecommendationSection
            title="Based On Your Interests"
            icon="📄"
            fetchFn={() => getRecommendations('cb', 10)}
          />
          <RecommendationSection
            title="Customers Also Bought"
            icon="🤝"
            fetchFn={() => getRecommendations('cf', 10)}
          />
        </>
      ) : (
        <div className="card p-10 text-center mb-10">
          <p className="text-4xl mb-4">🔒</p>
          <h2 className="text-xl font-bold text-gray-800 mb-2">
            Get Personalised Recommendations
          </h2>
          <p className="text-gray-500 mb-6 max-w-md mx-auto">
            Create a free account to get personalised picks and smarter suggestions.
          </p>
          <div className="flex gap-3 justify-center">
            <Link to="/register" className="btn-primary">Sign Up Free</Link>
            <Link to="/login"    className="btn-outline">Login</Link>
          </div>
        </div>
      )}

      {/* Always-visible sections */}
      <RecommendationSection title="Trending Now"   icon="🔥" badge="Trending"     fetchFn={() => getTrending(10)} />
      <RecommendationSection title="New Arrivals"   icon="🆕" badge="New"          fetchFn={() => getNewArrivals(10)} />
    </div>
  )
}
