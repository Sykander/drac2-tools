# Development
## Environments
There are multiple different environments, which all serve different purposes.
* Local - local development runs on your machine
* Development - deployed environment defined at `utils/sourcemap.dev.json`
* Production - deployed environment defined at `utils/sourcemap.prod.json`
## Local Setup
To run the project locally you'll need the following installed:
* [Node](https://nodejs.org/en)
* [uv](https://docs.astral.sh/uv/)
* [Make](https://www.gnu.org/software/make/)

You may also need the following environment variables:
* AVRAE_TOKEN - [guide](https://www.npmjs.com/package/publish-avrae#avrae-token)

You should now be able to run `make test` and run the tests locally.
## Deployment
We use [publish-avrae](https://www.npmjs.com/package/publish-avrae) to automatically deploy the project via the Deploy Github Actions `.github/workflows/deploy.yaml`.
### Sourcemaps
Publish-avrae relies on using sourcemaps which configures which files to deploy to which aliases, gvars and snippets in which workshops. We use these sourcemaps as a source of truth for other files, and so whenever you update a sourcemap you should also run `make rebuild`.

Development Environment Sourcemap `utils/sourcemap.dev.json`
Production Environment Sourcemap `utils/sourcemap.prod.json`
### Triggering a deployment
1. Head over to the Deploy action tab on github. [Link](https://github.com/Sykander/drac2-tools/actions/workflows/deploy.yaml)
2. Click the `Run Workflow` button and configure the branch and environment to deploy to
  * Deployments to `Production` should only happen when the package.json version is incremented and should only go from a tagged commit on the main branch
  * `Development` environment is available for dev testing
3. Observe the new action and wait for it to complete with a green check mark - if tests are failing then it will not deploy