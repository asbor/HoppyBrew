<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/asbor/HoppyBrew">
    <img src="documents/images/logo.png" alt="Logo" width="300">
  </a>

<h3 align="center">HoppyBrew</h3>

  <p align="center">
    A comprehensive self-hosted brewing management platform for homebrewers
    <br />
    Track recipes • Manage inventory • Monitor batches • Integrate with HomeAssistant
    <br />
    <br />
    <a href="wiki/Home.md"><strong>📚 Explore the Wiki »</strong></a>
    <br />
    <br />
    <a href="#quick-start">🚀 Quick Start</a>
    ·
    <a href="https://github.com/asbor/HoppyBrew/issues">🐛 Report Bug</a>
    ·
    <a href="https://github.com/asbor/HoppyBrew/issues">💡 Request Feature</a>
    ·
    <a href="API_DOCUMENTATION.md">📖 API Docs</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>📑 Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#architecture-overview">Architecture Overview</a></li>
    <li><a href="#key-features">Key Features</a></li>
    <li><a href="#quick-start">Quick Start (5 Minutes)</a></li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#documentation">Documentation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

---

## About The Project

<img src="documents/images/Brewmaster.webp" width="500" alt="HoppyBrew">

HoppyBrew is a comprehensive, self-hosted brewing management platform designed for homebrewers who want complete control over their brewing data and processes. Born from a Software Engineering course project at the International University of Applied Sciences Bad Honnef - Bonn, and inspired by Brewfather, HoppyBrew offers a powerful alternative for brewers who prefer self-hosting over subscription services.

### Why HoppyBrew?

- 🏠 **Complete Data Ownership**: Host on your own infrastructure
- 🆓 **No Subscriptions**: Free and open-source forever
- 🔧 **Fully Customizable**: Adapt it to your brewing workflow
- 🏡 **HomeAssistant Integration**: Monitor your brews from your smart home dashboard
- 🐳 **Easy Deployment**: Docker-based setup in minutes

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Architecture Overview

HoppyBrew follows a modern, cloud-native architecture with clear separation of concerns:

```
┌─────────────────┐
│   Web Browser   │
│  (React + Vue)  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐      ┌──────────────┐
│  Nuxt 3 + SPA   │◄────►│  FastAPI     │
│  (Frontend)     │      │  (Backend)   │
└─────────────────┘      └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  PostgreSQL  │
                         │  (Database)  │
                         └──────────────┘
```

**Key Components:**
- **Frontend**: Nuxt 3 with shadcn-vue for modern, reactive UI
- **Backend**: FastAPI with Pydantic for type-safe REST API
- **Database**: PostgreSQL for reliable data persistence
- **Integrations**: HomeAssistant REST sensors, ISpindel support
- **Deployment**: Docker Compose for easy orchestration

📖 **Learn More**: See [Architecture Documentation](wiki/Architecture.md) for detailed system design

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Key Features

- 🍺 **Recipe Management**: Create, edit, and manage brewing recipes
  - Import/export BeerXML format
  - Clone existing recipes
  - Calculate OG, FG, ABV, IBU, SRM
  
- 📊 **Batch Tracking**: Monitor batches through all production stages
  - Track fermentation with gravity readings
  - Record temperature and pH measurements
  - Manage brew day timeline
  
- 📦 **Inventory Management**: Track all ingredients
  - Real-time stock levels
  - Automatic deduction on batch creation
  - Low stock alerts
  
- 🏠 **HomeAssistant Integration**: Smart home monitoring
  - REST sensor endpoints
  - Real-time batch status
  - Temperature and gravity monitoring
  
- �� **Brewing Calculators**: Common brewing calculations
  - Strike water temperature
  - ABV calculation
  - Priming sugar amounts
  - Yeast starter calculations
  
- 🎯 **Style Guidelines**: BJCP style database
  - Complete style categories
  - Target ranges for OG, FG, IBU, SRM

- 🌡️ **Equipment & Water Profiles**: Equipment and chemistry management
  - Equipment efficiency tracking
  - Boil-off rate calculations
  - Water profile management

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Quick Start

Get HoppyBrew running in under 5 minutes using Docker Compose:

