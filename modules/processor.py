from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modules.models import Account, Ad, AdImage, AdParameter
from modules.DatabaseManager import DatabaseManager
from modules.puller import ResponseDict
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, database_manager: DatabaseManager):
        """
        Initialize the DataProcessor with a database manager.
        
        Args:
            database_manager (DatabaseManager): Database manager instance
        """
        self.db_manager = database_manager
    
    def process_response(self, response_data: ResponseDict) -> Dict[str, int]:
        """
        Process the Puller response and save all data to the database.
        
        Args:
            response_data (ResponseDict): Response from Puller.get_response()
            
        Returns:
            Dict[str, int]: Statistics about processed data
        """
        if not response_data or 'ads' not in response_data:
            logger.warning("No ads data found in response")
            return {"accounts": 0, "ads": 0, "images": 0, "parameters": 0}
        
        session = self.db_manager.get_session()
        stats = {"accounts": 0, "ads": 0, "images": 0, "parameters": 0}
        
        try:
            ads_data = response_data['ads']
            logger.info(f"Processing {len(ads_data)} ads from response")
            
            for ad_data in ads_data:
                try:
                    # Process account first
                    account = self._process_account(session, ad_data)
                    if account:
                        stats["accounts"] += 1
                    
                    # Process ad
                    ad = self._process_ad(session, ad_data, account)
                    if ad:
                        stats["ads"] += 1
                        
                        # Process images
                        images_count = self._process_ad_images(session, ad_data, ad)
                        stats["images"] += images_count
                        
                        # Process parameters
                        params_count = self._process_ad_parameters(session, ad_data, ad)
                        stats["parameters"] += params_count
                
                except Exception as e:
                    logger.error(f"Error processing ad {ad_data.get('ad_id', 'unknown')}: {e}")
                    session.rollback()
                    continue
            
            session.commit()
            logger.info(f"Successfully processed data: {stats}")
            
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            session.rollback()
            
        finally:
            session.close()
            
        return stats
    
    def _process_account(self, session: Session, ad_data: Dict[str, Any]) -> Optional[Account]:
        """Process and save account data."""
        try:
            account_id = ad_data.get('account_id')
            if not account_id:
                return None
            
            # Check if account already exists
            existing_account = session.query(Account).filter_by(account_id=account_id).first()
            if existing_account:
                # Update existing account with new data
                existing_account.account_oid = ad_data.get('account_oid', existing_account.account_oid)
                existing_account.account_name = ad_data.get('account_name', existing_account.account_name)
                existing_account.full_name = ad_data.get('full_name', existing_account.full_name)
                existing_account.avatar = ad_data.get('avatar', existing_account.avatar)
                
                # Update live_ads from seller_info if available
                seller_info = ad_data.get('seller_info', {})
                if seller_info.get('live_ads') is not None:
                    existing_account.live_ads = seller_info.get('live_ads')
                
                return existing_account
            
            # Create new account
            account = Account(
                account_id=account_id,
                account_oid=ad_data.get('account_oid', ''),
                account_name=ad_data.get('account_name', ''),
                full_name=ad_data.get('full_name', ''),
                avatar=ad_data.get('avatar'),
                live_ads=ad_data.get('seller_info', {}).get('live_ads')
            )
            
            session.add(account)
            session.flush()  # Get the ID
            return account
            
        except IntegrityError as e:
            logger.warning(f"Account {account_id} already exists: {e}")
            session.rollback()
            return session.query(Account).filter_by(account_id=account_id).first()
        except Exception as e:
            logger.error(f"Error processing account {ad_data.get('account_id')}: {e}")
            return None
    
    def _process_ad(self, session: Session, ad_data: Dict[str, Any], account: Account) -> Optional[Ad]:
        """Process and save ad data."""
        try:
            ad_id = ad_data.get('ad_id')
            if not ad_id:
                return None
            
            # Check if ad already exists
            existing_ad = session.query(Ad).filter_by(ad_id=ad_id).first()
            if existing_ad:
                # Update existing ad with new data
                self._update_ad_fields(existing_ad, ad_data, account)
                return existing_ad
            
            # Create new ad
            ad = Ad(
                ad_id=ad_id,
                list_id=ad_data.get('list_id'),
                list_time=ad_data.get('list_time'),
                state=ad_data.get('state'),
                type=ad_data.get('type'),
                region=ad_data.get('region'),
                category=ad_data.get('category'),
                subject=ad_data.get('subject'),
                body=ad_data.get('body'),
                image=ad_data.get('image'),
                status=ad_data.get('status'),
                commercial_type=ad_data.get('commercial_type'),
                size=ad_data.get('size'),
                area=ad_data.get('area'),
                longitude=ad_data.get('longitude'),
                latitude=ad_data.get('latitude'),
                property_legal_document=ad_data.get('property_legal_document'),
                region_v2=ad_data.get('region_v2'),
                area_v2=ad_data.get('area_v2'),
                ward=ad_data.get('ward'),
                furnishing_sell=ad_data.get('furnishing_sell'),
                street_name=ad_data.get('street_name'),
                location_id=ad_data.get('location_id'),
                unique_street_id=ad_data.get('unique_street_id'),
                is_main_street=ad_data.get('is_main_street'),
                location=ad_data.get('location'),
                date=ad_data.get('date'),
                category_name=ad_data.get('category_name'),
                area_name=ad_data.get('area_name'),
                region_name=ad_data.get('region_name'),
                price_string=ad_data.get('price_string'),
                webp_image=ad_data.get('webp_image'),
                number_of_images=ad_data.get('number_of_images'),
                ward_name=ad_data.get('ward_name'),
                pty_map=ad_data.get('pty_map'),
                pty_map_modifier=ad_data.get('pty_map_modifier'),
                thumbnail_image=ad_data.get('thumbnail_image'),
                size_unit_string=ad_data.get('size_unit_string'),
                contain_videos=ad_data.get('contain_videos'),
                account_id_fk=account.id if account else None
            )
            
            session.add(ad)
            session.flush()  # Get the ID
            return ad
            
        except IntegrityError as e:
            logger.warning(f"Ad {ad_id} already exists: {e}")
            session.rollback()
            return session.query(Ad).filter_by(ad_id=ad_id).first()
        except Exception as e:
            logger.error(f"Error processing ad {ad_data.get('ad_id')}: {e}")
            return None
    
    def _update_ad_fields(self, ad: Ad, ad_data: Dict[str, Any], account: Account) -> None:
        """Update existing ad with new data."""
        # Update fields that might change
        ad.list_time = ad_data.get('list_time', ad.list_time)
        ad.state = ad_data.get('state', ad.state)
        ad.status = ad_data.get('status', ad.status)
        ad.subject = ad_data.get('subject', ad.subject)
        ad.body = ad_data.get('body', ad.body)
        ad.image = ad_data.get('image', ad.image)
        ad.webp_image = ad_data.get('webp_image', ad.webp_image)
        ad.thumbnail_image = ad_data.get('thumbnail_image', ad.thumbnail_image)
        ad.number_of_images = ad_data.get('number_of_images', ad.number_of_images)
        ad.contain_videos = ad_data.get('contain_videos', ad.contain_videos)
        ad.price_string = ad_data.get('price_string', ad.price_string)
        if account:
            ad.account_id_fk = account.id
    
    def _process_ad_images(self, session: Session, ad_data: Dict[str, Any], ad: Ad) -> int:
        """Process and save ad images."""
        if not ad:
            return 0
        
        count = 0
        
        try:
            # Clear existing images for this ad
            session.query(AdImage).filter_by(ad_id_fk=ad.id).delete()
            
            # Process main images
            images = ad_data.get('images', [])
            for image_url in images:
                ad_image = AdImage(
                    ad_id_fk=ad.id,
                    image_url=image_url,
                    image_type='regular'
                )
                session.add(ad_image)
                count += 1
            
            # Process thumbnail images
            image_thumbnails = ad_data.get('image_thumbnails', [])
            for img_thumb in image_thumbnails:
                if isinstance(img_thumb, dict):
                    # Add full size image
                    if img_thumb.get('image'):
                        ad_image = AdImage(
                            ad_id_fk=ad.id,
                            image_url=img_thumb['image'],
                            thumbnail_url=img_thumb.get('thumbnail'),
                            image_type='regular'
                        )
                        session.add(ad_image)
                        count += 1
            
            # Process webp image
            if ad_data.get('webp_image'):
                ad_image = AdImage(
                    ad_id_fk=ad.id,
                    image_url=ad_data['webp_image'],
                    image_type='webp'
                )
                session.add(ad_image)
                count += 1
            
        except Exception as e:
            logger.error(f"Error processing images for ad {ad.ad_id}: {e}")
        
        return count
    
    def _process_ad_parameters(self, session: Session, ad_data: Dict[str, Any], ad: Ad) -> int:
        """Process and save ad parameters."""
        if not ad:
            return 0
        
        count = 0
        
        try:
            # Clear existing parameters for this ad
            session.query(AdParameter).filter_by(ad_id_fk=ad.id).delete()
            
            # Process parameters
            params = ad_data.get('params', [])
            for param in params:
                if isinstance(param, dict):
                    ad_param = AdParameter(
                        ad_id_fk=ad.id,
                        param_id=param.get('id', ''),
                        value=param.get('value', ''),
                        label=param.get('label', '')
                    )
                    session.add(ad_param)
                    count += 1
            
        except Exception as e:
            logger.error(f"Error processing parameters for ad {ad.ad_id}: {e}")
        
        return count

    def get_stats(self) -> Dict[str, int]:
        """
        Get current database statistics.
        
        Returns:
            Dict[str, int]: Current counts of records in database
        """
        session = self.db_manager.get_session()
        try:
            stats = {
                "accounts": session.query(Account).count(),
                "ads": session.query(Ad).count(),
                "images": session.query(AdImage).count(),
                "parameters": session.query(AdParameter).count()
            }
            return stats
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {"accounts": 0, "ads": 0, "images": 0, "parameters": 0}
        finally:
            session.close()
    
    def get_recent_ads(self, limit: int = 10) -> List[Ad]:
        """
        Get most recently created ads.
        
        Args:
            limit (int): Maximum number of ads to return
            
        Returns:
            List[Ad]: List of recent Ad objects
        """
        session = self.db_manager.get_session()
        try:
            ads = session.query(Ad).order_by(Ad.created_at.desc()).limit(limit).all()
            return ads
        except Exception as e:
            logger.error(f"Error getting recent ads: {e}")
            return []
        finally:
            session.close()
    
    def clear_all_data(self) -> bool:
        """
        Clear all data from database tables.
        WARNING: This will delete all data!
        
        Returns:
            bool: True if successful, False otherwise
        """
        session = self.db_manager.get_session()
        try:
            # Delete in order to avoid foreign key constraints
            session.query(AdParameter).delete()
            session.query(AdImage).delete()
            session.query(Ad).delete()
            session.query(Account).delete()
            session.commit()
            logger.info("All data cleared from database")
            return True
        except Exception as e:
            logger.error(f"Error clearing database: {e}")
            session.rollback()
            return False
        finally:
            session.close()
