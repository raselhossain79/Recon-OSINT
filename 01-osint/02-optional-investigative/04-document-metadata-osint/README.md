# Document Metadata OSINT

Extracting metadata from publicly available documents linked from the target's site or found via search.

## Techniques

```
exiftool document.pdf
exiftool document.docx
```
Common useful fields:
- **Author** — often a real employee name/username, feeds into `01-priority-technical/04-email-username-osint/`
- **Software used** — reveals internal tooling (e.g., a specific PDF generator or internal reporting tool name)
- **Company/organization field** — sometimes reveals an internal team or department name not visible elsewhere

## Where to find target documents
- Google dork: `site:target.com filetype:pdf`, `filetype:docx`, `filetype:xlsx`
- Company press kits, annual reports, and public RFP/tender documents are frequently metadata-rich and get far less scrutiny than the main website

## FOCA-style batch approach
Rather than checking documents one at a time, bulk-download every discoverable PDF/DOCX/XLSX from the dork results and run exiftool across the batch — a single interesting author name or software version is easy to miss checking files one by one, but stands out in aggregate.
