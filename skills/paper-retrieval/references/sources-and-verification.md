# Sources and verification

Choose sources for the missing evidence; these are starting points, not a
mandatory queue or guarantees of availability.

| Source | Contribution | Verification limit |
| --- | --- | --- |
| Author CV/site, publisher/journal | Identity, authoritative bibliography and publication relation | Reconcile dates, affiliations and versions against printed text. |
| [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/), [OpenAlex](https://docs.openalex.org/) | DOI/title/author metadata and relationships | A record or closed-access flag does not exhaust full-text discovery. |
| Scholar, [PhilArchive](https://philarchive.org/), [PhilSci-Archive](https://philsci-archive.pitt.edu/), university repositories | Versions and disciplinary manuscripts | Follow original record; verify file, author, deposit version and completeness. |
| [CORE](https://core.ac.uk/), [BASE](https://www.base-search.net/), [Unpaywall](https://unpaywall.org/products/api) | Repository/open-location leads | APIs may require registration, email or keys; follow current official docs. Empty results are bounded lookup results. |
| [CNKI](https://www.cnki.net/), [NSSD](https://www.ncpssd.cn/), Chinese journal/university sites | Chinese bibliography and available text | Login, entitlement and downloadable format require separate evidence. |
| [DOAB](https://www.doabooks.org/), [OAPEN](https://www.oapen.org/), library catalogues | Open books, editions, holdings | Catalogue, preview, borrowable record and downloadable whole book differ. |

For books compare title/copyright pages, contents, chapter range, final pages
and references with the publisher's edition. An ISBN identifies a particular
edition/format, not every translation. A chapter DOI and whole-book DOI name
different objects. Check ISBN checksums when reconciling identifiers; retain
source attribution instead of inventing missing identifiers.

For local PDF checks install [Poppler](https://poppler.freedesktop.org/) and use
`pdfinfo`, `pdftotext`, and optional `pdftoppm -f 1 -singlefile -png candidate.pdf first`.
The inspector's JSON is evidence for byte integrity and parsing, not an automated
bibliographic verdict. Image-only text extraction requires visual inspection or
explicitly labelled OCR. Page count must be compared with expected pagination;
missing internal pages can coexist with plausible endpoints. Keep SHA-256 of
acquired bytes separate from a catalogue-advertised MD5. Never identify a missing
complete work by the hash of an incomplete scan or HTML response.

This public adaptation preserves the private-origin method's distinctions
between relevance, identity, versions, access and acquisition gaps. It replaces
host-specific authenticated capture scripts and incident logs with standard
HTTP/browser download and local PDF inspection. No private library-client
configuration or third-party implementation is bundled. External tools and
retrieved publications retain their own licenses and access conditions.
