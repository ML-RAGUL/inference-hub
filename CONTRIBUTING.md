# Contributing to InferenceHub

First off, thank you for considering contributing to InferenceHub! 🎉

## How Can I Contribute?

### 🐛 Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/inference-hub/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### 💡 Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the feature and its use case
3. Explain why it would be useful

### 🔧 Pull Requests

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test your changes
5. Commit: `git commit -m 'Add some feature'`
6. Push: `git push origin feature/your-feature`
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/inference-hub.git
cd inference-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run with Docker
docker-compose up --build
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions

## Commit Messages

- Use present tense: "Add feature" not "Added feature"
- Be descriptive but concise
- Reference issues when applicable: "Fix #123"

## Questions?

Feel free to open an issue with the `question` label!
