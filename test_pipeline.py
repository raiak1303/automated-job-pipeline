#!/usr/bin/env python
"""Test the job pipeline"""

import sys
import subprocess

# Install dependencies
print("Installing dependencies...")
dependencies = ["requests", "beautifulsoup4", "openpyxl"]
for dep in dependencies:
    try:
        __import__(dep.replace("-", "_"))
        print(f"  ✓ {dep} already installed")
    except ImportError:
        print(f"  Installing {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", dep])

# Now run the pipeline
print("\n" + "="*60)
print("Running Job Pipeline")
print("="*60)

try:
    from pipeline import JobPipeline
    pipeline = JobPipeline()
    pipeline.run()
    print("✓ Pipeline completed successfully!")
except Exception as e:
    print(f"✗ Pipeline failed: {e}")
    import traceback
    traceback.print_exc()
