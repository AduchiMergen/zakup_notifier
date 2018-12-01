ROOT_DIR = $(CURDIR)
SOURCE_DIR = $(CURDIR)/src

MANAGER = python $(SOURCE_DIR)/manage.py
VENV = . $(ROOT_DIR)/.env/bin/activate;
SUPERVISOR = sudo supervisorctl

# Clean project
.PHONY : clean
clean:
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete

.PHONY : static
static:
	$(VENV) $(MANAGER) collectstatic --noinput

.PHONY : pip
pip:
	$(VENV) pip install -r $(ROOT_DIR)/requirements.txt

.PHONY : migrate
migrate:
	$(VENV) $(MANAGER) migrate --noinput

.PHONY : makemigrations
makemigrations:
	$(VENV) $(MANAGER) makemigrations --noinput

.PHONY : runserver
runserver:
	$(VENV) $(MANAGER) runserver 127.0.0.1:8000

.PHONY : reload
reload: clean
	cd $(ROOT_DIR); touch reload

# Update instance
.PHONY : update
update: pip migrate static reload

.PHONY : mm
mm: makemigrations migrate

.PHONY : shell
shell:
	$(VENV) $(MANAGER) shell_plus

.PHONY : test
test:
	cd $(SOURCE_DIR); $(VENV) $(MANAGER) test
