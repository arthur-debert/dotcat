package formatter

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"gopkg.in/ini.v1"
)

func TestFormatOutput(t *testing.T) {
	data := map[string]interface{}{
		"name":    "dotcat",
		"version": "0.1.0",
	}

	iniData := map[string]interface{}{
		"dotcat": map[string]interface{}{
			"name":    "dotcat",
			"version": "0.1.0",
		},
	}

	t.Run("raw format", func(t *testing.T) {
		output, err := FormatOutput(data, "raw")
		require.NoError(t, err)
		assert.Equal(t, "map[name:dotcat version:0.1.0]", output)
	})

	t.Run("json format", func(t *testing.T) {
		output, err := FormatOutput(data, "json")
		require.NoError(t, err)
		// Note: The order of keys in JSON is not guaranteed.
		// A more robust test would unmarshal and compare.
		expectedJSON := `{
  "name": "dotcat",
  "version": "0.1.0"
}`
		assert.JSONEq(t, expectedJSON, output)
	})

	t.Run("yaml format", func(t *testing.T) {
		output, err := FormatOutput(data, "yaml")
		require.NoError(t, err)
		expectedYAML := "name: dotcat\nversion: 0.1.0\n"
		assert.Equal(t, expectedYAML, output)
	})

	t.Run("toml format", func(t *testing.T) {
		output, err := FormatOutput(data, "toml")
		require.NoError(t, err)
		expectedTOML := "name = \"dotcat\"\nversion = \"0.1.0\"\n"
		assert.Equal(t, expectedTOML, output)
	})

	t.Run("ini format", func(t *testing.T) {
		output, err := FormatOutput(iniData, "ini")
		require.NoError(t, err)

		// Parse the output to avoid issues with key order and whitespace
		cfg, err := ini.Load([]byte(output))
		require.NoError(t, err)

		sec, err := cfg.GetSection("dotcat")
		require.NoError(t, err)
		assert.Equal(t, "dotcat", sec.Key("name").String())
		assert.Equal(t, "0.1.0", sec.Key("version").String())
	})

	t.Run("unsupported format", func(t *testing.T) {
		_, err := FormatOutput(data, "xml")
		assert.Error(t, err)
	})
} 