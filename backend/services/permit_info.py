"""
Copenhagen Mobile Vending Permit Information
"""

# Permit status classification
PERMIT_STATUS = {
    "GREEN": {
        "code": "green",
        "label": "Easy Permit",
        "description": "Standard permit applies, generally allowed",
        "color": "#22c55e"
    },
    "YELLOW": {
        "code": "yellow",
        "label": "Moderate Difficulty",
        "description": "May require additional approvals or restrictions apply",
        "color": "#eab308"
    },
    "RED": {
        "code": "red",
        "label": "Special Permit Required",
        "description": "Restricted zone - special permit needed (granted 1-2x/year)",
        "color": "#ef4444"
    }
}

# Define permit status for major Copenhagen locations
LOCATION_PERMITS = {
    # RED ZONE - Special Permit Required (Tourist/Restricted Areas)
    "Nyhavn": "RED",
    "Strøget": "RED",
    "Kongens Nytorv": "RED",
    "The Little Mermaid": "RED",
    "Nørreport Station": "RED",
    "Amalienborg Palace": "RED",
    "Christiansborg Palace": "RED",
    "Tivoli Gardens": "RED",  # Private property
    "Kultorvet": "RED",
    "Islands Brygge Havnebadet": "RED",  # Harbour park - restricted
    
    # YELLOW ZONE - Moderate (Competitive/Some Restrictions)
    "Torvehallerne Market": "YELLOW",
    "The Round Tower": "YELLOW",
    "Rosenborg Castle": "YELLOW",
    "Østerport Station": "YELLOW",
    "Copenhagen Central Station": "YELLOW",
    "Christianshavn Metro": "YELLOW",
    "Magasin du Nord": "YELLOW",
    "Fisketorvet Shopping Center": "YELLOW",
    "The King's Garden": "YELLOW",
    "Kastellet": "YELLOW",
    "Langelinie Promenade": "YELLOW",  # Near Little Mermaid
    "Reffen Street Food": "YELLOW",  # Market area
    
    # GREEN ZONE - Easy Permit (Residential/Parks/Open Areas)
    "Frederiksberg Gardens": "GREEN",
    "Fælled Park": "GREEN",
    "Amager Strandpark": "GREEN",
    "Nørrebro": "GREEN",
    "Vesterbro": "GREEN",
    "Østerbro": "GREEN",
    "Frederiksberg": "GREEN",
    "Christianshavn": "GREEN",
    "Islands Brygge": "GREEN",  # Not the harbour park
    "University of Copenhagen": "GREEN",
    "IT University": "GREEN",
    "National Gallery": "GREEN",
    "Frederiksberg Centret": "GREEN",
    "Forum Station": "GREEN",
    "Superkilen Park": "GREEN",
    "Assistens Cemetery": "GREEN",
    "Nørrebro Park": "GREEN",
    "Carlsberg City": "GREEN",
    "Trianglen": "GREEN",
    "Langebro Bridge": "GREEN",
    "Amager Strand Metro": "GREEN",
}

def get_permit_status(location_name: str) -> dict:
    """Get permit status for a location."""
    status_code = LOCATION_PERMITS.get(location_name, "YELLOW")  # Default to YELLOW if unknown
    status_info = PERMIT_STATUS[status_code]
    return {
        "status": status_code.lower(),
        "label": status_info["label"],
        "description": status_info["description"],
        "color": status_info["color"]
    }

