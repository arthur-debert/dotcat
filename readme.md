# dotcat

Cat structured data in a shell, i.e. cat some.json user.name.first # echos Janet

## Features


## Installation

You can install dotcat using pip:

```bash
pip install dotcat
```

## Usage

### Generating a Project

To generate a new project using `pykick`, run:

```bash
pykick.kick
```

This will create a new project based on the template.

### Setup

After generating the project, navigate to the project directory and run the setup script to install dependencies:

```bash
./scripts/setup
```

### Configuring PyPI Tokens

Before publishing your package, you need to configure your PyPI tokens. Run the following script with your production and optional test PyPI tokens:

```bash
./scripts/publish_setup <prod_token> [test_token]
```

### Publishing

To publish your package, you can use the `publish` script. Here are some common use cases:

#### Publishing to Production with Version Bump

```bash
./scripts/publish --version bump --production
```

This will:
1. Check if the git repository is clean (no uncommitted changes).
2. Call `poetry version patch` to increment the patch version.
3. Add the updated `pyproject.toml` to the git index and commit it.
4. Push the commit to the remote repository.
5. Publish the package to the production PyPI repository.

#### Publishing to Test PyPI

If you want to publish to the test PyPI repository, you can omit the `--production` flag:

```bash
./scripts/publish --version bump
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

Tests are done with [pytest](https://github.com/pytest-dev/pytest), makers of happy lives.

### License

[MIT License][def]

[def]: ./LICENSE