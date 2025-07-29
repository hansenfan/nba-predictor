#!/bin/bash

# NBA Predictor Project Setup Script
# This script installs all required dependencies for the NBA predictor project

set -e  # Exit on any error

echo "🏀 NBA Predictor Project Setup"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Homebrew is installed
check_homebrew() {
    if ! command -v brew &> /dev/null; then
        print_status "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        print_success "Homebrew installed successfully"
    else
        print_success "Homebrew already installed"
    fi
}

# Install Python and dependencies
setup_python() {
    print_status "Setting up Python environment..."

    # Install pyenv if not present
    if ! command -v pyenv &> /dev/null; then
        brew install pyenv
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
        source ~/.zshrc
    fi

    # Install Python 3.11
    pyenv install 3.11.0 -s
    pyenv global 3.11.0

    # Create virtual environment
    python -m venv venv
    source venv/bin/activate

    # Install Python packages
    pip install --upgrade pip
    pip install torch torchvision torchaudio
    pip install numpy pandas scikit-learn matplotlib seaborn plotly
    pip install requests beautifulsoup4 sqlalchemy psycopg2-binary redis
    pip install fastapi uvicorn flask jupyter notebook
    pip install black flake8 pytest pre-commit

    print_success "Python environment setup complete"
}

# Install Java and Maven
setup_java() {
    print_status "Setting up Java environment..."

    # Install OpenJDK 17
    brew install openjdk@17

    # Add Java to PATH
    echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Install Maven
    brew install maven

    print_success "Java environment setup complete"
}

# Install Node.js and dependencies
setup_node() {
    print_status "Setting up Node.js environment..."

    # Install nvm if not present
    if ! command -v nvm &> /dev/null; then
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
        source ~/.zshrc
    fi

    # Install Node.js 18
    nvm install 18
    nvm use 18
    nvm alias default 18

    print_success "Node.js environment setup complete"
}

# Install databases
setup_databases() {
    print_status "Setting up databases..."

    # Install PostgreSQL
    brew install postgresql@14
    brew services start postgresql@14

    # Install Redis
    brew install redis
    brew services start redis

    print_success "Databases setup complete"
}

# Install Docker
setup_docker() {
    print_status "Setting up Docker..."

    if ! command -v docker &> /dev/null; then
        print_warning "Docker Desktop not found. Please install manually from:"
        print_warning "https://www.docker.com/products/docker-desktop"
    else
        print_success "Docker already installed"
    fi
}

# Install development tools
setup_dev_tools() {
    print_status "Setting up development tools..."

    # Install Git (usually pre-installed)
    brew install git

    # Install VS Code
    brew install --cask visual-studio-code

    # Install database tools
    brew install --cask tableplus

    # Install API testing tools
    brew install --cask postman

    # Install terminal tools
    brew install tree htop wget

    print_success "Development tools setup complete"
}

# Create project structure
create_project_structure() {
    print_status "Creating project structure..."

    # Create directories
    mkdir -p {ml-backend,api-backend,frontend,data-pipeline,database,docs}
    mkdir -p {ml-backend/{models,data,logs},api-backend/{src,logs},data-pipeline/{data,logs}}

    print_success "Project structure created"
}

# Main setup function
main() {
    print_status "Starting NBA Predictor project setup..."

    check_homebrew
    setup_python
    setup_java
    setup_node
    setup_databases
    setup_docker
    setup_dev_tools
    create_project_structure

    print_success "Setup complete! 🎉"
    print_status "Next steps:"
    echo "1. Install Docker Desktop manually if not already installed"
    echo "2. Activate Python virtual environment: source venv/bin/activate"
    echo "3. Start the project: docker-compose up"
    echo "4. Open http://localhost:3000 for the frontend"
    echo "5. Open http://localhost:8080 for the API"
}

# Run main function
main "$@"
