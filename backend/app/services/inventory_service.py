from sqlalchemy.orm import Session
from app.models.asset import Asset, AssetType
from app.scanners.local_inventory import LocalInventoryScanner
import uuid
from datetime import datetime, timezone

class InventoryService:
    @staticmethod
    def discover_local_asset(db: Session) -> Asset:
        """Runs the local inventory scanner and updates/creates the asset in the DB."""
        info = LocalInventoryScanner.get_system_info()
        
        # Check if asset exists by hostname
        db_asset = db.query(Asset).filter(Asset.hostname == info["hostname"]).first()
        
        ips_str = ",".join(info["ip_addresses"])
        
        if db_asset:
            db_asset.ip_address = ips_str
            db_asset.os_name = info["os_name"]
            db_asset.os_version = info["os_version"]
            db_asset.architecture = info["architecture"]
            db_asset.discovery_timestamp = datetime.now(timezone.utc)
        else:
            db_asset = Asset(
                id=str(uuid.uuid4()),
                hostname=info["hostname"],
                ip_address=ips_str,
                os_name=info["os_name"],
                os_version=info["os_version"],
                architecture=info["architecture"],
                asset_type=AssetType.SERVER, # Defaulting to server for demo
                discovery_source="LOCAL_AGENT",
                status="ACTIVE"
            )
            db.add(db_asset)
            
        db.commit()
        db.refresh(db_asset)
        return db_asset
