NAME = bachelors
MAINFILE = $(NAME).tex

build:	$(MAINFILE)
	@echo Generating PDF
	@pdflatex -interaction=nonstopmode $(NAME);
	@bibtex $(NAME);
	@pdflatex -interaction=nonstopmode $(NAME);
	@pdflatex -interaction=nonstopmode $(NAME);
	@echo Done

clean:
	@echo Removing temporary files
	@rm bachelors.aux bachelors.bbl bachelors.blg bachelors.log bachelors.out bachelors.pdf bachelors.toc bachelors.xmpdata pdfa.xmpi 2>/dev/null || true
