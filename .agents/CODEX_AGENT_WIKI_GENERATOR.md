# CODEX AGENT: Wiki Generator with PlantUML Integration

## Agent Mission
Generate comprehensive GitHub Wiki documentation for HoppyBrew project, including:
- Project overview and roadmap
- Technical architecture documentation  
- API documentation with PlantUML diagrams
- User guides and tutorials
- Development workflow documentation
- Integration with existing PlantUML files

## Current Status
- **Phase**: Setup and Planning
- **Priority**: High
- **Access**: Read/Write to docs, plantuml, and new wiki directories
- **Dependencies**: PlantUML renderer, GitHub API access

## Core Responsibilities

### 1. Wiki Structure Creation
- [ ] Create wiki directory structure
- [ ] Generate Home.md with project overview
- [ ] Create navigation sidebar
- [ ] Set up wiki template system

### 2. PlantUML Integration
- [ ] Inventory existing PlantUML files (220+ files found)
- [ ] Generate PNG/SVG from .puml files
- [ ] Create diagram index and catalog
- [ ] Embed diagrams in wiki pages

### 3. Documentation Generation
- [ ] Technical architecture overview
- [ ] Database schema documentation
- [ ] API endpoint documentation
- [ ] Frontend component documentation
- [ ] Docker setup guides

### 4. Project Documentation
- [ ] Getting started guide
- [ ] Development workflow
- [ ] Deployment instructions
- [ ] Troubleshooting guide
- [ ] Contributing guidelines

## File Ownership and Scope

### Primary Files (Full Authority)
- `wiki/` (new directory)
- `documents/wiki-exports/` (new directory for generated content)
- `scripts/wiki-generator.sh` (new file)
- `scripts/plantuml-renderer.sh` (new file)

### Read-Only Resources
- `documents/docs/plantuml/` (220+ .puml files)
- `documents/docs/` (existing documentation)
- `README.md` (for project info)
- `services/` (for API/component analysis)
- `.agents/` (for workflow documentation)

### Generated Outputs
- `wiki/Home.md`
- `wiki/Architecture.md`
- `wiki/API-Documentation.md`
- `wiki/Database-Schema.md`
- `wiki/Frontend-Components.md`
- `wiki/Development-Guide.md`
- `wiki/Deployment.md`
- `wiki/diagrams/` (rendered PlantUML images)

## PlantUML Processing Strategy

### 1. Diagram Categorization
```bash
# Organize by type
ERD/            # Entity Relationship Diagrams
Components/     # Component Architecture  
Workflows/      # Process Flow Diagrams
API/           # API Interaction Diagrams
```

### 2. Rendering Pipeline
```bash
# Auto-generate from .puml to .png/.svg
find documents/docs/plantuml -name "*.puml" | while read file; do
    plantuml -tpng "$file" -o "wiki/diagrams/"
    plantuml -tsvg "$file" -o "wiki/diagrams/"
done
```

### 3. Wiki Integration
```markdown
# Embed in wiki pages
![Architecture Overview](diagrams/ComponentDiagram-HoppyBrew.png)
```

## Wiki Structure Template

```
wiki/
├── Home.md                    # Project overview and navigation
├── _Sidebar.md               # Navigation menu
├── Architecture.md           # Technical architecture with diagrams
├── Getting-Started.md        # Quick start guide
├── API-Documentation.md      # REST API reference
├── Database-Schema.md        # Database design with ERD
├── Frontend-Guide.md         # Nuxt3/Vue component guide
├── Docker-Setup.md           # Container deployment
├── Development-Workflow.md   # Developer onboarding
├── Troubleshooting.md        # Common issues and solutions
├── Contributing.md           # Contribution guidelines
├── diagrams/                 # Rendered PlantUML images
│   ├── architecture/
│   ├── database/
│   ├── workflows/
│   └── components/
└── assets/                   # Additional images and resources
```

## Agent Implementation Plan

### Phase 1: Setup and Discovery (30 minutes)
1. **Analyze Existing Documentation**
   - Scan `documents/docs/` for content
   - Inventory PlantUML files by category
   - Extract key information from README.md

