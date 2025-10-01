import pytest
import asyncio


@pytest.mark.asyncio
async def test_shorten_url(client):
    response = await client.post("/url/shorten", json={"original_url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_id" in data
    assert data["original_url"] == "https://example.com"


@pytest.mark.asyncio
async def test_redirect_url(client):
    # Shorten first
    response = await client.post("/url/shorten", json={"original_url": "https://google.com"})
    assert response.status_code == 200
    short_id = response.json()["short_id"]

    # Wait to simulate redirect (but before expiration)
    await asyncio.sleep(1)
    response = await client.get(f"/url/{short_id}", follow_redirects=False)
    assert response.status_code == 307  # FastAPI returns 307 for RedirectResponse
    assert response.headers["location"] == "https://google.com"


@pytest.mark.asyncio
async def test_expired_url(client):
    # Create short URL with short expiry manually
    response = await client.post("/url/shorten", json={"original_url": "https://expired.com"})
    short_id = response.json()["short_id"]

    await asyncio.sleep(31)  # Assuming 30 sec expiry
    response = await client.get(f"/url/{short_id}")
    assert response.status_code == 410
