import os
import sys

settings_path = os.path.join(os.getcwd(), "LibraryProject", "settings.py")

if os.path.exists(settings_path):
    print("✅ settings.py exists in the correct location.")
else:
    print("❌ settings.py not found in LibraryProject/LibraryProject.")
    sys.exit(1)
