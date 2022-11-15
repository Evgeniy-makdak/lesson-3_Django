import csv

from ads.models import Ad, Category
from users.models import User

# загрузка данных а БД

def load_data_cats():
    with open(f'datasets/category.csv', encoding="utf-8") as csvfile:
        rows_data = list(csv.DictReader(csvfile))
    for row_data in rows_data:
        cat = Category(
            name=row_data["name"],
        )
        try:
            cat.save()
        except:
            return False
    return True


def load_data_ads():
    with open(f'datasets/ad.csv', encoding="utf-8") as csvfile:
        rows_data = list(csv.DictReader(csvfile))
    for row_data in rows_data:
        ad = Ad(
            name=row_data["name"],
            price=int(row_data["price"]),
            description=row_data["description"],
            is_published=bool(row_data["is_published"]),
            image=row_data["image"],
            author=User.objects.get(id=int(row_data["author_id"])),
            category=Category.objects.get(id=int(row_data["category_id"])),
        )
        try:
            ad.save()
        except:
            return False
    return True
