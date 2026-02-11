# Contributing to Jellyfin Trilingual Subtitle Automation

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please include:
- A clear description of the feature
- Why it would be useful
- Possible implementation approach (if you have ideas)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages (`git commit -m 'Add: feature description'`)
6. Push to your fork (`git push origin feature/YourFeature`)
7. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guidelines
- Write clear, descriptive variable names
- Include docstrings for functions
- Add comments for complex logic
- Keep functions focused and single-purpose

### Testing

- Test your changes with real subtitle files
- Verify compatibility with Jellyfin
- Check that pinyin generation works correctly
- Ensure timestamp matching is accurate

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/jellyfin-trilingual-subtitles.git
cd jellyfin-trilingual-subtitles

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements.txt
```

## Questions?

Feel free to open an issue for any questions about contributing!
