import celery
from celery.utils.log import get_task_logger
from .utils import MarketHero

logger = get_task_logger(__name__)

@celery.shared_task
def add_user_to_maillist(email, first_name, last_name):
    MarketHero.tag_lead(email=email, first_name=first_name, last_name=last_name)
