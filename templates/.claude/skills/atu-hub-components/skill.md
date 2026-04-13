# Atu-Hub-Components Skill

## Description
Automatically generate high-quality React components for VacTours Hub System với consistent patterns, accessibility, và best practices. Skill này được tạo dựa trên learnings từ 2 pilot components (HeroVideo và CountryAtAGlance).

## Trigger Keywords
Use this skill when building hub components:
- "tạo [component name] hub component"
- "tạo hub component cho [section name]"
- "build [IntroSection|VoyageFinder|OverviewWithLink|FAQSection|etc.]"
- "implement [component] theo hub patterns"

## When to Use
- Building any of the 7 remaining Phase 1 components
- Building Phase 2 components (Duration/Category/Destination hubs)
- Creating reusable hub subcomponents
- Need consistent code structure across hub system

## When NOT to Use
- Non-hub components (use regular development)
- Backend/API development
- One-off custom components that don't follow hub patterns

---

## Project Context

### VacTours Hub System
- **Architecture:** Hub-and-spoke SEO system
- **Tech Stack:** Next.js 15, TypeScript, Tailwind CSS, Shadcn UI, Strapi v5
- **Design Philosophy:** Clean, accessible, SEO-optimized
- **Target:** French-speaking markets

### Files Structure
```
frontend/
├── components/hub/
│   ├── HeroVideo.tsx ✅ (Pilot #1)
│   ├── CountryAtAGlance.tsx ✅ (Pilot #2)
│   ├── InteractiveMap.tsx ✅ (Subcomponent)
│   ├── DestinationPin.tsx ✅ (Subcomponent)
│   ├── DestinationModal.tsx ✅ (Subcomponent)
│   └── [7 more components to build]
├── types/
│   └── hub.ts ✅ (All interfaces defined)
├── lib/
│   ├── strapi.ts ✅ (API functions)
│   └── hub-utils.ts ✅ (Helper functions)
└── app/
    └── globals.css ✅ (Animations added)
```

---

## Component Patterns Discovered from Pilots

### Pattern 1: File Structure Template

```typescript
'use client'; // Only if component has interactivity (useState, useEffect, event handlers)

// ============================================================================
// IMPORTS
// ============================================================================

// React & Next.js
import { useState, useEffect } from 'react'; // Only if needed
import Image from 'next/image'; // For images
import Link from 'next/link'; // For links

// Lucide Icons
import { IconName1, IconName2 } from 'lucide-react';

// Types
import { ComponentProps } from '@/types/hub';

// Utilities (if needed)
import { helperFunction } from '@/lib/hub-utils';
import { getStrapiMediaURL } from '@/lib/strapi';

// Subcomponents (if any)
import SubComponent from './SubComponent';

// ============================================================================
// COMPONENT DOCUMENTATION
// ============================================================================

/**
 * ComponentName Component
 *
 * [Brief description of what this component does]
 *
 * Features:
 * - Feature 1
 * - Feature 2
 * - Feature 3
 *
 * @param {ComponentProps} props - Component props
 */

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export default function ComponentName({
  prop1,
  prop2,
  prop3,
}: ComponentProps) {
  // State (if needed)
  const [state, setState] = useState<Type>(initialValue);

  // Effects (if needed)
  useEffect(() => {
    // Setup
    return () => {
      // Cleanup
    };
  }, [dependencies]);

  // Handlers (if needed)
  const handleEvent = () => {
    // Logic
  };

  // Render
  return (
    <section className="py-16 md:py-20 lg:py-24 bg-white">
      <div className="container mx-auto max-w-screen-xl px-4 md:px-6 lg:px-8">
        {/* Section Heading */}
        <h2 className="font-lora text-3xl md:text-4xl font-semibold text-teal-900 mb-8 md:mb-12">
          {title}
        </h2>

        {/* Content */}
        {/* ... */}
      </div>
    </section>
  );
}
```

---

### Pattern 2: Styling Conventions

