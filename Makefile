install:
	npm ci

rebuild: install rebuild_dev rebuild_prod

rebuild_dev: install
	ENVIRONMENT=Development npm run generate-env
	npm run generate-vars

rebuild_prod: install
	ENVIRONMENT=Production npm run generate-env
