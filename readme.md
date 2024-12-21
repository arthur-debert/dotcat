# dotcat

Cat structured data in a shell, i.e.

```bash
dotcat some.json  `user.name.first  # echoes Janet
```

Access data within JSON, YAML, TOML, and INI files using intuitive dot notation directly from your terminal.  `dotcat` simplifies scripting and configuration management by allowing you to easily extract specific values.

## Features

* Access data within structured data files (JSON, YAML, TOML, INI) using dot notation.
* Extract specific values and print them to the console.
* Simplify scripting by making it easy to retrieve configuration data.
* Supports nested keys and array indexing (e.g., `array[0]`).
* Clear error messages for file not found, invalid format, and key not found.

## Quick Start

```bash
echo '{"user": {"name": {"first": "Janet", "last": "Doe"}}}' > data.json
dotcat data.json user.name.first
# Output: Janet

dotcat data.json user.name.last

# Output: Doe

```

## Installation

You can install dotcat using pip:

```bash
pip install dotcat
```

``

## USAGE

dotcat `<file> <key>`

`<file>`: Path to the structured data file (JSON, YAML, TOML, INI).
`<key>`: The key to access using dot notation.

## Examples

```bash
# Accessing a simple key
dotcat config.json user.name

# Accessing nested keys
dotcat data.yaml server.location.city

# Accessing array elements
dotcat items.json products[0].name
dotcat items.json products[2].price


# Handling a missing key
dotcat config.json nonexistent.key
# Output: Key 'nonexistent.key' not found in file 'config.json'. 'nonexistent' was not found.

# Example with an invalid file format
dotcat invalid.txt some.key
# Output: Unable to parse file 'invalid.txt'. Supported formats: JSON, YAML, TOML, INI


# Using with pipes (if implemented in the tool)
cat config.json | dotcat user.name
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

Tests are done with pytest.

Development Setup
Clone the repository.
Create a virtual environment: `python3 -m venv .venv`
Activate the virtual environment: `source .venv/bin/activate`
Install development dependencies: `pip install -r requirements.txt`

(create a requirements file if one doesn't exist)

Run tests: pytest

### License

[MIT License][def]

[def]: ./LICENSE
