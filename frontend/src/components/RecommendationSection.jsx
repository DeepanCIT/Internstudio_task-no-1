import { useEffect, useState } from 'react'
import ProductCard from './ProductCard'

export default function RecommendationSection({ title, badge, fetchFn, emptyMsg, icon }) {
  const [products, setProducts] = useState([])
  const [loading,  setLoading]  = useState(true)

  useEffect(() => {
    fetchFn()
      .then(res => setProducts(res.data?.recommendations ?? res.data ?? []))
      .catch(() => setProducts([]))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <section className="my-10">
      <div className="flex items-center gap-2 mb-4">
        {icon && <span className="text-2xl">{icon}</span>}
        <h2 className="text-xl font-bold text-gray-800">{title}</h2>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        {Array.from({length: 5}).map((_,i) => (
          <div key={i} className="card animate-pulse h-72 bg-gray-100" />
        ))}
      </div>
    </section>
  )

  if (!products.length) return (
    <section className="my-10">
      <div className="flex items-center gap-2 mb-4">
        {icon && <span className="text-2xl">{icon}</span>}
        <h2 className="text-xl font-bold text-gray-800">{title}</h2>
      </div>
      <p className="text-gray-400 text-sm">{emptyMsg || 'No items to show.'}</p>
    </section>
  )

  return (
    <section className="my-10">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          {icon && <span className="text-2xl">{icon}</span>}
          <h2 className="text-xl font-bold text-gray-800">{title}</h2>
        </div>
        <span className="text-sm text-gray-400">{products.length} items</span>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        {products.map(p => <ProductCard key={p.id} product={p} badge={badge} />)}
      </div>
    </section>
  )
}
