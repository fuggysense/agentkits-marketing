# Component Sources Reference

## 21st.dev — Primary Component Source

### Overview
21st.dev is an open-source component marketplace built on shadcn/ui patterns. Components are React/Next.js based and can be installed via CLI or adapted to plain HTML+Tailwind.

### Browsing Components
```bash
python3 scripts/browser-tools.py browse-components hero --source 21st
python3 scripts/browser-tools.py browse-components pricing --source 21st
python3 scripts/browser-tools.py browse-components navbar --source 21st
```

### Installing (for React/Next.js builds)
```bash
npx 21st@latest add <component-name>
```

### Section-to-Component Mapping

| Website Section | 21st.dev Category | Fallback |
|----------------|-------------------|----------|
| Navigation/Header | `navbar`, `header` | Custom Tailwind nav |
| Hero Section | `hero`, `landing` | Tailwind hero template |
| Features Grid | `features`, `bento` | CSS Grid + Tailwind cards |
| Testimonials | `testimonial`, `review` | Flexbox carousel |
| Pricing Table | `pricing` | Tailwind pricing cards |
| CTA Section | `cta`, `banner` | Custom Tailwind CTA |
| Footer | `footer` | Standard footer layout |
| FAQ | `accordion`, `faq` | Details/summary HTML |
| Stats/Numbers | `stats`, `counter` | CSS Grid numbers |
| Logo Cloud | `logo-cloud`, `brands` | Flexbox image row |

---

## Converting React/JSX to Plain HTML+Tailwind

When the project doesn't use React, convert 21st.dev components:

### Pattern
```jsx
// React component
export function Hero() {
  return (
    <section className="py-24 bg-gray-900">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-5xl font-bold text-white">Title</h1>
      </div>
    </section>
  )
}
```

Becomes:
```html
<section class="py-24 bg-gray-900">
  <div class="max-w-7xl mx-auto px-4">
    <h1 class="text-5xl font-bold text-white">Title</h1>
  </div>
</section>
```

### Conversion Rules
1. `className` → `class`
2. `{variable}` → hardcode the value
3. `.map()` loops → repeat the HTML manually
4. `onClick` handlers → plain JS event listeners or Alpine.js `@click`
5. Conditional rendering `{condition && <div>}` → include or omit statically
6. Import statements → remove, inline the markup
7. State (`useState`) → Alpine.js `x-data` or vanilla JS

### Animations
React motion/framer-motion → replace with:
- CSS `@keyframes` + `animation`
- Intersection Observer + CSS classes
- GSAP (for cinematic builds)

---

## Fallback Component Sources

### shadcn/ui
- URL: https://ui.shadcn.com
- React/Next.js components
- Copy-paste, not npm install
- Best for: form elements, dialogs, dropdowns

### Aceternity UI
- URL: https://ui.aceternity.com
- Animated React components
- Best for: hero effects, text animations, card hovers
- Good cinematic feel

### Tailwind UI
- URL: https://tailwindui.com (paid)
- Official Tailwind Labs components
- HTML + Tailwind, no framework dependency
- Best for: production-ready, accessible components

### Flowbite
- URL: https://flowbite.com
- Open-source Tailwind components
- HTML + Tailwind (no React required)
- Best for: quick prototypes, standard UI patterns

---

## Component Selection Strategy

| Scenario | Source | Why |
|----------|--------|-----|
| React/Next.js project | 21st.dev → shadcn/ui | Native integration |
| Static HTML site | Convert 21st.dev → or use Flowbite | Tailwind compatible |
| Cinematic/animated | Aceternity UI + GSAP | Best motion design |
| Production/accessible | Tailwind UI | Battle-tested |
| Rapid prototype | Flowbite | Fastest to implement |
