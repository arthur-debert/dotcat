class Dotcat < Formula
  include Language::Python::Virtualenv  # <--- Add this line
  depends_on "python@3.9"
  depends_on "poetry"

  desc "Cat structured data, in style"
  homepage "https://github.com/arthur-debert/dotcat"

    url "https://files.pythonhosted.org/packages/69/1d/8743e6c1b833005ef757f3c61f1ba166571f932830b92793629e60e2bcef/dotcat-0.8.2.tar.gz"
    sha256 "d8049b66e9afe5914ce9ee255de9f9f3e8dbe8dae1bb548d1df32a3317865d3b"

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