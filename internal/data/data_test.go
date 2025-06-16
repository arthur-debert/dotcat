package data

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestFromDottedPath(t *testing.T) {
	data := map[string]interface{}{
		"name":    "dotcat",
		"version": "0.1.0",
		"dependencies": map[string]interface{}{
			"go": "1.18",
		},
		"contributors": []interface{}{
			map[string]interface{}{"name": "John Doe"},
			map[string]interface{}{"name": "Jane Doe"},
		},
	}

	t.Run("simple path", func(t *testing.T) {
		val, err := FromDottedPath(data, "name")
		require.NoError(t, err)
		assert.Equal(t, "dotcat", val)
	})

	t.Run("nested path", func(t *testing.T) {
		val, err := FromDottedPath(data, "dependencies.go")
		require.NoError(t, err)
		assert.Equal(t, "1.18", val)
	})

	t.Run("list access", func(t *testing.T) {
		val, err := FromDottedPath(data, "contributors@0.name")
		require.NoError(t, err)
		assert.Equal(t, "John Doe", val)
	})

	t.Run("key not found", func(t *testing.T) {
		_, err := FromDottedPath(data, "foo.bar")
		assert.Error(t, err)
	})

	t.Run("index out of bounds", func(t *testing.T) {
		_, err := FromDottedPath(data, "contributors@5")
		assert.Error(t, err)
	})
} 