import asyncio
from app.db.session import engine, create_all_tables
from app.models.user import User
from app.models.vault import VaultDeposit
from app.models.position import Position
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_db():
    print("Ensuring tables are created...")
    await create_all_tables()
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as db:
        print("Checking for existing test user...")
        # See if user exists
        import sqlalchemy
        res = await db.execute(sqlalchemy.text("SELECT * FROM users WHERE email='test@shadowalpha.io'"))
        user = res.fetchone()
        
        user_id = None
        if not user:
            print("Creating test user...")
            from uuid import uuid4
            user_id = str(uuid4())
            # Precomputed bcrypt hash for 'password123' to bypass Passlib environment errors
            hashed = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQmO"
            
            # Using raw SQL bypasses Pydantic/SQLAlchemy setup issues during direct scripts
            await db.execute(
                sqlalchemy.text("INSERT INTO users (id, email, hashed_password, is_active, role) VALUES (:id, :email, :pw, 1, 'user')"),
                {"id": user_id, "email": "test@shadowalpha.io", "pw": hashed}
            )
            print("Test user created: test@shadowalpha.io / password123")
        else:
            user_id = user[0] # assuming first column is id
            print(f"Test user already exists: {user_id}")

        # Add mock Vault Deposits
        print("Adding mock vault deposits...")
        await db.execute(
            sqlalchemy.text("INSERT INTO vault_deposits (id, user_id, amount, status, created_at) VALUES (:vid, :uid, :amt, 'active', :dt)"),
            {"vid": str(uuid4()), "uid": user_id, "amt": 500000.0, "dt": (datetime.utcnow() - timedelta(days=10)).isoformat()}
        )
        
        await db.commit()
    
    print("Database seeded successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_db())
