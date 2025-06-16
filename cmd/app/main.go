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

var completionCmd = &cobra.Command{
	Use:   "completion [bash|zsh|fish]",
	Short: "Generate completion script",
	Long: `To load completions:

Bash:
  $ source <(dotcat completion bash)

  # To load completions for each session, execute once:
  $ dotcat completion bash > /etc/bash_completion.d/dotcat
  
Zsh:
  # If shell completion is not already enabled in your environment,
  # you will need to enable it.  You can execute the following once:
  $ echo "autoload -U compinit; compinit" >> ~/.zshrc

  # To load completions for each session, execute once:
  $ dotcat completion zsh > "${fpath[1]}/_dotcat"

Fish:
  $ dotcat completion fish | source

  # To load completions for each session, execute once:
  $ dotcat completion fish > ~/.config/fish/completions/dotcat.fish
`,
	DisableFlagsInUseLine: true,
	ValidArgs:             []string{"bash", "zsh", "fish"},
	Args:                  cobra.ExactValidArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		switch args[0] {
		case "bash":
			cmd.Root().GenBashCompletion(os.Stdout)
		case "zsh":
			cmd.Root().GenZshCompletion(os.Stdout)
		case "fish":
			cmd.Root().GenFishCompletion(os.Stdout, true)
		}
	},
}

var manCmd = &cobra.Command{
	Use:   "man",
	Short: "Generate man page",
	Long:  `Generate man page for dotcat.`,
	Run: func(cmd *cobra.Command, args []string) {
		// Write directly to stdout since we'll redirect in the Makefile
		fmt.Println(".TH \"DOTCAT\" \"1\" \"\" \"dotcat " + version + "\" \"User Commands\"")
		fmt.Println(".SH NAME")
		fmt.Println("dotcat \\- Get a value from a structured data file using a dotted path")
		fmt.Println(".SH SYNOPSIS")
		fmt.Println(".B dotcat")
		fmt.Println("[\\fIfile\\fR] [\\fIdotted_path\\fR] [\\fIflags\\fR]")
		fmt.Println(".SH DESCRIPTION")
		fmt.Println("dotcat allows you to read a value from a structured data file (JSON, YAML, TOML, or INI) using a dot-separated path to the desired key.")
		fmt.Println(".SH OPTIONS")
		fmt.Println(".TP")
		fmt.Println("\\fB\\-o\\fR, \\fB\\-\\-output\\fR string")
		fmt.Println("Output format (raw, json, yaml, toml, ini) (default \"raw\")")
		fmt.Println(".TP")
		fmt.Println("\\fB\\-v\\fR, \\fB\\-\\-version\\fR")
		fmt.Println("Show version information")
		fmt.Println(".SH EXAMPLES")
		fmt.Println(".PP")
		fmt.Println("\\fBdotcat config.json user.name\\fR")
		fmt.Println(".PP")
		fmt.Println("Read a value from a JSON file")
		fmt.Println(".PP")
		fmt.Println("\\fBdotcat config.yaml servers.0.address\\fR")
		fmt.Println(".PP")
		fmt.Println("Read the first server's address from a YAML file")
		fmt.Println(".SH SEE ALSO")
		fmt.Println(".PP")
		fmt.Println("\\fBjq\\fR(1), \\fByq\\fR(1)")
	},
}

func init() {
	rootCmd.Flags().StringVarP(&outputFormat, "output", "o", "raw", "Output format (raw, json, yaml, toml, ini)")
	rootCmd.Flags().BoolVarP(&showVersion, "version", "v", false, "Show version information")
	
	rootCmd.AddCommand(completionCmd)
	rootCmd.AddCommand(manCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
