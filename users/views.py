import json
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from users.models import User, Location


class List_users_View(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(total_ads=Count('ad'))
        response = []
        for elem in self.object_list.order_by("username"):
            dict_obj = vars(elem)
            dict_obj.update({
                "total_ads": elem.total_ads,
                "locations": list(map(str, elem.locations.all()))})
            dict_obj.pop('_state')
            response.append(dict_obj)
        return JsonResponse(response, safe=False, status=200)


class Users_Detail_View(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        elem = self.get_object()
        dict_obj = vars(elem)
        dict_obj.update({"locations": list(map(str, elem.locations.all()))})
        dict_obj.pop('_state')
        return JsonResponse(dict_obj, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Users_Create_View(CreateView):
    model = User

    def post(self, request, *args, **kwargs):
        add_data = json.loads(request.body)
        locations = add_data["locations"]
        add_data.pop("locations")
        new_obj = self.model.objects.create(**add_data)
        for location_name in locations:
            location, _ = Location.objects.get_or_create(name=location_name)
            new_obj.locations.add(location)

        dict_obj = vars(new_obj)
        dict_obj.update({"locations": list(map(str, new_obj.locations.all()))})
        try:
            dict_obj.pop('_state')
        except:
            pass
        return JsonResponse(dict_obj, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Users_Update_View(UpdateView):
    model = User

    def patch(self, request, *args, **kwargs):
        apd_data = json.loads(request.body)
        locations = apd_data["locations"]
        apd_data.pop("locations")
        self.model.objects.filter(id=kwargs["pk"]).update(**apd_data)

        upd_obj = self.get_object()
        upd_obj.locations.clear()
        for location_name in locations:
            location, _ = Location.objects.get_or_create(name=location_name)
            upd_obj.locations.add(location)
        dict_obj = vars(upd_obj)
        dict_obj.update({"locations": list(map(str, upd_obj.locations.all()))})
        try:
            dict_obj.pop('_state')
        except:
            pass
        return JsonResponse(dict_obj, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Users_Delete_View(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


