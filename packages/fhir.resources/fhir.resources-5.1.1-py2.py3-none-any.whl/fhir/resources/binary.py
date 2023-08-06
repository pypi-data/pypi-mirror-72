# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/StructureDefinition/Binary
Release: R4
Version: 4.0.1
Build ID: 9346c8cc45
Last updated: 2019-11-01T09:29:23.356+11:00
"""


import sys

from . import resource


class Binary(resource.Resource):
    """ Pure binary content defined by a format other than FHIR.

    A resource that represents the data of a single raw artifact as digital
    content accessible in its native format.  A Binary resource can contain any
    content, whether text, image, pdf, zip archive, etc.
    """

    resource_type = "Binary"

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.

        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """

        self.contentType = None
        """ MimeType of the binary content.
        Type `str`. """

        self.data = None
        """ The actual content.
        Type `str`. """

        self.securityContext = None
        """ Identifies another resource to use as proxy when enforcing access
        control.
        Type `FHIRReference` referencing `['Resource']` (represented as `dict` in JSON). """

        super(Binary, self).__init__(jsondict=jsondict, strict=strict)

    def elementProperties(self):
        js = super(Binary, self).elementProperties()
        js.extend(
            [
                ("contentType", "contentType", str, "code", False, None, True),
                ("data", "data", str, "base64Binary", False, None, False),
                (
                    "securityContext",
                    "securityContext",
                    fhirreference.FHIRReference,
                    "Reference",
                    False,
                    None,
                    False,
                ),
            ]
        )
        return js


try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + ".fhirreference"]
