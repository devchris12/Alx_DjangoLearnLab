from django.urls import path, include

urlpatterns = [
    # ... other patterns
    path('', include('relationship_app.urls')),
]
