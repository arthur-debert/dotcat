class Dotcat < Formula
  include Language::Python::Virtualenv  # <--- Add this line
  depends_on "python@3.9"
  depends_on "poetry"

  desc "Cat structured data, in style"
  homepage "https://github.com/arthur-debert/dotcat"

    url "https://files.pythonhosted.org/packages/26/2d/a06e405e5a6e987e922b3622bea833ab2373c9e0839b9bfd9578dd56f80b/dotcat-0.8.15.tar.gz"
    sha256 "fa3b9155daccd1936d5e4f2598feebd79436b6308f887aa94831eabaf70fb4e5"

  def install
    virtualenv_path = libexec / "venv"

    python3_executable = Formula["python@3.9"].opt_bin / "python3.9"
    python3_version = `#{python3_executable} --version`.strip.split(" ")[1]

    if python3_version.blank? || python3_version < "3.9"
      odie "Python 3.9 or newer is required." # Error if Python < 3.9
    end

    poetry_executable = `which poetry`.strip

    ENV["POETRY_HOME"] = libexec
    system poetry_executable, "env", "use", python3_executable
    system poetry_executable, "install", "--no-dev"  # --no-dev if you only need runtime dependencies

    (bin / "dotcat").write <<~EOS
                             #!/bin/bash
                             exec "#{poetry_executable}" run dotcat "$@"
                           EOS
  end

  test do
    assert_match "Usage: dotcat", shell_output("#{bin}/dotcat --help")
  end
end