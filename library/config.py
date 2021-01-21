from datetime import datetime

class Config:
    """
    Config is a class that stores information about the configuration of a given dataset
    """

    def __init__(self, config:dict):
        self.schema_name =  config.get("schema_name", "")
        self.version_name = config.get("version_name", "")
        self.path =         config.get("path", "")
        self.layerCreationOptions = config.get("layerCreationOptions", ["OVERWRITE=YES"])
        self.dstSRS =       config.get("dstSRS", "EPSG:4326")
        self.srcSRS =       config.get("srcSRS", "EPSG:4326")
        self.geometryType = config.get("geometryType", "NONE")
        self.SQLStatement = config.get("SQLStatement", None)
        self.srcOpenOptions = config.get(
            "srcOpenOptions", ["AUTODETECT_TYPE=NO", "EMPTY_STRING_AS_NULL=YES"]
        )
        self.newFieldNames = config.get("newFieldNames", [])
        self.version = (
            datetime.today().strftime("%Y/%m/%d")
            if self.version_name == ""
            else self.version_name
        )
        self.layerName = f"{self.schema_name}.{self.version}"