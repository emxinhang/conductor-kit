# ATU Typography Standard Skill

**Mục đích**: Standardize typography cho tất cả tour card displays trên VacTour website.

**Usage**: Invoke skill này khi cần:
- Scan code để tìm typography inconsistencies
- Reference typography standards cho tour displays
- Review tour card implementations

## Trigger Keywords
Use this skill when the user mentions:
- "fix typo"


## Typography Standards Reference

Standards được extract từ `frontend/components/tour-detail/RelatedTours.tsx` (component reference chuẩn).

### 1. Tour Title

```tsx
className="text-2xl line-clamp-2 !text-primary-teal font-semibold font-crimson"
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Family | `font-crimson` | Crimson Pro (serif) |
| Font Size | `text-2xl` | 32px / 2rem |
| Font Weight | `font-semibold` | 600 |
| Color | `!text-primary-teal` | #2C5F7D |
| Line Clamp | `line-clamp-2` | 2 lines max |

### 2. Metadata (Duration, Number of Stops)

```tsx
<div className="flex items-center gap-4 text-neutral-600">
  <div className="flex items-center gap-1">
    <Calendar className="w-4 h-4" />
    <span>{tour.duration}</span>
  </div>
  <div className="flex items-center gap-1">
    <MapPin className="w-4 h-4" />
    <span>{tour.numberOfStops} arrêts</span>
  </div>
</div>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Container | `flex items-center gap-4` | - |
| Text Color | `text-neutral-600` | #525252 |
| Icon Size | `w-4 h-4` | 16px |
| Font Family | Default | Source Sans 3 |
| Font Size | Default | Inherit from body (18px) |

### 3. Description/Itinerary

```tsx
<p className="text-neutral-600 line-clamp-2">
  {tour.itinerary || tour.shortDescription}
</p>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Text Color | `text-neutral-600` | #525252 |
| Line Clamp | `line-clamp-2` | 2 lines max |
| Font Family | Default | Source Sans 3 |
| Font Size | Default | Inherit from body (18px) |

### 4. Pricing Section

#### "Dès" Label
```tsx
<p className="text-neutral-600">Dès</p>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Text Color | `text-neutral-600` | #525252 |

#### Main Price
```tsx
<span className="text-2xl !text-primary-teal font-semibold font-crimson">
  {tour.priceStartingFrom.toLocaleString('fr-FR')} €
</span>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Family | `font-crimson` | Crimson Pro (serif) |
| Font Size | `text-2xl` | 32px / 2rem |
| Font Weight | `font-semibold` | 600 |
| Color | `!text-primary-teal` | #2C5F7D |

#### Original Price (Strikethrough)
```tsx
<span className="text-lg line-through text-neutral-400">
  {tour.originalPrice.toLocaleString('fr-FR')} €
</span>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-lg` | 18px / 1.125rem |
| Text Decoration | `line-through` | - |
| Text Color | `text-neutral-400` | #A3A3A3 |

#### "par personne" Text
```tsx
<span className="text-lg font-normal text-neutral-600">par personne</span>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-lg` | 18px / 1.125rem |
| Font Weight | `font-normal` | 400 |
| Text Color | `text-neutral-600` | #525252 |

### 5. Badges

#### Discount Badge
```tsx
<Badge className="bg-white text-status-error font-semibold border border-status-error">
  -{tour.discountPercentage}% Offre
</Badge>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Background | `bg-white` | #FFFFFF |
| Text Color | `text-status-error` | #DC2626 |
| Font Weight | `font-semibold` | 600 |
| Border | `border border-status-error` | #DC2626 |

#### Tag Badge
```tsx
<Badge className="bg-accent-teal-pastel text-neutral-700 hover:bg-accent-teal-pastel">
  {tag.name}
</Badge>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Background | `bg-accent-teal-pastel` | #B8D4E0 |
| Text Color | `text-neutral-700` | #404040 |

## Color System Reference

| Variable | Tailwind Class | Hex Value | Usage |
|----------|---------------|-----------|-------|
| Primary Teal | `text-primary-teal` | #2C5F7D | Titles, prices, headings |
| Neutral 600 | `text-neutral-600` | #525252 | Body text, metadata |
| Neutral 700 | `text-neutral-700` | #404040 | Tag text |
| Neutral 400 | `text-neutral-400` | #A3A3A3 | Disabled, strikethrough |
| Status Error | `text-status-error` | #DC2626 | Discount badges |
| Accent Teal Pastel | `bg-accent-teal-pastel` | #B8D4E0 | Tag backgrounds |

## Font System Reference

| Usage | Font Family | Tailwind Class |
|-------|-------------|---------------|
| Titles & Prices | Crimson Pro (serif) | `font-crimson` |
| Body & Metadata | Source Sans 3 (sans-serif) | Default (no class) |

---

# Inquiry Form Typography Standards

Standards được extract từ `frontend/components/tour-detail/InquiryTeaser.tsx` và inquiry form steps.

## Inquiry Typography Reference

### 1. Section Heading (Inquiry Teaser)

```tsx
<h2 className="font-lora text-3xl md:text-4xl font-semibold text-primary-brown mb-4">
  Voyage en Indochine
</h2>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Family | `font-lora` | Lora (serif) |
| Font Size Mobile | `text-3xl` | 30px / 1.875rem |
| Font Size Desktop | `md:text-4xl` | 36px / 2.25rem |
| Font Weight | `font-semibold` | 600 |
| Color | `text-primary-brown` | Brown color |

### 2. Trust Text

