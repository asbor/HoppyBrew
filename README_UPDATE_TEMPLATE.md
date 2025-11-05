# README Update Template

This template provides quick snippets to help you update your README.md after migrating to a new repository.

## Step 1: Update Badge URLs

Replace the badge section at the bottom of README.md with:

```markdown
<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/YOUR-USERNAME/YOUR-REPO-NAME.svg?style=for-the-badge
[contributors-url]: https://github.com/YOUR-USERNAME/YOUR-REPO-NAME/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/YOUR-USERNAME/YOUR-REPO-NAME.svg?style=for-the-badge
[forks-url]: https://github.com/YOUR-USERNAME/YOUR-REPO-NAME/network/members
[stars-shield]: https://img.shields.io/github/stars/YOUR-USERNAME/YOUR-REPO-NAME.svg?style=for-the-badge
[stars-url]: https://github.com/YOUR-USERNAME/YOUR-REPO-NAME/stargazers
[issues-shield]: https://img.shields.io/github/issues/YOUR-USERNAME/YOUR-REPO-NAME.svg?style=for-the-badge
[issues-url]: https://github.com/YOUR-USERNAME/YOUR-REPO-NAME/issues
[license-shield]: https://img.shields.io/github/license/YOUR-USERNAME/YOUR-REPO-NAME.svg?style=for-the-badge
[license-url]: https://github.com/YOUR-USERNAME/YOUR-REPO-NAME/blob/master/LICENSE.txt
```

## Step 2: Find and Replace

Use your text editor's find-and-replace to update these values in **README.md**:

| Find This | Replace With |
|-----------|--------------|
| `YOUR-USERNAME` | Your GitHub username |
| `YOUR-REPO-NAME` | Your new repository name |
| `<your-repository-url>` | Full clone URL (e.g., `https://github.com/username/repo.git`) |

## Step 3: Update Project Link

In the **Contact** section of README.md, update:

```markdown
## Contact

Project Link: [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME)
```

## Step 4: Update Clone Command

In the **Installation** section of README.md, update:

```markdown
2. Clone the repo
   ```sh
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   ```
```

## Example: Complete Replacement

If your new repository is `https://github.com/johndoe/hoppybrew-app`:

- Replace `YOUR-USERNAME` → `johndoe`
- Replace `YOUR-REPO-NAME` → `hoppybrew-app`
- Replace `<your-repository-url>` → `https://github.com/johndoe/hoppybrew-app.git`

## Quick Commands

### Using sed (Linux/macOS)

```bash
# Update README.md (Linux)
sed -i 's/YOUR-USERNAME/johndoe/g' README.md
sed -i 's/YOUR-REPO-NAME/hoppybrew-app/g' README.md

# Update README.md (macOS)
sed -i '' 's/YOUR-USERNAME/johndoe/g' README.md
sed -i '' 's/YOUR-REPO-NAME/hoppybrew-app/g' README.md
```

### Using VS Code

1. Open README.md
2. Press `Ctrl+H` (Windows/Linux) or `Cmd+H` (macOS)
3. Find: `YOUR-USERNAME`
4. Replace: `your-actual-username`
5. Click "Replace All"
6. Repeat for `YOUR-REPO-NAME` and `<your-repository-url>`

## Verification Checklist

After updating, verify:

- [ ] All badge links work correctly
- [ ] Clone command has correct URL
- [ ] Project link in Contact section is correct
- [ ] No placeholder text remains (search for `YOUR-`, `<your-`, `[Add `)
- [ ] All images load correctly
- [ ] Links to issues, PRs, etc. point to new repository

## Additional Files to Update

Don't forget to update placeholders in these files too:

- [ ] `Project Setup Guide.md`
- [ ] `documents/##-Github-Doc/01-Installation-on-local-machine.md`
- [ ] `documents/##-Github-Doc/02-Build-Docker-Container.md`
- [ ] `documents/docs/HoppyBrew_Summary.md`

---

**Tip**: After completing all updates, you can delete this `README_UPDATE_TEMPLATE.md` file.
