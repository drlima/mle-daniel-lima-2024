from strenum import StrEnum


# TODO: think about using a TypeDict instead of StrEnum
class Predictors(StrEnum):
    TYPE = "type"
    SECTOR = "sector"
    NET_USABLE_AREA = "net_usable_area"
    NET_AREA = "net_area"
    N_ROOMS = "n_rooms"
    N_BATHROOM = "n_bathroom"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"

    @classmethod
    def categorical(cls):
        return [str(cls.TYPE), str(cls.SECTOR)]


class TargetColumn(StrEnum):
    PRICE = "price"
