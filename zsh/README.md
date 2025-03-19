# Dotcat Shell Completions

This directory contains files for shell completion support for the `dotcat`
command.

## Completion Options

Dotcat now supports two completion methods:

1. **Traditional ZSH Completion** - A custom ZSH completion script that provides
   basic file and dotted-path completions.
2. **Argcomplete-based Completion** - A more advanced completion system using
   Python's argcomplete library.

## Installation

### Automatic Installation

The simplest way to install completions is to run:

```bash
dotcat-install-completions
```

This script will:

1. Attempt to install traditional ZSH completions if ZSH is detected
2. Attempt to set up argcomplete global completion if argcomplete is installed

### Manual Installation

#### Traditional ZSH Completion

1. Copy the `_dotcat` file to a directory in your `$fpath` (e.g.,
   `/usr/local/share/zsh/site-functions/`)
2. Copy `dotcat-completion.py` to a directory in your `$PATH`
3. Run `compinit` or restart your shell

#### Argcomplete-based Completion

1. Install argcomplete:

   ```bash
   pip install argcomplete
   ```

2. Activate global completion:

   ```bash
   activate-global-python-argcomplete
   ```

3. Source your shell configuration or restart your shell.

## How It Works

### Traditional Completion

The traditional ZSH completion uses the `_dotcat` file which calls the
`dotcat-completion.py` helper script. This script parses files and extracts
dotted paths to suggest as completions.

### Argcomplete Completion

The argcomplete-based completion uses Python's argcomplete library to provide
more intelligent completions. It leverages the existing code in dotcat to parse
files and suggest completions.

The main advantages of argcomplete are:

- It works with both ZSH and Bash
- It's integrated directly with the Python code, so it's more maintainable
- It can provide better context-aware completions

## Choosing Between the Two

The installer will attempt to set up both systems, but argcomplete is preferred
if available. If you have both installed, argcomplete will take precedence.

If you prefer to use only the traditional ZSH completion, you can remove
argcomplete:

```bash
pip uninstall argcomplete
```

## Files

- `_dotcat` - ZSH completion script (uses the Python helper)
- `dotcat-completion.py` - Python helper script for extracting dotted paths
- `test-completion.zsh` - Script for testing the completion locally

## Testing

You can test the completion by typing:

```bash
# Test file completion
dotcat [TAB]

# Test dotted path completion
dotcat path/to/file.json [TAB]

# Test nested path completion
dotcat path/to/file.json python[TAB]
```

For local testing without installation, use the test script:

```bash
./zsh/test-completion.zsh
```

## Troubleshooting

If completion doesn't work:

1. Make sure the file is in a directory in your $fpath
2. Check that the file has the correct permissions:

```bash
chmod 755 /path/to/_dotcat
```

3. If using the Python helper, make sure it's in your PATH and executable:

```bash
which dotcat-completion.py
chmod +x /path/to/dotcat-completion.py
```

4. Run `compinit` to rebuild the completion system:

```bash
autoload -Uz compinit && compinit
```

5. Check for any error messages when sourcing your `.zshrc`

## Manual Testing

If you want to test the Python helper script directly:

```bash
# Get top-level paths from a file
dotcat-completion.py path/to/file.json

# Get nested paths
dotcat-completion.py path/to/file.json python
dotcat-completion.py path/to/file.json python.editor
```

You can also use the included test script to try the completion in a temporary
environment:

```bash
# Run the test script
./zsh/test-completion.zsh
```
