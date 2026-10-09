<!-- PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy. -->
# Docket AI — Code Showcase

**Privacy notice: This project contains selected code excerpts only. The full application code is intentionally omitted for privacy.**

Docket AI helps users inspect invoices, understand review warnings, ask questions about document evidence, and track follow-up work.

## What is shared

- Each code file contains **30–40 selected source lines**, or **35–45 lines including its privacy header and closing comment**.
- No excerpt contains more than half of its original source file.
- Short source files are omitted rather than sharing their complete implementation.
- Long minified lines are shortened and clearly marked.
- Every shared code file begins with an explicit privacy notice.

These excerpts are intentionally incomplete. They do not form a runnable application and should not be presented as the complete source code.
See [SNIPPETS.md](SNIPPETS.md) for the file index and source ranges.

## Application features

- Invoice extraction and a searchable document inbox.
- Review warnings for conflicting totals, possible duplicates, changed bank details, and unexpected recipients.
- Gemini answers grounded in invoice evidence with links to supporting documents.
- Document-specific questions, invoice details, and supplier follow-up tasks.

## Technology

Python, FastAPI, SQLite, PDF text extraction, Gemini, HTML, CSS, and JavaScript.

## Privacy and demonstration data

Credentials, environment files, databases, invoices, logs, personal files, and the original Git history are excluded.
The five detailed demo invoices are fictional samples. The incoming-invoice sequence is simulated; live Gmail integration is not implemented.
Review flags identify potential issues to investigate. The application does not send payments or independently verify bank settlement.

## Attribution

The extraction layer builds on [invoice_extraction](https://github.com/Manojbonthu/invoice_extraction).
This showcase does not grant rights to the omitted private implementation or change the rights of upstream code.
