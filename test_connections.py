"""
test_connections.py
-------------------
Purpose : Verify that the project's external services are reachable
          before building the pipeline.

Checks  :
  1. Neon (PostgreSQL)  - connects using DATABASE_URL from .env and
                          prints the database version.
                          (Used later to store engineered features.)
  2. DagsHub MLflow     - logs a dummy run named "hello" using
                          DAGSHUB_USER / DAGSHUB_TOKEN from .env.
                          (Used later to track model training runs.)

Usage   : python test_connections.py
Expected: Two lines in the terminal, plus a "hello" run under
          DagsHub -> Experiments -> connection-test.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import mlflow

load_dotenv()

# 1. Test Neon (PostgreSQL)
engine = create_engine(os.getenv("DATABASE_URL"))
with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    print("Neon connected:", version[:25])

# 2. Test DagsHub MLflow
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("DAGSHUB_USER")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("DAGSHUB_TOKEN")
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
mlflow.set_experiment("connection-test")
with mlflow.start_run(run_name="hello"):
    mlflow.log_param("test", 1)
print("MLflow connected: check DagsHub → Experiments tab")