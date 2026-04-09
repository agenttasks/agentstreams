---
name: algorithmic-art
description: Guide for creating generative art using p5.js through a two-phase system — first developing an algorithmic philosophy, then implementing it as interactive code. Use when users want to create computational art, generative visuals, or parametric designs.
license: Complete terms in LICENSE.txt
---

# Algorithmic Art Generation Guide

## Overview

This guide establishes a two-phase system for creating generative art using p5.js: first developing an algorithmic philosophy, then implementing it as interactive code.

## Phase 1: Algorithmic Philosophy

### Core Requirements

Create a computational aesthetic movement expressed through 4-6 paragraphs addressing:

- Mathematical relationships and noise functions
- Particle behaviors and field dynamics
- Temporal evolution and emergent complexity
- Parametric variation and controlled chaos

### Critical Emphasis

The philosophy must repeatedly stress that the final algorithm should appear "meticulously crafted," representing "deep computational expertise" and "master-level implementation."

### Key Principle

"The concept is a subtle, niche reference embedded within the algorithm itself -- not always literal, always sophisticated."

## Phase 2: P5.js Implementation

### Starting Point (Critical)

Read `templates/viewer.html` first. This file provides:

- Fixed layout structure and Anthropic branding
- Seed navigation controls (previous, next, random, jump)
- Action buttons (regenerate, reset, download)
- Sidebar organization

Replace only variable sections: the algorithm itself, parameter definitions, and UI controls for those parameters.

### Parameter Structure

Design parameters that answer: "What qualities of this system should be adjustable?" Focus on quantities, scales, probabilities, ratios, angles, and thresholds. Always include a seed parameter for reproducibility.

### Technical Requirements

- Use seeded randomness via `randomSeed()` and `noiseSeed()`
- Create self-contained single HTML artifacts with inline code
- Include all p5.js from CDN (no external files)
- Ensure real-time parameter updates
- Maintain performance and visual balance

### Craftsmanship Standards

Every parameter requires careful tuning. Achieve complexity without visual noise, order without rigidity. Balance composition and color harmony.

## Output Format

1. **Algorithmic Philosophy** (.md) - Poetic computational worldview
2. **Interactive HTML Artifact** - Self-contained generative art with controls, built from the template
