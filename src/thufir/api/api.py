from fastapi import APIRouter

router = APIRouter()


@router.get("/articles/")
def get_all_articles():
    return {"message": "List of all articles"}


@router.get("/channels/{channel_id}/articles/")
def get_all_articles_from_channel(channel_id: int):
    return {"message": f"List of articles from channel {channel_id}"}


@router.get("/articles/{article_id}")
def get_article(article_id: int):
    return {"message": f"Details of article {article_id}"}
