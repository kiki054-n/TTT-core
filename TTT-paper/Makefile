LATEXMK = latexmk
TEX = main.tex

all:
    $(LATEXMK) -pdf $(TEX)

clean:
    $(LATEXMK) -C

arxiv:
    rm -f TTT-paper.tar.gz
    tar -czf TTT-paper.tar.gz \
        main.tex \
        alpha_convergence.png \
        poly_transition.png \
        latexmkrc \
        Makefile
