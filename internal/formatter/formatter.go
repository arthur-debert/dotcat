package formatter

import (
	"bytes"
	"encoding/json"
	"fmt"
	"gopkg.in/yaml.v3"

	"github.com/BurntSushi/toml"
	"gopkg.in/ini.v1"
	// Note: We'll need a TOML writer. The standard library doesn't have one.
	// We can implement a simple one or find a library.
)

// FormatOutput formats the data based on the specified format.
func FormatOutput(data interface{}, format string) (string, error) {
	switch format {
	case "raw":
		return fmt.Sprintf("%v", data), nil
	case "json":
		b, err := json.MarshalIndent(data, "", "  ")
		if err != nil {
			return "", fmt.Errorf("could not format to JSON: %w", err)
		}
		return string(b), nil
	case "yaml":
		b, err := yaml.Marshal(data)
		if err != nil {
			return "", fmt.Errorf("could not format to YAML: %w", err)
		}
		return string(b), nil
	case "toml":
		var buf bytes.Buffer
		encoder := toml.NewEncoder(&buf)
		if err := encoder.Encode(data); err != nil {
			return "", fmt.Errorf("could not format to TOML: %w", err)
		}
		return buf.String(), nil
	case "ini":
		cfg := ini.Empty()
		m, ok := data.(map[string]interface{})
		if !ok {
			return "", fmt.Errorf("INI output requires a map structure")
		}

		for section, kv := range m {
			s, err := cfg.NewSection(section)
			if err != nil {
				return "", fmt.Errorf("could not create INI section: %w", err)
			}
			kvMap, ok := kv.(map[string]interface{})
			if !ok {
				return "", fmt.Errorf("INI section value must be a map")
			}
			for key, val := range kvMap {
				if _, err := s.NewKey(key, fmt.Sprintf("%v", val)); err != nil {
					return "", fmt.Errorf("could not create INI key: %w", err)
				}
			}
		}

		var buf bytes.Buffer
		if _, err := cfg.WriteTo(&buf); err != nil {
			return "", fmt.Errorf("could not write INI data: %w", err)
		}
		return buf.String(), nil
	default:
		return "", fmt.Errorf("unsupported output format: %s", format)
	}
} 