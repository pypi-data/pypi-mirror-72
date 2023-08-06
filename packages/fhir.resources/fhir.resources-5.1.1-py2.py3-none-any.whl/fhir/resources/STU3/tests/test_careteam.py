# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/StructureDefinition/CareTeam
Release: STU3
Version: 3.0.2
Revision: 11917
Last updated: 2019-10-24T11:53:00+11:00
"""

import io
import json
import os
import unittest

import pytest

from .. import careteam
from ..fhirdate import FHIRDate
from .fixtures import force_bytes


@pytest.mark.usefixtures("base_settings")
class CareTeamTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get("FHIR_UNITTEST_DATADIR") or ""
        with io.open(os.path.join(datadir, filename), "r", encoding="utf-8") as handle:
            js = json.load(handle)
            self.assertEqual("CareTeam", js["resourceType"])
        return careteam.CareTeam(js)

    def testCareTeam1(self):
        inst = self.instantiate_from("careteam-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a CareTeam instance")
        self.implCareTeam1(inst)

        js = inst.as_json()
        self.assertEqual("CareTeam", js["resourceType"])
        inst2 = careteam.CareTeam(js)
        self.implCareTeam1(inst2)

    def implCareTeam1(self, inst):
        self.assertEqual(
            force_bytes(inst.category[0].coding[0].code), force_bytes("encounter")
        )
        self.assertEqual(
            force_bytes(inst.category[0].coding[0].system),
            force_bytes("http://hl7.org/fhir/care-team-category"),
        )
        self.assertEqual(force_bytes(inst.contained[0].id), force_bytes("pr1"))
        self.assertEqual(force_bytes(inst.id), force_bytes("example"))
        self.assertEqual(force_bytes(inst.identifier[0].value), force_bytes("12345"))
        self.assertEqual(
            force_bytes(inst.name),
            force_bytes("Peter James Charlmers Care Plan for Inpatient Encounter"),
        )
        self.assertEqual(
            force_bytes(inst.participant[0].role.text), force_bytes("responsiblePerson")
        )
        self.assertEqual(
            inst.participant[1].period.end.date, FHIRDate("2013-01-01").date
        )
        self.assertEqual(inst.participant[1].period.end.as_json(), "2013-01-01")
        self.assertEqual(
            force_bytes(inst.participant[1].role.text), force_bytes("adviser")
        )
        self.assertEqual(inst.period.end.date, FHIRDate("2013-01-01").date)
        self.assertEqual(inst.period.end.as_json(), "2013-01-01")
        self.assertEqual(force_bytes(inst.status), force_bytes("active"))
        self.assertEqual(
            force_bytes(inst.text.div),
            force_bytes('<div xmlns="http://www.w3.org/1999/xhtml">Care Team</div>'),
        )
        self.assertEqual(force_bytes(inst.text.status), force_bytes("generated"))
