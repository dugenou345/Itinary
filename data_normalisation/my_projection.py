# data to be selected from mongodb with find()
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