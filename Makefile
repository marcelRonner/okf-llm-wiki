PY := python3
S  := scripts

# Hugo needs Dart Sass on PATH to compile Docsy's stylesheets. It is a project-local npm
# dependency rather than a global install, so `npm install` is all the setup there is.
HUGO := PATH="$(CURDIR)/node_modules/.bin:$$PATH" hugo

.PHONY: help schema index lint test serve build stage inbox new new-type move verify clean

## Show the available commands
help:
	@echo "make index    regenerate content/_index.md, content/tags.md and the backlink blocks"
	@echo "make schema   restamp the generated type tables in .github/ and README.md"
	@echo "make lint     regenerate, then check the wiki (errors fail, warnings are reported)"
	@echo "make test     run the OKF reader acceptance checks and the script tests"
	@echo "make lint STRICT=1   the same, but warnings fail too"
	@echo "make serve    live-reload site at http://localhost:1313/okf-llm-wiki/"
	@echo "make build    check nothing is stale or broken, then build site/"
	@echo "make stage    build, then assemble deploy/ exactly as the server receives it"
	@echo "make inbox    list unprocessed material waiting to be ingested"
	@echo ""
	@echo "make new TYPE=project TITLE=\"Acme Migration\" [DESCRIPTION=\"...\"] [FROM=content/x.md]"
	@echo "make move PAGE=content/topics/x.md TYPE=project     re-type a page, fixing every link"
	@echo "make new-type TYPE=meeting                       scaffold a type declared in schema.yml"
	@echo "make verify PAGE=content/topics/x.md [WHO=owner]  record that you read a page and it is true"
	@echo ""
	@echo "In Copilot or Claude Code: /note, /ingest, /query, /lint"

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

## Exercise the reader behaviour that OKF requires consumers to support, and the scripts' own checks.
test:
	@$(PY) -m unittest discover -s $(S) -p "test_*.py"

## Live-reload the site while writing
serve: index
	$(HUGO) server --buildDrafts

## Full check plus a build, same order a CI job would use.
## Nothing is regenerated here — a stale generated file is a failure, not a fixup, because the
## published site would otherwise disagree with the wiki it was built from.
##
## Warnings do not fail this. A site that will not build because a page is 401 words is a check
## people learn to bypass, and a bypassed check is worse than none. Use STRICT=1 if you disagree.
## STRICT=1 additionally makes Hugo fail on its own warnings — an unresolved Markdown link
## reported by layouts/_markup/render-link.html is the one worth catching.
build:
	@$(PY) $(S)/build_schema.py --check
	@$(PY) $(S)/build_index.py --check
	@$(PY) $(S)/lint_wiki.py $(if $(STRICT),--strict,)
	@$(PY) -m unittest discover -s $(S) -p "test_*.py"
	$(HUGO) --minify $(if $(STRICT),--panicOnWarning,)

## What CI runs before the deploy: the build, then deploy/ holding exactly what the server serves at
## https://www.wlrm.ch/okf-llm-wiki/. There is no landing page, so the site is the folder's root.
stage: build
	@rm -rf deploy && mkdir -p deploy
	@cp -R site/. deploy/
	@echo "stage: deploy/ holds the built site"

## What is waiting to be ingested
inbox:
	@$(PY) -c "from pathlib import Path; \
	items = sorted(p for p in Path('inbox').iterdir() if p.is_file() and p.name != '.gitkeep'); \
	print('\n'.join(f'  {p}' for p in items) if items else '  inbox is empty')"

## Create a page: make new TYPE=project TITLE="Acme Migration" [DESCRIPTION="..."] [FROM=content/topics/x.md]
new:
	@test -n "$(TYPE)"  || (echo "usage: make new TYPE=project TITLE=\"...\""; exit 1)
	@test -n "$(TITLE)" || (echo "usage: make new TYPE=project TITLE=\"...\""; exit 1)
	@$(PY) $(S)/new_page.py "$(TYPE)" "$(TITLE)" \
		$(if $(DESCRIPTION),--description "$(DESCRIPTION)",) $(if $(FROM),--link-from "$(FROM)",)

## Re-type or rename a page: make move PAGE=content/topics/x.md TYPE=project [SLUG=new-slug]
move:
	@test -n "$(PAGE)" || (echo "usage: make move PAGE=content/topics/x.md TYPE=project"; exit 1)
	@$(PY) $(S)/move_page.py "$(PAGE)" $(if $(TYPE),--type "$(TYPE)",) $(if $(SLUG),--slug "$(SLUG)",)

## Scaffold a type you have already declared in schema.yml
new-type:
	@test -n "$(TYPE)" || (echo "usage: make new-type TYPE=meeting  (declare it in schema.yml first)"; exit 1)
	@$(PY) $(S)/new_type.py "$(TYPE)"

## Record the owner's confirmation: make verify PAGE=content/topics/x.md [WHO=owner]
## Owner only — the assistant never runs this. See scripts/verify_page.py and AGENTS.md.
verify:
	@test -n "$(PAGE)" || (echo "usage: make verify PAGE=content/topics/x.md [WHO=owner]"; exit 1)
	@$(PY) $(S)/verify_page.py "$(PAGE)" $(if $(WHO),--who "$(WHO)",)

## Remove the built site and the deploy staging directory
clean:
	rm -rf site deploy
