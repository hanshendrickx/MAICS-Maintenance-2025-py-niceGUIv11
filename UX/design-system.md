# MACS Design System & UX Guidelines

## Core Design Principles

### 1. Minimalistic Medical Interface
- **Primary Goal**: Reduce cognitive load for medical professionals
- **Secondary Goal**: Ensure accessibility for all users
- **Tertiary Goal**: Professional, trustworthy appearance

### 2. Typography Hierarchy
```
Baseline: 18px (medical accessibility standard)
Scale: 18px → 20px → 24px → 30px → 36px

Font Weights:
- Titles: font-semibold (600)
- Cards: font-bold (700) - for importance
- Content: font-medium (500) - for readability
- Subtitles: font-normal (400)
```

### 3. Color Palette
```css
/* Primary Colors */
--primary-blue: #2563eb     /* Actions, links */
--text-primary: #374151     /* Main text */
--text-secondary: #6b7280   /* Supporting text */

/* Status Colors */
--required: #059669         /* Required tasks */
--optional: #6b7280         /* Optional tasks */
--success: #10b981          /* Completed states */
--warning: #f59e0b          /* Attention needed */
--evidence: #ea580c         /* Documentation */

/* Background Colors */
--bg-light: #f8fafc         /* Light theme background */
--bg-dark: #2d3748          /* Dark theme background */
--card-bg: #ffffff          /* Card backgrounds */
```

### 4. Spacing Scale (Consistent 8px grid)
```
xs: 4px  (gap-1)
sm: 8px  (gap-2)
md: 16px (gap-4)
lg: 24px (gap-6)
xl: 32px (gap-8)
```

### 5. Border Radius Standards
```
Cards: 8px (rounded-lg)
Buttons: 6px (rounded-md)
Icons: Full circle (rounded-full)
```

## Component Standards

### Cards
- **Border**: 2px solid (reduced from 3px for minimalism)
- **Shadow**: shadow-lg (not shadow-xl - too heavy)
- **Hover**: Subtle translate instead of scale
- **Padding**: Responsive p-3 sm:p-4 md:p-4

### Buttons
- **Primary**: bg-blue-600 hover:bg-blue-800
- **Secondary**: bg-gray-600 hover:bg-gray-800
- **Height**: Minimum 44px (accessibility)
- **Padding**: px-6 py-2 minimum

### Icons
- **Size**: 24px base (text-2xl)
- **Responsive**: 20px mobile → 24px desktop
- **Color**: Match content hierarchy
- **Usage**: Only functional icons, no decoration

## Accessibility Rules

### 1. Font Size Control
```python
# 4-level system: small → medium → large → xl
# Always 18px minimum for medical contexts
# Responsive scaling across breakpoints
```

### 2. High Contrast Support
```python
# Text contrast ratio: 4.5:1 minimum
# High contrast mode: 7:1 ratio
# Color coding + text labels (not color alone)
```

### 3. Touch Targets
```
Minimum: 44px × 44px
Preferred: 48px × 48px
Spacing: 8px minimum between targets
```

## Responsive Breakpoints

```
sm: 640px   (Tablet portrait)
md: 768px   (Tablet landscape)
lg: 1024px  (Desktop)
xl: 1280px  (Large desktop)
```

### Mobile-First Card Layout
```
Mobile: 45% width (2 cards per row)
Tablet: 36px fixed width (3-4 cards)
Desktop: 48px fixed width (5 cards)
```

## Animation Guidelines

### 1. Transitions
```css
/* Standard transitions */
transition: all 0.2s ease;

/* Hover effects */
transform: translateY(-2px);  /* NOT scale() */
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
```

### 2. Performance
- Use `transform` and `opacity` only
- Avoid animating `width`, `height`, `border`
- Maximum duration: 300ms
- Use `ease` or `ease-out` curves

## Content Strategy

### 1. Medical Content
- Clear, jargon-free language
- Bullet points over paragraphs
- Action-oriented labels
- Status indicators for urgency

### 2. Information Hierarchy
```
1. Card Title (what it does)
2. Status Label (required/optional)
3. Action Icon (visual cue)
4. Detailed content (in popups)
```

## Implementation Notes

### 1. State Management
```python
ui_state = {
    'high_contrast': False,
    'dark_mode': False, 
    'font_size': 'medium',  # small|medium|large|xl
    'large_text': False     # Additional accessibility boost
}
```

### 2. Responsive Text Classes
```python
# Example responsive typography
'text-base sm:text-lg md:text-xl lg:text-2xl'
# 16px → 18px → 20px → 24px
```

### 3. Card Interaction
```python
# Full card clickable (not just button)
.on('click', lambda: show_popup('card_type'))
# Better accessibility and UX
```

## Future Considerations

### 1. Progressive Enhancement
- Start with core functionality
- Add advanced features gradually
- Maintain fallbacks for older devices

### 2. Medical Compliance
- HIPAA compliance considerations
- Audit trail requirements
- Data privacy standards

### 3. Scalability
- Component-based architecture
- Consistent naming conventions
- Modular CSS/styling approach
