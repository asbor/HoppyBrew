# HoppyBrew Documentation

Welcome to the HoppyBrew documentation! This directory contains all project documentation organized by category.

## 📚 Quick Start

- **New Users?** Start with [guides/GETTING_STARTED.md](guides/GETTING_STARTED.md)
- **Looking for something?** Check the [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **Developers?** See [guides/DEVELOPMENT_SETUP.md](guides/DEVELOPMENT_SETUP.md)

## 📁 Directory Structure

### `/guides/` - User and Developer Guides
Step-by-step instructions and how-to guides:

- **GETTING_STARTED.md** - Complete installation and setup guide
- **USER_GUIDE.md** - Full user manual (9,300 words)
- **DEVELOPMENT_SETUP.md** - Developer environment setup (10,200 words)
- **CI_CD_FIXES.md** - CI/CD troubleshooting
- **CONFLICT_RESOLUTION_GUIDE.md** - Resolving Git conflicts
- **ISSUE_RESOLUTION_GUIDE.md** - Issue management
- **VALIDATION_CHECKLIST.md** - Quality assurance
- **GITHUB_CLEANUP_CHECKLIST.md** - Repository maintenance
- **MANAGING_AUTOMATED_ISSUES.md** - Automated issue handling

### `/github-guides/` - GitHub-Specific Guides
Guides for GitHub workflows and setup:

- **01-Installation-on-local-machine.md** - Local installation
- **02-Build-Docker-Container.md** - Docker builds
- **03-Push-to-DockerHub.md** - DockerHub publishing
- **04-CI-CD-Pipeline.md** - CI/CD setup

### `/docs/` - Architecture Documentation
Technical architecture using arc42 format:

- **chapters/** - Complete system documentation (14 chapters)
  - Introduction and goals
  - Architecture constraints
  - System scope and context
  - Solution strategy
  - Building blocks
  - Runtime views
  - Deployment
  - Cross-cutting concepts
  - Architecture decisions
  - Quality requirements
  - Risks and technical debt
  - Glossary
  - Bibliography

### `/features/` - Feature Specifications
Detailed feature documentation:

- **ARCHITECTURE.md** - Overall system architecture
- **BATCH_WORKFLOW_SYSTEM.md** - Batch tracking system
- **FERMENTATION_PROFILES.md** - Fermentation management
- **HOMEASSISTANT_INTEGRATION.md** - Home Assistant integration

### `/planning/` - Planning Documents
Project planning and roadmaps:

- **IMPLEMENTATION_ROADMAP.md** - Detailed implementation plan
- **HOMEASSISTANT_ENHANCEMENT_PLAN.md** - Home Assistant improvements

### `/status/` - Status Updates
Regular status reports:

- **README.md** - Status documentation index
- **2025-11-05.md** - Status updates
- **2025-11-06.md** - Status updates

### `/sessions/` - Session Documentation
Development session summaries:

- **SESSION_2025-11-08_issue_management.md** - Latest session
- Various session summaries and reports

### `/archive/` - Historical Documentation
Archived and historical documents:

- **agent-summaries/** - AI agent reports and analyses
- **analysis/** - Comprehensive analysis reports
- **sessions/** - Historical session summaries
- **legacy/** - Old documentation
- **templates/** - Documentation templates
- **docs-archive/** - Archived documentation versions

### Root Level Documentation Files

Located in this directory:

- **DOCUMENTATION_INDEX.md** - Complete documentation catalog
- **DEPLOYMENT_GUIDE.md** - Production deployment guide
- **DOCKERHUB_SETUP.md** - DockerHub configuration
- **BACKUP_RESTORE_GUIDE.md** - Backup and restore procedures
- **WATER_PROFILES.md** - Water chemistry reference
- **README_API.md** - API usage guide
- **FRONTEND_API_URL_MIGRATION.md** - API migration guide

### `/00-Development-Journal/` - Development Logs
Weekly development journal entries:

- **Week-01.md** - First week progress
- **Week-02.md** - Second week progress

### `/images/` - Documentation Images
Images and diagrams used in documentation

### `/templates/` - Document Templates
Templates for creating new documentation:

- **arc42/** - arc42 documentation templates

### `/EnterpriceArchitect/` - Enterprise Architect Files
EA project files (binary)

## 🔍 Finding Documentation

### By User Type

**End Users**
1. [Getting Started](guides/GETTING_STARTED.md)
2. [User Guide](guides/USER_GUIDE.md)
3. [Deployment Guide](DEPLOYMENT_GUIDE.md)

**Developers**
1. [Development Setup](guides/DEVELOPMENT_SETUP.md)
2. [API Reference](../api_endpoint_catalog.md)
3. [Architecture Docs](docs/chapters/)
4. [Frontend Architecture](../services/nuxt3-shadcn/FRONTEND_ARCHITECTURE.md)

**System Administrators**
1. [Deployment Guide](DEPLOYMENT_GUIDE.md)
2. [Backup & Restore](BACKUP_RESTORE_GUIDE.md)
3. [Docker Setup](github-guides/02-Build-Docker-Container.md)

**Project Managers**
1. [Roadmap](../ROADMAP.md)
2. [TODO](../TODO.md)
3. [Status Updates](status/)

### By Topic

**Installation & Setup**
- [Getting Started](guides/GETTING_STARTED.md)
- [Local Installation](github-guides/01-Installation-on-local-machine.md)
- [Docker Setup](github-guides/02-Build-Docker-Container.md)

**Usage**
- [User Guide](guides/USER_GUIDE.md)
- [API Guide](README_API.md)

**Development**
- [Development Setup](guides/DEVELOPMENT_SETUP.md)
- [Contributing](../CONTRIBUTING.md)
- [Testing Strategy](../TESTING_STRATEGY.md)

**Architecture**
- [System Architecture](features/ARCHITECTURE.md)
- [Frontend Architecture](../services/nuxt3-shadcn/FRONTEND_ARCHITECTURE.md)
- [Database Design](../services/backend/Database/Models/database_agent_relationships_and_indexes.md)
- [arc42 Docs](docs/chapters/)

**Features**
- [Batch Workflow](features/BATCH_WORKFLOW_SYSTEM.md)
- [Fermentation](features/FERMENTATION_PROFILES.md)
- [HomeAssistant](features/HOMEASSISTANT_INTEGRATION.md)

**Operations**
- [Deployment](DEPLOYMENT_GUIDE.md)
- [Backup & Restore](BACKUP_RESTORE_GUIDE.md)
- [CI/CD](github-guides/04-CI-CD-Pipeline.md)

## 📖 Documentation Standards

All documentation in this repository should follow these guidelines:

### Writing Style
- **Clear and Concise**: Get to the point quickly
- **Well-Structured**: Use headings, lists, and formatting
- **Complete**: Include all necessary information
- **Accurate**: Keep information up-to-date
- **Accessible**: Write for your target audience

### Markdown Best Practices
- Use clear hierarchical headings (# ## ### ####)
- Include a table of contents for long documents
- Use code blocks with language syntax highlighting
- Add links to related documentation
- Include examples where appropriate
- Use emoji sparingly for visual markers 📚 🚀 ⚠️

### Required Sections
Every guide should include:
- **Title**: Clear, descriptive title
- **Overview**: Brief introduction
- **Prerequisites**: What's needed before starting
- **Main Content**: Step-by-step instructions
- **Troubleshooting**: Common issues and solutions
- **Related Links**: Links to related documentation
- **Last Updated**: Date of last update

### File Naming
- Use descriptive, uppercase names: `USER_GUIDE.md`
- Use hyphens for multi-word names: `GETTING_STARTED.md`
- Use consistent prefixes for series: `01-`, `02-`, etc.

## 🔄 Updating Documentation

### When to Update
- When features change
- When bugs are fixed
- When new features are added
- When deployment procedures change
- When receiving feedback about unclear docs

### How to Update
1. Read [Contributing Guide](../CONTRIBUTING.md)
2. Make changes to relevant documentation
3. Update [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) if adding new docs
4. Update "Last Updated" date
5. Submit PR with clear description of changes

### Review Process
- All documentation changes go through PR review
- Check for clarity and accuracy
- Verify links work correctly
- Ensure formatting is consistent

## 📊 Documentation Statistics

As of November 8, 2025:

- **Total Documentation Files**: 130+
- **User Guides**: 3 comprehensive guides (26,500+ words)
- **Architecture Docs**: 14 arc42 chapters
- **Feature Specs**: 4 detailed specifications
- **How-To Guides**: 9+ step-by-step guides
- **Status Reports**: Regular updates
- **Archive**: Extensive historical documentation

## 🤝 Contributing

Want to improve documentation?

1. **Find What Needs Improvement**
   - Outdated information
   - Missing documentation
   - Unclear instructions
   - Broken links

2. **Make Changes**
   - Follow documentation standards
   - Write clear, concise content
   - Add examples and screenshots
   - Test all code samples

3. **Submit PR**
   - Describe changes clearly
   - Link related issues
   - Request review

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full guidelines.

## 🆘 Getting Help

Can't find what you're looking for?

1. **Search**: Use the [Documentation Index](DOCUMENTATION_INDEX.md)
2. **Ask**: Open a [Discussion](https://github.com/asbor/HoppyBrew/discussions)
3. **Report**: Open an [Issue](https://github.com/asbor/HoppyBrew/issues) for missing docs
4. **Browse**: Check the [Wiki Home](../WIKI_HOME.md)

## 📝 Documentation Roadmap

Future documentation improvements:

- [ ] Add video tutorials
- [ ] Create API examples and tutorials
- [ ] Add more screenshots to user guide
- [ ] Create deployment checklists
- [ ] Add troubleshooting flowcharts
- [ ] Create architecture diagrams
- [ ] Translate to other languages (future)
- [ ] Create PDF exports of guides

## 📮 Feedback

Have suggestions for documentation improvements?

- Open an issue with the `documentation` label
- Comment on existing documentation PRs
- Join discussions about documentation
- Submit PRs with improvements

---

**Last Updated**: November 8, 2025  
**Documentation Maintainer**: HoppyBrew Team

📌 **Remember**: Good documentation is as important as good code!
