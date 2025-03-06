from fastapi import status
from tests.conftest import generic_number


async def test_unxisted_url(test_client):
    async with test_client:
        response = await test_client.get('/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.text == '{"detail":"Not Found"}'


async def test_get_all_comments_endpoint_with_empty_db(test_client):
    async with test_client:
        response = await test_client.get("/comments/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == '{"message":"There are NO comments yet"}'


async def test_get_all_comments_endpoint_with_full_db(
        test_client, fill_database_with_comments):
    async with test_client:
        response = await test_client.get('/comments/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == generic_number
