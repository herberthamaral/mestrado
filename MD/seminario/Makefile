default:
	pdflatex apresentacao
	bibtex apresentacao
	pdflatex apresentacao
	bibtex apresentacao
	wait
	pdflatex apresentacao
	evince apresentacao.pdf
clean:
	python -c "import os; whitelist = ['.pdf', '.tex', '.sty', '.bib']; [os.unlink(f) for f in os.listdir('.') if not any([f.endswith(w) for w in whitelist]) and f.startswith('apresentacao')]"
