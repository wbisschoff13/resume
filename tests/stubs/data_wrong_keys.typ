// RED phase (T002): Deliberately broken YAML adapter stub
// Uses yaml() with correct file paths but maps keys incorrectly,
// verifying that wrong structure causes compilation failure.
//
// Expected: typst compile returns non-zero exit code.

#let _config = yaml("config.yaml")
#let _experience = yaml("experience.yaml")
#let _education = yaml("education.yaml")
#let _skills = yaml("skills.yaml")
#let _projects = yaml("projects.yaml")

// INTENTIONALLY WRONG: cv_data has wrong structure
// 1) experience is a single entry (dict) instead of array
// 2) education and skills use nonexistent keys
// 3) No .at() defensive access — raw field access
// 4) Many required keys missing: position, summary, ai_policy, etc.
//
// Nonexistent field access: _config.cover_letter.main_body
// returns none (Typst dict defaults), but entity is a dict
// not an array — .map/.filter will crash in template.

#let cv_data = (
  name: _config.name,
  email: _config.email,                 // wrong: nested under contact
  phone: _config.phone,                 // wrong: nested under contact
  location: _config.location,           // wrong: nested under contact
  github: _config.github,              // wrong: nested under contact
  website: _config.website,            // wrong: nested under contact
  linkedin: _config.linkedin,          // wrong: nested under contact

  // WRONG: single entry instead of array — template calls .filter() on this
  experience: _experience.at(0),

  // WRONG: wrong field names from education yaml
  education: _education.map(entry => (
    degree: entry.degree,              // correct
    institution: entry.institution,    // correct
    location: entry.location,          // doesn't exist in education yaml
    graduation_year: entry.graduation_year, // correct
    details: (),
  )),

  // WRONG: wrong field names from skills yaml
  skills: _skills.map(cat => (
    category_name: cat.category,       // correct: 'category' in yaml
    skills: cat.skills,                // wrong: 'items' in yaml
    variant: cat.variant,              // correct
  )),
)
