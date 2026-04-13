# React Component ATU (Auto Template & Utilities)

## Trigger Phrases
- "tạo react component [name]"
- "tạo component [name]"
- "generate react component [name]"
- "create component [name]"

## Description
Auto-generate React components theo VacTours project patterns với TypeScript, Tailwind CSS, accessibility, và best practices.

## When to Use
Dùng skill này khi bạn cần:
- Tạo React components mới cho blog system
- Generate component boilerplate với proper structure
- Đảm bảo consistency với existing components
- Follow VacTours styling và accessibility standards

## Input Required
- **Component name** (e.g., "ArticleCard", "Pagination", "CategoryBadge")
- **Component type** (optional):
  - `card` - Card/preview components
  - `layout` - Layout components (hero, sidebar, etc.)
  - `ui` - UI elements (buttons, badges, tabs)
  - `content` - Content blocks
  - `modal` - Modals and overlays
- **Props specification** (optional - can be inferred from context)
- **Special requirements** (e.g., client component, needs intersection observer, etc.)

## What This Skill Does

### 1. Analyze Existing Component Patterns
- Read existing components in `frontend/components/` to understand patterns
- Identify common imports and utilities
- Understand Tailwind styling conventions
- Check accessibility patterns (ARIA labels, semantic HTML)

### 2. Generate Component Structure

**Standard Component Template:**
```typescript
'use client' // If needed

import { /* relevant types */ } from '@/types/strapi'
import { /* utilities */ } from '@/lib/*'
// Additional imports as needed

interface Props {
  // TypeScript props interface
}

export default function ComponentName({ props }: Props) {
  // Component logic

  return (
    // JSX with Tailwind CSS
  )
}
```

### 3. Apply VacTours Patterns

**Key Patterns to Follow:**

#### TypeScript Types
```typescript
// Always use explicit types from @/types/strapi
import { Article, ArticlePreview, Category } from '@/types/strapi'

// Props interface with clear naming
interface ArticleCardProps {
  article: ArticlePreview
  featured?: boolean
  className?: string
}
```

#### Tailwind CSS Conventions
```typescript
// Use VacTours design tokens
const colors = {
  primary: 'bg-primary-teal text-white',
  secondary: 'bg-neutral-100 text-neutral-700',
  hover: 'hover:bg-primary-teal/90 transition-colors'
}

// Responsive design
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

// Typography
<h1 className="text-3xl md:text-4xl lg:text-5xl font-lora font-bold">
<p className="text-sm md:text-base text-neutral-600">
```

#### Accessibility
```typescript
// Semantic HTML
<nav aria-label="Breadcrumb">
<article aria-labelledby="article-title">

// ARIA attributes
<button
  aria-label="Close modal"
  aria-expanded={isOpen}
  aria-controls="modal-content"
>

// Focus management
<a
  href="/blog"
  className="focus:outline-none focus:ring-2 focus:ring-primary-teal"
>
```

#### Client Components
```typescript
'use client' // Only when needed:
// - useState, useEffect, event handlers
// - Browser APIs (window, document)
// - Third-party client libraries

// Server components by default
```

#### Image Handling
```typescript
import Image from 'next/image'
import { getStrapiMediaURL } from '@/lib/strapi'

const imageUrl = getStrapiMediaURL(image?.url)

<Image
  src={imageUrl}
  alt={altText}
  width={800}
  height={600}
  className="object-cover rounded-lg"
/>
```

### 4. Component Type Templates

#### Card Component Pattern
```typescript
'use client'

import Link from 'next/link'
import Image from 'next/image'
import { ArticlePreview } from '@/types/strapi'
import { formatArticleDate } from '@/lib/blog-utils'
import { getStrapiMediaURL } from '@/lib/strapi'

interface ArticleCardProps {
  article: ArticlePreview
  featured?: boolean
  className?: string
}

export default function ArticleCard({ article, featured, className }: ArticleCardProps) {
  const imageUrl = getStrapiMediaURL(article.heroImage?.url)

  return (
    <Link
      href={`/blog/${article.category.slug}/${article.slug}`}
      className={cn(
        'group block bg-white rounded-lg shadow-md overflow-hidden',
        'hover:shadow-xl transition-shadow duration-300',
        featured && 'md:col-span-2',
        className
      )}
    >
      {/* Image */}
      <div className="relative aspect-[16/9] overflow-hidden">
        <Image
          src={imageUrl}
          alt={article.heroImageAlt}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Category Badge */}
        <span className="inline-block px-3 py-1 bg-primary-teal text-white text-xs font-semibold rounded-full mb-3">
          {article.category.name}
        </span>

        {/* Title */}
        <h3 className="text-xl font-semibold mb-2 line-clamp-2 group-hover:text-primary-teal transition-colors">
          {article.title}
        </h3>

        {/* Excerpt */}
        <p className="text-neutral-600 text-sm mb-4 line-clamp-3">
          {article.excerpt}
        </p>

        {/* Meta */}
        <div className="flex items-center justify-between text-xs text-neutral-500">
          <span>{article.author.name}</span>
          <span>{article.readTime} min</span>
        </div>
      </div>
    </Link>
  )
}
```

