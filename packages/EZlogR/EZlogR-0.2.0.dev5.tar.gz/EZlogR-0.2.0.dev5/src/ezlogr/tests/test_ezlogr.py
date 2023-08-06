def test_ezlogr():
    from ezlogr import pylogr
    tags = ["Very cool app", "non-prod"]
    filename = __file__
    logger = pylogr.Ezlogr(filename=filename, tags=tags)
    logger.info("Here I go writin' logs!")
    
