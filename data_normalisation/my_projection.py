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
                     }
                }
            }
        }
    }
}