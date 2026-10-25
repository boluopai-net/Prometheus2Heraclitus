#let language = "LANGUAGE"
#let book-title = "BOOKTITLE"
#let subtitle = "BOOKSUBTITLE"
#let edition = "EDITION"
#let stamp = "BUILDSTAMP"
#let ink = rgb("273238")
#let teal = rgb("25646a")
#let muted = rgb("667278")
#set document(title: book-title + " · " + subtitle, author: "boluopai", description: edition)
#set page(width: 176mm, height: 250mm, margin: (top: 19mm, bottom: 20mm, left: 19mm, right: 19mm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 8pt, fill: muted, font: ("Helvetica Neue", "PingFang SC"))
      [#book-title #h(1fr) #edition]
      line(length: 100%, stroke: 0.4pt + rgb("d7dddd"))
    }
  },
  footer: context {
    if counter(page).get().first() > 1 {
      align(center, text(size: 9pt, fill: muted, counter(page).display("1")))
    }
  })
#set text(font: ("Libertinus Serif", "Songti SC", "Arial Unicode MS"), size: 11pt,
  lang: language, fill: ink, hyphenate: language == "en")
#set par(justify: true, leading: 0.72em, spacing: 0.85em)
#set heading(numbering: none)
#set outline(indent: 1.1em)
#show link: it => text(fill: teal, it)
#set math.equation(numbering: none)
#show math.equation: set text(font: "STIX Two Math")
#set table(inset: 5pt, stroke: 0.4pt + rgb("d7dddd"))
#show table: set text(size: 9pt)
#show figure.where(kind: table): set block(breakable: true)
#show table.cell.where(y: 0): set text(weight: "bold", fill: teal)
#set list(indent: 1em, body-indent: 0.6em, spacing: 0.5em)
#set enum(indent: 1.1em, body-indent: 0.6em, spacing: 0.5em)
#set terms(hanging-indent: 1.5em)
#let horizontalRule = line(length: 100%, stroke: 0.5pt + rgb("d7dddd"))
#let divider() = horizontalRule
#show raw: set text(size: 8.5pt, font: ("Menlo", "PingFang SC"))
#show raw.where(block: true): it => block(width: 100%, fill: rgb("f3f5f5"), inset: 9pt, radius: 3pt, breakable: true, it)
#show heading.where(level: 1): it => {
  block(sticky: true, above: 8mm, below: 4mm, text(font: ("Helvetica Neue", "PingFang SC"), size: 22pt, weight: "bold", fill: teal, it.body))
}
#show heading.where(level: 2): it => {
  block(sticky: true, above: 7mm, below: 4mm,
    text(font: ("Helvetica Neue", "PingFang SC"), size: 20pt, weight: "bold", fill: teal, it.body))
}
#show heading.where(level: 3): it => block(above: 1.5em, below: 0.7em,
  text(font: ("Helvetica Neue", "PingFang SC"), size: 15pt, weight: "bold", fill: teal, it.body))
#show heading.where(level: 4): it => block(above: 1.1em, below: 0.5em, text(size: 12pt, weight: "bold", it.body))
#let part(title) = {
  pagebreak(weak: true)
  heading(level: 1, text(fill: black, title))
  v(12mm)
}
#let chapter-art(path, caption) = {
  block(width: 100%, above: 2mm, below: 7mm)[
    #align(center, image(path, width: 80%, height: 65mm, fit: "contain"))
    #v(2mm)
    #text(size: 8.5pt, fill: muted, caption)
  ]
}
#let book-figure(path, title) = block(above: 4mm, below: 4mm, breakable: true, {
  block(sticky: true, below: 2mm, text(size: 10pt, weight: "bold", fill: teal, title))
  block(above: 1.5mm, below: 1.5mm, align(center, image(path, width: 100%)))
})

#v(25mm)
#v(11mm)
#text(size: 48pt, weight: "bold", font: ("Helvetica Neue", "PingFang SC"), fill: teal, book-title)
#v(6mm)
#text(size: 23pt, subtitle)
#v(14mm)
#text(size: 12pt, fill: muted, edition)
#v(1fr)
#text(size: 13pt, "boluopai")
#v(4mm)
#text(size: 9pt, fill: muted, stamp)
#v(4mm)
#text(size: 9pt, link("https://boluopai.net/philosophy/", "boluopai.net"))
#pagebreak()
#outline(title: if language == "zh" { [目录] } else { [Contents] }, depth: 2)
#pagebreak()
