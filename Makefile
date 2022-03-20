.PHONY: all forms zip clean format check
all: zip

forms: src/form.py

PACKAGE_NAME := bkrs_downloader

zip: forms $(PACKAGE_NAME).ankiaddon

src/form.py: designer/form.ui
	pyuic5 $^ > $@

$(PACKAGE_NAME).ankiaddon: src/*
	rm -f $@
	( cd src/; zip -r ../$@ * )


# Install in test profile
install: zip
	rm -r ankiprofile/addons21/$(PACKAGE_NAME)
	cp -r src/. ankiprofile/addons21/$(PACKAGE_NAME)

format:
	python -m black src/

check:
	python -m mypy src/

clean:
	rm -f src/form.py
	rm -f $(PACKAGE_NAME).ankiaddon
