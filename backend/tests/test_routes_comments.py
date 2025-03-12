import pytest
from fastapi import status

from settings import (IS_AI_MODERATION_ENABLED, MAX_COMMENT_LENGTH,
                      MIN_COMMENT_LENGTH)
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


async def test_get_all_comments_endpoint_with_full_db(
        test_client, fill_database_with_comments):
    async with test_client:
        response = await test_client.get('/comments/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == generic_number


async def test_get_unxisted_one_comment_endpoint(test_client):
    async with test_client:
        response = await test_client.get('/comments/1')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.text == '{"message":"Comment not found"}'


async def test_get_existed_one_comment_endpoint(
        test_client, fill_database_with_comments):
    async with test_client:
        response = await test_client.get('/comments/1')
    response_dict: dict = response.json()
    censored_text = response_dict.get('censored_text')
    assert response.status_code == status.HTTP_200_OK
    assert 'username' in response_dict
    assert 'id' in response_dict
    assert 'censored_text' in response_dict

    assert isinstance(censored_text, str)
    assert len(censored_text) < MAX_COMMENT_LENGTH
    assert len(censored_text) > MIN_COMMENT_LENGTH


@pytest.mark.skipif(
        IS_AI_MODERATION_ENABLED is True, reason="Test skipped AI is ON")
async def test_create_comment_endpoint_successfully(
        test_client, get_comment_data_in_json):
    async with test_client:
        response = await test_client.post(
            '/comments/', content=get_comment_data_in_json)
    comment_id = response.json().get('comment_id')
    assert response.status_code == status.HTTP_201_CREATED
    assert comment_id == 1


@pytest.mark.skipif(
        IS_AI_MODERATION_ENABLED is True, reason="Test skipped AI is ON")
async def test_create_comment_endpoint_with_wrong_data(
        test_client, get_empty_json):
    async with test_client:
        response = await test_client.post(
            '/comments/', content=get_empty_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.skipif(
        IS_AI_MODERATION_ENABLED is True, reason="Test skipped AI is ON")
async def test_update_comment_endpoint_successfully(
        test_client,
        fill_database_with_comments,
        get_json_for_comment_updating):
    async with test_client:
        response = await test_client.patch(
            '/comments/1',
            content=get_json_for_comment_updating
            )
    response_detail = response.json().get('detail')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response_detail, str)
    assert response_detail == 'Comment was updated'


@pytest.mark.skipif(
        IS_AI_MODERATION_ENABLED is True, reason="Test skipped AI is ON")
async def test_update_unexisted_comment(
        test_client,
        get_json_for_comment_updating):
    async with test_client:
        response = await test_client.patch(
            '/comments/1',
            content=get_json_for_comment_updating
            )
    response_detail = response.json().get('detail')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_detail is None


@pytest.mark.skipif(
        IS_AI_MODERATION_ENABLED is True, reason="Test skipped AI is ON")
async def test_update_comment_with_post_method(
        test_client,
        fill_database_with_comments,
        get_json_for_comment_updating):
    async with test_client:
        response = await test_client.post(
            '/comments/1',
            content=get_json_for_comment_updating
            )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.skipif(
        IS_AI_MODERATION_ENABLED is True, reason="Test skipped AI is ON")
async def test_update_comment_with_put_method(
        test_client,
        fill_database_with_comments,
        get_json_for_comment_updating):
    async with test_client:
        response = await test_client.put(
            '/comments/1',
            content=get_json_for_comment_updating
            )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


async def test_delete_comment_endpoint_successfully(
        test_client, fill_database_with_comments):
    async with test_client:
        response = await test_client.delete('/comments/1')
    response_detail = response.json().get('detail')
    assert response.status_code == status.HTTP_200_OK
    assert response_detail == 'Comment with id=1 deleted'


async def test_delete_unexisted_comment(test_client):
    async with test_client:
        response = await test_client.delete('/comments/1')
    response_detail = response.json().get('detail')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_detail is None
