.PHONY: all forms zip clean pylint mypy fix install
all: zip

forms: src/forms/form_qt5.py src/forms/form_qt6.py

PACKAGE_NAME := bkrs_downloader

zip: forms $(PACKAGE_NAME).ankiaddon

src/forms/form_qt5.py: designer/form.ui
	pyuic5 $^ > $@

src/forms/form_qt6.py: designer/form.ui
	pyuic6 $^ > $@

$(PACKAGE_NAME).ankiaddon: src/*
	rm -f $@
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )


# Install in test profile
install: forms
	rm -rf src/__pycache__
	rm -r ankiprofile/addons21/$(PACKAGE_NAME)
	cp -r src/. ankiprofile/addons21/$(PACKAGE_NAME)

fix:
	python -m black src --exclude=forms
	python -m isort src

mypy:
	python -m mypy src

pylint:
	python -m pylint src

clean:
	rm -f $(PACKAGE_NAME).ankiaddon
