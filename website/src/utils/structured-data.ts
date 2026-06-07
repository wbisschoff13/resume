/**
 * Structured Data Utilities
 *
 * Generates JSON-LD schema.org structured data for SEO.
 * Single source of truth for all schemas - import from pages to ensure consistency.
 */

import { CONTACT_INFO } from '~/config/contact';
import type { CollectionEntry } from 'astro:content';

/**
 * Generate Person schema with contract availability
 */
export const getPersonSchema = (): object => {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: CONTACT_INFO.name,
    jobTitle: `${CONTACT_INFO.jobTitle} — Available for Contract`,
    url: CONTACT_INFO.siteUrl,
    address: {
      '@type': 'PostalAddress',
      addressLocality: CONTACT_INFO.location,
      addressCountry: CONTACT_INFO.country,
    },
    sameAs: [
      CONTACT_INFO.social.github.url,
      CONTACT_INFO.social.linkedin.url,
      ...(CONTACT_INFO.social.twitter ? [CONTACT_INFO.social.twitter.url] : []),
    ],
    knowsAbout: [
      'Embedded Systems',
      'System Architecture',
      'Spec-Driven Development',
      'AI Agentic Workflows',
      'Performance Optimization',
    ],
    seeks: {
      '@type': 'Demand',
      itemOffered: {
        '@type': 'Service',
        name: 'Software Engineering Contract',
        description: 'Freelance software engineer available for contract work, consulting, and part-time engagements.',
      },
    },
  };
};

/**
 * Generate WebSite schema
 */
export const getWebSiteSchema = (): object => {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    url: CONTACT_INFO.siteUrl,
    name: CONTACT_INFO.name,
    description: `${CONTACT_INFO.jobTitle} based in ${CONTACT_INFO.location}, ${CONTACT_INFO.country}`,
  };
};

/**
 * Generate FAQPage schema
 */
export const getFaqSchema = (): object => {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: `Is ${CONTACT_INFO.name} available for contract or freelance work?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `Yes — currently open to freelance, contract, part-time, and full-time opportunities. Based in ${CONTACT_INFO.location}, ${CONTACT_INFO.country}, available for remote work internationally. Specializes in embedded systems, backend services, and AI-assisted development workflows.`,
        },
      },
      {
        '@type': 'Question',
        name: `What type of work is ${CONTACT_INFO.name} available for?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `Open to freelance, contract, part-time, full-time, and remote work opportunities. Based in ${CONTACT_INFO.location}, ${CONTACT_INFO.country}.`,
        },
      },
      {
        '@type': 'Question',
        name: `What are ${CONTACT_INFO.name}'s key skills?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Specializes in AI-agentic workflows, spec-driven development, and resilient systems architecture. Expert in C/C++, Python, JavaScript/TypeScript, Elixir, embedded systems (ESP32, FreeRTOS, BLE), and cloud technologies (AWS, Docker).',
        },
      },
      {
        '@type': 'Question',
        name: `What is ${CONTACT_INFO.name}'s educational background?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `${CONTACT_INFO.education.degree} from ${CONTACT_INFO.education.school}, graduated in ${CONTACT_INFO.education.year}.`,
        },
      },
      {
        '@type': 'Question',
        name: `Where is ${CONTACT_INFO.name} located?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `Based in ${CONTACT_INFO.location}, ${CONTACT_INFO.country}. Open to remote work internationally.`,
        },
      },
    ],
  };
};

/**
 * Generate ContactPage schema
 */
export const getContactPageSchema = (): object => {
  return {
    '@context': 'https://schema.org',
    '@type': 'ContactPage',
    name: `Contact ${CONTACT_INFO.name}`,
    url: `${CONTACT_INFO.siteUrl}/contact`,
    description: 'Get in touch to discuss software engineering needs, freelance opportunities, or contract work.',
    contactPoint: {
      '@type': 'ContactPoint',
      email: CONTACT_INFO.email,
      contactType: 'professional',
      availableLanguage: ['English'],
    },
    sameAs: [CONTACT_INFO.social.github.url, CONTACT_INFO.social.linkedin.url],
  };
};

export interface JobPostingInput {
  title: string;
  company: string;
  period: string;
  description: string[];
  location?: string;
  employmentType?: string;
}

/**
 * Generate JobPosting schema for a single experience
 */
export const getJobPostingSchema = (job: JobPostingInput): object => {
  return {
    '@context': 'https://schema.org',
    '@type': 'JobPosting',
    title: job.title,
    employer: {
      '@type': 'Organization',
      name: job.company,
    },
    datePosted: job.period.split('--')[0].trim() + '-01',
    description: job.description.join(' '),
    jobLocation: {
      '@type': 'Place',
      address: {
        '@type': 'PostalAddress',
        addressLocality: job.location || CONTACT_INFO.location,
        addressCountry: CONTACT_INFO.country,
      },
    },
    employmentType: job.employmentType || 'FULL_TIME',
  };
};

/**
 * Generate EducationalOccupationalCredential schema
 */
export const getEducationSchema = (): object => {
  return {
    '@context': 'https://schema.org',
    '@type': 'EducationalOccupationalCredential',
    name: CONTACT_INFO.education.degree,
    about: {
      '@type': 'Course',
      name: CONTACT_INFO.education.field,
    },
    provider: {
      '@type': 'Organization',
      name: CONTACT_INFO.education.school,
    },
    dateCompleted: String(CONTACT_INFO.education.year),
  };
};

export interface BlogPost {
  title: string;
  excerpt?: string;
  publishDate: Date;
  slug: string;
}

/**
 * Generate BlogPosting schema for a blog post
 */
export const getBlogPostingSchema = (post: CollectionEntry<'post'>, siteUrl: string): object => {
  const publishDate = post.data.publishDate || new Date();
  const updateDate = post.data.updateDate || post.data.publishDate;
  return {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.data.title,
    description: post.data.excerpt || '',
    datePublished: publishDate.toISOString(),
    dateModified: updateDate?.toISOString() || publishDate.toISOString(),
    author: {
      '@type': 'Person',
      name: CONTACT_INFO.name,
    },
    url: `${siteUrl}/notes/${post.id}`,
  };
};
