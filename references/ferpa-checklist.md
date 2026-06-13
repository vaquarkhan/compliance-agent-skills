# FERPA Checklist (34 CFR Part 99)

EdTech and AI agent deployments. Not legal advice.

## Scope

- [ ] Education records inventory (SIS, LMS, agent logs, MCP DB)
- [ ] PII elements identified per student
- [ ] Maintainer identified (LEA vs vendor)
- [ ] Directory information categories defined

## School official / vendor

- [ ] Vendor performs institutional service under LEA control
- [ ] DPA meets §99.31(a)(1) school official requirements
- [ ] LLM subprocessors listed and approved
- [ ] Prohibition on vendor model training on identifiable records (unless consented)

## Legitimate educational interest

- [ ] LEI documented per agent feature
- [ ] Minimum necessary access enforced (RBAC)
- [ ] No unrelated LLM experimentation on live student records

## Rights and notices

- [ ] Annual FERPA rights notice to parents/eligible students
- [ ] Directory information opt-out process
- [ ] Parent/eligible student access procedure (§99.10)
- [ ] Amendment and hearing process (§99.20)

## Technical controls

- [ ] Student/teacher/admin RBAC
- [ ] Pseudonymous session IDs in LLM prompts where possible
- [ ] Redaction before external LLM calls
- [ ] §99.32 disclosure audit log (who, what, recipient, purpose)
- [ ] Deanonymization disabled in student production paths

## Incidents

- [ ] Improper disclosure playbook (state law + contract)
- [ ] Linked to breach-incident-response

---

## Authoritative sources

- FERPA: [34 CFR Part 99](https://www.ecfr.gov/current/title-34/subtitle-B/chapter-XI/part-99)
- US ED FERPA guidance: [Student Privacy Policy Office](https://studentprivacy.ed.gov/)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | 34 CFR Part 99 (FERPA) |
| **Version / effective** | Current eCFR as of 2026-06-13 |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer |
| **Next review due** | 2027-06-13 |
| **Notes** | EdTech/agent subset; not ED official guidance |
