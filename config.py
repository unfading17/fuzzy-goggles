"""
PermitAI - Configuration Module
Comprehensive configuration with regulatory codes, discipline requirements, and jurisdiction-specific rules
"""

import logging
from datetime import datetime
from enum import Enum

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class Severity(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

class Discipline(Enum):
    ARCHITECTURE = "Architecture"
    STRUCTURAL = "Structural"
    ELECTRICAL = "Electrical"
    MECHANICAL = "Mechanical"
    PLUMBING = "Plumbing"
    FIRE_PROTECTION = "Fire Protection"
    CIVIL = "Civil"
    LANDSCAPE = "Landscape"
    GENERAL = "General"

# ============================================================================
# CONFIG CLASS
# ============================================================================

class Config:
    """Master configuration for PermitAI"""
    
    # File Upload
    MAX_UPLOAD_MB = 200
    SUPPORTED_FORMATS = {'.pdf', '.png', '.jpg', '.jpeg', '.tif', '.tiff'}
    MAX_FILES_PER_UPLOAD = 50
    
    # Processing
    EXTRACT_TIMEOUT = 60
    ANALYSIS_TIMEOUT = 120
    
    # Disciplines
    DISCIPLINES = [
        "Architecture",
        "Structural",
        "Electrical",
        "Mechanical",
        "Plumbing",
        "Fire Protection",
        "Civil",
        "Landscape",
        "General"
    ]
    
    # Building Types
    BUILDING_TYPES = {
        "Residential": {"floors_max": 5, "area_max": 100000, "complexity": "Low"},
        "Commercial": {"floors_max": 40, "area_max": 500000, "complexity": "Medium"},
        "Industrial": {"floors_max": 8, "area_max": 1000000, "complexity": "High"},
        "Institutional": {"floors_max": 15, "area_max": 500000, "complexity": "Medium"},
        "Mixed Use": {"floors_max": 50, "area_max": 1000000, "complexity": "High"},
        "Multi-Family": {"floors_max": 40, "area_max": 500000, "complexity": "Medium"},
        "Healthcare": {"floors_max": 20, "area_max": 500000, "complexity": "Very High"},
        "Educational": {"floors_max": 8, "area_max": 300000, "complexity": "High"},
        "Hospitality": {"floors_max": 30, "area_max": 500000, "complexity": "High"},
        "Other": {"floors_max": 100, "area_max": 1000000, "complexity": "Medium"},
    }
    
    # States and Jurisdictions
    JURISDICTIONS = {
        "FL": {
            "name": "Florida",
            "code": "FBC",
            "primary_code": "Florida Building Code",
            "hurricane_zones": {"H", "I", "II", "III", "IV"},
            "wind_speed_mapping": {
                "H": 110,
                "I": 110,
                "II": 120,
                "III": 130,
                "IV": 140
            },
            "counties": {
                "Miami-Dade": {"jurisdiction_code": "MDC-BCD", "wind_zone": "IV", "flood_zone": "A"},
                "Broward": {"jurisdiction_code": "BCO-DEV", "wind_zone": "III", "flood_zone": "A"},
                "Hillsborough": {"jurisdiction_code": "HBC-BCS", "wind_zone": "I", "flood_zone": "A"},
                "Orange": {"jurisdiction_code": "ORC-BCD", "wind_zone": "I", "flood_zone": "A"},
                "Duval": {"jurisdiction_code": "DBC-BCD", "wind_zone": "II", "flood_zone": "A"},
            }
        },
        "CA": {
            "name": "California",
            "code": "CBC",
            "primary_code": "California Building Code",
            "seismic_zones": True,
            "wildfire_zones": True,
        },
        "TX": {
            "name": "Texas",
            "code": "TBC",
            "primary_code": "Texas Building Code",
            "wind_zones": True,
        },
        "NY": {
            "name": "New York",
            "code": "NYC-BC",
            "primary_code": "New York City Building Code",
        }
    }

# ============================================================================
# DISCIPLINE-SPECIFIC REQUIREMENTS
# ============================================================================

class DisciplineRequirements:
    """Discipline-specific regulatory and technical requirements"""
    
    ARCHITECTURE = {
        "required_elements": [
            "Floor plans with dimensions",
            "Elevations (front, side, rear)",
            "Building sections",
            "Roof plan",
            "Door and window schedules",
            "Finish schedules",
            "Professional seal and signature",
            "Egress and circulation diagrams",
            "Accessibility compliance (ADA/IBC)",
            "Zoning compliance notes",
            "Site plan",
            "Dimensioning (all critical dimensions)",
            "Notes and legends",
            "Title block with project information",
            "Revision clouds and revision history",
        ],
        "code_references": ["IBC", "ADA", "IEBC", "Florida Building Code"],
        "compliance_items": [
            "Egress path widths and distances",
            "Door swing clearances",
            "Ramp slopes and landings",
            "Stair dimensions and handrails",
            "Accessible routes and signage",
            "Room dimensions and clearances",
        ],
        "common_errors": [
            "Missing egress calculations",
            "Incorrect stair dimensions",
            "Missing accessibility features",
            "Unclear dimensioning",
            "Missing professional seal",
            "Coordination issues with other disciplines",
        ]
    }
    
    STRUCTURAL = {
        "required_elements": [
            "Foundation plans and details",
            "Framing plans (roof and floor)",
            "Structural elevations",
            "Beam and column schedules",
            "Connection details",
            "Rebar schedules",
            "Concrete specifications",
            "Professional PE seal and signature",
            "Load calculations and notes",
            "Wind and seismic bracing details",
            "Shear wall layouts",
            "Material specifications",
            "Design notes and assumptions",
        ],
        "code_references": ["IBC", "AISC", "ACI", "NDS", "ASCE 7"],
        "compliance_items": [
            "Wind load compliance",
            "Seismic load compliance",
            "Dead and live load capacity",
            "Foundation bearing pressure",
            "Deflection limits",
            "Connection adequacy",
        ],
        "common_errors": [
            "Missing load calculations",
            "Inadequate wind bracing",
            "Poor foundation design",
            "Missing connection details",
            "Incorrect rebar placement",
            "Inadequate lateral support",
            "Hurricane tie-down deficiencies",
        ]
    }
    
    ELECTRICAL = {
        "required_elements": [
            "Power plan with panel locations",
            "Lighting plan with fixture schedules",
            "Panel schedule with breaker ratings",
            "Switchgear and transformer details",
            "Emergency generator details",
            "Fire alarm schematic",
            "Data and communication system plan",
            "Professional PE or Licensed Electrician seal",
            "Grounding and bonding details",
            "Conduit and wire routing",
            "Outlet and switch schedules",
            "Load calculations",
            "Single line diagram",
        ],
        "code_references": ["NEC", "IBC", "NFPA 70", "NFPA 72"],
        "compliance_items": [
            "Panel capacity and breaker coordination",
            "Branch circuit protection",
            "Outlet spacing compliance",
            "Emergency lighting adequacy",
            "Fire alarm coverage",
            "Grounding system integrity",
            "Fault current coordination",
        ],
        "common_errors": [
            "Undersized panels or feeders",
            "Missing GFCI/AFCI protection",
            "Incorrect outlet spacing",
            "Inadequate emergency lighting",
            "Poor fire alarm coverage",
            "Missing equipment grounding",
            "Overloaded circuits",
        ]
    }
    
    MECHANICAL = {
        "required_elements": [
            "HVAC floor plan with ductwork",
            "Equipment schedule with specifications",
            "Ductwork sizing and routing",
            "VAV/damper details",
            "Diffuser and return grille schedule",
            "Controls schematic",
            "Professional PE seal",
            "Load calculations",
            "Outdoor air intake details",
            "Exhaust air details",
            "Vibration isolation details",
            "Pipe sizing and routing",
            "Equipment installation notes",
        ],
        "code_references": ["IECC", "ASHRAE 90.1", "ASHRAE 62.1", "IBC"],
        "compliance_items": [
            "Indoor air quality (ventilation rates)",
            "Energy efficiency compliance",
            "Outdoor air intake separation",
            "Noise and vibration control",
            "Equipment nameplate compliance",
            "Ductwork leakage rates",
        ],
        "common_errors": [
            "Inadequate outdoor air intake",
            "Poor equipment sizing",
            "Ductwork leakage",
            "Missing vibration isolation",
            "Inadequate clearances",
            "Poor maintenance access",
            "Noise issues",
        ]
    }
    
    PLUMBING = {
        "required_elements": [
            "Plumbing fixture plan with locations",
            "Riser diagrams (cold water, hot water, sanitary, storm)",
            "Fixture schedule with specifications",
            "Pipe sizing calculations",
            "Trap and vent details",
            "Water heater details and sizing",
            "Backflow prevention details",
            "Professional PE or Plumber seal",
            "Grease trap details (if applicable)",
            "Roof drain details",
            "Sump pump details",
            "Pressure reducing valve details",
            "Accessibility compliance (ADA)",
        ],
        "code_references": ["IPC", "IBC", "ADA", "ASHRAE"],
        "compliance_items": [
            "Fixture count and trap sizing",
            "Water pressure requirements",
            "Hot water temperature maintenance",
            "Backflow prevention",
            "Trap seals and venting",
            "Slope and flow rates",
            "Accessibility features",
        ],
        "common_errors": [
            "Undersized water service",
            "Missing or incorrect venting",
            "Trap seal damage",
            "Cross-connections",
            "Inadequate hot water sizing",
            "Poor slope or blockages",
            "Missing backflow prevention",
        ]
    }
    
    FIRE_PROTECTION = {
        "required_elements": [
            "Fire alarm system plan",
            "Sprinkler system layout and design",
            "Device location plan",
            "System riser diagram",
            "Equipment and device schedule",
            "Design calculations",
            "Professional certification",
            "Water supply details",
            "Standpipe locations",
            "Fire extinguisher locations",
            "Emergency egress lighting plan",
            "Smoke control details",
        ],
        "code_references": ["NFPA 70", "NFPA 72", "NFPA 13", "IBC"],
        "compliance_items": [
            "Detector spacing and coverage",
            "Sprinkler head placement",
            "Water supply adequacy",
            "Alarm transmission",
            "Emergency voice communication",
            "Fire department access",
        ],
        "common_errors": [
            "Inadequate sprinkler coverage",
            "Missing detectors",
            "Poor device placement",
            "Insufficient water supply",
            "Blocked fire lanes",
            "Inadequate alarm coverage",
            "Missing emergency lighting",
        ]
    }
    
    CIVIL = {
        "required_elements": [
            "Site plan with grading",
            "Utility layout (water, sewer, power, gas, telecom)",
            "Drainage plan with calculations",
            "Erosion and sediment control",
            "Stormwater management details",
            "Survey data and topography",
            "Access and circulation plan",
            "Professional PE seal",
            "Utility coordination",
            "Slope stability analysis",
            "Cut and fill calculations",
            "Environmental compliance notes",
        ],
        "code_references": ["IBC", "NRCS", "State/Local Stormwater Code"],
        "compliance_items": [
            "Stormwater detention/retention",
            "Slope stability",
            "Grading compliance",
            "Utility separation",
            "Erosion control effectiveness",
            "Environmental protection",
        ],
        "common_errors": [
            "Inadequate stormwater management",
            "Poor slope stability",
            "Utility conflicts",
            "Inadequate erosion control",
            "Missing survey data",
            "Improper grading",
            "Inadequate drainage",
        ]
    }

# ============================================================================
# FLORIDA-SPECIFIC HURRICANE & REGULATORY CODES
# ============================================================================

class FloridaHurricaneCompliance:
    """Florida-specific hurricane and wind compliance codes"""
    
    WIND_ZONES = {
        "I": {"speed": 110, "region": "Central Florida", "code": "FBC 2020"},
        "II": {"speed": 120, "region": "Jacksonville, Panhandle", "code": "FBC 2020"},
        "III": {"speed": 130, "region": "South Florida, Gulf Coast", "code": "FBC 2020"},
        "IV": {"speed": 140, "region": "Miami-Dade, Monroe", "code": "FBC 2020"},
    }
    
    HURRICANE_COMPLIANCE_ITEMS = [
        "Wind-resistant roof decking",
        "Roof-to-wall connections (ties/straps)",
        "Wall-to-foundation connections",
        "Hurricane shutters or impact-resistant windows",
        "Garage door wind rating",
        "Soffit and fascia protection",
        "Roof pitch adequacy (minimum 4:12)",
        "Barrel roof or curved roof design review",
        "Opening protection (windows, doors)",
        "Exterior wall covering durability",
        "Proper fastening schedules",
        "Concrete block wall integrity",
        "Foundation design for uplift",
        "Pool enclosure wind resistance",
    ]
    
    RECENT_REGULATORY_UPDATES = {
        "2024": {
            "wind_speed_increase": "Effective January 1, 2024 - Miami-Dade wind speeds increased to 140+ mph",
            "roof_requirements": "Enhanced roof-to-wall connection requirements",
            "window_standards": "All windows and doors must meet HVHZ standards in high-wind areas",
        },
        "2023": {
            "tie_down_requirements": "Enhanced roof tie-down spacing (16\" on center minimum for major wind zone)",
            "soffit_rules": "All soffits must be wind-resistant or enclosed",
        },
        "2022": {
            "pool_enclosure": "Pool enclosures must withstand Design Wind Pressure in compliance zones",
        }
    }
    
    COMMON_HURRICANE_VIOLATIONS = [
        "Inadequate roof-to-wall connections (missing straps)",
        "Undersized or incorrectly spaced roof ties",
        "Impact-resistant windows not installed in required zones",
        "Missing or inadequate soffit bracing",
        "Improper foundation tie-down",
        "Non-compliant garage doors",
        "Missing hurricane shutters in required areas",
        "Weak pool enclosure structure",
        "Improper roof pitch for wind zone",
        "Fastener corrosion or improper spacing",
        "Missing lateral bracing",
        "Inadequate concrete cover on reinforcement",
    ]

# ============================================================================
# VALIDATORS
# ============================================================================

class Validator:
    """Validation utility class"""
    
    @staticmethod
    def validate_file(file_obj) -> tuple[bool, str]:
        """Validates uploaded file"""
        try:
            if not file_obj:
                return False, "No file provided"
            
            filename = getattr(file_obj, "name", "")
            file_size = getattr(file_obj, "size", 0)
            
            if not filename:
                return False, "File has no name"
            
            ext = filename[filename.rfind('.'):].lower() if '.' in filename else ""
            if ext not in Config.SUPPORTED_FORMATS:
                return False, f"Unsupported format: {ext}. Allowed: {Config.SUPPORTED_FORMATS}"
            
            if file_size > Config.MAX_UPLOAD_MB * 1024 * 1024:
                return False, f"File too large: {file_size / (1024*1024):.1f}MB (max {Config.MAX_UPLOAD_MB}MB)"
            
            if file_size == 0:
                return False, "File is empty"
            
            return True, ""
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def validate_project_name(name: str) -> tuple[bool, str]:
        """Validates project name"""
        if not name or not name.strip():
            return False, "Project name required"
        if len(name) > 100:
            return False, "Project name too long (max 100 chars)"
        if len(name) < 3:
            return False, "Project name too short (min 3 chars)"
        return True, ""

# ============================================================================
# DEFAULT STRUCTURES
# ============================================================================

DEFAULT_PROJECT = {
    "nombre": "New Project",
    "direccion": "",
    "ciudad": "",
    "condado": "",
    "estado": "FL",
    "tipo_construccion": "Residential",
    "metros": 0,
    "numero_pisos": 1,
    "documentos": [],
    "findings": [],
    "probability": None,
    "analysis_by_file": {},
    "created_at": datetime.now().isoformat(),
    "updated_at": datetime.now().isoformat(),
}

DEFAULT_FINDING = {
    "title": "Untitled observation",
    "description": "No description provided.",
    "severity": "Medium",
    "probability": 50,
    "code": "GEN-000",
    "discipline": "General",
    "sheet": "Unknown",
    "priority": "Medium",
    "how_to_fix": "No specific action provided.",
    "impact": "No impact described.",
    "estimated_fix_time": "Unknown",
    "page": 0,
    "source_file": "Unknown",
}

# ============================================================================
# LOGGING UTILITIES
# ============================================================================

def log_analysis(project_name: str, file_name: str, findings_count: int, duration: float):
    """Logs analysis completion"""
    logger.info(f"Project: {project_name} | File: {file_name} | Findings: {findings_count} | Duration: {duration:.2f}s")

def log_error(context: str, error: Exception):
    """Logs errors with context"""
    logger.error(f"{context}: {str(error)}")
