#set text(ligatures: false)

#let _cv_fonts = ("Helvetica", "Libertinus Serif")

#let _resolve(value, variant) = {
  if type(value) == dictionary and variant in value {
    value.at(variant)
  } else {
    value
  }
}

#let _resolve_entries(entries, variant) = {
  entries.map(entry => (
    role: _resolve(entry.at("role", default: "Role"), variant),
    company: entry.at("company", default: ""),
    location: entry.at("location", default: none),
    start_date: entry.at("start_date", default: ""),
    end_date: entry.at("end_date", default: none),
    description: _resolve(entry.at("description", default: ()), variant),
  ))
}

#let _resolve_education(entries, variant) = {
  entries.map(entry => (
    degree: entry.at("degree", default: ""),
    institution: entry.at("institution", default: ""),
    location: entry.at("location", default: ""),
    graduation_year: entry.at("graduation_year", default: ""),
    details: _resolve(entry.at("details", default: ()), variant),
  ))
}

#let _resolve_projects(entries, variant) = {
  entries.map(entry => (
    name: entry.at("name", default: ""),
    description: _resolve(entry.at("description", default: ()), variant),
    link: entry.at("link", default: none),
  ))
}

#let _section(title) = {
  text(size: 12pt, weight: "bold", title)
  line(length: 100%)
  v(0.1cm)
}

#let render_header(name, email, phone, location) = {
  align(center, text(size: 18pt, weight: "bold", name))
  align(center, text(size: 10pt)[
    #email \
    #phone \
    #location
  ])
  v(0.4cm)
}

#let render_summary(summary) = {
  _section("Professional Summary")
  summary
  v(0.25cm)
}

#let render_experience(entries) = {
  if entries.len() > 0 {
    _section("Experience")
    for entry in entries {
      grid(
        columns: (1fr, auto),
        gutter: 0.2cm,
        [#text(weight: "bold", entry.role) \ #if entry.location != none { entry.location }],
        [#text(entry.company) \ #entry.start_date #if entry.end_date != none { [-- #entry.end_date] }],
      )
      v(0.05cm)
      for desc in entry.description {
        [- #desc]
        v(0.05cm)
      }
      v(0.2cm)
    }
  }
}

#let render_education(entries) = {
  if entries.len() > 0 {
    _section("Education")
    for entry in entries {
      grid(
        columns: (1fr, auto),
        gutter: 0.2cm,
        [#text(weight: "bold", entry.degree) \ #entry.location],
        [#text(entry.institution) \ #entry.graduation_year],
      )
      v(0.05cm)
      for detail in entry.details {
        [- #detail]
        v(0.05cm)
      }
      v(0.2cm)
    }
  }
}

#let render_skills(categories) = {
  if categories.len() > 0 {
    _section("Skills")
    for cat in categories {
      [#cat.category_name: #cat.skills.join(", ")]
      v(0.05cm)
    }
    v(0.25cm)
  }
}

#let render_projects(entries) = {
  if entries.len() > 0 {
    _section("Projects")
    for entry in entries {
      text(weight: "bold", entry.name)
      v(0.05cm)
      for desc in entry.description {
        [- #desc]
        v(0.05cm)
      }
      v(0.2cm)
    }
  }
}

#let render_ai_policy(content) = {
  if content != none {
    _section("AI Policy")
    for item in content {
      item
      v(0.05cm)
    }
    v(0.25cm)
  }
}

#let render_job_target(content) = {
  if content != none {
    _section("Job Target")
    content
    v(0.25cm)
  }
}

#let render_cv(data, variant: "general") = {
  set page(
    paper: "a4",
    margin: (top: 1.5cm, bottom: 1.5cm, left: 2cm, right: 2cm),
  )
  set text(
    font: _cv_fonts,
    ligatures: false,
    size: 10pt,
  )
  set par(justify: true, leading: 0.65em)

  let name = _resolve(data.at("name", default: ""), variant)
  let email = _resolve(data.at("email", default: ""), variant)
  let phone = _resolve(data.at("phone", default: ""), variant)
  let location = _resolve(data.at("location", default: ""), variant)
  let position = _resolve(data.at("position", default: none), variant)
  let summary = _resolve(data.at("summary", default: none), variant)
  let entries = _resolve_entries(
    data.at("experience", default: data.at("experience_entries", default: ())),
    variant,
  )
  let education = _resolve_education(
    data.at("education", default: data.at("education_entries", default: ())),
    variant,
  )
  let skills = data.at("skills", default: data.at("skill_categories", default: ()))
  let projects = _resolve_projects(
    data.at("projects", default: data.at("project_entries", default: ())),
    variant,
  )
  let ai_policy = data.at("ai_policy", default: none)
  let job_target = data.at("job_target", default: none)

  render_header(name, email, phone, location)
  if position != none {
    align(center, text(size: 11pt, weight: "bold", position))
    v(0.3cm)
  }
  if summary != none { render_summary(summary) }
  render_experience(entries)
  render_education(education)
  render_skills(skills)
  render_projects(projects)
  render_ai_policy(ai_policy)
  render_job_target(job_target)
}

#let render_cover_letter(data, variant: "general") = {
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  )
  set text(
    font: _cv_fonts,
    ligatures: false,
    size: 11pt,
  )
  set par(justify: true, leading: 0.65em)

  let cl = data.at("cover_letter_data", default: (:))
  let recipient_name = cl.at("recipient_name", default: none)
  let recipient_title = cl.at("recipient_title", default: none)
  let company = cl.at("company", default: none)
  let date = cl.at("date", default: none)
  let about_me = _resolve(cl.at("about_me", default: none), variant)
  let why_me = _resolve(cl.at("why_me", default: none), variant)
  let name = data.at("name", default: "")
  let email = data.at("email", default: "")
  let phone = data.at("phone", default: "")
  let location = data.at("location", default: "")

  if date != none {
    [#date \ ]
  }
  v(1cm)
  if recipient_name != none {
    [#recipient_name \ ]
  }
  if recipient_title != none {
    [#recipient_title \ ]
  }
  if company != none {
    [#company \ ]
  }
  v(0.5cm)

  if recipient_name != none {
    [Dear #recipient_name,]
    v(0.3cm)
  }

  if about_me != none {
    about_me
    v(0.3cm)
  }

  if why_me != none {
    for point in why_me {
      point
      v(0.15cm)
    }
  }
  v(0.3cm)

  [Sincerely,]
  [#name]
  [#email]
  [#phone]
  [#location]
}