```tsx
<p className="text-lg text-neutral-700">
  Plus de 3000 clients font confiance à Vactours
</p>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-lg` | 18px / 1.125rem |
| Text Color | `text-neutral-700` | #404040 |

### 3. Step Headers

```tsx
<h4 className="text-lg md:text-xl font-serif font-semibold text-neutral-900 mb-2">
  Combien de voyageurs ?
</h4>
<p className="text-neutral-600">
  Indiquez le nombre de personnes qui voyageront
</p>
```

| Element | Property | Value | CSS Value |
|---------|----------|-------|-----------|
| **Title** | Font Size Mobile | `text-lg` | 18px / 1.125rem |
| | Font Size Desktop | `md:text-xl` | 20px / 1.25rem |
| | Font Family | `font-serif` | Serif |
| | Font Weight | `font-semibold` | 600 |
| | Color | `text-neutral-900` | #171717 |
| **Description** | Font Size | Default | 18px (inherit from body) |
| | Color | `text-neutral-600` | #525252 |

### 4. Form Content Text

#### Main Labels
```tsx
<div className="font-semibold text-neutral-900">Adultes</div>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Weight | `font-semibold` | 600 |
| Color | `text-neutral-900` | #171717 |
| Font Size | Default | 18px (inherit from body) |

#### Secondary Text (Descriptions)
```tsx
<div className="text-base text-neutral-600">13 ans et plus</div>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-base` | 16px / 1rem |
| Color | `text-neutral-600` | #525252 |

#### Helper Text
```tsx
<p className="text-sm text-neutral-600 mt-2">
  Entre 1 et 90 jours
</p>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-sm` | 14px / 0.875rem |
| Color | `text-neutral-600` | #525252 |

#### Error Messages
```tsx
<p className="text-red-500 text-sm mt-1">{error.message}</p>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-sm` | 14px / 0.875rem |
| Color | `text-red-500` | Red error color |

### 5. Form Labels

```tsx
<label className="block text-sm font-semibold text-neutral-900 mb-2">
  Prénom *
</label>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-sm` | 14px / 0.875rem |
| Font Weight | `font-semibold` | 600 |
| Color | `text-neutral-900` | #171717 |

### 6. Info Boxes

```tsx
<p className="text-base text-neutral-700">
  <strong>À savoir :</strong> Tous nos circuits incluent...
</p>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-base` | 16px / 1rem |
| Color | `text-neutral-700` | #404040 |

### 7. Buttons

```tsx
<button className="px-8 py-3 bg-primary-amber text-primary-teal font-semibold rounded-lg">
  Continuer
</button>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Weight | `font-semibold` | 600 |
| Color | `text-primary-teal` | #2C5F7D |
| Background | `bg-primary-amber` | #FFD559 |

### 8. Badge Text

```tsx
<span className="text-sm font-medium">
  Populaire
</span>
```

| Property | Value | CSS Value |
|----------|-------|-----------|
| Font Size | `text-sm` | 14px / 0.875rem |
| Font Weight | `font-medium` | 500 |

## Inquiry Font Size Hierarchy

| Element Type | Font Size | Tailwind Class | Usage |
|--------------|-----------|----------------|-------|
| Section Heading | 30-36px | `text-3xl md:text-4xl` | Main section titles |
| Step Title | 18-20px | `text-lg md:text-xl` | Step headers |
| Body Text | 18px | Default (no class) | Main descriptions, primary content |
| Secondary Text | 16px | `text-base` | Sub-descriptions, helper text |
| Helper/Error Text | 14px | `text-sm` | Input helpers, errors, badges |
| Form Labels | 14px | `text-sm` | Input field labels |

## Inquiry Color Usage

| Element | Color Class | Hex Value |
|---------|-------------|-----------|
| Primary Headings | `text-neutral-900` | #171717 |
| Body Text | `text-neutral-600` | #525252 |
| Secondary Text | `text-neutral-700` | #404040 |
| Buttons Primary | `text-primary-teal` | #2C5F7D |
| Error Messages | `text-red-500` | Red |

## Scan Workflow

Khi user cung cấp code cần scan:

1. **Identify elements**: Xác định các elements (title, metadata, description, pricing, badges)
2. **Compare**: So sánh với standards trên
3. **Report**: List ra các inconsistencies theo format:

```markdown
## Typography Scan Report

### ✅ Compliant Elements
- [Element name]: Matches standard

### ⚠️ Inconsistencies Found

#### [Element Name]
**Current**: `className="..."`
**Standard**: `className="..."`
**Issue**: [Description]
**Recommendation**: [Fix suggestion]
```

## Examples

### ✅ Correct Implementation
```tsx
// Tour Title - CORRECT
<h3 className="text-2xl line-clamp-2 !text-primary-teal font-semibold font-crimson">
  {tour.title}
</h3>

// Price - CORRECT
<span className="text-2xl !text-primary-teal font-semibold font-crimson">
  {price} €
</span>
```

### ❌ Incorrect Implementation
```tsx
// Tour Title - WRONG (missing font-crimson, wrong size)
<h3 className="text-xl font-bold text-primary-teal">
  {tour.title}
</h3>

// Price - WRONG (wrong font, wrong weight)
<span className="text-xl text-teal-600 font-bold">
  {price} €
</span>
```

## Notes

- **Font imports**: Đảm bảo Crimson Pro và Source Sans 3 được import trong layout
- **Color variables**: Sử dụng Tailwind classes, không hard-code hex colors
- **Consistency**: Tất cả tour cards trên site phải follow cùng 1 standard
- **Updates**: Khi standards thay đổi, update file này và re-scan toàn bộ components