**Container Pattern:**
```tsx
<section className="py-16 md:py-20 lg:py-24 bg-white">
  <div className="container mx-auto max-w-screen-xl px-4 md:px-6 lg:px-8">
    {/* Content */}
  </div>
</section>
```

**Responsive Typography:**
```tsx
// Headings
<h2 className="font-lora text-3xl md:text-4xl font-semibold text-teal-900 mb-8 md:mb-12">
<h3 className="font-lora text-2xl md:text-3xl font-semibold text-teal-900 mb-4">

// Body text
<p className="text-neutral-700 leading-relaxed mb-4">
<p className="text-lg text-neutral-600">
```

**Grid Layouts:**
```tsx
// 2-column
<div className="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12">

// 3-column
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">

// Custom ratio (60/40)
<div className="grid grid-cols-1 lg:grid-cols-[60%_40%] gap-8">
```

**Button Styles:**
```tsx
// Primary CTA
<button className="inline-flex items-center gap-2 px-6 py-3 bg-teal-600 hover:bg-teal-700 text-white font-medium rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2">

// Secondary
<button className="inline-flex items-center gap-2 px-6 py-3 bg-white hover:bg-neutral-50 text-teal-900 font-medium rounded-lg border border-neutral-200 transition-colors duration-200">
```

**Card Styles:**
```tsx
<div className="bg-white rounded-xl shadow-lg p-6 md:p-8 hover:shadow-xl transition-shadow duration-300">
```

---

### Pattern 3: Accessibility Requirements

**ALWAYS Include:**

1. **Semantic HTML**
```tsx
<section> for sections
<nav> for navigation
<article> for content blocks
<button> for actions (never <div onClick>)
```

2. **ARIA Labels**
```tsx
<button aria-label="Descriptive action">
<nav aria-label="Breadcrumb">
<section aria-labelledby="section-heading">
```

3. **Screen Reader Content**
```tsx
<div className="sr-only">
  Content only for screen readers
</div>
```

4. **Focus States**
```tsx
focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2
```

5. **Keyboard Navigation**
```tsx
// ESC key for modals
useEffect(() => {
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape') onClose();
  };
  document.addEventListener('keydown', handleEscape);
  return () => document.removeEventListener('keydown', handleEscape);
}, [onClose]);
```

---

### Pattern 4: State Management

**Modal State:**
```tsx
const [isOpen, setIsOpen] = useState(false);
const [selectedItem, setSelectedItem] = useState<Type | null>(null);

const handleOpen = (item: Type) => {
  setSelectedItem(item);
  setIsOpen(true);
};

const handleClose = () => {
  setIsOpen(false);
  setSelectedItem(null);
};
```

**Hover State:**
```tsx
const [showTooltip, setShowTooltip] = useState(false);

<div
  onMouseEnter={() => setShowTooltip(true)}
  onMouseLeave={() => setShowTooltip(false)}
>
  {showTooltip && <Tooltip />}
</div>
```

**Loading State:**
```tsx
const [isLoading, setIsLoading] = useState(true);
const [error, setError] = useState(false);

const handleLoad = () => setIsLoading(false);
const handleError = () => {
  console.error('Failed to load');
  setError(true);
  setIsLoading(false);
};
```

---

### Pattern 5: Error Handling

**Image Loading:**
```tsx
<Image
  src={imageUrl}
  alt={altText}
  onLoad={handleLoad}
  onError={handleError}
  // ... other props
/>

{error && (
  <div className="flex items-center justify-center bg-neutral-100 p-8">
    <p className="text-neutral-600">Unable to load image</p>
  </div>
)}
```

**API Error Handling:**
```tsx
try {
  const data = await fetchData();
  // Process data
} catch (error) {
  console.error('Error:', error);
  // Show fallback UI
  return null; // or fallback component
}
```

---

### Pattern 6: ReactMarkdown Integration

