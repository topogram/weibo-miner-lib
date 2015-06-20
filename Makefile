#
# Topogram Makefile
# ~~~~~~~~~~~~~~~~~
#
# Shortcuts for various tasks.
#
# :copyright: (c) 2008 by the Werkzeug Team, see AUTHORS for more details.
# :license: BSD, see LICENSE for more details.
#

documentation:
	@(cd docs; make html)

release:
	python scripts/make-release.py

test:
	py.test tests --tb=native

coverage:
	@(coverage run --source=topogram --module py.test tests)
	coverage html

doc-coverage:
	sphinx-build -b coverage docs docs/_build/coverage/.

doctest:
	@(cd docs; sphinx-build -b doctest . _build/doctest)
	
upload-docs:
	# $(MAKE) -C docs html dirhtml latex
	# $(MAKE) -C docs/_build/latex all-pdf

	cd docs; git init . ; git add . ; git commit -m "Deploy" ; git push "git@github.com:topogram/topogram-docs.git" master --force; rm -rf .git
