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
	@echo "NOTE: Skipping completions generation (not implemented)"
	@mkdir -p ./completions
	@touch ./completions/$(BINARY_NAME).bash
	@touch ./completions/_$(BINARY_NAME)
	@touch ./completions/$(BINARY_NAME).fish

# Optional: Only run these if the app supports man pages
man-page:
	@echo "NOTE: Skipping man page generation (not implemented)"
	@mkdir -p ./man/man1
	@touch ./man/man1/$(BINARY_NAME).1

# Skip completions and man-page for now as they're not critical
release:
	@echo "Creating a release..."
	@docker run --rm -it \
		-v "$(CURDIR):/go/src/github.com/arthur-debert/$(BINARY_NAME)" \
		-w /go/src/github.com/arthur-debert/$(BINARY_NAME) \
		-e PKG_NAME=$(BINARY_NAME) \
		goreleaser/goreleaser release --snapshot --clean 