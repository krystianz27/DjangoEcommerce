from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import IntegrityError

import logging

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()

    if not User.objects.filter(username="admin").exists():
        try:
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="admin123",
            )
            logger.info("Superuser 'admin' created.")
            print("Superuser 'admin' created")
        except IntegrityError:
            logger.warning("Superuser 'admin' creation failed due to IntegrityError.")
            print("Superuser 'admin' creation failed.")
    else:
        logger.info("Superuser 'admin' already exists.")
        print("Superuser 'admin' already exists")
