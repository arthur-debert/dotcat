# Go CLI Project Template

This repository is a template for creating Go command-line interface (CLI) projects. It includes a basic structure, build scripts, and a pre-configured release process with GoReleaser.

## Getting Started

1. **Clone this repository:**

    ```bash
    git clone https://github.com/your-username/your-project
    cd your-project
    ```

2. **Set your package name:**
    - Open the `.envr` file.
    - Change `export PKG_NAME="myapp"` to your desired application name (e.g., `export PKG_NAME="my-cli-tool"`).
    - If you're using `direnv`, run `direnv allow` to load the environment variable.

3. **Update `go.mod`:**
    - Open `go.mod` and change `module github.com/your-username/your-project` to your project's module path.

4. **Install dependencies:**

    ```bash
    go mod tidy
    ```

5. **Build your application:**

    ```bash
    make build
    ```

    This will create a binary in the `bin/` directory with the name you set in `.envr`.

## Features

- **Cobra CLI Framework:** Comes with a basic Cobra setup in `cmd/app/main.go`.
- **GoReleaser Integration:** The `.goreleaser.yml` file is configured to build and release your application for multiple platforms.
- **Makefile:** Includes common tasks like `build`, `test`, and `clean`.
- **GitHub Actions:** Includes workflows for testing and releasing your application.

## Development

- Your main application code goes in `cmd/app/main.go`.
- You can add shared packages in the `internal/` directory.

## License

[MIT](LICENSE)
