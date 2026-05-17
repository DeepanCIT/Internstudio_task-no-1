const clampText = (value, max) => {
  const text = String(value || '').trim()
  if (!text) return ''
  if (text.length <= max) return text
  return `${text.slice(0, Math.max(0, max - 3))}...`
}

const ICONS = {
  headphones: `
    <path d="M120 150 C140 90 260 90 280 150" stroke="#4f46e5" stroke-width="12" fill="none" stroke-linecap="round" />
    <rect x="105" y="150" width="48" height="78" rx="18" fill="#818cf8" />
    <rect x="247" y="150" width="48" height="78" rx="18" fill="#818cf8" />
  `,
  tablet: `
    <rect x="140" y="90" width="120" height="190" rx="18" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <circle cx="200" cy="255" r="6" fill="#4f46e5" />
  `,
  tv: `
    <rect x="110" y="110" width="180" height="120" rx="10" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="170" y="235" width="60" height="16" rx="8" fill="#4f46e5" />
  `,
  mouse: `
    <rect x="160" y="110" width="80" height="140" rx="36" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="195" y="125" width="10" height="24" rx="5" fill="#4f46e5" />
  `,
  laptop: `
    <rect x="110" y="100" width="180" height="120" rx="10" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="90" y="225" width="220" height="24" rx="12" fill="#4f46e5" />
  `,
  powerbank: `
    <rect x="160" y="90" width="80" height="190" rx="18" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <circle cx="200" cy="120" r="6" fill="#4f46e5" />
    <rect x="185" y="240" width="30" height="8" rx="4" fill="#4f46e5" />
  `,
  camera: `
    <rect x="120" y="130" width="160" height="100" rx="16" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <circle cx="200" cy="180" r="34" fill="#e0e7ff" stroke="#4f46e5" stroke-width="6" />
    <rect x="150" y="110" width="60" height="20" rx="6" fill="#4f46e5" />
  `,
  earbuds: `
    <rect x="150" y="120" width="36" height="90" rx="18" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="214" y="120" width="36" height="90" rx="18" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <circle cx="168" cy="220" r="8" fill="#4f46e5" />
    <circle cx="232" cy="220" r="8" fill="#4f46e5" />
  `,
  sneaker: `
    <path d="M110 210 Q160 170 210 190 L280 210 Q300 215 290 230 L110 230 Z" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="150" y="205" width="80" height="12" rx="6" fill="#4f46e5" />
  `,
  clothing: `
    <path d="M160 120 L200 90 L240 120 L270 110 L290 150 L250 170 L250 240 L150 240 L150 170 L110 150 L130 110 Z" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
  `,
  sunglasses: `
    <rect x="120" y="150" width="70" height="50" rx="16" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="210" y="150" width="70" height="50" rx="16" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="190" y="170" width="20" height="8" rx="4" fill="#4f46e5" />
  `,
  appliance: `
    <rect x="120" y="140" width="160" height="120" rx="20" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="140" y="110" width="120" height="30" rx="15" fill="#4f46e5" opacity="0.5" />
    <rect x="180" y="100" width="40" height="14" rx="7" fill="#4f46e5" />
  `,
  vacuum: `
    <rect x="210" y="120" width="20" height="140" rx="10" fill="#4f46e5" />
    <rect x="160" y="240" width="120" height="30" rx="15" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="200" y="90" width="40" height="20" rx="10" fill="#4f46e5" />
  `,
  bulb: `
    <circle cx="200" cy="150" r="50" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="175" y="200" width="50" height="30" rx="6" fill="#4f46e5" />
  `,
  cabinet: `
    <rect x="130" y="120" width="140" height="160" rx="12" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="170" y="180" width="20" height="10" rx="5" fill="#4f46e5" />
    <rect x="210" y="180" width="20" height="10" rx="5" fill="#4f46e5" />
  `,
  watch: `
    <rect x="180" y="80" width="40" height="60" rx="12" fill="#4f46e5" />
    <circle cx="200" cy="190" r="46" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="180" y="240" width="40" height="60" rx="12" fill="#4f46e5" />
  `,
  dumbbell: `
    <rect x="120" y="170" width="40" height="60" rx="10" fill="#4f46e5" />
    <rect x="240" y="170" width="40" height="60" rx="10" fill="#4f46e5" />
    <rect x="160" y="190" width="80" height="20" rx="10" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
  `,
  yoga: `
    <rect x="120" y="190" width="160" height="50" rx="25" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <circle cx="120" cy="215" r="25" fill="#4f46e5" opacity="0.5" />
  `,
  book: `
    <rect x="130" y="120" width="120" height="170" rx="10" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="250" y="120" width="80" height="170" rx="10" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <rect x="230" y="120" width="10" height="170" fill="#4f46e5" opacity="0.4" />
  `,
  default: `
    <rect x="140" y="120" width="120" height="120" rx="16" fill="#ffffff" stroke="#4f46e5" stroke-width="6" />
    <circle cx="200" cy="180" r="28" fill="#4f46e5" opacity="0.25" />
  `,
}

