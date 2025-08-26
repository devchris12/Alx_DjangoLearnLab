import os
import sys

manage_path = os.path.join(os.getcwd(), "manage.py")

if os.path.exists(manage_path):
    print("✅ manage.py exists in the correct location.")
else:
    print("❌ manage.py not found in the expected location.")
    sys.exit(1)
