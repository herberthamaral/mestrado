default:
	pdflatex artigo
	bibtex artigo
	pdflatex artigo
	bibtex artigo
	wait
	pdflatex artigo
	evince artigo.pdf
clean:
	python -c "import os; whitelist = ['.pdf', '.tex', '.sty', '.bib']; [os.unlink(f) for f in os.listdir('.') if not any([f.endswith(w) for w in whitelist]) and f.startswith('artigo')]"
