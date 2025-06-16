# dotcat - Structured Data Reader

`dotcat` is a CLI tool for reading structured data files (JSON, YAML, TOML, INI) using dot notation to access nested values.

## Features

- Supports multiple file formats: JSON, YAML, TOML, and INI
- Uses dot notation to access nested values (e.g., `user.address.city`)
- Supports list access with `@` symbol (e.g., `users@0.name`)
- Multiple output formats: raw, JSON, YAML, TOML, and INI

## Installation

```bash
# Clone the repository
git clone https://github.com/adebert/dotcat
cd dotcat

# Build the binary
make build
```

## Usage

```bash
# Basic usage
dotcat <file> <dotted_path>

# Example: Read a value from a JSON file
dotcat config.json user.name

# Example: With specific output format
dotcat config.json user.address --output json

# Example: Access an array element
dotcat config.json users@0.name
```

## Examples

```bash
# Read a simple value
$ dotcat config.json version
1.0.0

# Read a nested value
$ dotcat config.json user.address.city
New York

# Read an array element
$ dotcat config.json users@0.name
John Doe

# Output as JSON
$ dotcat config.json user --output json
{
  "name": "John Doe",
  "address": {
    "city": "New York",
    "zip": "10001"
  }
}
```

## Running Tests

```bash
# Run all tests
./run-tests.sh

# Run tests with coverage report
./run-tests.sh --coverage

# Open HTML coverage report
./run-tests.sh --coverage --html
```

## License

[MIT](LICENSE)

```bash
# Access data by attribute path
dotcat data.json person.name.first
# John
dotcat data.json person.name.last
# Doe

# Controle your output format
dotcat data.json person.name --output=yaml
# name:
#   first: John
#   last: Doe
dotcat data.json person.name --output=json
# {"first": "John", "last": "Doe"}

# List access
dotcat data.json person.friends@0
# {"name":{"first": "Alice", "last": "Smith"}, "age": 25} -> item access
dotcat data.json person.friends@2:4
# [{"name":{"first": "Alice", "last": "Smith"}, "age": 25}, {"name":{"first": "Bob", "last": "Johnson"}, "age": 30}]  -> slice access
dotcat data.json person.friends@4:-1
# ... from 5th to last item
```

## The good times are here

Easily read values from **JSON, YAML, TOML, and INI** files without complex scripting or manual parsing.

Access deeply **nested values** using intuitive dot-separated paths (e.g., **`person.first.name`**) while controlling the **output format** with `--output` flag.

Dotcat is a good **unix citizen** with well structured **exit codes** so it can take part of your command pipeline like cat or grep would.

Includes **ZSH autocompletion** for both file paths and dotted paths, making it even easier to navigate complex data structures.

## Installation

If you have a global pip install, this will install dotcat globally:

```bash
brew install dotcat
```

## ZSH Completion

Dotcat comes with ZSH completion support that is automatically installed when you install the package with pip. The installation script will:

1. Look for appropriate ZSH completion directories
2. Install the completion files if possible
3. Notify you of the installation location

If the automatic installation fails, you can manually install the completions:

```bash
# Copy the completion script to your ZSH completions directory
mkdir -p ~/.zsh/completions
cp /path/to/installed/package/zsh/_dotcat ~/.zsh/completions/

# Or run the installation script directly
dotcat-install-completions
```

See the [ZSH completion README](zsh/README.md) for detailed instructions.
