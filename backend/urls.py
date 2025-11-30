from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path(
        "", RedirectView.as_view(url="/static/index.html", permanent=False)
    ),  # root -> frontend index
    path("admin/", admin.site.urls),
    path("api/tasks/", include("tasks.urls")),
]