# Full permit regulations information
PERMIT_REGULATIONS = {
    "title": "Copenhagen Coffee Cart Permit Guide",
    "sections": [
        {
            "heading": "Required Permits",
            "items": [
                {
                    "title": "City of Copenhagen Permit",
                    "details": [
                        "FREE until 2028 for mobile street vending",
                        "Valid for 1 calendar year (renew annually)",
                        "Applications open October 1st for next year",
                        "Processing time: ~4 weeks",
                        "Contact: Byliv@kk.dk"
                    ]
                },
                {
                    "title": "Danish Food Authority Registration",
                    "details": [
                        "Required for all food/beverage sales",
                        "Register as 'mobile business'",
                        "Exception: <30 days/year operation",
                        "Website: foedevarestyrelsen.dk"
                    ]
                },
                {
                    "title": "Business Registration",
                    "details": [
                        "CVR number (Central Business Register)",
                        "VAT registration if earnings >50,000 DKK/year",
                        "Register at virk.dk"
                    ]
                }
            ]
        },
        {
            "heading": "Cart Size Requirements",
            "items": [
                {
                    "title": "Small Carts (<2.5 m²)",
                    "details": [
                        "Coffee scooters, bikes, Ape Cars",
                        "Allowed: Public squares, wide pavements (>2m)",
                        "Allowed: Pedestrian areas, most parks",
                        "Best for mobility and flexibility"
                    ]
                },
                {
                    "title": "Large Carts (>2.5 m²)",
                    "details": [
                        "Food trucks, vans",
                        "Restricted to parking lots only",
                        "Special permit needed for city squares",
                        "Not allowed in Latin Quarter (Inner City)"
                    ]
                }
            ]
        },
        {
            "heading": "Operating Rules",
            "items": [
                {
                    "title": "Must Do",
                    "details": [
                        "Display permit visibly at front of cart",
                        "Follow parking regulations (pay fees)",
                        "Keep area clean (responsible for customer trash)",
                        "Post CVR/VAT number on cart",
                        "Vacate at night (no vending 12 AM - 5 AM)"
                    ]
                },
                {
                    "title": "Cannot Do",
                    "details": [
                        "Sell alcohol (>2.8%), tobacco, soft drinks, candy",
                        "Set up loose equipment (chairs, signs on ground)",
                        "Play loud music or hawk/shout",
                        "Block traffic, wheelchair access, or storefronts",
                        "Use municipal waste bins for business trash"
                    ]
                }
            ]
        },
        {
            "heading": "Food Safety Requirements",
            "items": [
                {
                    "title": "Essential Equipment",
                    "details": [
                        "Toilet access if operating >2 hours",
                        "Hand washing facilities (hot/cold water)",
                        "Sneeze screen for unpackaged food (40-50 cm)",
                        "Fire extinguisher + blanket (if using gas)",
                        "Food storage at correct temperatures"
                    ]
                }
            ]
        },
        {
            "heading": "Restricted Zones",
            "items": [
                {
                    "title": "Special Permit Areas (RED)",
                    "details": [
                        "Nyhavn, Strøget, Kongens Nytorv",
                        "Nørreport Station, Little Mermaid area",
                        "Islands Brygge Harbour Park",
                        "Tivoli Gardens (private property)",
                        "Special permits granted 1-2 times/year only"
                    ]
                }
            ]
        }
    ],
    "disclaimer": "NomNom Lite is not responsible for the accuracy of this information. Regulations may change.",
    "application_url": "https://erhverv.kk.dk/tilladelser/udendorsservering-og-gadesalg",
    "general_rules": [
        "Display permit visibly at front of cart",
        "Follow parking regulations (pay fees)",
        "Keep area clean (responsible for customer trash)",
        "Post CVR/VAT number on cart",
        "Vacate at night (no vending 12 AM - 5 AM)",
        "No alcohol (>2.8%), tobacco, soft drinks, candy",
        "No loose equipment (chairs, signs on ground)",
        "Do not block traffic, wheelchair access, or storefronts"
    ],
    "zones": {
        "green": {
            "locations": ["Frederiksberg Gardens", "Fælled Park", "Amager Strandpark", "Nørrebro", "Vesterbro"],
            "requirements": "Standard mobile permit. Allowed in most public parks and wide pavements.",
            "cost": "Free (until 2028)"
        },
        "yellow": {
            "locations": ["Torvehallerne", "Round Tower", "Central Station", "Shopping Areas"],
            "requirements": "Moderate restrictions. May require specific spot allocation or market fee.",
            "cost": "Free (public) / Market fees apply (private)"
        },
        "red": {
            "locations": ["Nyhavn", "Strøget", "Tivoli", "Little Mermaid", "Inner City Squares"],
            "requirements": "Highly restricted. Special event permits only. No permanent mobile vending.",
            "cost": "Special Event Fees apply"
        }
    }
}