2. **Create Wiki Structure**
   - Initialize wiki directory
   - Set up navigation framework
   - Create template files

### Phase 2: PlantUML Processing (45 minutes)
1. **Render Diagrams**
   - Install/verify PlantUML renderer
   - Process all .puml files to PNG/SVG
   - Organize by category in wiki/diagrams/

2. **Create Diagram Index**
   - Generate catalog of all diagrams
   - Add descriptions and categories
   - Link to source .puml files

### Phase 3: Content Generation (60 minutes)
1. **Technical Documentation**
   - Architecture overview with component diagrams
   - Database schema with ERD diagrams
   - API documentation with interaction diagrams

2. **User Documentation**
   - Getting started guide
   - Development workflow
   - Docker deployment guide

### Phase 4: Integration and Polish (30 minutes)
1. **Cross-Reference Links**
   - Internal wiki navigation
   - Links to GitHub issues/PRs
   - Reference to external resources

2. **Quality Assurance**
   - Validate all diagram links
   - Test navigation flow
   - Ensure consistent formatting

## Tool Requirements

### PlantUML Rendering
```bash
# Install PlantUML (if not available)
sudo apt-get install plantuml
# or
wget http://plantuml.com/plantuml.jar

# Rendering commands
plantuml -tpng *.puml
plantuml -tsvg *.puml
```

### GitHub Wiki Access
```bash
# Clone wiki repository
git clone https://github.com/asbor/HoppyBrew.wiki.git wiki

# Or use GitHub API for direct publishing
gh api repos/asbor/HoppyBrew/wiki -X POST
```

## Success Metrics

### Completion Criteria
- [ ] 220+ PlantUML diagrams rendered and categorized
- [ ] 10+ wiki pages created with navigation
- [ ] All major project components documented
- [ ] Embedded diagrams in technical documentation
- [ ] Working navigation and cross-references
- [ ] Deployment-ready wiki structure

### Quality Metrics
- [ ] All diagram links functional
- [ ] Consistent formatting across pages
- [ ] Clear navigation flow
- [ ] Comprehensive technical coverage
- [ ] User-friendly getting started guide

## MCP Server Integration

### GitHub MCP Capabilities
- Repository wiki management
- Issue/PR linking in documentation
- Automated publishing workflow
- Branch-based wiki updates

### Publishing Options
1. **Direct Wiki Publishing** (with MCP access)
   - Push directly to GitHub wiki repository
   - Automated diagram rendering and upload
   - Immediate publication

2. **Export for Manual Publishing** (without MCP access)
   - Generate complete wiki structure locally
   - Provide upload instructions
   - Export to `documents/wiki-exports/`

## Coordination with Other Agents

### Dependencies
- **Database Agent**: Provide schema documentation
- **Frontend Agent**: Component documentation  
- **CI/CD Agent**: Deployment workflow documentation
- **Docker Agent**: Container setup guides

### Outputs for Other Agents
- Wiki templates for ongoing documentation
- PlantUML rendering pipeline
- Documentation standards and guidelines

## Agent Execution Command

### With MCP Server Access (Full Publishing)
```bash
codex exec -s workspace-write \
  "Generate comprehensive GitHub wiki for HoppyBrew project with PlantUML integration. 
   Process 220+ existing PlantUML files, create technical documentation, 
   and publish directly to GitHub wiki repository. 
   Include architecture diagrams, API docs, database schemas, and user guides."
```

### Without MCP Server Access (Local Generation)
```bash
codex exec -s workspace-write \
  "Create comprehensive wiki documentation structure for HoppyBrew project. 
   Process all PlantUML files to generate diagrams, create technical documentation 
   with embedded diagrams, and prepare export-ready wiki structure in documents/wiki-exports/. 
   Include complete setup instructions for manual GitHub wiki publishing."
```

## Agent Log
- **2025-11-08 07:50 UTC**: Agent context created
- **2025-11-08 07:50 UTC**: Discovered 220+ PlantUML files for processing
- **2025-11-08 07:50 UTC**: Ready for headless execution

## Next Steps
1. Execute agent with chosen MCP access level
2. Monitor progress through generated logs
3. Review wiki structure before publishing
4. Coordinate with other agents for ongoing documentation