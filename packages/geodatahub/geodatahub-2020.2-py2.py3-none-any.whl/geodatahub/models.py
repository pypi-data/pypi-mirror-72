#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class Dataset(object):

    '''
    Create a dataset object through the current GeoDataHub connection.

    :param id: Identifier
    :type id: int
    :param owner: Owner
    :type owner: int
    :param Organization: Elevation at well top [m]
    :type Organization: int
    :param type: Data type
    :type type: str
    :param parent: Source of the data
    :type parent: int
    :param datalink: Location of the data
    :type datalink: json
    :param metadata: Additional metadata
    :type metadata: json
    :param geom: Geometry
    :type geom: str
    '''

    def __init__(self,
                 datatype,
                 projected_geometry,
                 result,
                 distribution_info,
                 identifier = None,
                 description = None,
                 larger_work = None,
                 citation = None,
                 created_at = None,
                 updated_at = None,
                 owner = None,
                 organization = None,
                 disable_validation = False):
        self.identifier = identifier
        self.projected_geometry = projected_geometry
        self.datatype = datatype
        self.owner = owner
        self.organization = organization
        self.larger_work = larger_work
        self.result = result
        self.description = description
        self.distribution_info = distribution_info

    @classmethod
    def fromJSON(cls, json_dict):
        '''
        Create a well object from values in JSON dictionary.

        :param json_dict: Dictionary containing well key and value pairs.
        :type json_dict: dict
        :rtype: geodatahub.well
        '''
        return cls(lat=json_dict['geom']['lat'],
                   lng=json_dict['geom']['lng'],
                   datatype=json_dict['type'],
                   orgnization=json_dict['organization'],
                   owner=json_dict['owner'],
                   parent=json_dict['parent'],
                   geophResult=json_dict['geophResult'],
                   metadata=json_dict['metadata'],
                   identifier=json_dict["identifier"])

    def toJSON(self):
        '''
        Return dataset metadata in JSON formatted string.

        :rtype: str
        '''
        json_str = json.dumps(self, default=lambda o: o.__dict__,
                              sort_keys=True, indent=4)
        return json.loads(json_str)

    def geom_to_wkt(self):
        '''Convert the geometry to WKT format
        '''
        geom_type = self.projected_geometry['type'].upper()
        coords = self.projected_geometry['coordinates']
        coords_str = ""

        if geom_type == "POLYGON":
            for c in coords:
                coords_str += "(("
                for itt, (x, y) in enumerate(c):
                    if itt < len(c) - 1:
                        coords_str += f"{x} {y}, "
                    else:
                        coords_str += f"{x} {y}"
            coords_str += "))"
        elif geom_type == "POINT":
            coords_str = f"({coords[0]} {coords[1]})"
        elif geom_type == "LINESTRING":
            coords_str += "("
            for itt, c in enumerate(coords):
                x, y = c
                if itt < len(coords) - 1:
                    coords_str += f"{x} {y}, "
                else:
                    coords_str += f"{x} {y}"
            coords_str += ")"
        else:
            if "MULTI" in geom_type:
                raise NotImplementedError("Multi-geometry types are currently not supported")
            else:
                raise NotImplementedError("The geometry type {geom_type} is not supported")

        wkt = f"{geom_type} {coords_str}"
        return wkt

    def __repr__(self):
        """Format the class when printing parameters
        """
        dataset_str = "\n"
        for attr in ["identifier", "datatype", "description", "distribution_info", "projected_geometry"]:
            if self.__dict__[attr] is not None:
                dataset_str += "{:10} {:10}\n".format(attr, str(self.__dict__[attr]))
        return dataset_str
