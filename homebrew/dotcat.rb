class Dotcat < Formula
  include Language::Python::Virtualenv  # <--- Add this line
  depends_on "python@3.9"
  depends_on "poetry"

  desc "Cat structured data, in style"
  homepage "https://github.com/arthur-debert/dotcat"

    url "https://files.pythonhosted.org/packages/42/89/9ee249aa599012a1f0f05cc8aa747f4df626a56d2d551ad533ceab15adc7/dotcat-0.8.5.tar.gz"
    sha256 "85b0a512c67ee14ffe1c04f951b866a0eccfd4a7dbbe14771c22fbe74d9d516b"

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