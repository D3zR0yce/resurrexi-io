# resurrexi.io

**Resurrexi Labs** main research site - publications, technical work, and autonomous compute access.

## Structure

```
resurrexi-io/
├── templates/          # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── publications.html
│   ├── technical-work.html
│   ├── about.html
│   └── compute.html
├── content/            # Markdown content
│   ├── publications/   # Research papers
│   └── technical-work/ # Technical projects
├── static/             # Static assets
│   ├── css/
│   ├── images/
│   └── papers/         # Downloadable PDFs
├── k8s/               # Kubernetes manifests
├── build.py           # Static site generator
├── app.py             # Flask backend
└── deploy.sh          # Deployment script
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Build static site
python3 build.py

# Run Flask dev server
python3 app.py

# Access at http://localhost:5000
```

## Deployment

### Manual Deployment (rsync)

```bash
./deploy.sh
```

Syncs `public/` directory to SudoSenpai:/mnt/storage/resurrexi-io/

### Kubernetes Deployment

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl -n resurrexi-io get pods,svc

# Access via NodePort
curl http://192.168.1.98:30801
```

### Docker Build

```bash
# Build image
docker build -t resurrexi-io:latest .

# Run locally
docker run -p 5000:5000 resurrexi-io:latest
```

## Content Management

### Adding Publications

Create markdown file in `content/publications/`:

```markdown
---
title: "Paper Title"
authors: "Author Name"
date: "Month Year"
venue: "Conference/Journal"
doi: "10.xxxx/xxxxx"
pdf: "/static/papers/filename.pdf"
github: "https://github.com/org/repo"
abstract: "Brief abstract..."
---

## Section 1
Content here...
```

Copy PDF to `static/papers/`.

### Adding Technical Work

Create markdown file in `content/technical-work/`:

```markdown
---
title: "Project Title"
category: "Offensive Security" | "Infrastructure Engineering" | "Experimental Systems"
date: "Month Year"
github: "https://github.com/resurrexio/repo"
description: "Brief description..."
tags: ["tag1", "tag2"]
---

## Overview
Project details...
```

### Rebuild

```bash
python3 build.py
./deploy.sh
```

## Form Submissions

Compute interest forms saved to `submissions/` directory as JSON:

```json
{
  "name": "Researcher Name",
  "email": "email@example.com",
  "institution": "University",
  "research_area": "ai-ml",
  "project_description": "...",
  "timeline": "asap",
  "open_access": true,
  "reproducible": true,
  "submitted_at": "2025-11-24T16:00:00",
  "ip_address": "192.168.1.X"
}
```

## Architecture

- **Static site generation:** Jinja2 + Markdown → HTML
- **Backend:** Flask (form handling, static file serving)
- **Deployment:** K8s with 2 replicas, NodePort 30801
- **Storage:** PersistentVolumes on SudoSenpai (pwnie-storage)
- **Access:** Cloudflare Tunnel for public HTTPS

## Tech Stack

- Python 3.13
- Flask 3.0
- Jinja2 (templating)
- Markdown (content)
- Pico CSS (styling)
- Kubernetes (deployment)

## Site Structure

- `/` - Homepage (research overview)
- `/publications.html` - Published papers with PDFs
- `/work.html` - Technical projects and write-ups
- `/compute.html` - Autonomous research agent info + interest form
- `/about.html` - Lab info, PI bio, infrastructure
- `/api/compute-interest` - Form submission endpoint

## Brand Identity

- **resurrexi.io** - Main research site (this)
- **resurrexi.dev** - Technical documentation, lab notes, sessions
- **farzulla.org** - Academic research portfolio
- **farzulla.com** - Personal site

## License

- **Content:** CC-BY-4.0
- **Code:** MIT
