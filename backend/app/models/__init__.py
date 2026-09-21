from app.database import Base, engine
from app.models.asset import Asset
from app.models.audit import Audit
from app.models.finding import Finding
from app.models.evidence import Evidence
from app.models.remediation import Remediation
from app.models.control import Control

def init_db():
    Base.metadata.create_all(bind=engine)
