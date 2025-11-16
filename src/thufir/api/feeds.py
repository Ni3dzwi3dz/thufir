# from fastapi import APIRouter

# router = APIRouter('/feeds') # TODO: We can declare prefix in config, or other file with such consts

# @router.get("/feeds")
# def get_feeds():
#     '''
#     Returns a list of all feeds that current user subscribes to
#     '''
#     return {"message": "List of feeds"}

# @router.get('/feeds/')


# @router.get("/feeds/{feed_id}")
# def get_feed(feed_id: str):
#     '''
#     Returns a specific feed by its ID
#     '''
#     return {"message": f"Feed {feed_id}"}
