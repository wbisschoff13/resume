// T003 RED: Template must handle YAML-original data shapes
//
// Before template changes (T003 Green), the current template expects:
//   - skills: cat.category_name, cat.skills
//   - education: entry.details (array), no entry.field
//   - exp description: flat string array (star_ref baked in by adapter)
//
// But when fed data in the canonical YAML shape (without adapter mapping):
//   - skills use category/items keys  → cat.skills is none → .map() type error
//   - bullets are objects with text/star_ref → not rendered as nested content
//
// Expected: typst compile returns non-zero exit code

#import "lib/template.typ": render_cv

#let raw_data = (
  name: "Test User",
  email: "test@test.com",
  phone: "+27 00 000 0000",
  location: "Cape Town",
  github: "testuser",
  website: "https://test.dev",
  linkedin: "testuser",
  position: (general: "Engineer"),
  summary: none,
  certification: none,
  ai_policy: (),
  job_target: (),
  cover_letter_data: (:),

  // RAW YAML shape: bullets are objects with text + star_ref
  experience: (
    (
      role: (general: "Engineer", systems: "Systems Eng"),
      company: "Test Corp",
      location: "Cape Town",
      start_date: "Jan 2020",
      end_date: "Dec 2023",
      variant_tags: ("general", "systems"),
      description: (
        (text: "Built distributed systems", star_ref: "star-001"),
        (text: "Fixed critical bugs", star_ref: none),
      ),
    ),
  ),

  // RAW YAML shape: education has field (not details array)
  education: (
    (
      degree: "B.Sc. Computer Science",
      institution: "Test University",
      location: "",
      graduation_year: "2020",
      field: "Computer Science",
    ),
  ),

  // RAW YAML shape: skills use category + items (not category_name + skills)
  skills: (
    (category: "Primary", items: ("C++", "Python"), variant: "general"),
    (category: "Secondary", items: ("Docker", "Linux"), variant: "general"),
  ),

  projects: (),
)

// This call FAILS because cat.skills is none (key is 'items', not 'skills')
// none.map(s => text(s)) → type error
#render_cv(raw_data, variant: "general")
