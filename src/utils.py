import requests

# reference:
# https://gis.stackexchange.com/questions/212796/getting-latlon-extent-of-country-by-its-name-using-python
def get_boundingbox_or_center_of_a_country(country: str, output_as="center"):
    """
    get the bounding box of a country in EPSG4326 given a country name

    Parameters
    ----------
    country : str
        name of the country in english and lowercase
    output_as : 'str
        chose from 'boundingbox' or 'center'.
         - 'boundingbox' for [latmin, latmax, lonmin, lonmax]
         - 'center' for [latcenter, loncenter]

    Returns
    -------
    output : list
        list with coordinates as str
    """
    try:
        # create url
        url = "{0}{1}{2}".format(
            "http://nominatim.openstreetmap.org/search?country=",
            country,
            "&format=json&polygon=0",
        )
        response = requests.get(url).json()[0]

        # parse response to list
        if output_as == "boundingbox":
            lst = response[output_as]
            output = [float(i) for i in lst]
        if output_as == "center":
            lst = [response.get(key) for key in ["lat", "lon"]]
            output = [float(i) for i in lst]
        return output
    except:
        print(
            f"Warning, country {country}'s boudingbox or center info can not be found"
        )
        return [None, None]


if __name__ == "__main__":
    print(get_boundingbox_or_center_of_a_country(country="netherlands"))
    print(get_boundingbox_or_center_of_a_country(country="USA"))
