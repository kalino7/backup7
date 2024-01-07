.PHONY: report clean

DIRECTORY=ReproEngReport
PAPERNAME=main

report: $(DIRECTORY)/$(PAPERNAME).pdf

$(DIRECTORY)/$(PAPERNAME).pdf: $(DIRECTORY)/$(PAPERNAME).tex $(DIRECTORY)/acmart.cls $(DIRECTORY)/sample.bib $(DIRECTORY)/ACM-Reference-Format.bst
	cd $(DIRECTORY) && pdflatex $(PAPERNAME).tex; bibtex $(PAPERNAME); pdflatex $(PAPERNAME).tex; pdflatex $(PAPERNAME).tex;

clean:
	rm -rfv $(DIRECTORY)/*.pdf $(DIRECTORY)/*.log $(DIRECTORY)/*.aux $(DIRECTORY)/*.out $(DIRECTORY)/*.bbl $(DIRECTORY)/*.blg
