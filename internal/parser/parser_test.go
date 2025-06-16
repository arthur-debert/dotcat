package parser

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"gopkg.in/ini.v1"
)

func TestParseFile_JSON(t *testing.T) {
	data, err := ParseFile("testdata/test.json")
	require.NoError(t, err)

	m, ok := data.(map[string]interface{})
	require.True(t, ok)

	assert.Equal(t, "dotcat", m["name"])
	assert.Equal(t, "0.1.0", m["version"])

	deps, ok := m["dependencies"].(map[string]interface{})
	require.True(t, ok)
	assert.Equal(t, "1.18", deps["go"])
}

func TestParseFile_YAML(t *testing.T) {
	data, err := ParseFile("testdata/test.yaml")
	require.NoError(t, err)

	m, ok := data.(map[string]interface{})
	require.True(t, ok, "data should be a map")

	assert.Equal(t, "dotcat", m["name"])
	assert.Equal(t, "0.1.0", m["version"])

	deps, ok := m["dependencies"].(map[string]interface{})
	require.True(t, ok, "dependencies should be a map")
	assert.Equal(t, "1.18", deps["go"])
}

func TestParseFile_TOML(t *testing.T) {
	data, err := ParseFile("testdata/test.toml")
	require.NoError(t, err)

	m, ok := data.(map[string]interface{})
	require.True(t, ok, "data should be a map")

	assert.Equal(t, "dotcat", m["name"])
	assert.Equal(t, "0.1.0", m["version"])

	deps, ok := m["dependencies"].(map[string]interface{})
	require.True(t, ok, "dependencies should be a map")
	assert.Equal(t, "1.18", deps["go"])
}

func TestParseFile_INI(t *testing.T) {
	data, err := ParseFile("testdata/test.ini")
	require.NoError(t, err)

	cfg, ok := data.(*ini.File)
	require.True(t, ok, "data should be a *ini.File")

	dotcatSection, err := cfg.GetSection("dotcat")
	require.NoError(t, err)
	assert.Equal(t, "dotcat", dotcatSection.Key("name").String())
	assert.Equal(t, "0.1.0", dotcatSection.Key("version").String())

	depsSection, err := cfg.GetSection("dependencies")
	require.NoError(t, err)
	assert.Equal(t, "1.18", depsSection.Key("go").String())
} 