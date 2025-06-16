package parser

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/BurntSushi/toml"
	"gopkg.in/ini.v1"
	"gopkg.in/yaml.v3"
)

// ParseFile reads a file and parses it based on its extension.
func ParseFile(filePath string) (interface{}, error) {
	ext := strings.ToLower(filepath.Ext(filePath))
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("could not read file: %w", err)
	}

	switch ext {
	case ".json":
		return parseJSON(content)
	case ".yaml", ".yml":
		return parseYAML(content)
	case ".toml":
		return parseTOML(content)
	case ".ini":
		return parseINI(content)
	default:
		return nil, fmt.Errorf("unsupported file format: %s", ext)
	}
}

func parseJSON(content []byte) (interface{}, error) {
	var data interface{}
	if err := json.Unmarshal(content, &data); err != nil {
		return nil, fmt.Errorf("could not parse JSON: %w", err)
	}
	return data, nil
}

func parseYAML(content []byte) (interface{}, error) {
	var data interface{}
	if err := yaml.Unmarshal(content, &data); err != nil {
		return nil, fmt.Errorf("could not parse YAML: %w", err)
	}
	return data, nil
}

func parseTOML(content []byte) (interface{}, error) {
	var data interface{}
	if _, err := toml.Decode(string(content), &data); err != nil {
		return nil, fmt.Errorf("could not parse TOML: %w", err)
	}
	return data, nil
}

func parseINI(content []byte) (interface{}, error) {
	cfg, err := ini.Load(content)
	if err != nil {
		return nil, fmt.Errorf("could not parse INI: %w", err)
	}
	
	// Convert the INI File structure to a map of maps for consistent access pattern
	result := make(map[string]interface{})
	
	for _, section := range cfg.Sections() {
		if section.Name() == "DEFAULT" && len(section.Keys()) == 0 {
			continue // Skip empty DEFAULT section
		}
		
		sectionMap := make(map[string]interface{})
		for _, key := range section.Keys() {
			sectionMap[key.Name()] = key.Value()
		}
		
		result[section.Name()] = sectionMap
	}
	
	return result, nil
} 