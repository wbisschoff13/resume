#import "modern-cv.typ": *

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
    location: entry.at("location", default: ""),
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

#let render_cv(data, variant: "general") = {
  let name = _resolve(data.at("name", default: ""), variant)
  let name_parts = name.split(" ")
  let firstname = name_parts.first()
  let lastname = name_parts.slice(1).join(" ")
  let email = data.at("email", default: "")
  let phone = data.at("phone", default: "")
  let address = data.at("location", default: "")
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
  let filtered_skills = skills.filter(cat => cat.variant == variant)
  let certification = data.at("certification", default: none)
  let author = (
    firstname: firstname,
    lastname: lastname,
    email: email,
    phone: phone,
    address: address,
    github: data.at("github", default: ""),
    website: data.at("website", default: ""),
    linkedin: data.at("linkedin", default: ""),
    positions: if position != none { (position,) } else { () },
    certification: certification,
  )

  let cfg = resume.with(
    author: author,
    date: datetime.today().display(),
    language: "en",
    colored-headers: true,
    show-footer: false,
    show-address-icon: true,
    paper-size: "a4",
    profile-picture: none,
  )

  cfg[
    #if summary != none [
      #v(0.3cm)
      #set text(size: 10pt)
      #summary
      #v(0.1cm)
    ]

    #if filtered_skills.len() > 0 [
      = Skills
      #for cat in filtered_skills [
        #resume-skill-item(cat.category_name, cat.skills.map(s => text(s)))
      ]
    ]

    #if entries.len() > 0 [
      = Experience
      #for entry in entries [
        #resume-entry(
          title: entry.role,
          location: if entry.location != none { entry.location } else { "" },
          date: if entry.end_date != none {
            entry.start_date + " – " + entry.end_date
          } else { entry.start_date },
          description: entry.company,
        )
        #if entry.description.len() > 0 [
          #resume-item[
            #for desc in entry.description [
              - #desc
            ]
          ]
        ]
      ]
    ]

    #if education.len() > 0 [
      = Education
      #for entry in education [
        #resume-entry(
          title: entry.degree,
          location: entry.location,
          date: entry.graduation_year,
          description: entry.institution,
        )
        #if entry.details.len() > 0 [
          #resume-item[#entry.details.join(" · ")]
        ]
      ]
    ]

    #if projects.len() > 0 [
      = Projects
      #for entry in projects [
        #resume-entry(
          title: entry.name,
          location: if entry.link != none { entry.link } else { "" },
        )
        #if entry.description.len() > 0 [
          #resume-item[
            #for desc in entry.description [
              - #desc
            ]
          ]
        ]
      ]
    ]
  ]
}

#let render_cover_letter(data, variant: "general") = {
  let name = data.at("name", default: "")
  let name_parts = name.split(" ")
  let firstname = name_parts.first()
  let lastname = name_parts.slice(1).join(" ")
  let email = data.at("email", default: "")
  let phone = data.at("phone", default: "")
  let address = data.at("location", default: "")
  let position = _resolve(data.at("position", default: none), variant)
  let cl = data.at("cover_letter_data", default: (:))
  let about_me = _resolve(cl.at("about_me", default: none), variant)
  let why_me = _resolve(cl.at("why_me", default: none), variant)
  let how_i_work = _resolve(cl.at("how_i_work", default: none), variant)

  let cfg = coverletter.with(
    author: (
      firstname: firstname,
      lastname: lastname,
      email: email,
      phone: phone,
      address: address,
      github: data.at("github", default: ""),
      website: data.at("website", default: ""),
      linkedin: data.at("linkedin", default: ""),
      positions: if position != none { (position,) } else { () },
    ),
    profile-picture: none,
    date: datetime.today().display(),
    language: "en",
    show-footer: false,
    show-address-icon: true,
    paper-size: "a4",
  )

  cfg[
    #if position != none [
      #letter-heading(job-position: position, addressee: "Hiring Manager")
    ]

    #if about_me != none [
      #about_me
      #v(0.3cm)
    ]

    #if why_me != none [
      #for point in why_me [
        #point
        #v(0.15cm)
      ]
    ]

    #if how_i_work != none [
      #how_i_work
    ]
  ]
}