**For Rich Text Content:**
```tsx
import ReactMarkdown from 'react-markdown';

<ReactMarkdown
  components={{
    ul: ({ ...props }) => (
      <ul className="space-y-3 list-none" {...props} />
    ),
    li: ({ children, ...props }) => (
      <li className="flex items-start gap-3" {...props}>
        <span className="text-teal-600 text-xl shrink-0 mt-0.5">•</span>
        <span className="text-neutral-700 leading-relaxed">{children}</span>
      </li>
    ),
    p: ({ ...props }) => (
      <p className="text-neutral-700 leading-relaxed mb-4" {...props} />
    ),
    strong: ({ ...props }) => (
      <strong className="font-semibold text-neutral-900" {...props} />
    ),
  }}
>
  {content}
</ReactMarkdown>
```

---

### Pattern 7: Responsive Design

**Breakpoints:**
- Mobile: Default (no prefix)
- Tablet: `md:` (768px+)
- Desktop: `lg:` (1024px+)
- Large Desktop: `xl:` (1280px+)

**Common Patterns:**
```tsx
// Spacing
py-12 md:py-16 lg:py-20

// Grid columns
grid-cols-1 md:grid-cols-2 lg:grid-cols-3

// Text size
text-base md:text-lg lg:text-xl

// Padding
p-4 md:p-6 lg:p-8

// Gap
gap-4 md:gap-6 lg:gap-8
```

---

### Pattern 8: Animation Usage

**Available Animations:**
```tsx
animate-fade-in      // Opacity 0 → 1 (0.6s)
animate-scale-in     // Scale 0.95 → 1 (0.3s) - modals
animate-slide-up     // Translate Y 20px → 0 (0.5s)
animate-ping         // Pulse ring (infinite)
animate-bounce       // Bounce effect (infinite)
```

**When to Use:**
- `animate-fade-in`: Hero sections, content reveal
- `animate-scale-in`: Modal entrance
- `animate-slide-up`: Staggered content reveal
- `animate-ping`: Attention indicators (pins, notifications)
- `animate-bounce`: Scroll indicators

---

## Component Specifications

### Phase 1 Remaining Components (7 components)

#### 1. IntroSection
**File:** `frontend/components/hub/IntroSection.tsx`
**Complexity:** LOW
**Props:** `IntroSectionProps { content: string }`

**Features:**
- ReactMarkdown for content
- Centered layout
- Max-width constraint
- Typography styling

**Template:**
```tsx
'use client';

import ReactMarkdown from 'react-markdown';
import { IntroSectionProps } from '@/types/hub';

export default function IntroSection({ content }: IntroSectionProps) {
  return (
    <section className="py-16 md:py-20 lg:py-24 bg-white">
      <div className="container mx-auto max-w-4xl px-4 md:px-6 lg:px-8">
        <div className="prose prose-lg max-w-none text-center">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </section>
  );
}
```

---

#### 2. VoyageFinder (+ 3 subcomponents)
**File:** `frontend/components/hub/VoyageFinder.tsx`
**Subcomponents:** VoyageTabs, HubCard, HubModal
**Complexity:** HIGH
**Props:** `VoyageFinderProps`

**Features:**
- 3-tab navigation (Shadcn Tabs)
- Tab 1: Duration cards (3 cards)
- Tab 2: Category cards (3 cards)
- Tab 3: Related tours carousel
- Modal on card click
- Responsive grid

**Key Implementation:**
- Use `@radix-ui/react-tabs` from Shadcn
- Tab state management
- HubCard: Reusable for duration & category
- HubModal: Show modal content + CTA

---

#### 3. OverviewWithLink
**File:** `frontend/components/hub/OverviewWithLink.tsx`
**Complexity:** MEDIUM
**Props:** `OverviewWithLinkProps`

**Features:**
- 2-column layout (text + visual)
- Visual types: image, card, chart
- Alternating image position (left/right)
- Icon display (Lucide)
- Link button

**Visual Type Handling:**
```tsx
{visual.type === 'image' && <Image src={visual.data.url} ... />}
{visual.type === 'card' && <CardGrid cards={visual.data.cards} />}
{visual.type === 'chart' && <ChartComponent data={visual.data.chartData} />}
```

