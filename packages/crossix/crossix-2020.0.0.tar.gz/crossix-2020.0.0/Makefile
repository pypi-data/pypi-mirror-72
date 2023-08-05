# VARS
# ====

PACKAGE = crossix
PROJECT_DIR = crossix

# JS toolchain
WEBPACK = npx webpack

FRONTEND_DIR = frontend
FRONTEND_DIST_DIR = $(PROJECT_DIR)/static/$(PACKAGE)
DJANGO_ASSETS_DIR = $(PROJECT_DIR)/assets

APP_JS_FILES = $(shell find $(FRONTEND_DIR) -name '*.js')
APP_CSS_FILES = $(shell find $(FRONTEND_DIR) -name '*.css')

DJANGO_ASSETS_SENTINEL = .success-collectstatic

# Django
MANAGE_PY = python manage.py
DJANGO_ADMIN = django-admin.py
PO_FILES = $(shell find $(PACKAGE) -name '*.po')
MO_FILES = $(PO_FILES:.po=.mo)


.DEFAULT_GOAL := build


build: $(MO_FILES) $(DJANGO_ASSETS_SENTINEL)


FRONTEND_TARGETS = $(FRONTEND_DIST_DIR)/js/app.js $(FRONTEND_DIST_DIR)/css/styles.css

$(DJANGO_ASSETS_SENTINEL): $(FRONTEND_TARGETS)
	CROSSIX_APP_MODE=dist $(MANAGE_PY) collectstatic --noinput --verbosity 2
	touch $@

$(FRONTEND_DIST_DIR)/js/app.js: $(FRONTEND_DIR)/app.js $(APP_JS_FILES) webpack.config.js package.json package-lock.json
	# Build a module named 'app' from `app.js`
	$(WEBPACK) --entry $(basename $(notdir $@))=./$< --output-path $(dir $@)

$(FRONTEND_DIST_DIR)/css/styles.css: $(FRONTEND_DIR)/app.css
	mkdir --parents $(dir $@)
	cp $< $@

package-lock.json: package.json
	npm install


# Run DJANGO_ADMIN compilemessages for checkout/<project>/locale/<lang>/LC_MESSAGES/<name>.po
# Must run from checkout/<project>
%.mo: %.po
	cd $(abspath $(dir $<)/../../..) && $(DJANGO_ADMIN) compilemessages

.PHONY: build


clean:
	-rm --recursive $(FRONTEND_DIST_DIR) $(DJANGO_ASSETS_SENTINEL) $(DJANGO_ASSETS_DIR)
	find $(PROJECT_DIR) -type f -name '*.pyc' -delete

distclean: clean
	-rm --recursive --force node_modules/
	-rm package-lock.json

.PHONY: clean distclean


# QUALITY
# =======

test: build
	$(MANAGE_PY) test crossix
	check-manifest

.PHONY: test


# DEPENDENCIES
# ============

update: update-js
	pip install --upgrade pip setuptools
	pip install -r requirements_dev.txt

update-js:
	npm install

release:
	fullrelease


.PHONY: update update-js release


# MISC
# ====

runserver:
	$(MANAGE_PY) runserver

.PHONY: runserver
