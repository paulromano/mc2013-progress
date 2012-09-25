# Name of manuscript
manuscript = mc2013-progress

# List of images to be included
images = opr-without-ufs.pdf opr-with-ufs.pdf opr-histogram.pdf

# PdfLaTeX compilation options
latexopt   = -halt-on-error -file-line-error

#=================================================================
# Generate PDF of manuscript using PdfLaTeX
#=================================================================

all: $(manuscript).pdf

$(manuscript).pdf: $(manuscript).tex $(images) references.bib
	pdflatex $(latexopt) $<
	bibtex -terse $(basename $<).aux
	pdflatex $(latexopt) $<
	pdflatex $(latexopt) $<

#=================================================================
# Generate Images
#=================================================================

opr-with%.pdf: make_meshplots.py
	python $<

opr-histogram.pdf: make_histogram.py
	python $<

#=================================================================
# Other
#=================================================================

clean:
	@rm -f *.aux *.bbl *.blg *.log *.out *.spl $(manuscript).pdf

.PHONY: all clean
