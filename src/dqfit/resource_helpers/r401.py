import pandas as pd


class ResourceHelper:
    @staticmethod
    def get_id(resource) -> str:
        return resource["id"]

    @staticmethod
    def get_bundle_index(resource) -> str:
        ## bundle index is feature we made
        return resource.get("bundle_index")

    @staticmethod
    def get_type(resource) -> str:
        return resource["resourceType"]

    @staticmethod
    def get_val(resource):
        return resource["valueQuantity.value"]

    @staticmethod
    def get_date(resource) -> str:
        try:
            resourceType = resource["resourceType"]
            if resourceType == "Patient":
                return None
            elif resourceType == "MedicationDispense":
                date = resource["whenHandedOver"]
            elif resourceType == "Procedure":
                try:
                    # looks like we are out of date
                    date = resource["performedDateTime"]
                except Exception as e:
                    # did this for the synthea data
                    date = resource["performedPeriod.start"]
            elif resourceType == "Condition":
                date = resource.get("onsetDateTime", "")
            elif resourceType == "Observation":
                date = resource["effectiveDateTime"]
            elif resourceType == "Claim":
                date = resource["created"]
            elif resourceType == "Immunization":
                date = resource["occurrenceDateTime"]
            return date[0:10]  # really wish casting to date here wasnt so slow
        except Exception as e:
            print(resourceType, e)

    @staticmethod
    def _get_coding(resource) -> list:
        resourceType = resource["resourceType"]
        if resourceType in ["Patient", "Claim"]:
            return None
        elif resource["resourceType"] == "MedicationDispense":
            return resource["medicationCodeableConcept.coding"]
        elif resource["resourceType"] == "Immunization":
            return resource["vaccineCode.coding"]
        else:
            return resource["code.coding"]

    @staticmethod
    def get_code(resource) -> str:
        try:
            coding = ResourceHelper._get_coding(resource)
            return coding[0]["code"]  # re-eval someday
        except:
            return None

    @staticmethod
    def get_system(resource) -> str:
        try:
            coding = ResourceHelper._get_coding(resource)
            return coding[0]["system"]  # re-eval someday
        except:
            return None

    @staticmethod
    def get_patient_reference(resource):
        try:
            if resource["resourceType"] == "Patient":
                key = f"{resource['id']}"
            elif resource["resourceType"] in ["Claim", "Immunization"]:
                key = resource["patient.reference"]
            else:
                key = resource["subject.reference"]
            key = key.replace("Patient/Patient.", "")
            key = key.replace("urn:uuid:", "")  # from synthea pass
            return key.split(".")[-1]
        except Exception as e:
            print(e, resource)

    @staticmethod
    def get_patient_gender(resource) -> int:
        return resource["gender"]

    # @staticmethod
    # def get_patient_zip5(resource) -> int:
    #     if resource['resourceType'] != "Patient":
    #         return None
    #     try:
    #         return resource['address'][0]['postalCode'][0:5]
    #     except:
    #         return None

    @staticmethod
    def get_patient_age_decile(resource) -> int:
        """
        returns int 0-9
        Enables normalization against US Census, e.g. census max is 85+
        """
        if resource["resourceType"] != "Patient":
            return None

        birth_year = int(resource["birthDate"][0:4])
        age = pd.to_datetime("today").year - birth_year
        if age > 84:
            return 9
        else:
            return int(age / 10)
