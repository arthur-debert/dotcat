.PHONY: all build test install uninstall clean completions man-page release

BINARY_NAME?=$(shell echo $$PKG_NAME)
VERSION?=$(shell git describe --tags --abbrev=0)

all: build

build:
	@echo "Building $(BINARY_NAME)..."
	@go build -o ./bin/$(BINARY_NAME) ./cmd/app

test:
	go test ./...

clean:
	@echo "Cleaning up..."
	@rm -rf ./bin
	@rm -rf ./dist
	@rm -rf ./completions
	@rm -rf ./man

# Optional: Only run these if the app supports completions
completions:
	@echo "Generating shell completions..."
	@mkdir -p ./completions
	@./bin/$(BINARY_NAME) completion bash > ./completions/$(BINARY_NAME).bash
	@./bin/$(BINARY_NAME) completion zsh > ./completions/_$(BINARY_NAME)
	@./bin/$(BINARY_NAME) completion fish > ./completions/$(BINARY_NAME).fish

# Optional: Only run these if the app supports man pages
man-page:
	@echo "Generating man page..."
	@mkdir -p ./man/man1
	@./bin/$(BINARY_NAME) man > ./man/man1/$(BINARY_NAME).1

# Include completions and man-pages in the release process
release: completions man-page
	@echo "Creating a release..."
	@docker run --rm -it \
		-v "$(CURDIR):/go/src/github.com/arthur-debert/$(BINARY_NAME)" \
		-w "/go/src/github.com/arthur-debert/$(BINARY_NAME)" \
		-e PKG_NAME=$(BINARY_NAME) \
		goreleaser/goreleaser release --snapshot --clean 