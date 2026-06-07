/**
 * Contact Information Configuration
 *
 * Single source of truth for all contact/personal details across the site.
 * Update these values to change contact information everywhere.
 */

export const CONTACT_INFO = {
  // Personal details
  name: 'Werner Bisschoff',
  jobTitle: 'Software Engineer',
  location: 'Cape Town',
  country: 'South Africa',

  // Contact
  email: 'contact@bisschoff.dev',
  siteUrl: 'https://werner.bisschoff.dev',

  // Resume PDF
  resume: {
    pdfUrl: 'https://github.com/wbisschoff13/resume/releases/latest/download/W_Bisschoff_CV.pdf',
  },

  // Education
  education: {
    degree: 'B.Eng. Computer and Electronic Engineering',
    field: 'Computer and Electronic Engineering',
    school: 'North-West University',
    year: 2020,
  },

  // Social links
  social: {
    github: {
      url: 'https://github.com/wbisschoff13',
      username: 'wbisschoff13',
      icon: 'tabler:brand-github',
    },
    linkedin: {
      url: 'https://linkedin.com/in/wbisschoff13',
      username: 'wbisschoff13',
      icon: 'tabler:brand-linkedin',
    },
    twitter: {
      url: 'https://twitter.com/wbisschoff13',
      username: 'wbisschoff13',
    },
  },
} as const;
