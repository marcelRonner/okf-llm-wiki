PY := python3
S  := scripts

.PHONY: help index lint serve build inbox new clean

## Show the available commands
help:
	@echo "make index    regenerate wiki/index.md from page frontmatter"
	@echo "make lint     check the wiki (frontmatter, links, orphans, index freshness)"
	@echo "make serve    live-reload site at http://127.0.0.1:8000"
	@echo "make build    lint, then build the static site into site/"
	@echo "make inbox    list unprocessed material waiting to be ingested"
	@echo ""
	@echo "make new TYPE=project TITLE=\"Acme Migration\"     create a page from its template"
	@echo ""
	@echo "In Copilot chat: /ingest, /query, /lint"

## Regenerate the catalogue
index:
	@$(PY) $(S)/build_index.py

## Mechanical checks — run this before calling any change done
lint:
	@$(PY) $(S)/build_index.py --check
	@$(PY) $(S)/lint_wiki.py

## Live-reload the site while writing
serve: index
	mkdocs serve

## Full check plus a strict build, same order a CI job would use
build: index lint
	mkdocs build --strict

## What is waiting to be ingested
inbox:
	@$(PY) -c "from pathlib import Path; \
	items = sorted(p for p in Path('inbox').iterdir() if p.is_file() and p.name != '.gitkeep'); \
	print('\n'.join(f'  {p}' for p in items) if items else '  inbox is empty')"

## Create a page: make new TYPE=person TITLE="Jane Doe" [SUMMARY="..."]
new:
	@test -n "$(TYPE)"  || (echo "usage: make new TYPE=project TITLE=\"...\""; exit 1)
	@test -n "$(TITLE)" || (echo "usage: make new TYPE=project TITLE=\"...\""; exit 1)
	@$(PY) $(S)/new_page.py "$(TYPE)" "$(TITLE)" $(if $(SUMMARY),--summary "$(SUMMARY)",)

## Remove the built site
clean:
	rm -rf site
