import os
import sys

# Add backend directory to sys path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal
from app.models import init_db
from app.services.seed_service import SeedService

def seed_demo_data():
    """Seeds the enterprise demo dataset via the unified SeedService."""
    init_db()
    db = SessionLocal()
    try:
        print("[*] Seeding Enterprise Demo Scenario (NexusBridge Technologies)...")
        SeedService.seed_demo_scenario(db)
        print("[+] Demo Scenario seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
