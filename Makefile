report: .venv/bin/python
	.venv/bin/pytest test.py
.PHONY: report

.venv/bin/python: Makefile
	python3 -m venv .venv
	.venv/bin/pip install pytest matplotlib
