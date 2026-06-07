#import "content/data.typ": cv_data
#import "lib/template.typ": render_cv

#let filtered_experience = cv_data.experience.filter(entry =>
  entry.variant_tags.contains("infrastructure")
)

#let filtered_skills = cv_data.skills.filter(cat =>
  cat.variant == "infrastructure"
)

#let variant_data = cv_data + (
  position: "Cloud Infrastructure Engineer / Platform Developer",
  experience: filtered_experience,
  skills: filtered_skills,
)

#render_cv(variant_data, variant: "infrastructure")
