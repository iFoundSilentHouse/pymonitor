#!/usr/bin/env python3
"""
init_db_modern.py - SQLAlchemy 2.0+ with no deprecated methods
"""
from pathlib import Path
import sys

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def init_database():
    """Initialize database with modern SQLAlchemy"""
    print("🚀 Initializing database with SQLAlchemy 2.0+")

    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.orm import sessionmaker, DeclarativeBase
        from sqlalchemy.orm import Mapped, mapped_column
        from datetime import datetime

        # ✅ Modern DeclarativeBase
        class Base(DeclarativeBase):
            pass

        # Define model inline (or import from your app)
        class HealthCheck(Base):
            __tablename__ = "health_checks"
            id: Mapped[int] = mapped_column(primary_key=True, index=True)
            timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
            is_active: Mapped[bool] = mapped_column(default=True)

        # Create engine
        engine = create_engine(
            "sqlite:///./data/monitoring.db",
            connect_args={"check_same_thread": False},
            echo=True  # Shows SQL for debugging
        )

        # Create tables
        print("📝 Creating tables...")
        Base.metadata.create_all(engine)

        # Verify
        with engine.connect() as conn:
            # ✅ Modern way: Use text() for raw SQL
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result]

            print(f"✅ Created tables: {tables}")

            # Add sample data
            if 'health_checks' in tables:
                Session = sessionmaker(bind=engine)
                db = Session()

                # Add 3 sample records
                from datetime import datetime
                for i in range(3):
                    check = HealthCheck(is_active=True)
                    db.add(check)

                db.commit()

                # Count using modern query
                count = db.execute(text("SELECT COUNT(*) FROM health_checks")).scalar()
                print(f"📊 Added {count} sample records")

                db.close()

        print(f"\n🎉 Database initialized successfully!")
        print("📍 File: data/monitoring.db")

        return True

    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    # Check for existing database
    db_file = Path("data/monitoring.db")

    if db_file.exists():
        response = input(f"⚠️  Database exists at {db_file}. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Using existing database.")
            sys.exit(0)
        db_file.unlink()
        print("🗑️  Old database removed.")

    # Initialize
    success = init_database()

    if success:
        print("\n" + "=" * 50)
        print("📚 Quick Commands:")
        print("  Start server:  uvicorn main:app --reload")
        print("  Test GET:      curl http://localhost:8000/health")
        print("  Test POST:     curl -X POST http://localhost:8000/api/v1/health")
        print("  View data:     sqlite3 data/monitoring.db '.tables'")
        print("=" * 50)
    else:
        sys.exit(1)