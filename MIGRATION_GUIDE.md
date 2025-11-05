# Migration Guide - Moving to a New Repository

This guide will help you move the HoppyBrew project to a new repository and continue development.

## Pre-Migration Checklist

Before moving to a new repository, this codebase has been cleaned up to remove:
- ✅ Old repository URLs (GitLab and GitHub references)
- ✅ Hardcoded repository-specific links
- ✅ Repository-specific badges

## Steps to Set Up in a New Repository

### 1. Create Your New Repository

1. Go to GitHub (or your preferred Git hosting platform)
2. Create a new repository with your desired name
3. **Do NOT initialize it with README, .gitignore, or license** (this project already has these)
4. Copy the new repository URL (e.g., `https://github.com/YOUR-USERNAME/YOUR-NEW-REPO.git`)

### 2. Clone This Project and Push to New Repository

```bash
# Clone this repository (if you haven't already)
git clone https://github.com/asbor/iu-project-software-engineering.git
cd iu-project-software-engineering

# Remove the old remote
git remote remove origin

# Add your new repository as the remote
git remote add origin https://github.com/YOUR-USERNAME/YOUR-NEW-REPO.git

# Push all branches and tags
git push -u origin --all
git push -u origin --tags
```

### 3. Update Repository-Specific References

After pushing to your new repository, update the following placeholders:

#### In `README.md`:
Replace all instances of:
- `YOUR-USERNAME` with your GitHub username
- `YOUR-REPO-NAME` with your new repository name

Update the following sections:
- Badge URLs (lines starting with `[contributors-shield]`, `[forks-shield]`, etc.)
- Project Link in the Contact section
- Clone URL in the Installation section

#### In `Project Setup Guide.md`:
Replace:
- `<your-repository-url>` with your actual repository URL
- `YOUR-REPO-NAME` with your new repository name

#### In `documents/##-Github-Doc/01-Installation-on-local-machine.md`:
Replace:
- `<your-repository-url>` with your actual repository URL
- `YOUR-REPO-NAME` with your new repository name

#### In `documents/##-Github-Doc/02-Build-Docker-Container.md`:
Replace:
- `<your-repository-url>` with your actual repository URL

#### In `documents/docs/HoppyBrew_Summary.md`:
Replace:
- `[Add your repository link here]` with your actual repository URL
- `[Add your cloud hosting links here if applicable]` with your cloud hosting URLs (if you have any)

### 4. Review and Update CI/CD Configuration

This project includes a `.gitlab-ci.yml` file from the previous setup. You have several options:

#### Option A: Remove GitLab CI (if using GitHub Actions)
```bash
rm .gitlab-ci.yml
git add .gitlab-ci.yml
git commit -m "Remove GitLab CI configuration"
git push
```

#### Option B: Keep GitLab CI (if using GitLab)
Keep the file as-is if you're moving to a GitLab repository.

#### Option C: Set up GitHub Actions (recommended for GitHub)
1. Create `.github/workflows/` directory structure
2. Add your GitHub Actions workflow files
3. Remove `.gitlab-ci.yml` if no longer needed

### 5. Update Environment Configuration

1. Review `.env` file and update any repository-specific values
2. Ensure sensitive data is not committed (already included in `.gitignore`)
3. Update `docker-compose.yml` if it contains any old repository references

### 6. Test Your Setup

After migrating:

```bash
# Test local setup
make install

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Test Docker setup
docker-compose up
```

### 7. Update Documentation

Consider updating:
- **CHANGELOG.md**: Add an entry about the repository migration
- **README.md**: Ensure all links and badges work correctly
- **LICENSE.txt**: Verify the license is appropriate for your new repository

### 8. Post-Migration Tasks

- [ ] Enable GitHub Pages (if applicable)
- [ ] Set up branch protection rules
- [ ] Configure CI/CD pipelines
- [ ] Set up issue templates
- [ ] Configure repository settings (description, topics, etc.)
- [ ] Update any external documentation or links pointing to the old repository
- [ ] Inform collaborators about the new repository location

## Quick Reference: Find and Replace

Use your editor's find-and-replace functionality to update these common placeholders:

| Find | Replace With |
|------|-------------|
| `YOUR-USERNAME` | Your actual GitHub username |
| `YOUR-REPO-NAME` | Your new repository name |
| `<your-repository-url>` | Your full repository URL |

Example using `sed` (Linux/macOS):
```bash
# Replace YOUR-USERNAME with your actual username
sed -i 's/YOUR-USERNAME/johndoe/g' README.md

# Replace YOUR-REPO-NAME with your actual repo name
sed -i 's/YOUR-REPO-NAME/hoppybrew-new/g' README.md

# For macOS, use: sed -i '' 's/pattern/replacement/g' file
```

## Troubleshooting

### Problem: Git push fails with "remote already exists"
**Solution**: Remove the old remote first: `git remote remove origin`

### Problem: Some commits are missing after migration
**Solution**: Ensure you pushed all branches: `git push origin --all`

### Problem: Badges show wrong repository
**Solution**: Update all badge URLs in README.md to point to your new repository

### Problem: CI/CD not working
**Solution**: Update your CI/CD configuration files (`.gitlab-ci.yml` or `.github/workflows/`) with correct settings

## Additional Resources

- [GitHub Documentation](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [Docker Documentation](https://docs.docker.com)

## Support

If you encounter issues during migration:
1. Check the project documentation
2. Review this migration guide
3. Consult Git and platform-specific documentation

---

**Note**: This migration guide was created to help transition the HoppyBrew project to a new repository. After completing the migration, you may delete this file if desired.
