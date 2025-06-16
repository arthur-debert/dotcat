package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/adebert/dotcat/internal/parser"
	"github.com/adebert/dotcat/internal/data"
	"github.com/adebert/dotcat/internal/formatter"
)

var outputFormat string

var rootCmd = &cobra.Command{
	Use:   "dotcat [file] [dotted_path]",
	Short: "Get a value from a structured data file using a dotted path",
	Long: `dotcat allows you to read a value from a structured data file
(JSON, YAML, TOML, or INI) using a dot-separated path to the desired key.`,
	Run: func(cmd *cobra.Command, args []string) {
		if len(args) != 2 {
			fmt.Println("Usage: ")
			fmt.Println("dotcat  <file> <variable path> ")
			fmt.Println("dotcat data.json person.name")
			fmt.Println()
			cmd.Usage()
			os.Exit(1)
		}

		filePath := args[0]
		dotPath := args[1]

		parsedData, err := parser.ParseFile(filePath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error parsing file: %v\n", err)
			os.Exit(1)
		}

		value, err := data.FromDottedPath(parsedData, dotPath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error looking up value: %v\n", err)
			os.Exit(1)
		}

		formattedValue, err := formatter.FormatOutput(value, outputFormat)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error formatting output: %v\n", err)
			os.Exit(1)
		}

		fmt.Println(formattedValue)
	},
}

func init() {
	rootCmd.Flags().StringVarP(&outputFormat, "output", "o", "raw", "Output format (raw, json, yaml, toml, ini)")
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}
