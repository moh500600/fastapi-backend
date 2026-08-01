from database import engine
import models

print("Dropping existing tables...")
models.Base.metadata.drop_all(bind=engine)
print("Recreating tables with new schema...")
models.Base.metadata.create_all(bind=engine)
print("Done!")
