---
applyTo: "content/people/**,content/orgs/**"
---

# People and organisations

These pages exist so that you can walk into a conversation already knowing the context. They
are working notes, not a dossier.

## Boundaries — read this first

Record **professional context**: what someone does, what they own, what they have said and
decided, how they prefer to work, what they have asked for. This is the same information you
would keep in a CRM or a handover note.

Do **not** record: personal or medical information, opinions about someone's character, gossip,
anything told to you in confidence, or anything you would be uncomfortable with that person
reading. Assume every page will one day be read by its subject — because one day it might be.

If the owner dictates something that crosses this line, write the professional part and say
plainly that you left the rest out.

## Person pages

File naming: `firstname-lastname.md`.

```markdown
# {Name}

One sentence: role, organisation, and why they appear in this wiki.

## Context
Where they sit, what they are responsible for, who they answer to — as far as you know it,
with dates.

## Working with them
Preferences that actually matter: how they like to be approached, what they respond to,
what they consider settled. Only things observed or stated, never inferred character.

## Involved in
- [Project](../projects/x.md) — their role in it
- [Decision](../decisions/y.md) — what they decided or pushed for

## History
Dated notes of interactions worth remembering, newest first.
- **2026-08-01** — what happened, what came out of it

## Open questions

## Related
```

## Organisation pages

File naming: `org-name.md`.

```markdown
# {Organisation}

One sentence: what they do and your relationship to them (employer, client, vendor, partner).

## Relationship
What the arrangement is, since when, and who holds it on each side.

## People
- [Name](../people/name.md) — their role there

## What they do
Enough to be useful. Link out for detail.

## History
Dated notes, newest first.

## Open questions

## Related
```

## Rules

- **Every claim about a person needs a date and ideally a source.** People change roles; a
  page that says "leads the platform team" with no date will mislead you within a year.
- **Distinguish observed from reported.** "Said in the 2026-07 review" is a fact.
  "Reportedly unhappy with the vendor" is hearsay — mark it as such or leave it out.
- Link people to orgs and orgs to people in both directions.
- When someone changes role, do not overwrite — add a dated History entry and update the
  opening sentence.
