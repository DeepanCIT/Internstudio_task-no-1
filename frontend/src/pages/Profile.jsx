import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { getBrowseHistory, getRecommendations } from '../services/api'
import ProductCard from '../components/ProductCard'

export default function Profile() {
  const { user } = useAuth()
  const [history, setHistory] = useState([])
  const [recs,    setRecs]    = useState([])
  const [tab,     setTab]     = useState('recs')

  useEffect(() => {
    getBrowseHistory().then(r => setHistory(r.data))
    getRecommendations('hybrid', 8).then(r => setRecs(r.data.recommendations || []))
  }, [])

  if (!user) return null

  const tabs = [
    { id: 'recs',    label: '✨ For You' },
    { id: 'history', label: '👁 Browsed' },
  ]

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Profile header */}
      <div className="card p-6 flex gap-5 items-center mb-8">
        <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center text-3xl font-extrabold text-indigo-600">
          {user.username[0].toUpperCase()}
        </div>
        <div>
          <h1 className="text-2xl font-extrabold text-gray-900">{user.username}</h1>
          <p className="text-gray-500 text-sm">{user.email}</p>
          <div className="flex gap-3 mt-2 text-sm text-gray-400">
            {user.age      && <span>🎂 {user.age} yrs</span>}
            {user.gender   && <span>👤 {user.gender}</span>}
            {user.location && <span>📍 {user.location}</span>}
          </div>
        </div>
        <div className="ml-auto text-center">
          <p className="text-xs text-gray-400 uppercase tracking-wide">Recommendations</p>
          <span className="inline-block mt-1 bg-indigo-100 text-indigo-700 text-xs font-bold px-3 py-1 rounded-full">
            ⚡ Personalised
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`px-5 py-2 rounded-full text-sm font-semibold transition-colors ${
              tab === t.id ? 'bg-indigo-500 text-white' : 'bg-white text-gray-600 border hover:bg-gray-50'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'recs' && (
        <div>
          <p className="text-sm text-gray-500 mb-4">
            Personalised for you using your browsing history and purchase patterns.
          </p>
          {recs.length ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {recs.map(p => <ProductCard key={p.id} product={p} badge="For You"/>)}
            </div>
          ) : (
            <p className="text-gray-400">Browse and rate more products to get recommendations!</p>
          )}
        </div>
      )}

      {tab === 'history' && (
        <div>
          <p className="text-sm text-gray-500 mb-4">Products you've recently viewed</p>
          {history.length ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {history.map(p => <ProductCard key={p.id} product={p}/>)}
            </div>
          ) : (
            <p className="text-gray-400">No browsing history yet. Start exploring!</p>
          )}
        </div>
      )}
    </div>
  )
}
