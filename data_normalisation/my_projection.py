# data to be selected from mongodb with aggregate()

# List of specific keys to match
keys_to_match = ['dc:identifier',
                 'rdfs:label.fr',
#                 'hasContact.schema:email',
#                'schema:telephone',
#                 'hasDescription.shortDescription.fr',
#                 'hasTheme.rdfs:label.fr',
                 'isLocatedAt.schema:address.schema:addressLocality',
                 'isLocatedAt.schema:address.schema:postalCode',
                 'isLocatedAt.schema:address.schema:streetAddress',
                 'isLocatedAt.schema:address.hasAddressCity.isPartOfDepartment.rdfs:label.fr',
                 'isLocatedAt.schema:address.hasAddressCity.isPartOfDepartment.isPartOfRegion.rdfs:label.fr',
                 'isLocatedAt.schema:geo.schema:latitude',
                 'isLocatedAt.schema:geo.schema:longitude',
#                 'isLocatedAt.schema:openingHoursSpecification.schema:validFrom',
#                 'isLocatedAt.schema:openingHoursSpecification.schema:validThrough',
#                 'offers.schema:priceSpecification.schema:maxPrice',
#                 'offers.schema:priceSpecification.schema:minPrice',
#                 'offers.schema:priceSpecificationschema:priceCurrency',
#                 'hasReview.hasReviewValue.rdfs:label.fr'
               ]


# Field mappings
field_mappings = {
    "dc:identifier": "identifier",
    "rdfs:label.fr": "label",
#    "hasContact.schema:email": "email",
#    'schema:telephone': 'telephone',
#    'hasDescription.shortDescription.fr': 'shortdescription',
#    'hasTheme.rdfs:label.fr': 'label',
    'isLocatedAt.schema:address.schema:streetAddress': 'streetaddress',
    'isLocatedAt.schema:address.schema:postalCode': 'postalcode',
    'isLocatedAt.schema:address.hasAddressCity.isPartOfDepartment.rdfs:label.fr': 'department',
    'isLocatedAt.schema:address.hasAddressCity.isPartOfDepartment.isPartOfRegion.rdfs:label.fr': 'region',
    'isLocatedAt.schema:geo.schema:latitude': 'latitude',
    'isLocatedAt.schema:geo.schema:longitude': 'longitude',
#    'isLocatedAt.schema:openingHoursSpecification.schema:validFrom': 'validfrom',
#    'isLocatedAt.schema:openingHoursSpecification.schema:validThrough': 'validthrough',
    'offers.schema:priceSpecification.schema:maxPrice': 'maxprice',
    'offers.schema:priceSpecification.schema:minPrice': 'minprice',
    'offers.schema:priceSpecificationschema:priceCurrency': 'pricecurrency',
    'hasReview.hasReviewValue.rdfs:label.fr': 'review'
}

# List of field names to project
fields_to_project = list(field_mappings.values())

# Aggregate query using match and projection
"""
pipeline = [
    { "$match": { "$or": [ { key: { "$exists": True } } for key in field_mappings.keys() ] } },
    { "$project": { field_mappings[field]: f"${field}" for field in field_mappings.keys() } }
]
"""
"""
pipeline = [
    { "$match": { "$or": [ { key: { "$exists": True } } for key in field_mappings.keys() ] } },
    { "$project": { field_mappings[field]: { "$toInt": f"${field}" } if field_mappings[field] == "isLocatedAt.schema:geo.schema:latitude" else f"${field}" for field in field_mappings.keys() } }
]
"""
"""
pipeline = [
    { "$match": { "$or": [ { key: { "$exists": True } } for key in field_mappings.keys() ] } },
    {
        "$project": {
            field_mappings[field]: {
                "$cond": {
                    "if": { "$eq": [field_mappings[field], "latitude"] },
#                    "if": { "$eq": [field_mappings[field], "isLocatedAt.schema:geo.schema:latitude"] },
                    "then": { "$toDouble": { "$arrayElemAt": [f"${field}", 0] } },
                    #"then": { "$toInt": { "$toDouble": { "$arrayElemAt": [f"${field}", 0] } } },
                    "else": f"${field}"
                }
            }
            for field in field_mappings.keys()
        }
    }
]
"""

pipeline = [
    { "$match": { "$or": [ { key: { "$exists": True } } for key in field_mappings.keys() ] } },
    {
        "$project": {
            field_mappings[field]: {
                "$switch": {
                    "branches": [
                        {
                            "case": { "$eq": [field_mappings[field], "latitude"] },
                            "then": { "$toDouble": { "$arrayElemAt": [f"${field}", 0] } }
                        },
                        {
                            "case": { "$eq": [field_mappings[field], "longitude"] },
                            "then": { "$toDouble": { "$arrayElemAt": [f"${field}", 0] } }
                        },
                        # Add more branches as needed
                    ],
                    "default": f"${field}"  # Default value if none of the cases match
                }
            }
            for field in field_mappings.keys()
        }
    }
]

""""
my_projection = {
        "dc:identifier": 1,
        "hasContact": {
            "schema:email": 1,
            "schema:telephone": 1
        },
        "hasDescription": {
            "shortDescription": {
                "fr": 1
            }
        },
        "hasTheme": {
            "rdfs:label": {
                "fr": 1
            }
        },
        "isLocatedAt" : {
            "schema:address" : {
                "schema:addressLocality": 1,
                "schema:postalCode": 1,
                "schema:streetAddress": 1,
                "hasAddressCity": {
                    "rdfs:label": {
                        "fr": 1
                    },
                    "isPartOfDepartment": {
                        "rdfs:label": {
                            "fr": 1
                        },
                    "isPartOfRegion": {
                        "rdfs:label": {
                            "fr": 1
                        }
                    }
                    }
                }
            },
            "schema:geo": {
                "schema:latitude": 1,
                "schema:longitude": 1
            },
            "schema:openingHoursSpecification":{
                "schema:validFrom": 1,
                "schema:validThrough": 1
            }
        },
        "offers":{
            "schema:priceSpecification": {
                "schema:maxPrice": 1,
                "schema:minPrice": 1,
                "schema:priceCurrency": 1
            }
        },
        "hasReview": {
            "hasReviewValue": {
                "rdfs:label": {
                    "fr": 1,
                }
            }
        }
}
"""