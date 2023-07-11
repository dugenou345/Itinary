# data to be selected from mongodb with aggregate()

# List of specific keys to match and Field mappings
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
