class Dotcat < Formula
  include Language::Python::Virtualenv
  desc "Cat structured data, in style"
  homepage "https://github.com/arthur-debert/dotcat"
  url "https://files.pythonhosted.org/packages/30/56/f503f2b45aecc95c715abeaf0ba71899da0fafddbe6014b068c2ca9c1097/dotcat-0.8.19.tar.gz"
  sha256 "adefff16d291a1b84f78db8ded1806fedfe243f64f74bcd8c99c1b5a9f3a9f78"
  depends_on "poetry"
  depends_on "python@3.9"

  def install
    python3_executable = Formula["python@3.9"].opt_bin / "python3.9"
    python3_version = `#{python3_executable} --version`.strip[1]

    if python3_version.blank? || python3_version < "3.9"
      odie "Python 3.9 or newer is required." # Error if Python < 3.9
    end

    poetry_executable = `which poetry`.strip

    ENV["POETRY_HOME"] = libexec
    system poetry_executable, "env", "use", python3_executable
    system poetry_executable, "install", "--no-dev"

    (bin / "dotcat").write <<~EOS
      #!/bin/bash
      exec "#{poetry_executable}" run dotcat "$@"
    EOS
  end

  test do
    assert_match "Usage: dotcat", shell_output("#{bin}/dotcat --help")
  end
end