const pickIconType = product => {
  const name = String(product?.name || '')
  const category = String(product?.category || '')
  const subcategory = String(product?.subcategory || '')
  const tags = Array.isArray(product?.tags) ? product.tags.join(' ') : String(product?.tags || '')
  const hay = `${name} ${category} ${subcategory} ${tags}`.toLowerCase()

  if (hay.includes('headphone')) return 'headphones'
  if (hay.includes('earbud')) return 'earbuds'
  if (hay.includes('tablet') || hay.includes('ipad')) return 'tablet'
  if (hay.includes('tv') || hay.includes('qled')) return 'tv'
  if (hay.includes('mouse')) return 'mouse'
  if (hay.includes('laptop') || hay.includes('xps')) return 'laptop'
  if (hay.includes('powerbank') || hay.includes('charger')) return 'powerbank'
  if (hay.includes('camera')) return 'camera'
  if (hay.includes('sneaker') || hay.includes('shoe') || hay.includes('running')) return 'sneaker'
  if (hay.includes('jean') || hay.includes('blazer')) return 'clothing'
  if (hay.includes('sunglass') || hay.includes('aviator')) return 'sunglasses'
  if (hay.includes('air fryer') || hay.includes('pressure') || hay.includes('cooker')) return 'appliance'
  if (hay.includes('vacuum')) return 'vacuum'
  if (hay.includes('bulb') || hay.includes('smart bulb')) return 'bulb'
  if (hay.includes('drawer') || hay.includes('furniture')) return 'cabinet'
  if (hay.includes('watch') || hay.includes('tracker') || hay.includes('wearable') || hay.includes('gps')) return 'watch'
  if (hay.includes('dumbbell') || hay.includes('weight')) return 'dumbbell'
  if (hay.includes('yoga')) return 'yoga'
  if (hay.includes('book') || hay.includes('habits') || hay.includes('money') || hay.includes('dune')) return 'book'

  return 'default'
}

export const buildImagePlaceholder = product => {
  const title = clampText(product?.name || 'Product', 28)
  const category = clampText((product?.category || 'ShopSmart').toUpperCase(), 18)
  const iconType = pickIconType(product)
  const iconSvg = ICONS[iconType] || ICONS.default
  const initials = title
    .split(' ')
    .filter(Boolean)
    .map(word => word[0])
    .join('')
    .slice(0, 2)
    .toUpperCase() || 'PS'

  const svg = `
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#eef2ff" />
      <stop offset="100%" stop-color="#c7d2fe" />
    </linearGradient>
  </defs>
  <rect width="400" height="300" fill="url(#g)" />
  <rect x="24" y="28" width="160" height="26" rx="13" fill="#e0e7ff" />
  <text x="36" y="46" font-size="12" fill="#4338ca" font-family="Arial, sans-serif" font-weight="700">${category}</text>
  <g transform="translate(0 0)">
    ${iconSvg}
  </g>
  <text x="24" y="118" font-size="18" fill="#111827" font-family="Arial, sans-serif" font-weight="700">${title}</text>
  <text x="24" y="145" font-size="11" fill="#6b7280" font-family="Arial, sans-serif">Image placeholder</text>
  <circle cx="330" cy="90" r="38" fill="#6366f1" opacity="0.18" />
  <text x="330" y="97" text-anchor="middle" font-size="18" fill="#4338ca" font-family="Arial, sans-serif" font-weight="700">${initials}</text>
</svg>
  `.trim()

  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
}
