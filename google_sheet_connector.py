from auth import get_client


def get_google_sheet(key: str):
    client = get_client()
    sheet = client.open_by_key(key)
    return sheet

