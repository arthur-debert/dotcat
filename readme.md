# dotcat: Catting Structured Data in Style

`dotcat` gives your shell the ability to cat + grep structured data.

```bash
# With a sample json file:
echo '{"name": "John Doe", "age": 30, "address": {"street": "123 Main St", "city": "Anytown"}}' > data.json

# Get the name
dotcat data.json name
# Output: John Doe

# Get the city
dotcat data.json address.city
# Output: Anytown

# Format the output
dotcat data.json address --format=yaml
# Output:
# street: 123 Main St
# city:
#   Anytown

# Use with a YAML file (data.yaml)
echo 'name: Jane Doe\noccupation: Developer' > data.yaml
dotcat data.yaml occupation
# Output: Developer

# Use array index in path (array.json)
echo '{"items":[{"id":1}, {"id":2}]}' > array.json
dotcat array.json items.1.id
# Output: 2
```

## Key Features

* **Structured Data Extraction:** Easily read values from JSON, YAML, TOML, and INI files. No more complex scripting or manual parsing.
* **Dot-Separated Paths:** Access deeply nested values using intuitive dot-separated paths (e.g., `a.b.c`).
* **Configurable Output:** Control the output format with `--output` flag. Choose from:
  * `raw`:  Default. Direct string representation of the extracted value.
  * `formatted`: Pretty-printed JSON output, ideal for readability.
  * `json`: Compact JSON output.
  * `yaml`: YAML output.
  * `toml`: TOML output.
  * `ini`: INI output.
* **Clear Error Handling:** Provides informative error messages for invalid files, incorrect paths, or unsupported formats.
* **Lightweight and Fast:** Built for speed and efficiency.

## Installation

```bash
pip install dotcat
```

Usage
Basic usage involves specifying the file and the dot-separated key:

```bash
dotcat <file> <dot_separated_key> [--output <format>]
```

### Contributing

Contributions are welcome! General 
