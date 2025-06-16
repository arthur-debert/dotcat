package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/arthur-debert/dotcat/internal/parser"
	"github.com/arthur-debert/dotcat/internal/data"
	"github.com/arthur-debert/dotcat/internal/formatter"
)

// Version information - will be set during build
var (
	version = "dev"
	commit  = "none"
	date    = "unknown"
)

var outputFormat string
var showVersion bool

var rootCmd = &cobra.Command{
	Use:   "dotcat [file] [dotted_path]",
	Short: "Get a value from a structured data file using a dotted path",
	Long: `dotcat allows you to read a value from a structured data file
(JSON, YAML, TOML, or INI) using a dot-separated path to the desired key.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		// If version flag is provided, print version and exit
		if showVersion {
			fmt.Printf("dotcat version %s, commit %s, built at %s\n", version, commit, date)
			return nil
		}
	
		if len(args) != 2 {
			fmt.Println("Usage: ")
			fmt.Println("dotcat  <file> <variable path> ")
			fmt.Println("dotcat data.json person.name")
			fmt.Println()
			cmd.Usage()
			return fmt.Errorf("accepts 2 arg(s), received %d", len(args))
		}

		filePath := args[0]
		dotPath := args[1]

		parsedData, err := parser.ParseFile(filePath)
		if err != nil {
			return fmt.Errorf("Error parsing file: %w", err)
		}

		value, err := data.FromDottedPath(parsedData, dotPath)
		if err != nil {
			return fmt.Errorf("Error looking up value: %w", err)
		}

		formattedValue, err := formatter.FormatOutput(value, outputFormat)
		if err != nil {
			return fmt.Errorf("Error formatting output: %w", err)
		}

		fmt.Println(formattedValue)
		return nil
	},
}

func init() {
	rootCmd.Flags().StringVarP(&outputFormat, "output", "o", "raw", "Output format (raw, json, yaml, toml, ini)")
	rootCmd.Flags().BoolVarP(&showVersion, "version", "v", false, "Show version information")
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