---

#### 4. FAQSection
**File:** `frontend/components/hub/FAQSection.tsx`
**Complexity:** MEDIUM
**Props:** `FAQSectionProps`

**Features:**
- Shadcn Accordion component
- FAQ Schema markup (JSON-LD)
- Optional "En savoir plus" links
- Expandable sections

**Key Implementation:**
```tsx
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { generateFAQSchema } from '@/lib/hub-utils';

// Add script tag for schema
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify(generateFAQSchema(faqs))
  }}
/>
```

---

#### 5. InquiryFormSection
**File:** `frontend/components/hub/InquiryFormSection.tsx`
**Complexity:** MEDIUM
**Props:** `InquiryFormSectionProps`

**Features:**
- Wrapper around existing InquiryForm
- Trust badges grid
- Background gradient
- Prefilled data logic

**Key Implementation:**
```tsx
// Reuse existing InquiryForm component
import InquiryForm from '@/components/forms/InquiryForm';

<InquiryForm
  prefilledData={{
    country: prefilledData?.country,
    category: prefilledData?.category,
  }}
/>
```

---

#### 6. CommentsSection
**File:** `frontend/components/hub/CommentsSection.tsx`
**Complexity:** HIGH
**Props:** `CommentsSectionProps`

**Features:**
- Comment form (name, email, content)
- Comments list (hierarchical with replies)
- Reply functionality
- Report button
- API integration

**Key Implementation:**
```tsx
import { getComments, submitComment, reportComment } from '@/lib/strapi';

// Form submission
const handleSubmit = async (data: CommentFormData) => {
  const result = await submitComment(relatedTo, data);
  if (result.success) {
    // Refresh comments
    // Show success message
  }
};
```

---

#### 7. Dynamic Route Page
**File:** `frontend/app/[country]/page.tsx`
**Complexity:** MEDIUM

**Features:**
- Fetch hub data by slug
- Render all Dynamic Zone sections
- generateMetadata()
- generateStaticParams()
- Error handling

**Template:**
```tsx
import { getCountryHubBySlug, getAllCountryHubs } from '@/lib/strapi';
import { getSectionByType, filterSectionsByType } from '@/lib/hub-utils';
import HeroVideo from '@/components/hub/HeroVideo';
// ... import all section components

export async function generateStaticParams() {
  const hubs = await getAllCountryHubs();
  return hubs.map((hub) => ({ country: hub.slug }));
}

export async function generateMetadata({ params }: { params: { country: string } }) {
  const hub = await getCountryHubBySlug(params.country);
  if (!hub) return {};

  return {
    title: hub.seoTitle,
    description: hub.seoDescription,
  };
}

export default async function CountryHubPage({ params }: { params: { country: string } }) {
  const hub = await getCountryHubBySlug(params.country);

  if (!hub) {
    notFound();
  }

  // Extract sections
  const introSection = getSectionByType<IntroTextSection>(hub.sections, 'hub.intro-text');
  const atAGlanceSection = getSectionByType<CountryAtAGlanceSection>(hub.sections, 'hub.country-at-a-glance');
  // ... etc

  return (
    <>
      <HeroVideo
        videoUrl={hub.heroVideo?.url}
        fallbackImage={hub.heroImage.url}
        title={hub.heroTitle}
        subtitle={hub.heroSubtitle}
        breadcrumbs={[
          { label: 'Accueil', href: '/' },
          { label: hub.name, href: `/${hub.slug}` }
        ]}
      />

      {introSection && <IntroSection content={introSection.content} />}
      {atAGlanceSection && <CountryAtAGlance ... />}
      {/* ... render all sections */}
    </>
  );
}
```

---

## Workflow

### Step 1: Identify Component Type
- Simple (no state, no subcomponents): IntroSection
- Medium (state, single file): OverviewWithLink, FAQSection
- Complex (state + subcomponents): VoyageFinder, CommentsSection

