/**
 * Accessibility Utilities
 *
 * Utility functions for detecting and respecting user accessibility preferences.
 * Ensures WCAG 2.1 AA compliance for motion preferences.
 *
 * PRD Reference: FR-019, FR-020, FR-021
 * Task Reference: TM-013
 */

/**
 * Check if animations should be enabled based on user's motion preference.
 *
 * Respects the `prefers-reduced-motion` media query to support users who
 * experience vestibular motion disorders or prefer reduced motion.
 *
 * @returns {boolean} True if animations should play, false if motion is reduced
 *
 * @example
 * ```ts
 * import { shouldAnimate } from '~/utils/a11y';
 *
 * if (shouldAnimate()) {
 *   animate(element, { opacity: [0, 1] });
 * } else {
 *   // Apply final state immediately without animation
 *   element.style.opacity = '1';
 * }
 * ```
 */
export function shouldAnimate(): boolean {
  // SSR safety check: window is not available during server-side rendering
  if (typeof window === 'undefined') {
    return false;
  }

  // Check if user prefers reduced motion
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Return true (should animate) only if user does NOT prefer reduced motion
  return !prefersReducedMotion;
}

/**
 * Get the appropriate animation duration based on user's motion preference.
 *
 * Returns 0 duration if user prefers reduced motion, otherwise returns the
 * provided duration in milliseconds.
 *
 * @param durationMs - Duration in milliseconds when animations are enabled
 * @returns {number} Duration in milliseconds (0 if reduced motion preferred)
 *
 * @example
 * ```ts
 * import { getAnimationDuration } from '~/utils/a11y';
 *
 * const duration = getAnimationDuration(500); // Returns 0 or 500
 * animate(element, { opacity: [0, 1] }, { duration: duration / 1000 });
 * ```
 */
export function getAnimationDuration(durationMs: number): number {
  return shouldAnimate() ? durationMs : 0;
}

/**
 * Safely execute an animation only if the user does not prefer reduced motion.
 * Otherwise, apply the final state immediately.
 *
 * @param element - The element to animate
 * @param keyframes - Animation keyframes
 * @param options - Animation options
 * @param finalState - CSS properties to apply if animation is skipped
 *
 * @example
 * ```ts
 * import { safeAnimate } from '~/utils/a11y';
 * import { animate } from 'motion';
 *
 * safeAnimate(
 *   myElement,
 *   { opacity: [0, 1] },
 *   { duration: 0.5 },
 *   { opacity: '1' }
 * );
 * ```
 */
export async function safeAnimate(
  element: HTMLElement | HTMLElement[],
  keyframes: Record<string, unknown>,
  options?: Record<string, unknown>,
  finalState?: Record<string, string | number>
): Promise<void> {
  if (!shouldAnimate() || typeof window === 'undefined') {
    // Apply final state immediately without animation
    const elements = Array.isArray(element) ? element : [element];

    elements.forEach((el) => {
      if (finalState) {
        Object.assign(el.style, finalState);
      } else if (keyframes && typeof keyframes === 'object') {
        // Extract final values from keyframes (last frame of array or object values)
        Object.entries(keyframes).forEach(([prop, value]) => {
          const finalValue = Array.isArray(value) ? value[value.length - 1] : value;
          // Type assertion needed for dynamic property assignment
          (el as HTMLElement & { style: Record<string, string> }).style[prop] = String(finalValue);
        });
      }
    });

    return Promise.resolve();
  }

  // Import animate dynamically to avoid SSR issues
  const { animate } = await import('motion');
  return animate(element, keyframes, options);
}
