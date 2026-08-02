PY := python3
S  := scripts

.PHONY: help schema index lint serve build inbox new new-type move clean

## Show the available commands
help:
	@echo "make index    regenerate wiki/index.md, wiki/tags.md and the backlink blocks"
	@echo "make schema   restamp the generated type tables in .github/ and README.md"
	@echo "make lint     regenerate, then check the wiki (errors fail, warnings are reported)"
	@echo "make lint STRICT=1   the same, but warnings fail too"
	@echo "make serve    live-reload site at http://127.0.0.1:8000"
	@echo "make build    check nothing is stale or broken, then build site/"
	@echo "make inbox    list unprocessed material waiting to be ingested"
	@echo ""
	@echo "make new TYPE=project TITLE=\"Acme Migration\" [SUMMARY=\"...\"] [FROM=wiki/x.md]"
	@echo "make move PAGE=wiki/topics/x.md TYPE=project     re-type a page, fixing every link"
	@echo "make new-type TYPE=meeting                       scaffold a type declared in schema.yml"
	@echo ""
	@echo "In Copilot chat: /note, /ingest, /query, /lint"

## Restamp the generated blocks that restate schema.yml
schema:
	@$(PY) $(S)/build_schema.py

## Regenerate the catalogue, the tag listing and the backlinks
index:
	@$(PY) $(S)/build_index.py

## Regenerate first, then check. Bookkeeping should never be something you can fail on.
## STRICT=1 makes warnings fail too — for a CI job that wants the higher bar.
lint: schema index
	@$(PY) $(S)/lint_wiki.py $(if $(STRICT),--strict,)

## Live-reload the site while writing
serve: index
	mkdocs serve

## Full check plus a build, same order a CI job would use.
## Nothing is regenerated here — a stale generated file is a failure, not a fixup, because the
## published site would otherwise disagree with the wiki it was built from.
##
## Warnings do not fail this. A site that will not build because a page is 401 words is a check
## people learn to bypass, and a bypassed check is worse than none. Use STRICT=1 if you disagree.
build:
	@$(PY) $(S)/build_schema.py --check
	@$(PY) $(S)/build_index.py --check
	@$(PY) $(S)/lint_wiki.py $(if $(STRICT),--strict,)
	mkdocs build --strict

## What is waiting to be ingested
inbox:
	@$(PY) -c "from pathlib import Path; \
	items = sorted(p for p in Path('inbox').iterdir() if p.is_file() and p.name != '.gitkeep'); \
	print('\n'.join(f'  {p}' for p in items) if items else '  inbox is empty')"

## Create a page: make new TYPE=person TITLE="Jane Doe" [SUMMARY="..."] [FROM=wiki/orgs/acme.md]
new:
	@test -n "$(TYPE)"  || (echo "usage: make new TYPE=project TITLE=\"...\""; exit 1)
	@test -n "$(TITLE)" || (echo "usage: make new TYPE=project TITLE=\"...\""; exit 1)
	@$(PY) $(S)/new_page.py "$(TYPE)" "$(TITLE)" \
		$(if $(SUMMARY),--summary "$(SUMMARY)",) $(if $(FROM),--link-from "$(FROM)",)

## Re-type or rename a page: make move PAGE=wiki/topics/x.md TYPE=project [SLUG=new-slug]
move:
	@test -n "$(PAGE)" || (echo "usage: make move PAGE=wiki/topics/x.md TYPE=project"; exit 1)
	@$(PY) $(S)/move_page.py "$(PAGE)" $(if $(TYPE),--type "$(TYPE)",) $(if $(SLUG),--slug "$(SLUG)",)

## Scaffold a type you have already declared in schema.yml
new-type:
	@test -n "$(TYPE)" || (echo "usage: make new-type TYPE=meeting  (declare it in schema.yml first)"; exit 1)
	@$(PY) $(S)/new_type.py "$(TYPE)"

## Remove the built site
clean:
	rm -rf site
