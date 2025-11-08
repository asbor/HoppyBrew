#!/bin/bash

# Manual Wiki Setup Instructions
# Since GitHub Wiki needs to be manually initialized

set -euo pipefail

echo "📚 HoppyBrew Wiki Setup Instructions"
echo "====================================="
echo ""
echo "The wiki content has been generated locally but needs to be published to GitHub."
echo "GitHub Wiki repositories are only created after the first page is created manually."
echo ""
echo "🔧 Manual Setup Steps:"
echo ""
echo "1. 🌐 Visit: https://github.com/asbor/HoppyBrew/wiki"
echo ""
echo "2. 📝 Click 'Create the first page'"
echo ""
echo "3. 📋 Copy and paste the Home page content:"
echo "   - Title: 'Home'"
echo "   - Content: Copy from ./wiki/Home.md"
echo ""
echo "4. 💾 Save the page"
echo ""
echo "5. 🔄 Once the wiki is initialized, run:"
echo "   cd /tmp && git clone https://github.com/asbor/HoppyBrew.wiki.git"
echo "   cp -r /home/asbo/repo/HoppyBrew/wiki/* HoppyBrew.wiki/"
echo "   cd HoppyBrew.wiki"
echo "   git add ."
echo "   git commit -m 'Initial wiki content with comprehensive documentation'"
echo "   git push"
echo ""
echo "📊 Generated Content Summary:"
echo "  📄 Wiki Pages: $(find wiki -name "*.md" | wc -l)"
echo "  🖼️  Diagrams: $(find wiki/diagrams -name "*.png" | wc -l) PNG files"
echo "  📈 Total Size: $(du -sh wiki | cut -f1)"
echo ""
echo "📂 Local Wiki Content:"
find wiki -name "*.md" | sort | sed 's/^/  📄 /'
echo ""
echo "📂 Diagram Categories:"
find wiki/diagrams -type d | tail -n +2 | sed 's|wiki/diagrams/|  🖼️  |'
echo ""
echo "🌐 After setup, your wiki will be available at:"
echo "   https://github.com/asbor/HoppyBrew/wiki"
echo ""