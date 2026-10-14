---
name: paper-retrieval
description: "论文检索：筛选中英文论文与学术书籍，核对题录、版本和全文。 Find scholarly papers, books and chapters; reconcile author identity and citations; acquire available authorized texts and verify their identity, version and completeness."
---

# Paper Retrieval

A useful collection connects a question to work worth reading and to the actual
text behind its citation. Relevance, bibliographic coverage, access, and file
identity are different claims. Keep each visible so the reader can trust the
result without repeating the search. This portable package requires a search
or HTTP/browser capability supplied by the recipient host; it does not install
an authenticated browser or grant library access. Use the companion
[research](../research/SKILL.md) for evidence selection, current external
investigation and conflicting-source assessment; this Skill owns scholarly
identity, acquisition and text verification. See [setup and dependencies](README.md) and the
[sources and verification guide](references/sources-and-verification.md).

For controlled or authenticated pages, retain a separate browser/session owner
using [browser-relay](../browser-relay/SKILL.md) for exact target custody,
authorized session reuse, destination/readback verification, desktop placement
and cleanup. A browser API is the execution capability; a companion Skill
supplies its method and ownership contract. Neither provides entitlement.
The dependency table distinguishes companion methods from host capabilities.
For evidenced network faults, use [network](../network/SKILL.md) with the
recipient’s configured diagnosis capabilities; a retrieval failure does not itself
authorize proxy, DNS or routing changes.

## Establish the collection

Resolve question, authors, languages, date range, selected versus exhaustive
scope, requested editions/versions, and destination from the task. Inspect an
existing manifest before downloading. Select substantive relevant contributions
by abstract and, where available, argument, conclusion and references. Explain
their contribution; prestige and citation counts alone do not establish quality.
Mark abstract-only relevance judgments as provisional.

For an author bibliography, verify identity through official CV/faculty pages,
coauthors, field, title and affiliation history. Names and transliterations alone
are insufficient. Keep current institutional grouping distinct from affiliation
printed on an older work. Separate verified bibliographic coverage from obtained
texts. For books resolve author/editor, language/translation, publisher, edition
and ISBN; for chapters identify the containing book as well.

## Discover and reconcile

Search exact titles and meaningful variants, official author pages, publishers,
DOI records and disciplinary/university repositories. Scholar's versions view,
Crossref/OpenAlex, repository indexes and open-location services supply different
evidence. Follow records to their original source. A closed-access flag or failed
profile search does not establish that no author copy exists.

For Chinese works, combine author bibliographies, journal/university sites and
Chinese indexes such as CNKI or NSSD when available. Inspect actual result rows,
including asynchronous results; a heading/count is not a verified bibliography.
Cross-check conflicting metadata against publisher records and the text. Preserve
the source citation and explain supported corrections. Article, chapter, book and
review-container identifiers are not interchangeable. Record search sources and
remaining coverage rather than claiming exhaustive absence from a single index.

## Acquire available text

Use a labelled direct public file or the repository/publisher's official download
control. For a public HTTPS PDF, a concrete CLI route is:

```sh
curl --fail --location --proto '=https' --proto-redir '=https' --output candidate.pdf 'DIRECT_PDF_URL'
python3 scripts/inspect_pdf.py candidate.pdf
```

Replace the placeholder with an inspected public file URL. `curl` does not handle
interactive login, CAPTCHA, institutional access or JavaScript download controls.
For those, use the host's available browser/download API within the task's actual
authorization, or download through the recipient's normal authorized interface
and inspect the local file. Associate the returned file with the initiating work
and download action. Reconcile an uncertain prior download before retrying.
Reuse a session only under its owner's actual authorization. Separate owned
pages may share a session; extra browser instances do not establish throughput
or entitlement. Page-local response capture can be associated with its initiating
page. If a browser-wide download channel is shared, serialize capture or use a
supported unique initiating-action identifier and verify its matching completion;
otherwise concurrent downloads cannot be safely attributed. Preserve the
official navigation/control path when source validation depends on it. Distinguish
transport, visible challenge, session, entitlement, format and capture failure.
Do not export cookies, derive entitlement from a logged-in page, evade site
restrictions, or use private adapters. Preserve existing personal authentication,
consent, payment and outbound-contact boundaries; reuse authorization already
given. A technical failure alone is not proof of denied entitlement.

## Verify before adoption

Run the bundled inspector for PDF signature, parseability, page count, SHA-256,
and first/last-page text. These checks deliberately report identity/completeness
as unverified. Inspect title, authors, year, publication/version information,
body coverage, ending and references against the intended record. Render pages
with `pdftoppm` or a PDF viewer when text is absent or unclear. Inspect intervening
pages/contents when the scope requires it; endpoints alone cannot detect missing
middle pages. HTTP success, filenames and `%PDF-` do not prove the correct work.
Reject HTML/errors, wrong works, previews and damaged files. Compare hashes across
the collection to detect repeated bytes returned under different citations.

Identify format by bytes even when extension is `.caj`. Preserve a genuine CAJ/KDH
original if obtained; conversion needs a separately available legitimate tool.
Verify any derivative independently. Do not reconstruct a purported original
from webpage text. Label manuscripts, preprints, translations, OCR, excerpts,
appended abstract sheets and composition differences accurately; none silently
becomes the version of record or a complete book.

Keep original files and an existing manifest schema. A new small manifest needs
title, authors, year/edition, verified identifiers and stable source links, local
file, version, retrieval date, hash, identity/completeness evidence, and relevant
limits. Store neither signed download URLs nor session secrets. Deduplicate by
identifier, edition/version and bytes; retain materially different versions.
Respect the destination's link/rename conventions when reorganizing.

## Resolve and report gaps

For every selected work without the requested verified text, record the actual
condition: unresolved identity, unconfirmed version, unsearched source coverage,
technical failure, personal authentication step, confirmed entitlement limit,
or no open copy exposed by the inspected sources. These conditions can coexist;
`not_found` alone is insufficient. Continue recoverable work and independent
accessible items. Seek another fitting source, meaningful title variants or
format route when evidence supports it. Stop an item only at an evidenced
external boundary or the user's stopping scope, with a concrete resume condition.

Keep observed dates, attempted route/result, remaining coverage, next action,
and whether personal participation is useful in the owning manifest. Notify the
user when the actual next action requires their participation, rather than
asking them to repair technical failures. At the handoff, identify every still
required incomplete work directly in the conversation: title, author, year or
edition, missing scope, supported stable link and copyable verified DOI/ISBN or
other source-labelled identifier. Distinguish partial/unverified files, obtained
alternate versions, and optional upgrades. A count or manifest link cannot
replace that per-item explanation. Acquired text and remaining gaps are separate
results; inaccessible scholarship is not absent scholarship.
