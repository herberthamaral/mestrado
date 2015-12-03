default:
	pdflatex resumo
	bibtex resumo
	pdflatex resumo
	bibtex resumo
	wait
	pdflatex resumo
	evince resumo.pdf
clean:
	python -c "import os; whitelist = ['.pdf', '.tex', '.sty', '.bib']; [os.unlink(f) for f in os.listdir('.') if not any([f.endswith(w) for w in whitelist]) and f.startswith('resumo')]"
