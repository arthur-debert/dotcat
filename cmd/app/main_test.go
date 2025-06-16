package main

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
)

// executeCommand is a helper function to execute the root command and capture its output.
func executeCommand(args ...string) (*bytes.Buffer, error) {
	b := new(bytes.Buffer)
	rootCmd.SetOut(b)
	rootCmd.SetErr(b)
	rootCmd.SetArgs(args)

	err := rootCmd.Execute()

	return b, err
}

func TestRootCmd_NoArgs(t *testing.T) {
	_, err := executeCommand()
	assert.Error(t, err)
}


func TestRootCmd_FileNotFound(t *testing.T) {
	_, err := executeCommand("nonexistent.json", "key")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "Error parsing file:")
	assert.Contains(t, err.Error(), "no such file or directory")
} 