import json

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.csv_v_ads import load_data_cats, load_data_ads
from ads.models import Category, Ad
from users.csv_v_users import load_data_locations, load_data_users
from users.models import User


def index_ads(request):
    return JsonResponse({"status": "ok"}, status=200)


def csv_in_bd(request):
    """загружаем данные в БД"""
    return JsonResponse({
        "locations": str(load_data_locations()),
        "users": str(load_data_users()),
        "cats": str(load_data_cats()),
        "ads": str(load_data_ads()),
    })


class Ads_Ad_List_View(ListView):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related('author').order_by("-price")
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ads = []
        for elem in page_obj:
            dict_obj = vars(elem)
            dict_obj.pop('_state')
            ads.append(dict_obj)
        response = {
            "items": ads,
            "total": page_obj.paginator.count,
            "num_pages": page_obj.paginator.num_pages,

        }
        return JsonResponse(response, safe=False, status=200)


class Ads_Cat_List_View(ListView):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = []
        for elem in self.object_list.order_by("name"):
            dict_obj = vars(elem)
            dict_obj.pop('_state')
            response.append(dict_obj)
        return JsonResponse(response, safe=False, status=200)


class Ads_Loc_List_View(ListView):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = []
        for elem in self.object_list:
            dict_obj = vars(elem)
            dict_obj.pop('_state')
            response.append(dict_obj)
        return JsonResponse(response, safe=False, status=200)


class Ads_Detail_View(DetailView):  # общий класс для детальных записей (model задается в urls)
    def get(self, request, *args, **kwargs):
        elem = self.get_object()
        dict_obj = vars(elem)
        dict_obj.pop('_state')
        return JsonResponse(dict_obj, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Ads_Create_View(CreateView):  # общий класс (кроме Ad) для создания записей (model задается в urls)
    def post(self, request, *args, **kwargs):
        add_data = json.loads(request.body)
        new_obj = self.model.objects.create(**add_data)
        dict_obj = vars(new_obj)
        dict_obj.pop('_state')
        return JsonResponse(dict_obj, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Ads_Ad_Create_View(CreateView):  # класс для создания Ad
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        add_data = json.loads(request.body)
        author = get_object_or_404(User, add_data["author_id"])
        category = get_object_or_404(Category, add_data["category_id"])

        new_obj = Ad.objects.create(
            name=add_data["name"],
            author=author,
            price=add_data["price"],
            description=add_data["description"],
            is_published=add_data["is_published"],
            category=category,
        )
        dict_obj = vars(new_obj)
        try:
            dict_obj["image"] = dict_obj["image"].url
        except:
            dict_obj["image"] = None
        dict_obj.pop('_state')
        return JsonResponse(dict_obj, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Ads_Update_View(UpdateView):  # общий класс для изменения (model задается в urls)
    def patch(self, request, *args, **kwargs):
        apd_data = json.loads(request.body)
        self.model.objects.filter(id=kwargs["pk"]).update(**apd_data)

        new_obj = self.get_object()
        dict_obj = vars(new_obj)
        try:
            dict_obj["image"] = dict_obj["image"].url
        except:
            dict_obj["image"] = None
        dict_obj.pop('_state')
        return JsonResponse(dict_obj, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Ads_Delete_View(DeleteView):  # общий класс для удаления (model задается в urls)
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Ads_Image_View(UpdateView):  # работа с картинками
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        image_url = None
        if self.object.image:
            image_url = self.object.image.url
        self.object.save()

        dict_obj = vars(self.object)
        dict_obj.update({"image": image_url})
        dict_obj.pop('_state')
        return JsonResponse(dict_obj, status=200)
