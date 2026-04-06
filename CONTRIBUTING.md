# Contributing to AI Cultural Coordination Platform

We welcome contributions to the AI Cultural Coordination Platform! This guide will help you get started with contributing to the project.

## 📝 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Issue Guidelines](#issue-guidelines)

## 🤝 Code of Conduct

This project follows a Code of Conduct to ensure a welcoming and inclusive environment. Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) before contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ for backend development
- Node.js 18+ for frontend development
- Git for version control
- Docker for containerized development
- GitHub CLI for GitHub integration

### Setup Development Environment

1. **Fork the Repository**
   ```bash
   gh repo fork ava-agent/awesome-ai-ideas
   git clone https://github.com/YOUR_USERNAME/awesome-ai-ideas.git
   cd awesome-ai-ideas/prs
   ```

2. **Set Up Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Set Up Frontend**
   ```bash
   cd ../frontend
   npm install
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Install Pre-commit Hooks**
   ```bash
   cd backend
   pre-commit install
   cd ../frontend
   npm install --save-dev husky lint-staged
   npx husky install
   npx husky add .husky/pre-commit "npm run lint && npm run format"
   ```

## 🔄 Development Workflow

### 1. Choose Your Contribution Type

#### Bug Fix
- Look for issues with the `bug` label
- Ensure you understand the problem and expected behavior
- Write a test that reproduces the issue
- Fix the bug and verify the test passes

#### Feature Request
- Look for issues with the `feature` label
- Discuss the feature in the issue comments
- Create a detailed implementation plan
- Get consensus from maintainers

#### Documentation
- Look for issues with the `documentation` label
- Ensure documentation is accurate and up-to-date
- Add examples where helpful
- Update both README and inline documentation

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for a bug fix
git checkout -b fix/your-bug-description

# Or for documentation
git checkout -b docs/your-docs-change
```

### 3. Make Your Changes

#### Backend Changes (Python)
```python
# Follow Python coding standards
def analyze_cultural_context(text: str, context: str) -> dict:
    """
    Analyze cultural context in text.
    
    Args:
        text: The text to analyze
        context: The context of the communication
        
    Returns:
        Dict containing cultural analysis results
    """
    # Implementation here
    pass
```

#### Frontend Changes (React/TypeScript)
```typescript
// Follow React and TypeScript standards
const CulturalAnalyzer: React.FC<CulturalAnalyzerProps> = ({ text }) => {
  const [analysis, setAnalysis] = useState<CulturalAnalysis | null>(null);
  
  useEffect(() => {
    // Component logic here
  }, [text]);
  
  return (
    <div className="cultural-analyzer">
      {/* JSX here */}
    </div>
  );
};
```

### 4. Write Tests

#### Backend Tests
```python
# tests/test_analyzer.py
import pytest
from app.services.cultural_analyzer import CulturalAnalyzer

def test_cultural_analysis():
    analyzer = CulturalAnalyzer()
    result = analyzer.analyze("Hello team!", "meeting")
    
    assert result is not None
    assert "cultural_dimensions" in result
    assert "suggestions" in result
```

#### Frontend Tests
```typescript
// src/components/__tests__/CulturalAnalyzer.test.tsx
import { render, screen } from '@testing-library/react';
import CulturalAnalyzer from '../CulturalAnalyzer';

test('renders cultural analyzer', () => {
  render(<CulturalAnalyzer text="Hello team!" />);
  expect(screen.getByText('Cultural Analysis')).toBeInTheDocument();
});
```

### 5. Run Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
npm test

# Integration tests
npm run test:integration
```

### 6. Check Code Quality

```bash
# Backend linting and formatting
cd backend
flake8 app/
black app/
mypy app/

# Frontend linting and formatting
cd frontend
npm run lint
npm run format
npm run type-check
```

## 🔄 Pull Request Process

### 1. Create Pull Request

```bash
# Push your changes
git push origin your-branch-name

# Create pull request
gh pr create --title "Your descriptive title" --body "Your detailed description"
```

### 2. Pull Request Template

```markdown
## Description
Brief description of what your PR does

## Changes Made
- [ ] Feature addition
- [ ] Bug fix
- [ ] Documentation update
- [ ] Code refactor

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Breaking Changes
- [ ] Yes
- [ ] No

