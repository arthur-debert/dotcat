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

# List access examples
echo '{"foo": {"bar": ["item1", "item2", "item3", "item4", "item5"]}}' > list.json

# Get one item (zero based)
dotcat list.json foo.bar@2
# Output: item3

# Get items from index 2 to 4
dotcat list.json foo.bar@2:4
# Output: ["item3", "item4"]

# Get items from start to index 3
dotcat list.json foo.bar@:3
# Output: ["item1", "item2", "item3"]

# Get items from index 3 to the end
dotcat list.json foo.bar@3:-1
# Output: ["item4", "item5"]
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
