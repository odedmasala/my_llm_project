# 🧠 IntelliQuery

**AI-Powered Question Answering API with Context Understanding**

IntelliQuery is a sophisticated question-answering application that leverages the power of Hugging Face Transformers to provide intelligent answers based on contextual information. Built with FastAPI, PostgreSQL, and modern Python tooling, it offers both a RESTful API and a user-friendly web interface.

## ✨ Features

- **🤖 Advanced NLP**: Powered by DistilBERT for accurate question answering
- **📊 Context-Aware**: Provides answers based on user-provided context
- **💾 Persistent Storage**: Automatically saves all Q&A interactions to PostgreSQL
- **🌐 Web Interface**: Clean, responsive web UI for easy interaction
- **🚀 Fast API**: High-performance asynchronous API endpoints
- **🐳 Docker Ready**: Fully containerized for easy deployment
- **☸️ Kubernetes Support**: Production-ready with Kubernetes manifests
- **🔧 Developer Tools**: Comprehensive testing, linting, and pre-commit hooks

## 🏗️ Architecture

- **Backend**: FastAPI with async support
- **AI Model**: DistilBERT (distilbert-base-uncased-distilled-squad)
- **Database**: PostgreSQL with async SQLAlchemy
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Development**: Tilt for local Kubernetes development
- **Containerization**: Docker with multi-stage builds

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- Docker & Docker Compose (for containerized setup)
- Kubernetes & Tilt (for advanced development)

### Method 1: Local Development with Poetry

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Install dependencies**

   ```bash
   poetry install
   ```

3. **Set up environment variables**

   ```bash
   # Create a .env file
   echo "DATABASE_URL=sqlite+aiosqlite:///./test.db" > .env
   ```

4. **Run the application**

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

5. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Interactive API: http://localhost:8000/redoc

### Method 2: Docker Development

1. **Build and run with Docker**

   ```bash
   docker build -t intelliquery .
   docker run -p 8000:8000 -e DATABASE_URL="sqlite+aiosqlite:///./test.db" intelliquery
   ```

2. **Access the application**
   - Web Interface: http://localhost:8000

### Method 3: Kubernetes with Tilt (Recommended for Development)

1. **Prerequisites**

   ```bash
   # Install Tilt
   curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash

   # Ensure you have a local Kubernetes cluster (Docker Desktop, minikube, etc.)
   ```

2. **Start the development environment**

   ```bash
   tilt up
   ```

3. **Access the application**
   - Web Interface: http://localhost:8000
   - Tilt Dashboard: http://localhost:10350

## 📖 Usage

### Web Interface

1. Navigate to http://localhost:8000
2. Enter your question in the "Question" field
3. Provide relevant context in the "Context" textarea
4. Click "Ask" to get your answer

### API Endpoints

#### Ask a Question

```bash
GET /ask?question=<your-question>&context=<your-context>
```

**Example:**

```bash
curl "http://localhost:8000/ask?question=What%20is%20the%20capital%20of%20France?&context=Paris%20is%20the%20capital%20and%20largest%20city%20of%20France."
```

**Response:**

```json
{
  "answer": "Paris"
}
```

#### Health Check

```bash
GET /
```

Returns the web interface.

## 🛠️ Development

### Setting up the development environment

1. **Install development dependencies**

   ```bash
   poetry install --with dev
   ```

2. **Set up pre-commit hooks**

   ```bash
   poetry run pre-commit install
   ```

3. **Run tests**

   ```bash
   poetry run pytest
   ```

4. **Code formatting and linting**

   ```bash
   # Format code
   poetry run black .
   poetry run isort .

   # Lint code
   poetry run flake8 .
   ```

### Environment Variables

| Variable       | Description                | Default  |
| -------------- | -------------------------- | -------- |
| `DATABASE_URL` | Database connection string | Required |

**Example configurations:**

- SQLite: `sqlite+aiosqlite:///./test.db`
- PostgreSQL: `postgresql+asyncpg://user:pass@localhost/dbname`

### Database Schema

The application uses a simple schema with one table:

```sql
CREATE TABLE qa_records (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    context TEXT NOT NULL,
    answer TEXT NOT NULL
);
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app

# Run specific test file
poetry run pytest tests/test_main.py
```

## 🚢 Deployment

### Production Deployment

1. **Build the Docker image**

   ```bash
   docker build -t intelliquery:latest .
   ```

2. **Deploy to your preferred platform**
   - Use the provided Kubernetes manifests in `.tilt/k8s/`
   - Deploy to cloud providers (AWS ECS, Google Cloud Run, etc.)
   - Use Docker Compose for simple deployments

### Environment Configuration

For production, ensure you set:

- `DATABASE_URL` to your production database
- Proper resource limits in Kubernetes
- Security configurations (HTTPS, authentication, etc.)

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── db.py               # Database configuration
│   └── static/
│       └── index.html      # Web interface
├── tests/
│   ├── __init__.py
│   └── test_main.py        # Test suite
├── .tilt/
│   ├── Tiltfile            # Tilt configuration
│   ├── development.env     # Development environment
│   └── k8s/               # Kubernetes manifests
├── .github/
│   └── workflows/
│       └── python-app.yml  # CI/CD pipeline
├── Dockerfile              # Container definition
├── Tiltfile               # Tilt entry point
├── pyproject.toml         # Poetry configuration
├── .pre-commit-config.yaml # Pre-commit hooks
└── README.md              # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code passes all tests and follows the project's coding standards.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/) for the powerful NLP models
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [DistilBERT](https://huggingface.co/distilbert-base-uncased-distilled-squad) for the question-answering model

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the existing [Issues](../../issues)
2. Create a new issue with detailed information
3. Contact the maintainer: Oded Masala (odedmasala6@gmail.com)

---

**Made with ❤️ by Oded Masala**