## Additional Notes
Any additional context or information
```

### 3. Review Process

1. **Automated Checks**: All tests and linting must pass
2. **Code Review**: Maintainers will review your code
3. **Discussion**: Address any feedback comments
4. **Approval**: Get approval from at least one maintainer
5. **Merge**: Maintainer will merge the PR

## 📏 Coding Standards

### Python Backend

#### PEP 8 Compliance
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use meaningful variable and function names
- Type hints required for all function signatures

#### Code Structure
```python
# File structure
app/
├── __init__.py
├── main.py              # Application entry point
├── api/                 # API endpoints
│   ├── __init__.py
│   ├── routes.py
│   └── dependencies.py
├── core/                # Business logic
│   ├── __init__.py
│   ├── cultural_analyzer.py
│   └── services.py
├── models/              # Data models
│   ├── __init__.py
│   ├── schemas.py
│   └── database.py
└── utils/               # Utilities
    ├── __init__.py
    ├── helpers.py
    └── logging.py
```

#### Error Handling
```python
from fastapi import HTTPException, status

def analyze_text(text: str) -> dict:
    if not text or len(text.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty"
        )
    
    # Rest of implementation
    pass
```

### Frontend Standards

#### React/TypeScript
- Use functional components with hooks
- TypeScript types required
- Follow React patterns and best practices
- Use CSS modules or Tailwind CSS for styling

#### File Structure
```typescript
src/
├── components/          # Reusable components
│   ├── CulturalAnalyzer/
│   │   ├── CulturalAnalyzer.tsx
│   │   ├── CulturalAnalyzer.test.tsx
│   │   └── index.ts
│   └── shared/
│       ├── Button/
│       └── Modal/
├── pages/              # Page components
│   ├── Dashboard.tsx
│   └── Settings.tsx
├── services/           # API services
│   ├── culturalApi.ts
│   └── authApi.ts
├── types/              # TypeScript types
│   ├── cultural.ts
│   └── api.ts
└── utils/              # Utilities
    ├── helpers.ts
    └── constants.ts
```

#### Component Patterns
```typescript
import { useState, useEffect } from 'react';
import { CulturalAnalysis } from '../types/cultural';

interface CulturalAnalyzerProps {
  text: string;
  onAnalysis?: (analysis: CulturalAnalysis) => void;
}

export const CulturalAnalyzer: React.FC<CulturalAnalyzerProps> = ({ text, onAnalysis }) => {
  const [analysis, setAnalysis] = useState<CulturalAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const analyzeText = async () => {
      if (!text) return;
      
      setLoading(true);
      setError(null);
      
      try {
        const result = await culturalApi.analyze(text);
        setAnalysis(result);
        onAnalysis?.(result);
      } catch (err) {
        setError('Failed to analyze text');
      } finally {
        setLoading(false);
      }
    };

    analyzeText();
  }, [text, onAnalysis]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="cultural-analyzer">
      {/* Component JSX */}
    </div>
  );
};
```

## 🧪 Testing Guidelines

### Backend Testing

#### Unit Tests
```python
# tests/unit/test_cultural_analyzer.py
import pytest
from unittest.mock import Mock, patch
from app.services.cultural_analyzer import CulturalAnalyzer

@pytest.fixture
def analyzer():
    return CulturalAnalyzer()

def test_analyzer_initialization():
    analyzer = CulturalAnalyzer()
    assert analyzer is not None

@patch('app.services.cultural_analyzer.CulturalAnalyzer._call_ai_api')
def test_analyze_cultural_context(mock_call_api, analyzer):
    mock_call_api.return_value = {
        'dimensions': {'individualism': 0.8},
        'suggestions': ['Consider more collective language']
    }
    
    result = analyzer.analyze("I think this is the best approach", "meeting")
    
    assert result['dimensions']['individualism'] == 0.8
    assert 'suggestions' in result
```

#### Integration Tests
```python
# tests/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_endpoint():
    response = client.post(
        "/api/analyze",
        json={"text": "Hello team", "context": "meeting"}
    )
    assert response.status_code == 200
    assert "dimensions" in response.json()
```

### Frontend Testing

#### Component Testing
```typescript
// src/components/__tests__/CulturalAnalyzer.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import CulturalAnalyzer from '../CulturalAnalyzer';

test('renders analyzer with input', () => {
  render(<CulturalAnalyzer />);
  expect(screen.getByPlaceholderText('Enter text to analyze')).toBeInTheDocument();
});

test('calls analysis on text input', () => {
  const mockOnAnalysis = jest.fn();
  render(<CulturalAnalyzer onAnalysis={mockOnAnalysis} />);
  
  const input = screen.getByPlaceholderText('Enter text to analyze');
  fireEvent.change(input, { target: { value: 'Hello team' } });
  
  expect(mockOnAnalysis).toHaveBeenCalled();
});
```

#### Testing Utilities
```typescript
// src/test-utils/index.tsx
import { render as rtlRender } from '@testing-library/react';
import { ThemeProvider } from '../contexts/ThemeContext';

