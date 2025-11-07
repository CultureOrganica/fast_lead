#!/bin/bash

# Fast Lead - Mac Development Setup Script
# Автоматическая настройка окружения разработки на macOS

set -e  # Exit on error

echo "🚀 Fast Lead - Mac Development Setup"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is for macOS only"
    exit 1
fi

print_info "Checking macOS version..."
MAC_VERSION=$(sw_vers -productVersion)
print_success "macOS version: $MAC_VERSION"

# Check and install Homebrew
echo ""
print_info "Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    print_info "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    print_success "Homebrew installed"
else
    print_success "Homebrew already installed"
fi

# Update Homebrew
print_info "Updating Homebrew..."
brew update
print_success "Homebrew updated"

# Install pyenv
echo ""
print_info "Checking pyenv..."
if ! command -v pyenv &> /dev/null; then
    print_info "Installing pyenv..."
    brew install pyenv

    # Add to shell config
    SHELL_CONFIG="$HOME/.zshrc"
    if [ -f "$HOME/.bash_profile" ]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    fi

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$SHELL_CONFIG"
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> "$SHELL_CONFIG"
    echo 'eval "$(pyenv init --path)"' >> "$SHELL_CONFIG"
    echo 'eval "$(pyenv init -)"' >> "$SHELL_CONFIG"

    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"

    print_success "pyenv installed"
else
    print_success "pyenv already installed"
fi

# Install Python 3.11
echo ""
print_info "Checking Python 3.11..."
if ! pyenv versions | grep -q "3.11.7"; then
    print_info "Installing Python 3.11.7..."
    pyenv install 3.11.7
    print_success "Python 3.11.7 installed"
else
    print_success "Python 3.11.7 already installed"
fi

pyenv global 3.11.7
print_success "Python 3.11.7 set as global"

# Install PostgreSQL
echo ""
print_info "Checking PostgreSQL..."
if ! brew list postgresql@14 &> /dev/null; then
    print_info "Installing PostgreSQL 14..."
    brew install postgresql@14
    print_success "PostgreSQL 14 installed"
else
    print_success "PostgreSQL 14 already installed"
fi

# Start PostgreSQL
print_info "Starting PostgreSQL..."
brew services start postgresql@14
print_success "PostgreSQL started"

# Wait for PostgreSQL to be ready
sleep 3

# Create database and user
print_info "Setting up database..."
if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw fast_lead_dev; then
    createuser -s postgres 2>/dev/null || true
    createdb fast_lead_dev
    print_success "Database 'fast_lead_dev' created"
else
    print_success "Database already exists"
fi

# Install Redis
echo ""
print_info "Checking Redis..."
if ! brew list redis &> /dev/null; then
    print_info "Installing Redis..."
    brew install redis
    print_success "Redis installed"
else
    print_success "Redis already installed"
fi

# Start Redis
print_info "Starting Redis..."
brew services start redis
print_success "Redis started"

# Wait for Redis to be ready
sleep 2

# Test Redis
if redis-cli ping | grep -q "PONG"; then
    print_success "Redis is running"
else
    print_error "Redis failed to start"
fi

# Install nvm
echo ""
print_info "Checking nvm..."
if [ ! -d "$HOME/.nvm" ]; then
    print_info "Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

    print_success "nvm installed"
else
    print_success "nvm already installed"
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

# Install Node.js 20 LTS
print_info "Checking Node.js..."
if ! nvm list | grep -q "v20"; then
    print_info "Installing Node.js 20 LTS..."
    nvm install 20
    nvm use 20
    nvm alias default 20
    print_success "Node.js 20 LTS installed"
else
    print_success "Node.js 20 already installed"
    nvm use 20
fi

# Setup Backend
echo ""
print_info "Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate venv and install dependencies
print_info "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null
pip install -r requirements-dev.txt > /dev/null
print_success "Python dependencies installed"

cd ..

# Create .env file
echo ""
print_info "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env

    # Generate SECRET_KEY
    SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

    # Update .env with actual values
    sed -i '' "s|DATABASE_URL=.*|DATABASE_URL=postgresql://postgres@localhost:5432/fast_lead_dev|" .env
    sed -i '' "s|REDIS_URL=.*|REDIS_URL=redis://localhost:6379/0|" .env
    sed -i '' "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" .env

    print_success ".env file created"
else
    print_success ".env file already exists"
fi

# Setup Frontend Dashboard
echo ""
print_info "Setting up Frontend Dashboard..."
cd frontend/dashboard

if [ ! -d "node_modules" ]; then
    print_info "Installing npm dependencies..."
    npm install > /dev/null 2>&1
    print_success "npm dependencies installed"
else
    print_success "npm dependencies already installed"
fi

# Create .env.local
if [ ! -f ".env.local" ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    print_success ".env.local created"
else
    print_success ".env.local already exists"
fi

cd ../..

# Setup Frontend Marketing
echo ""
print_info "Setting up Frontend Marketing..."
cd frontend/marketing

if [ ! -d "node_modules" ]; then
    print_info "Installing npm dependencies..."
    npm install > /dev/null 2>&1
    print_success "npm dependencies installed"
else
    print_success "npm dependencies already installed"
fi

# Create .env.local
if [ ! -f ".env.local" ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    print_success ".env.local created"
else
    print_success ".env.local already exists"
fi

cd ../..

# Setup Widget
echo ""
print_info "Setting up Widget..."
cd frontend/widget

if [ ! -d "node_modules" ]; then
    print_info "Installing npm dependencies..."
    npm install > /dev/null 2>&1
    print_success "npm dependencies installed"
else
    print_success "npm dependencies already installed"
fi

# Create .env
if [ ! -f ".env" ]; then
    echo "VITE_API_URL=http://localhost:8000" > .env
    print_success ".env created"
else
    print_success ".env already exists"
fi

cd ../..

# Final summary
echo ""
echo "======================================"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "======================================"
echo ""
echo "Services running:"
echo "  • PostgreSQL: localhost:5432"
echo "  • Redis: localhost:6379"
echo ""
echo "Next steps:"
echo "  1. Run database migrations:"
echo "     cd backend && source venv/bin/activate && alembic upgrade head"
echo ""
echo "  2. Start backend (in terminal 1):"
echo "     cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "  3. Start dashboard (in terminal 2):"
echo "     cd frontend/dashboard && npm run dev"
echo ""
echo "  4. Start marketing site (in terminal 3):"
echo "     cd frontend/marketing && npm run dev"
echo ""
echo "  5. Start widget (in terminal 4):"
echo "     cd frontend/widget && npm run dev"
echo ""
echo "  6. Open in browser:"
echo "     • API: http://localhost:8000/docs"
echo "     • Dashboard: http://localhost:3000"
echo "     • Marketing: http://localhost:3001"
echo "     • Widget: http://localhost:5173"
echo ""
echo "For more details, see: docs/setup-mac.md"
echo ""
