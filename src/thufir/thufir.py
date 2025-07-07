import uvicorn


def dev():
    uvicorn.run("src.thufir.api.api:app", port=8000, reload=True)