export function render(ui: React.ReactElement, options?: any) {
  return rtlRender(
    <ThemeProvider>
      {ui}
    </ThemeProvider>,
    options
  );
}
```

## 📚 Documentation Standards

### Code Documentation

#### Python Docstrings
```python
def analyze_cultural_text(
    text: str, 
    context: str, 
    target_culture: str = None
) -> CulturalAnalysis:
    """
    Analyze cultural context in text with optional target culture.
    
    Args:
        text: The text to analyze for cultural content
        context: Communication context (e.g., 'meeting', 'email', 'chat')
        target_culture: Optional target culture for comparison
        
    Returns:
        CulturalAnalysis: Object containing cultural dimensions and suggestions
        
    Raises:
        ValueError: If text is empty or invalid
        CulturalAnalysisError: If analysis fails
    """
    pass
```

#### JSDoc for TypeScript
```typescript
/**
 * Analyzes cultural context in text input
 * @param text - The text to analyze
 * @param context - Communication context (meeting, email, chat)
 * @param options - Additional analysis options
 * @returns Promise<CulturalAnalysis> - Analysis results
 * @throws CulturalAnalysisError
 */
export async function analyzeCulturalText(
  text: string,
  context: string,
  options: AnalysisOptions = {}
): Promise<CulturalAnalysis> {
  // Implementation
}
```

### README Documentation

#### Feature Documentation
```markdown
## Feature: Cultural Context Analysis

The cultural context analysis feature examines text for cultural dimensions and provides suggestions for culturally appropriate communication.

### Usage

```typescript
import { analyzeCulturalText } from '@/services/culturalApi';

const analysis = await analyzeCulturalText(
  "I think this approach is best",
  "meeting",
  { targetCulture: "collectivist" }
);
```

### Output

```json
{
  "dimensions": {
    "individualism": 0.8,
    "powerDistance": 0.3,
    "uncertaintyAvoidance": 0.6
  },
  "suggestions": [
    "Consider using more inclusive language",
    "Acknowledge team contributions"
  ]
}
```
```

## 🐛 Issue Guidelines

### Creating Issues

#### Bug Reports
```markdown
## Bug Report

**Environment:**
- OS: [e.g., Ubuntu 20.04]
- Browser: [e.g., Chrome 91]
- Version: [e.g., v1.0.0]

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior:**
[What you expected to happen]

**Actual Behavior:**
[What actually happened]

**Error Messages:**
```
[Error message stack trace]
```

**Additional Context:**
[Any additional context that might be helpful]
```

#### Feature Requests
```markdown
## Feature Request

**Problem:**
[Describe the problem or need you're trying to solve]

**Proposed Solution:**
[Describe your proposed solution]

**Alternatives Considered:**
[Describe alternatives you've considered]

**Additional Context:**
[Any additional context, screenshots, or examples]
```

### Issue Labels

- `bug`: Bug report
- `feature`: Feature request
- `documentation`: Documentation needed
- `enhancement`: Enhancement to existing feature
- `question`: Question about the project
- `help wanted`: Help needed from community
- `good first issue`: Good for first-time contributors
- `needs discussion`: Requires maintainer discussion

## 🏆 Contribution Levels

### Contributor
- Made at least 1 valid contribution
- Follows contribution guidelines
- Participates in discussions

### Active Contributor
- Regular contributions (monthly)
- Helps review PRs
- Mentors new contributors

### Core Contributor
- Major feature contributions
- High-quality code reviews
- Helps set technical direction
- Represents the project in community

## 📞 Getting Help

### Community Resources

- **GitHub Discussions**: [Project Discussions](../../discussions)
- **Issues**: [GitHub Issues](../../issues)
- **Discord**: [Project Discord](../../discord-invite)

### Maintainers

- **Lead Maintainer**: [@maintainer1](../../maintainer1)
- **Technical Lead**: [@maintainer2](../../maintainer2)
- **Documentation Lead**: [@maintainer3](../../maintainer3)

### Code of Conduct

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

## 🎯 Recognition

We recognize contributors in several ways:

- **Contributor of the Month**: Featured in project newsletter
- **Hall of Fame**: Outstanding contributors listed in README
- **Special Badges**: Recognition for exceptional contributions

---

Thank you for contributing to the AI Cultural Coordination Platform! 🎉