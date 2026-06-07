/**
 * Motion Animation Utilities
 *
 * Utility functions for Motion (Framer Motion) library.
 * Provides re-exported animation functions for use across the site.
 *
 * PRD Reference: FR-001, FR-002
 * Task Reference: TM-011
 */

// Core animation function
export { animate } from 'motion';

// Re-export types for TypeScript support
export type { AnimationPlaybackControls, AnimationOptions, AnimationScope, DOMKeyframesDefinition } from 'motion';
