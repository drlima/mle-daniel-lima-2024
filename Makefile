help:
	@echo 'Main CLI for project management.'
	@echo 'Usage: make COMMAND'
	@echo 'Available commands:'
	@echo '  QA'
	@echo '    lint | llint | local_lint | lint_local ...... Runs lint script locally'
	@echo '  OTHERS'
	@echo '    clean ....................................... Removes Python cached files'
	@echo '    help ........................................ Shows this message'


clean:
	@find . -name *.pyc -delete
	@find . -name __pycache__ -delete


lint llint local_lint lint_local:
	./bin/lint.sh -l


.PHONY: clean lint llint local_lint lint_local
