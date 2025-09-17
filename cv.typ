#let details = toml("details.toml")

#set document(
  title: "Curriculum Vitae of Stéphane Wirtel",
  author: "Stéphane Wirtel",
  date: datetime.today(),
)
#set page(
  footer: context[
    Updated on #datetime.today().display()
  ]
)

= Introduction
Firstname: #details.personal.first_name
#linebreak()
Lastname: #details.personal.last_name
#linebreak()
#details.personal.about_me
#link(details.personal.github)[Github]
#linebreak()
#link(details.personal.linkedin)[LinkedIn]
#linebreak()

Updated: #datetime.today().display()

#let find_current_position(position) = ("current" in position and position.at("current") == true)

#let positions = details.positions.sorted(key: it => it.date_from).rev()

#let current_position = positions.find(find_current_position)

#let render_position(position) = {
  // if not "date_to" in position {
  //   [Current]
  // }
  grid(
    columns: (5fr, 35fr),
    row-gutter: 0.5em,
    column-gutter: 1em,
    align: (left, left),
    ..(
          ..if position.date_from != none { (position.date_from,) },
          ..if position.title != none and position.name != none {
            (
              grid(
                columns: (1fr, 1fr),
                align: (left, right),
              )[
                #text(weight: "bold", position.title)
                #text(fill: black.lighten(75%), box(width: 1fr, repeat[.]))
              ][
                #text(fill: black.lighten(75%), box(width: 1fr, repeat[.]))
                #text(fill: black.lighten(70%))[#position.name]
              ],
            )
          },
          {
            set text(fill: black.lighten(70%))
            grid(
              row-gutter: .5em,
              "Fulltime", "Brussels"
            )
          },
          {
            text(position.description)
          }
    )
  )
}

#if current_position != none {
  [== Current Position]
  [#render_position(current_position)]
  linebreak()
}

#let select_former_position(position) = ((not "current" in position) or position.at("current") == false)
#let former_positions = positions.filter(select_former_position)

== Former Positions
#for position in former_positions {
  [#render_position(position)]
  linebreak()
}

== Projects

#for project in details.projects {
  [- #project.name]
}

== Conferences
#details.conferences.map(conference => conference.name).join(", ", last: " and ")

== Skills

#for skill in details.skills [
  - #skill
]
