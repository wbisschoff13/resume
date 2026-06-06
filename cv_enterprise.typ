#import "content/data.typ": cv_data
#import "lib/template.typ": render_cv

#let filtered_experience = cv_data.experience.filter(entry =>
  entry.variant_tags.contains("enterprise")
)

#let filtered_skills = cv_data.skills.filter(cat =>
  cat.variant == "enterprise"
)

#let variant_data = cv_data + (
  position: "Enterprise Systems & Automation Architect",
  experience: filtered_experience,
  experience_entries: filtered_experience,
  skills: filtered_skills,
  skill_categories: filtered_skills,
)

#render_cv(variant_data, variant: "enterprise")