### Prerequisites
- Docker & Docker Compose installed ([Get Docker](https://docs.docker.com/get-docker/))
- 2GB RAM minimum, 4GB recommended
- Ports 8000 (backend) and 3000 (frontend) available

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/asbor/HoppyBrew.git
   cd HoppyBrew
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env if needed to change database credentials or ports
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the applications**
   - 🌐 Frontend: http://localhost:3000
   - 🔧 Backend API: http://localhost:8000
   - 📚 API Documentation: http://localhost:8000/docs

5. **Load sample data (optional)**
   ```bash
   docker exec hoppybrew-backend python /app/seeds/seed_sample_dataset.py
   ```

That's it! You now have a fully functional brewing management system. 

🆘 **Having issues?** Check the [Troubleshooting Guide](DEVELOPMENT_GUIDE.md#troubleshooting) or [open an issue](https://github.com/asbor/HoppyBrew/issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Tech Stack

### Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | [![Vue.js][Vue.js]][Vue-url] Nuxt 3 | 3.16.0+ | SPA framework with SSR support |
| **UI** | shadcn-vue | Latest | Accessible component library |
| **Backend** | [![FastAPI][FastAPI.org]][FastAPI-url] | Latest | High-performance Python API |
| **Validation** | [![pydantic][pydantic]][pydantic-url] | Latest | Type-safe data validation |
| **Server** | [![uvicorn][uvicorn]][uvicorn-url] | Latest | ASGI web server |
| **Database** | [![PostgreSQL][PostgreSQL.org]][PostgreSQL-url] | 16+ | Primary data store |
| **ORM** | [![sqlalchemy][sqlalchemy]][sqlalchemy-url] | 2.x | Database abstraction |
| **Caching** | [![Redis][Redis]][Redis-url] | Latest | Session & cache store |
| **Containers** | [![Docker.com][Docker.com]][Docker-url] | Latest | Application packaging |

### Development Tools

| Category | Tools |
|----------|-------|
| **IDE** | [![VsCode][VsCode]][VsCode-url] |
| **Documentation** | [![Markdown][Markdown]][Markdown-url] [![PlantUML][PlantUML]][PlantUML-url] |
| **Version Control** | [![Git-scm][Git-scm]][Git-scm-url] [![GitHub][GitHub]][GitHub-url] |
| **CI/CD** | GitHub Actions |
| **Code Quality** | Black, Prettier, ESLint |
| **Testing** | pytest, Vitest, Playwright |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Project Structure

```
HoppyBrew/
├── services/
│   ├── backend/       # FastAPI backend with database models
│   └── nuxt3-shadcn/  # Nuxt 3 frontend with shadcn-vue UI
├── documents/         # Project documentation
│   ├── docs/          # Architecture and design docs
│   └── images/        # Images and diagrams
├── wiki/              # GitHub wiki pages
├── alembic/           # Database migrations
├── seeds/             # Database seed scripts
├── tools/             # Utility tools and scripts
├── .github/           # GitHub workflows
├── docker-compose.yml # Docker orchestration
├── API_DOCUMENTATION.md        # Complete API reference
├── DEVELOPMENT_GUIDE.md        # Development setup guide
├── CONTRIBUTING.md             # Contribution guidelines
├── SECURITY.md                 # Security policy
├── README.md                   # This file
├── ROADMAP.md                  # Project roadmap
└── TODO.md                     # Task tracking
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Documentation

HoppyBrew has comprehensive documentation to help you get started:

### 📚 Core Documentation

- **[API Documentation](API_DOCUMENTATION.md)** - Complete REST API reference
  - All endpoints with examples
  - Request/response schemas
  - Error handling
  - Integration guides (HomeAssistant, Python, TypeScript)
  
- **[Development Guide](DEVELOPMENT_GUIDE.md)** - Local setup and development
  - Environment setup
  - Testing guide
  - Debugging procedures
  - Troubleshooting common issues
  
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
  - Code standards
  - Pull request process
  - Testing requirements
  
- **[Security Policy](SECURITY.md)** - Security information
  - Vulnerability reporting
  - Security updates
  - Current security status

### 🌐 Wiki Pages

The [GitHub Wiki](wiki/Home.md) contains detailed documentation:

- **[Home](wiki/Home.md)** - Wiki overview and quick links
- **[Architecture](wiki/Architecture.md)** - System architecture and design
- **[API Reference](wiki/API-Reference.md)** - Detailed API documentation
- **[Database Schema](wiki/Database-Schema.md)** - Database structure
- **[Development Guide](wiki/Development-Guide.md)** - Local development setup
- **[Deployment Guide](wiki/Deployment-Guide.md)** - Production deployment
- **[Frontend Guide](wiki/Frontend-Guide.md)** - Frontend architecture
- **[User Onboarding](wiki/User-Onboarding.md)** - Getting started guide
- **[Diagram Catalog](wiki/Diagram-Catalog.md)** - Architecture diagrams

### 🎯 Quick References

- **Interactive API Docs**: http://localhost:8000/docs (when running)
- **[Roadmap](ROADMAP.md)** - Project direction and milestones
- **[TODO](TODO.md)** - Current tasks and backlog
- **[Changelog](CHANGELOG.md)** - Version history

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Usage

### Running with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Local Development

**Backend:**
```bash
cd services/backend
source .venv/bin/activate
uvicorn main:app --reload
```

**Frontend:**
```bash
cd services/nuxt3-shadcn
yarn dev
```

### HomeAssistant Integration

Add to your `configuration.yaml`:

```yaml
sensor:
  - platform: rest
    name: "Brewery Status"
    resource: http://your-hoppybrew-host:8000/homeassistant/summary
    value_template: "{{ value_json.active_batches }}"
```

See [API Documentation](API_DOCUMENTATION.md#homeassistant-integration) for complete integration guide.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contributing

Contributions are what make the open source community amazing! Any contributions you make are **greatly appreciated**.

### How to Contribute

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Before Contributing

- Read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
- Check [open issues](https://github.com/asbor/HoppyBrew/issues)
- Review [ROADMAP.md](ROADMAP.md) for project direction
- Follow the [Development Guide](DEVELOPMENT_GUIDE.md) for setup

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full project roadmap.

**Current Focus Areas:**
- ✅ Infrastructure improvements (CI/CD, security)
- ✅ Documentation enhancement
- 🔄 Code quality improvements
- 📋 Testing strategy implementation
- 🚀 Feature enhancements

Track our progress in [Issues](https://github.com/asbor/HoppyBrew/issues) and [Projects](https://github.com/asbor/HoppyBrew/projects).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## License

Distributed under the MIT License. See [LICENSE.txt](LICENSE.txt) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contact

**Project Link**: [https://github.com/asbor/HoppyBrew](https://github.com/asbor/HoppyBrew)

**Issues**: [https://github.com/asbor/HoppyBrew/issues](https://github.com/asbor/HoppyBrew/issues)

**Discussions**: [https://github.com/asbor/HoppyBrew/discussions](https://github.com/asbor/HoppyBrew/discussions)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Acknowledgments

This project is an original AI-assisted development showcasing modern brewing management technology.

- Thanks to all contributors
- Inspired by Brewfather
- Built with amazing open-source tools

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[forks-shield]: https://img.shields.io/github/forks/asbor/HoppyBrew.svg?style=for-the-badge
[forks-url]: https://github.com/asbor/HoppyBrew/network/members
[stars-shield]: https://img.shields.io/github/stars/asbor/HoppyBrew.svg?style=for-the-badge
[stars-url]: https://github.com/asbor/HoppyBrew/stargazers
[issues-shield]: https://img.shields.io/github/issues/asbor/HoppyBrew.svg?style=for-the-badge
[issues-url]: https://github.com/asbor/HoppyBrew/issues
[license-shield]: https://img.shields.io/github/license/asbor/HoppyBrew.svg?style=for-the-badge
[license-url]: https://github.com/asbor/HoppyBrew/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: www.linkedin.com/in/asbjørn-bordoy-89b0462a
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Python-url]: https://www.python.org/
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Docker.com]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[PostgreSQL.org]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[FastAPI.org]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[sqlalchemy]: https://img.shields.io/badge/sqlalchemy-316192?style=for-the-badge&logo=sqlalchemy&logoColor=white
[sqlalchemy-url]: https://www.sqlalchemy.org/
[pydantic]: https://img.shields.io/badge/pydantic-005571?style=for-the-badge&logo=pydantic
[pydantic-url]: https://pydantic-docs.helpmanual.io/
[GitHub]: https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white
[GitHub-url]: https://github.com/asbor/HoppyBrew
[Markdown]: https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white
[Markdown-url]: https://www.markdownguide.org/
[PlantUML]: https://img.shields.io/badge/PlantUML-000000?style=for-the-badge&logo=plantuml&logoColor=white
[PlantUML-url]: https://plantuml.com/
[uvicorn]: https://img.shields.io/badge/uvicorn-316192?style=for-the-badge&logo=uvicorn&logoColor=white
[uvicorn-url]: https://www.uvicorn.org/
[Git-scm]: https://img.shields.io/badge/Git-181717?style=for-the-badge&logo=git&logoColor=F05032
[Git-scm-url]: https://git-scm.com/
[VsCode]: https://img.shields.io/badge/Visual_Studio_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white
[VsCode-url]: https://code.visualstudio.com/
[Redis]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/
