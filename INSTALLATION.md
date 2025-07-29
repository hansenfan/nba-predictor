# 🏀 NBA Predictor - Installation Guide

This guide will walk you through installing all the necessary tools and dependencies for the NBA Predictor project.

## 📋 Prerequisites

- **macOS** (you're on darwin 23.5.0) ✅
- **At least 8GB RAM** (16GB recommended for ML training)
- **At least 20GB free disk space**
- **Stable internet connection**

## 🚀 Quick Start (Automated)

### Option 1: Run the Setup Script

```bash
# Make the script executable
chmod +x setup.sh

# Run the automated setup
./setup.sh
```

### Option 2: Manual Installation

## 📦 Step-by-Step Installation

### 1. Install Homebrew (Package Manager)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python Environment

#### Install pyenv (Python Version Manager)

```bash
brew install pyenv

# Add to your shell profile (~/.zshrc)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Reload shell
source ~/.zshrc
```

#### Install Python 3.11

```bash
pyenv install 3.11.0
pyenv global 3.11.0

# Verify installation
python --version  # Should show Python 3.11.0
```

#### Create Virtual Environment

```bash
# Create project directory
mkdir nba-predictor
cd nba-predictor

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Java Environment

#### Install OpenJDK 17

```bash
brew install openjdk@17

# Add to PATH
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
java --version
javac --version
```

#### Install Maven

```bash
brew install maven

# Verify installation
mvn --version
```

### 4. Install Node.js Environment

#### Install nvm (Node Version Manager)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell
source ~/.zshrc
```

#### Install Node.js 18

```bash
nvm install 18
nvm use 18
nvm alias default 18

# Verify installation
node --version
npm --version
```

### 5. Install Databases

#### PostgreSQL 14

```bash
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Create database
createdb nba_predictor

# Verify connection
psql -d nba_predictor -c "SELECT version();"
```

#### Redis 7

```bash
brew install redis

# Start Redis service
brew services start redis

# Test Redis connection
redis-cli ping  # Should return PONG
```

### 6. Install Docker

#### Docker Desktop

1. Download Docker Desktop for Mac from: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation:

```bash
docker --version
docker-compose --version
```

### 7. Install Development Tools

#### Git (usually pre-installed)

```bash
brew install git

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### VS Code

```bash
brew install --cask visual-studio-code
```

#### Database Management Tools

```bash
# TablePlus (recommended)
brew install --cask tableplus

# Or pgAdmin
brew install --cask pgadmin4
```

#### API Testing Tools

```bash
# Postman
brew install --cask postman

# Or Insomnia
brew install --cask insomnia
```

#### Terminal Tools

```bash
brew install tree htop wget
```

### 8. Install Additional Tools (Optional)

#### Oh My Zsh (Better Terminal)

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

#### Jupyter Lab

```bash
pip install jupyterlab
```

## 🔧 Environment Setup

### Create Environment Variables

```bash
# Create .env file
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://nba_user:nba_password@localhost:5432/nba_predictor
REDIS_URL=redis://localhost:6379

# NBA API Configuration
NBA_API_KEY=your_nba_api_key_here

# Spring Boot Configuration
SPRING_PROFILES_ACTIVE=development
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/nba_predictor
SPRING_DATASOURCE_USERNAME=nba_user
SPRING_DATASOURCE_PASSWORD=nba_password

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8080/api/v1
EOF
```

### Get NBA API Key

1. Go to https://developer.nba.com/
2. Sign up for an account
3. Request an API key
4. Add the key to your `.env` file

## 🧪 Verify Installation

### Test Python Environment

```bash
# Activate virtual environment
source venv/bin/activate

# Test PyTorch
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

# Test other libraries
python -c "import pandas as pd; import numpy as np; print('Pandas and NumPy working')"
```

### Test Java Environment

```bash
# Test Java
java --version

# Test Maven
mvn --version
```

### Test Node.js Environment

```bash
# Test Node.js
node --version

# Test npm
npm --version
```

### Test Databases

```bash
# Test PostgreSQL
psql -d nba_predictor -c "SELECT 'PostgreSQL is working!' as status;"

# Test Redis
redis-cli ping
```

### Test Docker

```bash
# Test Docker
docker run hello-world
```

## 🚀 Start the Project

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd nba-predictor
```

### 2. Start Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Or start individual services
docker-compose up postgres redis -d
docker-compose up api-backend -d
docker-compose up ml-backend -d
docker-compose up frontend -d
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8080
- **API Documentation**: http://localhost:8080/swagger-ui.html
- **Database**: localhost:5432 (use TablePlus or pgAdmin)

## 🔍 Troubleshooting

### Common Issues

#### Python Issues

```bash
# If pyenv not found
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

# If virtual environment not activating
source venv/bin/activate

# If packages not installing
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Java Issues

```bash
# If Java not found
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"

# If Maven not found
brew install maven
```

#### Database Issues

```bash
# Restart PostgreSQL
brew services restart postgresql@14

# Restart Redis
brew services restart redis

# Check if services are running
brew services list
```

#### Docker Issues

```bash
# Restart Docker Desktop
# Check Docker status
docker info

# Clean up Docker
docker system prune -a
```

### Memory Issues

If you encounter memory issues during ML training:

```bash
# Increase Docker memory limit in Docker Desktop settings
# Recommended: 8GB+ for ML training

# Or use smaller batch sizes in your ML models
```

## 📚 Next Steps

1. **Read the Documentation**: Check the `docs/` folder
2. **Explore the Code**: Start with `ml-backend/` for ML models
3. **Run Tests**: `pytest` for Python, `mvn test` for Java
4. **Start Developing**: Pick a component and start coding!

## 🆘 Getting Help

- **GitHub Issues**: Create an issue for bugs
- **Documentation**: Check the `docs/` folder
- **Community**: Join our Discord/Slack (if available)

## 📝 Notes

- Keep your virtual environment activated when working on Python code
- Use `docker-compose logs <service-name>` to check service logs
- The setup script automates most of this process
- All services are containerized for consistency across environments
