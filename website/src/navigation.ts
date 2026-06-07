import { getPermalink, getBlogPermalink } from './utils/permalinks';
import { CONTACT_INFO } from './config/contact';

export const headerData = {
  links: [
    { text: 'Home', href: getPermalink('/') },
    { text: 'Work', href: getPermalink('/work') },
    { text: 'Resume', href: getPermalink('/resume') },
    { text: 'Notes', href: getBlogPermalink() },
    { text: 'Contact', href: getPermalink('/contact') },
  ],
  actions: [],
};

export const footerData = {
  email: CONTACT_INFO.email,
  socialLinks: [
    {
      ariaLabel: 'GitHub',
      icon: CONTACT_INFO.social.github.icon,
      href: CONTACT_INFO.social.github.url,
    },
    {
      ariaLabel: 'LinkedIn',
      icon: CONTACT_INFO.social.linkedin.icon,
      href: CONTACT_INFO.social.linkedin.url,
    },
  ],
  // footNote: '© 2026 Werner Bisschoff. All rights reserved.',
  links: [],
  secondaryLinks: [],
};
