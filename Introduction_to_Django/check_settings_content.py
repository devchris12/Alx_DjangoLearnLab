import os
import sys

settings_path = os.path.join(os.getcwd(), "LibraryProject", "settings.py")

if not os.path.exists(settings_path):
    print("❌ settings.py not found.")
    sys.exit(1)

with open(settings_path, "r") as f:
    content = f.read()

checks = {
    "INSTALLED_APPS": "INSTALLED_APPS" in content,
    "MIDDLEWARE": "MIDDLEWARE" in content,
    "ROOT_URLCONF": "ROOT_URLCONF = 'LibraryProject.urls'" in content,
    "WSGI_APPLICATION": "WSGI_APPLICATION = 'LibraryProject.wsgi.application'" in content,
}

for key, passed in checks.items():
    if passed:
        print(f"✅ {key} found and valid.")
    else:
        print(f"❌ {key} missing or incorrect.")
        sys.exit(1)
