from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Company, KBEntry, QueryLog
from .permissions import IsAdminUser
from .serializers import KBEntrySerializer

def generate_access_token(user):
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)

class RegisterView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        company_name = request.data.get("company_name")
        email = request.data.get("email")

        if not username or not password or not company_name or not email:
            return Response(
                {
                    "error": "username, password, company_name and email are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {
                    "error": "Username already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            company = user.company

            company.company_name = company_name
            company.save(update_fields=["company_name"])

        access_token = generate_access_token(user)

        return Response(
            {
                "username": user.username,
                "company_name": company.company_name,
                "api_key": company.api_key,
                "access": access_token,
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response(
                {
                    "error": "Invalid username or password"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = generate_access_token(user)

        company = user.company

        return Response(
            {
                "access": access_token,
                "company_name": company.company_name,
                "api_key": company.api_key,
            },
            status=status.HTTP_200_OK
        )

class KBQueryView(APIView):

    def post(self, request):

        search_term = request.data.get("search")

        if not search_term or not search_term.strip():

            return Response(
                {
                    "error": "search field is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        search_term = search_term.strip()

        company = request.user.company

        with transaction.atomic():

            queryset = KBEntry.objects.filter(
                Q(question__icontains=search_term)
                |
                Q(answer__icontains=search_term)
            )

            count = queryset.count()

            QueryLog.objects.create(
                company=company,
                search_term=search_term,
                results_count=count
            )

            serializer = KBEntrySerializer(
                queryset,
                many=True
            )

        return Response(
            {
                "search": search_term,
                "count": count,
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )

class UsageSummaryView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        total_queries = QueryLog.objects.aggregate(
            total=Count("id")
        )["total"]

        active_companies = (
            QueryLog.objects
            .values("company")
            .distinct()
            .count()
        )

        top_search_terms = (
            QueryLog.objects
            .values("search_term")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        return Response(
            {
                "total_queries": total_queries,
                "active_companies": active_companies,
                "top_search_terms": list(top_search_terms),
            },
            status=status.HTTP_200_OK
        )