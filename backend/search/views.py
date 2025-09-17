# D:\nam5ky1\ERP\AgriERP\backend\search\views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def search_api(request):
    query = request.query_params.get('q', None)

    if not query:
        return Response({"message": "Search query parameter 'q' is required."}, status=400)

    searchable_items = [
      { 'id': 1, 'type': 'page', 'name': 'Website Management', 'url': '/websites', 'description': 'Manage your company website' },
      { 'id': 2, 'type': 'page', 'name': 'E-commerce Platform', 'url': '/e-commerce', 'description': 'Oversee your online store' },
      { 'id': 3, 'type': 'page', 'name': 'Human Resources (HRM)', 'url': '/hrm', 'description': 'Access employee information' },
    ]
    
    lower_case_query = query.lower()
    
    results = [
        item for item in searchable_items 
        if lower_case_query in item['name'].lower() or lower_case_query in item['description'].lower()
    ]

    return Response(results)