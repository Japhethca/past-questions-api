
def to_str(slug):
    """
    converts slug to str
    :param slug:
    :return: str
    """
    if not isinstance(slug, str):
        raise ValueError("to_str expects arguments of type 'str'")

    return ' '.join(slug.split('-'))

