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

doctest:
	@(cd docs; sphinx-build -b doctest . _build/doctest)
	
upload-docs:
	$(MAKE) -C docs html dirhtml latex
	$(MAKE) -C docs/_build/latex all-pdf

	
	# npm run build && cd build && git init . && git add . && git commit -m \"Deploy\"; git push \"git@github.com:leClub/leClub.github.io.git\" master --force && rm -rf .git

	# cd docs/_build/; mv html werkzeug-docs; zip -r werkzeug-docs.zip werkzeug-docs; mv werkzeug-docs html
	# rsync -a docs/_build/dirhtml/ flow.srv.pocoo.org:/srv/websites/werkzeug.pocoo.org/docs/
	# rsync -a docs/_build/latex/Werkzeug.pdf flow.srv.pocoo.org:/srv/websites/werkzeug.pocoo.org/docs/
	# rsync -a docs/_build/werkzeug-docs.zip flow.srv.pocoo.org:/srv/websites/werkzeug.pocoo.org/docs/werkzeug-docs.zip
