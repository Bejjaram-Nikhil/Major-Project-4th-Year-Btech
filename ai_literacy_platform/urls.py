from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('accounts/', include('accounts.urls')),
    path('ai-literacy/', include('ai_literacy.urls')),
    path('assessments/', include('assessments.urls')),
    path('curriculum/', include('curriculum.urls')),
    path('inclusivity/', include('inclusivity.urls')),
    path('analytics/', include('analytics.urls')),
    path('ethics/', include('ethics.urls')),
    path('feedback/', include('feedback.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
