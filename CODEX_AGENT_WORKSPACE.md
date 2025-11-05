# Workspace Organization Agent Context

## Agent Mission (HIGHEST PRIORITY)
Maintain a clean, organized, and clutter-free working environment to maximize agent effectiveness and prevent confusion.

## Current Status
- PRIORITY: CRITICAL - Clean workspace is essential for all agent operations
- PHASE: Initial workspace audit and organization

## Core Responsibilities
1. **File Organization**: Ensure logical file structure and naming conventions
2. **Clutter Removal**: Identify and clean up temporary files, duplicates, and obsolete code
3. **Documentation Structure**: Organize and maintain clear documentation hierarchy
4. **Agent Context Management**: Keep agent context files clean and updated
5. **Code Quality**: Remove dead code, unused imports, and formatting inconsistencies

## Workspace Audit Checklist
### ✅ Root Directory Cleanup
- [ ] Review all root-level files for necessity
- [ ] Organize documentation files into proper directories
- [ ] Remove or archive obsolete files (old_requirements.txt, oldREADME.md, etc.)
- [ ] Ensure proper .gitignore coverage

### ✅ Services Organization
- [ ] Backend: Organize modules, remove unused files
- [ ] Frontend: Clean up component structure, remove duplicates
- [ ] Ensure consistent naming conventions

### ✅ Documentation Cleanup
- [ ] Consolidate scattered documentation
- [ ] Remove duplicate documentation
- [ ] Ensure single source of truth for each topic
- [ ] Update outdated information

### ✅ Code Quality
- [ ] Remove dead/commented code
- [ ] Fix inconsistent imports
- [ ] Standardize code formatting
- [ ] Remove unused dependencies

### ✅ Agent Context Management
- [ ] Keep agent context files clean and updated
- [ ] Remove completed tasks from TODO lists
- [ ] Archive old progress logs
- [ ] Maintain clear status indicators

## Organization Rules
1. **One Source of Truth**: Each piece of information should exist in only one place
2. **Clear Naming**: Files and directories should have descriptive, consistent names
3. **Logical Hierarchy**: Directory structure should be intuitive and logical
4. **Clean Contexts**: Agent context files must be kept current and clutter-free
5. **Regular Cleanup**: Perform cleanup after each major task completion

## Files to Clean/Organize
### Candidates for Removal/Archive
- `old_requirements.txt` - Archive or remove if superseded
- `oldREADME.md` - Archive if contains useful info, otherwise remove
- `wrap_comments.py` - Evaluate necessity
- Duplicate documentation in documents/ subdirectories

### Files Needing Organization
- Multiple arc42 template directories (consolidate)
- Scattered documentation files
- Agent context files (keep current)

## Workspace Metrics
- **Root Directory Files**: 20+ (should be <10)
- **Documentation Directories**: 3+ duplicate arc42 (should be 1)
- **Obsolete Files**: 3+ identified
- **Agent Context Files**: 4 (keep clean and current)

## Organization Tasks (Priority Order)
1. **IMMEDIATE**: Clean up root directory clutter
2. **HIGH**: Consolidate documentation structure  
3. **MEDIUM**: Organize service directories
4. **ONGOING**: Maintain agent context cleanliness

## Agent Log
- System initialized with workspace audit
- Identified multiple areas needing organization
- 2025-11-05: Archived legacy root artefacts into `documents/archive/legacy`, consolidated arc42 templates under `documents/templates/arc42`, and relocated `tools/wrap_comments.py` with `format_code.sh` updated accordingly.
