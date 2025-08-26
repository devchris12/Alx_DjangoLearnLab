import os
import sys

readme_path = os.path.join(os.getcwd(), "README.md")

if os.path.exists(readme_path) and os.path.getsize(readme_path) > 0:
    print("✅ README.md exists and is not empty.")
else:
    print("❌ README.md missing or empty.")
    sys.exit(1)
