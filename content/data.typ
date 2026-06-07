#let _config = yaml("config.yaml")
#let _experience = yaml("experience.yaml")
#let _education = yaml("education.yaml")
#let _skills = yaml("skills.yaml")
#let _projects = yaml("projects.yaml")
#let _star_stories = yaml("star-stories.yaml")

#let _variants = ("general", "systems", "infrastructure", "embedded", "enterprise")

#let _star_map = {
  let m = (:)
  for s in _star_stories {
    m.insert(s.at("id", default: ""), s)
  }
  m
}

#let _init_variant_dict(f) = {
  let d = (:)
  for v in _variants { d.insert(v, f(v)) }
  d
}

#let _star_text(star_ref) = {
  if star_ref == none { return none }
  let story = _star_map.at(star_ref, default: none)
  if story == none { return none }
  let parts = ()
  for k in ("situation", "task", "action", "result") {
    let v = story.at(k, default: "")
    if v != "" { parts = parts + (v,) }
  }
  if parts.len() == 0 { none } else { parts.join("\n\n") }
}

#let _variant_cap(v) = if v == "general" { 3 } else { 2 }

#let _bullets_for_variant(bullets, variant) = {
  let mp = _variant_cap(variant)
  bullets
    .filter(b => b.at("variant", default: "") == variant and b.at("cv_priority", default: 3) <= mp)
    .map(b => (
      text: b.at("text", default: ""),
      star_story: _star_text(b.at("star_ref", default: none)),
    ))
}

#let _exp_entries = _experience.map(e => {
  let bullets = e.at("bullets", default: ())
  let desc = (:)
  let tags = ()
  for v in _variants {
    let bv = _bullets_for_variant(bullets, v)
    desc.insert(v, bv)
    if bv.len() > 0 { tags = tags + (v,) }
  }
  (
    role: e.at("role", default: (general: "")),
    company: e.at("company", default: ""),
    location: e.at("location", default: ""),
    start_date: e.at("start_date", default: ""),
    end_date: e.at("end_date", default: none),
    variant_tags: tags,
    description: desc,
  )
})

#let _edu_entries = _education.map(e => (
  degree: e.at("degree", default: ""),
  institution: e.at("institution", default: ""),
  location: "",
  graduation_year: e.at("end_date", default: ""),
  details: _init_variant_dict(v => ()),
))

#let _skill_cats = _skills.map(c => (
  category: c.at("category", default: ""),
  items: c.at("items", default: ()),
  variant: c.at("variant", default: ""),
))

#let _proj_entries = _projects.map(p => {
  let pd = p.at("description", default: "")
  (
    name: p.at("name", default: ""),
    description: _init_variant_dict(v => if pd != "" { (pd,) } else { () }),
    link: p.at("url", default: none),
  )
})

#let _cl_block = _config.at("cover_letter", default: (:))
#let _cl_data = (
  about_me: _cl_block.at("about_me", default: none),
  why_me: _cl_block.at("why_me", default: none),
  how_i_work: _cl_block.at("how_i_work", default: none),
)

#let _contact = _config.at("contact", default: (:))

#let cv_data = (
  name: _config.at("name", default: ""),
  email: _contact.at("email", default: ""),
  phone: _contact.at("phone", default: ""),
  location: _contact.at("location", default: ""),
  github: _contact.at("github", default: ""),
  website: _contact.at("website", default: ""),
  linkedin: _contact.at("linkedin", default: ""),
  position: _config.at("title", default: (general: "")),
  summary: _config.at("summary", default: none),
  ai_policy: _config.at("ai_policy", default: ()),
  job_target: _config.at("job_target", default: ()),
  certification: _config.at("certification", default: none),
  experience: _exp_entries,
  education: _edu_entries,
  skills: _skill_cats,
  projects: _proj_entries,
  cover_letter_data: _cl_data,
)
