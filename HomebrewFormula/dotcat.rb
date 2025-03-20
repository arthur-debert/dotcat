class Dotcat < Formula
  include Language::Python::Virtualenv

  desc "Cat structured data , in style"
  homepage "https://pypi.org/project/dotcat/"
  url "https://files.pythonhosted.org/packages/61/7a/2b5ba10c4b31846f56cebbf7b761da5ec316a124d2c35c3627bc45dbfb75/dotcat-0.9.6.tar.gz"
  sha256 "24a9fcb3286fb9267443ceb3416dd4e64956641662a1154bdb78d23ec030e5b3"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources

    # Install zsh completion
    zsh_completion.install "zsh/_dotcat" => "_dotcat"
    # Install the helper script for ZSH completions if it exists
    if File.exist?("zsh/dotcat-completion.py")
      bin.install "zsh/dotcat-completion.py"
    end
  end

  test do
    # Add some basic tests to verify the installation
    assert_match "dotcat v0.9.6",
                 shell_output("#{{bin}}/dotcat --version")

    # Test if the completions are installed correctly
    assert_predicate zsh_completion/"_dotcat", :exist?
  end
end