#### UI Element Pattern
```typescript
'use client'

import { Category } from '@/types/strapi'
import { cn } from '@/lib/utils'

interface CategoryTabsProps {
  categories: Category[]
  activeCategory?: string
  onCategoryChange?: (slug: string) => void
  className?: string
}

export default function CategoryTabs({
  categories,
  activeCategory,
  onCategoryChange,
  className
}: CategoryTabsProps) {
  return (
    <nav
      className={cn('flex gap-2 overflow-x-auto pb-2', className)}
      aria-label="Category filter"
    >
      {categories.map(category => (
        <button
          key={category.id}
          onClick={() => onCategoryChange?.(category.slug)}
          className={cn(
            'px-4 py-2 rounded-full whitespace-nowrap text-sm font-medium',
            'transition-colors duration-200',
            activeCategory === category.slug
              ? 'bg-primary-teal text-white'
              : 'bg-neutral-100 text-neutral-700 hover:bg-neutral-200'
          )}
          aria-current={activeCategory === category.slug ? 'page' : undefined}
        >
          {category.name}
        </button>
      ))}
    </nav>
  )
}
```

#### Content Block Pattern
```typescript
'use client'

import { QuoteBlock as QuoteBlockType } from '@/types/strapi'
import { cn } from '@/lib/utils'

interface Props {
  block: QuoteBlockType
  className?: string
}

export default function QuoteBlock({ block, className }: Props) {
  const { text, author, highlight } = block

  return (
    <blockquote
      className={cn(
        'my-8 p-6 rounded-lg',
        highlight
          ? 'bg-primary-teal/10 border-l-4 border-primary-teal'
          : 'bg-neutral-50 border-l-4 border-neutral-300',
        className
      )}
    >
      <p className="text-lg md:text-xl italic text-neutral-800 mb-4">
        &ldquo;{text}&rdquo;
      </p>
      {author && (
        <footer className="text-sm text-neutral-600">
          &mdash; {author}
        </footer>
      )}
    </blockquote>
  )
}
```

### 5. Best Practices Checklist

#### TypeScript
- ✅ All props have explicit types
- ✅ No `any` types
- ✅ Optional props use `?:`
- ✅ Import types from `@/types/strapi`

#### Styling
- ✅ Use Tailwind utility classes
- ✅ Follow VacTours color palette
- ✅ Responsive design (mobile-first)
- ✅ Hover/focus states
- ✅ Transitions for smooth UX

#### Accessibility
- ✅ Semantic HTML elements
- ✅ ARIA labels where needed
- ✅ Keyboard navigation support
- ✅ Focus indicators
- ✅ Alt text for images

#### Performance
- ✅ Use Next.js `Image` component
- ✅ Lazy load heavy components
- ✅ Optimize re-renders (memo if needed)
- ✅ Client components only when needed

#### Code Quality
- ✅ Clear component and prop names
- ✅ Single responsibility principle
- ✅ Reusable and composable
- ✅ Comments for complex logic
- ✅ Consistent file naming (PascalCase.tsx)

### 6. File Placement

**Component location based on type:**
```
frontend/components/blog/
├── ArticleCard.tsx           # Blog-specific components
├── CategoryTabs.tsx
├── blocks/                   # Content block components
│   ├── RichTextBlock.tsx
│   ├── ImageBlock.tsx
│   └── ...
└── ...

frontend/components/shared/   # Reusable across features
├── Button.tsx
├── Modal.tsx
└── ...
```

## Example Usage

```bash
# Example 1: Simple card component
"tạo component ArticleCard"
→ Generates ArticleCard with image, title, excerpt, meta

# Example 2: UI element
"tạo react component CategoryTabs with active state"
→ Generates tabs with active/hover states

# Example 3: Content block
"tạo component QuoteBlock for blog content"
→ Generates quote block with highlight option

# Example 4: Complex component
"tạo component TableOfContents with sticky behavior and intersection observer"
→ Generates TOC with scroll tracking
```

## Output Format

The skill will:
1. **Analyze** existing components for patterns
2. **Generate** component file with proper structure
3. **Explain** key features and usage
4. **Provide** integration instructions
5. **List** files created:
   - `frontend/components/blog/[ComponentName].tsx`

## Success Criteria

- ✅ Component compiles without TypeScript errors
- ✅ Follows VacTours styling patterns
- ✅ Includes proper accessibility attributes
- ✅ Uses semantic HTML
- ✅ Responsive design implemented
- ✅ Props properly typed
- ✅ No breaking changes to existing code

## Notes

- This skill follows **VacTours project conventions**
- Uses **Tailwind CSS** for all styling
- Follows **Next.js 15 App Router** patterns
- Compatible with **React 19** features
- Emphasizes **accessibility** and **performance**

## Related Skills
- `strapi-frontend-atu`: For API/type generation
- `nextjs`: For page-level components
- `tailwindcss`: For styling utilities
