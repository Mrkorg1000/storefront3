#from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import pytest
from store.models import Collection, Product
from model_bakery import baker
from conftests import api_client

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    #@pytest.mark.skip
    def test_if_user_is_anonimous_returns_401(self, create_collection):
        # Arrange
        #Act
        response = create_collection({'title': 'a'})
        # response = api_client.post('/store/collections/', { 'title': 'a'})
        #Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, api_client):
        # Arrange
        #Act
        api_client.force_authenticate(user={})
        response = api_client.post('/store/collections/', {'title': 'a'})
        #Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_not_valid_returns_400(self, api_client):
        # Arrange
        #Act
        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post('/store/collections/', {'title': ''})
        #Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_if_data_is_valid_returns_201(self, api_client):
        # Arrange
        #Act
        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post('/store/collections/', {'title': 'a'})
        #Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        #Arrange
        collection = baker.make(Collection)
        #baker.make(Product, collection=collection, _quantity=10)
        # creates 10 products of the samr collection
        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }


