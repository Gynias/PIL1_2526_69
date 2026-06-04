---
name: Academic Nexus
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#464554'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#767586'
  outline-variant: '#c7c4d7'
  surface-tint: '#494bd6'
  primary: '#4648d4'
  on-primary: '#ffffff'
  primary-container: '#6063ee'
  on-primary-container: '#fffbff'
  inverse-primary: '#c0c1ff'
  secondary: '#006b5f'
  on-secondary: '#ffffff'
  secondary-container: '#6df5e1'
  on-secondary-container: '#006f64'
  tertiary: '#825100'
  on-tertiary: '#ffffff'
  tertiary-container: '#a36700'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#71f8e4'
  secondary-fixed-dim: '#4fdbc8'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005048'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  container-max: 1280px
  sidebar-width: 260px
  navbar-height: 64px
---

## Brand & Style
The design system is built for a mentorship environment that balances academic rigor with modern accessibility. The brand personality is **Knowledgeable, Supportive, and Focused**. It aims to evoke a sense of professional growth and reliable guidance for university students and mentors.

The visual style is **Corporate / Modern** with a lean towards **Minimalism**. It prioritizes clarity and information density without overwhelming the user. The interface utilizes generous whitespace, crisp typography, and a systematic approach to hierarchy to ensure that the focus remains on human connection and educational advancement.

## Colors
The color strategy employs a vibrant **Indigo (#6366F1)** as the primary driver for actions and brand recognition. This is paired with a **Teal (#14B8A6)** secondary color used for success states and secondary highlights, representing growth.

The neutral palette is grounded in slate grays to maintain a sophisticated, academic feel. The background uses a very light cool gray (`#F8FAFC`) to differentiate from white surface cards. Semantic colors for compatibility scores are strictly mapped: 
- **Green (>80%)**: High compatibility.
- **Amber (60-80%)**: Moderate compatibility.
- **Red (<60%)**: Low compatibility/Requires attention.

## Typography
This design system utilizes **Inter** exclusively to leverage its exceptional legibility and systematic weight distribution. 

Headlines use tighter letter-spacing and heavier weights to create a strong visual anchor. The body text is optimized for long-form reading of mentor bios and program descriptions. Labels for compatibility scores and metadata use a slightly heavier weight (`500` or `600`) to ensure they stand out against body copy.

## Layout & Spacing
The system follows an **8px grid** for consistent spatial rhythm. 

- **Desktop Dashboard:** Utilizes a fixed 260px sidebar for navigation with a fluid content area.
- **Public/Landing Pages:** Utilizes a 12-column centered fixed grid with a 1280px max-width.
- **Margins & Gutters:** Mobile views use 16px side margins; tablet and desktop use 24px or 32px depending on content density.
- **Reflow Rules:** On mobile, sidebars transition to a bottom-sheet navigation or a hidden hamburger menu, and 3-column card layouts stack vertically.

## Elevation & Depth
Hierarchy is achieved through **Tonal Layers** and subtle **Ambient Shadows**. 

The base background is neutral gray, while cards and primary containers are white. To suggest interactivity, cards use a low-blur, low-opacity shadow (e.g., `0px 4px 12px rgba(0, 0, 0, 0.05)`). When a user hovers over a mentor card, the elevation should increase slightly via a more pronounced shadow to provide tactile feedback. High-contrast outlines (`1px solid #E2E8F0`) are used for input fields and non-elevated containers to maintain a structured, academic look.

## Shapes
The shape language is **Rounded**, signifying a modern and approachable academic environment. 

The standard radius is **8px** (`0.5rem`) for standard components like buttons, input fields, and small cards. Larger containers, such as main dashboard cards or modals, utilize **16px** (`1rem`) to soften the overall appearance of the interface. Badges and tags utilize a full "pill" radius for distinct visual separation from interactive buttons.

## Components

### Buttons
- **Primary:** Solid Indigo (`#6366F1`) with white text. High contrast is mandatory.
- **Secondary:** Outlined Indigo with a 1px border.
- **Tertiary:** Ghost style, using text color only, with a light gray background on hover.

### Badges (Compatibility Scores)
Badges feature a subtle background tint and a high-contrast text color of the same hue.
- **High (>80%):** Green background (10% opacity) + Green text.
- **Medium (60-80%):** Amber background (10% opacity) + Amber text.
- **Low (<60%):** Red background (10% opacity) + Red text.

### Inputs & Validation
Standard inputs use an 8px radius with a 1px slate-200 border. On focus, the border transitions to Primary Indigo with a subtle outer glow. Validation states must show a clear 1px border in the semantic color (Red for error) and a supporting helper text below the field.

### Loading Skeletons
Use a shimmering gray gradient (`#F1F5F9` to `#E2E8F0`) for all card-based content to reduce perceived latency during mentor searches.

### Cards
Cards are the primary container for mentor profiles. They must include a standard 16px padding, 1px subtle border, and the level 1 shadow. Headers within cards should use `headline-sm`.