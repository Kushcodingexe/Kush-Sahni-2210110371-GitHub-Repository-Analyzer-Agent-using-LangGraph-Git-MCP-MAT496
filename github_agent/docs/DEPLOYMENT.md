# Deployment Guide

Complete guide for deploying the GitHub Repository Analyzer Agent in production.

---

## Table of Contents

- [Local Installation](#local-installation)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Checklist](#production-checklist)
- [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Installation

### Method 1: Install from Source

```bash
# Clone repository
git clone <repository-url>
cd github_agent

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Verify installation
github-agent config
```

### Method 2: Install from PyPI (Future)

```bash
# Install package
pip install github-repository-analyzer

# Create .env file
cat > .env << EOF
GITHUB_TOKEN=your_token_here
TAVILY_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DEFAULT_MODEL=openai:gpt-4o-mini
EOF

# Run
github-agent interactive
```

---

## Docker Deployment

### Quick Start with Docker

```bash
# Build image
docker build -t github-agent .

# Run with environment variables
docker run -it --rm \
  -e GITHUB_TOKEN=your_token \
  -e TAVILY_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  github-agent
```

### Using Docker Compose (Recommended)

```bash
# Ensure .env file exists with all API keys
cp .env.example .env
# Edit .env with your credentials

# Start container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

### Docker Commands

```bash
# Build image
docker build -t github-agent:latest .

# Run interactive mode
docker run -it --rm --env-file .env github-agent

# Run specific command
docker run --rm --env-file .env github-agent \
  github-agent ask openai/openai-python "What is this repo?"

# Run with volume for data persistence
docker run -it --rm \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  github-agent
```

---

## Cloud Deployment

### AWS Deployment

#### Option 1: AWS ECS (Elastic Container Service)

```bash
# 1. Build and push to ECR
aws ecr create-repository --repository-name github-agent
docker tag github-agent:latest <account-id>.dkr.ecr.<region>.amazonaws.com/github-agent:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/github-agent:latest

# 2. Create ECS task definition
# 3. Create ECS service
# 4. Configure environment variables in task definition
```

#### Option 2: AWS Lambda (For API mode)

```python
# lambda_handler.py
from src.main import ask_about_repository

def lambda_handler(event, context):
    repo = event['repo']
    question = event['question']
    result = ask_about_repository(repo, question)
    return {
        'statusCode': 200,
        'body': str(result)
    }
```

### Google Cloud Platform

#### Cloud Run Deployment

```bash
# 1. Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/github-agent

# 2. Deploy to Cloud Run
gcloud run deploy github-agent \
  --image gcr.io/PROJECT_ID/github-agent \
  --platform managed \
  --set-env-vars GITHUB_TOKEN=xxx,TAVILY_API_KEY=xxx \
  --allow-unauthenticated
```

### Azure Deployment

#### Azure Container Instances

```bash
# Create resource group
az group create --name github-agent-rg --location eastus

# Deploy container
az container create \
  --resource-group github-agent-rg \
  --name github-agent \
  --image github-agent:latest \
  --cpu 1 --memory 2 \
  --environment-variables \
    GITHUB_TOKEN=xxx \
    TAVILY_API_KEY=xxx \
    OPENAI_API_KEY=xxx
```

---

## Production Checklist

### Pre-Deployment

- [ ] All API keys configured in `.env`
- [ ] API keys tested and valid
- [ ] Model selection confirmed (`DEFAULT_MODEL`)
- [ ] Resource limits configured appropriately
- [ ] Docker image built and tested locally
- [ ] Security review completed

### Security

- [ ] `.env` file is git ignored
- [ ] API keys stored securely (use secrets manager)
- [ ] No hardcoded credentials in code
- [ ] Container runs as non-root user
- [ ] Network policies configured (if applicable)
- [ ] HTTPS enabled (for API mode)

### Configuration

```bash
# Recommended production settings
DEFAULT_MODEL=openai:gpt-4o-mini       # Cost-effective
MAX_CONCURRENT_RESEARCH_UNITS=2        # Conservative
MAX_RESEARCHER_ITERATIONS=2            # Limit depth
MAX_SEARCH_RESULTS=3                   # Limit searches

# For high-quality analysis
DEFAULT_MODEL=openai:gpt-4o            # More capable
MAX_CONCURRENT_RESEARCH_UNITS=3
MAX_RESEARCHER_ITERATIONS=3
MAX_SEARCH_RESULTS=5
```

### Resource Requirements

**Minimum:**
- CPU: 0.5 cores
- Memory: 512MB
- Disk: 1GB

**Recommended:**
- CPU: 1 core
- Memory: 2GB
- Disk: 5GB

**For Heavy Usage:**
- CPU: 2 cores
- Memory: 4GB
- Disk: 10GB

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check if agent is responding
docker exec github-agent github-agent config

# Check logs
docker logs github-agent --tail 100

# Check resource usage
docker stats github-agent
```

### Logging

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Cost Monitoring

Monitor API usage:
- **GitHub API:** Check rate limits in response headers
- **Tavily API:** Track search count (free tier: 1000/month)
- **OpenAI/Anthropic:** Monitor token usage in dashboard

### Troubleshooting

**Container won't start:**
```bash
docker logs github-agent
# Check for missing environment variables
```

**API rate limits:**
```bash
# Reduce concurrent operations
MAX_CONCURRENT_RESEARCH_UNITS=1
MAX_SEARCH_RESULTS=2
```

**Out of memory:**
```bash
# Increase memory limit in docker-compose.yml
memory: 4G
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | Yes | - | GitHub personal access token |
| `TAVILY_API_KEY` | Yes | - | Tavily search API key |
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key |
| `ANTHROPIC_API_KEY` | Yes* | - | Anthropic API key |
| `DEFAULT_MODEL` | No | `openai:gpt-4o-mini` | LLM model to use |
| `MAX_CONCURRENT_RESEARCH_UNITS` | No | 3 | Max parallel sub-agents |
| `MAX_RESEARCHER_ITERATIONS` | No | 3 | Max research iterations |
| `MAX_SEARCH_RESULTS` | No | 3 | Max search results |

*One of OpenAI or Anthropic API key is required

---

## Support

For issues or questions:
- Check [GETTING_STARTED.md](GETTING_STARTED.md)
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [API.md](API.md) for tool reference
- Open an issue on GitHub

---

## Next Steps

After deployment:
1. Test with a simple query
2. Monitor logs and resource usage
3. Adjust configuration as needed
4. Set up automated backups (if needed)
5. Configure monitoring/alerting

**Your agent is now ready for production use!** 🚀
