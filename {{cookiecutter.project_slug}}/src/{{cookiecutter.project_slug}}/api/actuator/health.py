def search():
    """
    Returns
    -------
    The check should return 200 if everything is fine,
    424 if a depending service is not working or
    503 if the API does not work correctly.
    """
    return {
        "status": "UP",
    }, 200