### Step 2: Check TypeScript Interface
- All prop interfaces already defined in `frontend/types/hub.ts`
- Use exact interface names
- Import from `@/types/hub`

### Step 3: Apply Patterns
- Use File Structure Template
- Follow Styling Conventions
- Add Accessibility Requirements
- Implement Error Handling

### Step 4: Test Checklist
- [ ] TypeScript compiles without errors
- [ ] Component renders without console errors
- [ ] Responsive on mobile/tablet/desktop
- [ ] Keyboard navigation works
- [ ] Screen reader accessible
- [ ] Links work correctly
- [ ] Images load with fallback

---

## Common Mistakes to Avoid

❌ **DON'T:**
- Use `<div onClick>` instead of `<button>`
- Forget `'use client'` directive for interactive components
- Skip accessibility attributes
- Use inline styles instead of Tailwind
- Hardcode colors (use theme variables)
- Forget responsive breakpoints
- Skip error handling
- Use relative imports for types (use `@/types/...`)

✅ **DO:**
- Use semantic HTML
- Include ARIA labels
- Test keyboard navigation
- Handle loading/error states
- Use consistent spacing (py-16 md:py-20 lg:py-24)
- Follow responsive pattern (mobile → md: → lg:)
- Add TypeScript types for all props
- Use absolute imports with `@/`

---

## Helper Functions Available

From `frontend/lib/hub-utils.ts`:

```typescript
// Section filtering
filterSectionsByType<T>(sections, 'hub.component-name'): T[]
getSectionByType<T>(sections, 'hub.component-name'): T | null

// Data parsing
parseSvgCoordinates(coordinates): [number, number]
parseJsonField<T>(field): T | null

// SEO
generateBreadcrumbSchema(breadcrumbs)
generateFAQSchema(faqs)

// Formatting
formatDate(dateString, locale, options): string
getRelativeTime(dateString, locale): string
truncateText(text, maxLength): string

// Validation
isValidEmail(email): boolean
sanitizeHtml(html): string

// Avatar helpers
getInitials(name): string
getAvatarColor(name): string

// Performance
debounce(func, wait)
throttle(func, limit)
```

From `frontend/lib/strapi.ts`:

```typescript
// Hub API
getCountryHubBySlug(slug): Promise<CountryHub | null>
getAllCountryHubs(): Promise<CountryHub[]>

// Comments API
getComments(relatedTo): Promise<Comment[]>
submitComment(relatedTo, data): Promise<{success: boolean, error?: string}>
reportComment(commentId, reason, content?): Promise<{success: boolean, error?: string}>

// Media
getStrapiMediaURL(url): string
```

---

## Quick Reference

### Component Checklist

When building a new hub component:

1. ✅ Create file in `frontend/components/hub/[ComponentName].tsx`
2. ✅ Add `'use client'` if interactive
3. ✅ Import types from `@/types/hub`
4. ✅ Follow File Structure Template
5. ✅ Use Container Pattern for layout
6. ✅ Add section heading with `font-lora`
7. ✅ Implement responsive breakpoints
8. ✅ Add accessibility attributes
9. ✅ Handle loading/error states
10. ✅ Add animations where appropriate
11. ✅ Test keyboard navigation
12. ✅ Verify TypeScript types

---

## Examples from Pilots

### Simple Component: HeroVideo (180 lines)
- Video/image handling
- Breadcrumbs navigation
- Scroll indicator
- prefers-reduced-motion support

### Complex Component: CountryAtAGlance (450+ lines, 4 files)
- Main component + 3 subcomponents
- SVG map interaction
- Modal system
- Hover states
- Coordinate parsing

Use these as reference for patterns!

---

## Notes

- This skill was created based on 2 production-ready pilot components
- All patterns have been tested and verified
- TypeScript interfaces are complete and accurate
- Helper functions cover all common use cases
- CSS animations are ready to use
- Follow these patterns strictly for consistency across all 18+ components

**Remember:** Quality over speed - ensure accessibility and error handling in every component.
