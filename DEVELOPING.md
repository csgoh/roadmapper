# Dev Guide

## Linting

Opening or changing a PR to the `main` branch automatically triggers checks of the linter Ruff. The configuration of the
linter can be found in the [`pyproject.toml](./pyproject.toml).

The linter is installed on your machine when you satisfy the specified dependencies with
`pip install -r requirements.txt`. You can run the linter locally with executing `ruff check .` in the root directory of
the repo. Some rule violations can be fixed by running `ruff check . --fix`.

## Automated Tests

Before merging any PR into our `main` branch, we run automated tests on your modified source code. Besides some platform
independent unit tests, several of these tests are platform dependent and require to be executed remotely on the GitHub
build agents. These tests generate roadmaps on different OSs with your modified code and compare them to how these 
roadmaps should look like.

All the required tests are triggered automatically once you open or change a PR. To verify that the `main` branch hosts
a correct version of the code, any merge to the `main` branch also triggers the tests.

### Change Example Roadmaps

Usually, the appearance of the newly generated roadmaps should not change between different releases of `Roadmapper`.
However, some code changes purposefully change the appearance of the generated roadmaps. To let our tests succeed with
the new version, we will then have to generate new example roadmaps on the GitHub build agents which accommodate these
changes.

To generate these example roadmaps on different GitHub build agents, we have the manual workflow
[generate_examples](.github/workflows/generate_examples.yaml). We can trigger it manually through the
[Actions tab](https://github.com/csgoh/roadmapper/actions/workflows/generate_examples.yaml). In the dropdown to trigger
a run of the workflow, we can also select on which branch the workflow should run, i.e. we can influence which code 
should be used to generate the example roadmaps.

As we usually want to generate new example roadmaps for code which is not present on the `main` branch, we have to run
the workflow on the branch where the respective code changes are present. When ran, the workflow produces artifacts for
the different platforms which contain the example roadmaps. These artifacts can be found in the summary of the 
respective workflow run. To use these new example roadmaps, we should download them and commit them manually to the 
directory [`src/tests/example_roadmaps`](src/tests/example_roadmaps).