from database import engine, Base
import models

print("Connecting to PostgreSQL and creating tables...")
# This command creates all tables defined in models.py if they don't already exist
Base.metadata.create_all(bind=engine)
print("Success! Database tables are ready.")