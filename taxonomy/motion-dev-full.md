---
source: https://motion.dev/sitemap.xml
domain: motion.dev
crawled_at: 2026-04-08T00:00:00Z
page_count: 3
error_count: 0
crawler: webfetch (sandbox fallback — run crawl-sitemap.py for full crawl)
---

# motion.dev — Animation Library Taxonomy

Source: `https://motion.dev/sitemap.xml`
Crawled: 2026-04-08 (partial — 3 key docs pages via WebFetch; full sitemap has 900+ URLs)
Pages: 3 fetched, 0 errors

Note: Full crawl requires running outside sandbox:
```bash
uv run scripts/crawl-sitemap.py https://motion.dev/sitemap.xml \
  taxonomy/motion-dev-full.md --max-pages 500 --concurrency 10 --rate-delay 0.1
```

## Pages

### react-quick-start

URL: https://motion.dev/docs/react-quick-start
Hash: motion-quickstart

```
Motion for React (formerly Framer Motion) is a React animation library for
building smooth, production-grade UI animations. The library leverages a hybrid
engine using Web Animations API and ScrollTimeline for 120fps performance.

Core Capabilities:
- Animation Types: Spring physics for physical properties (x, scale); tween easing
  for visual properties (opacity)
- Gesture Support: robust, cross-device gesture recognisers for tap, drag, and hover
- Scroll Animations: Both scroll-triggered (whileInView) and scroll-linked (useScroll)
- Layout Animations: Detects and animates size, position, and reorder changes
- SVG Animations: Full support including pathLength and viewBox animations
- Exit Animations: AnimatePresence component enables DOM removal animations

Installation: npm install motion
Import: import { motion } from "motion/react"

Main Components:
- motion (base component with animate, whileHover, exit props)
- AnimatePresence
- MotionConfig
- LazyMotion
- LayoutGroup
- AnimateNumber, Carousel, ScrambleText, Ticker, Typewriter

Key Hooks:
- useScroll, useSpring, useTransform
- useMotionTemplate, useMotionValueEvent
- useTime, useVelocity
- useAnimate, useAnimationFrame
- useDragControls, useInView, useReducedMotion

Code Examples:
  <motion.button animate={{ opacity: 1 }} />
  <motion.button initial={{ scale: 0 }} animate={{ scale: 1 }} />
  <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }} />
  <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} />
  <motion.div layout />
  <motion.div layoutId="underline" />
```

### react-animation

URL: https://motion.dev/docs/react-animation
Hash: motion-animation-api

```
Animation Props:
- animate: Target values for continuous animations
- initial: Starting values before animation begins
- exit: Values applied when element leaves DOM
- whileHover, whileTap, whileFocus, whileDrag, whileInView: Gesture triggers

Animatable Values:
- Transform: x, y, z, scale, scaleX, scaleY, rotate, rotateX, rotateY, rotateZ, skewX, skewY
- CSS: opacity, filter, any standard CSS property
- Colors: hex, rgba, hsla, oklch, oklab, color-mix
- Complex strings: box-shadow
- Display/visibility: "none", "block", "hidden", "visible"
- CSS variables: "--variable-name"
- SVG attributes: attrX, attrY

Keyframe Animations:
  animate={{ x: [0, 100, 0] }}
  Wildcard keyframes: null references current value
  Timing: times option with progress values 0-1

Transition Configuration:
- duration: seconds
- ease: "easeOut", custom curves
- type: "spring", "tween", "inertia"
- repeat: Infinity for continuous
- stagger(): stagger child animations
- when: "beforeChildren", "afterChildren"

Variants System:
  const variants = { visible: { opacity: 1 }, hidden: { opacity: 0 } }
  Dynamic variants: functions receiving custom prop
  Propagation: children inherit parent variant changes

Advanced Components:
- AnimateNumber: animated numeric values
- Reorder: animated list reordering
- Carousel: image carousel
- ScrambleText: text scramble effects
- Ticker: scrolling ticker
- Typewriter: typewriter text effect

Hooks for Imperative Control:
- useAnimate(): sequence animations, control playback
- useMotionValue(): track individual values
- useTransform(): derive values from other motion values
- useSpring(): spring physics animations
```

### react-scroll-animations

URL: https://motion.dev/docs/react-scroll-animations
Hash: motion-scroll

```
Scroll Animation APIs:

whileInView Prop:
  <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} />
  viewport={{ once: true }} for single-play animations

useScroll Hook:
  Returns scrollX, scrollY, scrollXProgress, scrollYProgress (0 to 1)
  Links CSS styles directly to scroll position

useInView Hook:
  Sets React state when element enters/leaves viewport
  Works with non-motion components

useTransform Hook:
  Maps scroll progress to any CSS value — colors, positions, blur

useSpring Hook:
  Smooths scroll value changes through configurable spring physics

Key Patterns:

Scroll-Triggered: Fire when elements enter/exit viewport
  viewport={{ once: true }} for one-time play

Scroll-Linked: Connect values directly to scroll position
  Parallax, progress bars, interactive effects

Parallax Scrolling:
  Background at 0.5px/scroll-px, foreground at 2px/scroll-px

Progress Bars:
  Link scrollYProgress to scaleX for reading progress

Horizontal Scroll Sections:
  300vh height container + sticky positioning + useTransform
  Maps vertical scroll to horizontal translation

Direction Detection:
  useMotionValueEvent on scrollY for directional changes

Performance:
  Native ScrollTimeline for hardware acceleration
  IntersectionObserver pooling for minimal overhead
```

---

Crawl complete: 3 pages fetched, 0 errors
