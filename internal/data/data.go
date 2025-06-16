package data

import (
	"fmt"
	"strconv"
	"strings"
)

// FromDottedPath traverses a nested structure using a dot-separated path.
func FromDottedPath(data interface{}, path string) (interface{}, error) {
	parts := strings.Split(path, ".")
	var current interface{} = data

	for _, part := range parts {
		if strings.Contains(part, "@") {
			// Handle list access, e.g., key@index
			listParts := strings.Split(part, "@")
			key := listParts[0]
			indexStr := listParts[1]

			if m, ok := current.(map[string]interface{}); ok {
				if val, exists := m[key]; exists {
					current = val
				} else {
					return nil, fmt.Errorf("key not found: %s", key)
				}
			} else {
				return nil, fmt.Errorf("cannot access key '%s' in non-map structure", key)
			}

			if list, ok := current.([]interface{}); ok {
				index, err := strconv.Atoi(indexStr)
				if err != nil {
					return nil, fmt.Errorf("invalid list index: %s", indexStr)
				}
				if index >= 0 && index < len(list) {
					current = list[index]
				} else {
					return nil, fmt.Errorf("index out of bounds: %d", index)
				}
			} else {
				return nil, fmt.Errorf("key '%s' is not a list", key)
			}
		} else {
			// Handle map access
			if m, ok := current.(map[string]interface{}); ok {
				if val, exists := m[part]; exists {
					current = val
				} else {
					return nil, fmt.Errorf("key not found: %s", part)
				}
			} else {
				return nil, fmt.Errorf("cannot access key '%s' in non-map structure", part)
			}
		}
	}
	return current, nil
} 