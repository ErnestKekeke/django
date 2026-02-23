from django.core.management.base import BaseCommand
from api.models import Post
# from api.models import Post, Store
from faker import Faker

class Command(BaseCommand):
    help = "Seed the database with initial posts"

    def handle(self, *args, **kwargs):
        fake = Faker()
        # Seed Posts
        for _ in range(10):
            Post.objects.create(title=fake.sentence(), body=fake.text())

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

        # # Seed Stores
        # for _ in range(20):
        #     Store.objects.create(name=fake.company(), location=fake.city())    
        # self.stdout.write(self.style.SUCCESS(f"{len(stores)} stores created"))
