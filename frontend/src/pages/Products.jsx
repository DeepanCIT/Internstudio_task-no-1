import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { getProducts, getCategories } from '../services/api'
import ProductCard from '../components/ProductCard'

export default function Products() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [products,   setProducts]   = useState([])
  const [categories, setCategories] = useState([])
  const [total,      setTotal]      = useState(0)
  const [loading,    setLoading]    = useState(false)
  const [page,       setPage]       = useState(1)

  const category = searchParams.get('category') || ''
  const search   = searchParams.get('search')   || ''

  useEffect(() => {
    getCategories().then(r => setCategories(r.data))
  }, [])

  useEffect(() => {
    setLoading(true)
    setPage(1)
    getProducts({ page: 1, per_page: 20, category, search })
      .then(r => { setProducts(r.data.products); setTotal(r.data.total) })
      .finally(() => setLoading(false))
  }, [category, search])

  const loadMore = () => {
    const next = page + 1
    setLoading(true)
    getProducts({ page: next, per_page: 20, category, search })
      .then(r => { setProducts(prev => [...prev, ...r.data.products]); setPage(next) })
      .finally(() => setLoading(false))
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 flex gap-6">
      {/* Sidebar */}
      <aside className="hidden md:block w-48 shrink-0">
        <h3 className="font-semibold text-gray-700 mb-3 text-sm uppercase tracking-wide">Category</h3>
        <ul className="space-y-1">
          <li>
            <button onClick={() => setSearchParams({})}
              className={`text-sm w-full text-left px-3 py-1.5 rounded-lg ${!category ? 'bg-indigo-100 text-indigo-700 font-semibold' : 'text-gray-600 hover:bg-gray-100'}`}>
              All Products
            </button>
          </li>
          {categories.map(cat => (
            <li key={cat}>
              <button onClick={() => setSearchParams({ category: cat })}
                className={`text-sm w-full text-left px-3 py-1.5 rounded-lg ${category === cat ? 'bg-indigo-100 text-indigo-700 font-semibold' : 'text-gray-600 hover:bg-gray-100'}`}>
                {cat}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      {/* Main */}
      <div className="flex-1">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-bold text-gray-800">
            {search ? `Results for "${search}"` : category || 'All Products'}
          </h1>
          <span className="text-sm text-gray-500">{total} products</span>
        </div>

        {loading && products.length === 0 ? (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {Array.from({length: 8}).map((_,i) => (
              <div key={i} className="card animate-pulse h-72 bg-gray-100"/>
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-5xl mb-4">🔍</p>
            <p className="text-gray-500">No products found.</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {products.map(p => <ProductCard key={p.id} product={p}/>)}
            </div>
            {products.length < total && (
              <div className="text-center mt-8">
                <button onClick={loadMore} disabled={loading}
                  className="btn-outline px-8">
                  {loading ? 'Loading…' : 'Load More'}
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
