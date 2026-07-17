"""
PermitAI - Advanced AI Analyzer
Integrates OpenAI for intelligent permit analysis with discipline-specific logic
"""

import json
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from config import (
    Discipline, Severity, DisciplineRequirements, 
    FloridaHurricaneCompliance, Config
)

logger = logging.getLogger(__name__)

# ============================================================================
# AI ANALYZER ENGINE
# ============================================================================

class AIAnalyzer:
    """Advanced AI-powered permit analysis engine"""
    
    def __init__(self, api_key: str = None):
        """Initialize AI Analyzer with optional OpenAI API key"""
        self.api_key = api_key
        self.client = None
        self.model = "gpt-4-turbo-preview"
        
        if api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
            except ImportError:
                logger.warning("OpenAI library not installed. Falling back to rule-based analysis.")
                self.client = None
    
    def analyze_extraction(self, extracted_text: str, file_name: str, 
                          building_type: str = "Residential",
                          disciplines: List[str] = None) -> Dict:
        """
        Analyzes extracted document text using AI
        
        Args:
            extracted_text: Text extracted from plan/document
            file_name: Name of the source file
            building_type: Type of building project
            disciplines: List of disciplines relevant to this file
        
        Returns:
            Dictionary with analysis findings
        """
        
        if disciplines is None:
            disciplines = ["Architecture", "General"]
        
        if self.client:
            return self._ai_analysis(extracted_text, file_name, building_type, disciplines)
        else:
            return self._rule_based_analysis(extracted_text, file_name, building_type, disciplines)
    
    def _ai_analysis(self, text: str, file_name: str, building_type: str, 
                     disciplines: List[str]) -> Dict:
        """Uses OpenAI for advanced analysis"""
        
        try:
            prompt = self._build_analysis_prompt(text, file_name, building_type, disciplines)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert building permit reviewer with deep knowledge of building codes, hurricane compliance, architectural standards, and multi-discipline construction requirements."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                top_p=0.9
            )
            
            analysis_text = response.choices[0].message.content
            findings = self._parse_ai_response(analysis_text)
            
            return {
                "success": True,
                "findings": findings,
                "method": "AI-Powered",
                "model": self.model,
            }
        
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}. Falling back to rule-based.")
            return self._rule_based_analysis(text, file_name, building_type, disciplines)
    
    def _build_analysis_prompt(self, text: str, file_name: str, 
                               building_type: str, disciplines: List[str]) -> str:
        """Builds detailed analysis prompt for AI"""
        
        discipline_str = ", ".join(disciplines)
        
        prompt = f"""
Analyze this construction permit document and identify ALL potential compliance issues:

FILE: {file_name}
BUILDING TYPE: {building_type}
DISCIPLINES: {discipline_str}

DOCUMENT TEXT:
{text[:3000]}

ANALYSIS REQUIREMENTS:
1. Hurricane Compliance (Florida-specific):
   - Wind resistance requirements (110-140 mph zones)
   - Roof-to-wall connections and tie-downs
   - Impact-resistant windows (HVHZ areas)
   - Foundation tie-down adequacy
   - Soffit and fascia protection

2. Code Compliance Issues:
   - Missing required elements per discipline
   - Dimensional errors or violations
   - Missing calculations or specifications
   - Professional seal or signature issues

3. Multi-Discipline Coordination:
   - Conflicts between architectural and structural plans
   - Mechanical/plumbing accessibility issues
   - Electrical safety concerns
   - Fire protection gaps

4. Recent Regulatory Updates (2024):
   - Miami-Dade wind speeds 140+ mph
   - Enhanced roof tie-down requirements
   - Updated window standards

RESPONSE FORMAT (JSON):
{{
  "findings": [
    {{
      "title": "Issue title",
      "severity": "Critical|High|Medium|Low",
      "probability": 75,
      "code": "FBC-2024-001",
      "discipline": "Architecture|Structural|Electrical|Mechanical|Plumbing|Fire Protection",
      "description": "Detailed explanation",
      "how_to_fix": "Specific corrective action",
      "impact": "Consequences if not fixed",
      "estimated_fix_time": "Time in hours"
    }}
  ]
}}

Provide ONLY valid JSON response.
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> List[Dict]:
        """Parses AI response and extracts findings"""
        
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.warning("No JSON found in AI response")
                return []
            
            json_str = response_text[json_start:json_end]
            data = json.loads(json_str)
            
            findings = []
            for item in data.get("findings", []):
                finding = self._normalize_finding(item)
                findings.append(finding)
            
            return findings
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI JSON response: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error processing AI response: {str(e)}")
            return []
    
    def _rule_based_analysis(self, text: str, file_name: str, 
                            building_type: str, disciplines: List[str]) -> Dict:
        """Fallback rule-based analysis without AI"""
        
        findings = []
        
        # Check each discipline's requirements
        for discipline in disciplines:
            discipline_findings = self._check_discipline(
                text, file_name, discipline, building_type
            )
            findings.extend(discipline_findings)
        
        # Check Florida hurricane compliance
        if "FL" in text.upper() or "FLORIDA" in text.upper():
            hurricane_findings = self._check_hurricane_compliance(text, file_name)
            findings.extend(hurricane_findings)
        
        # Check recent regulatory updates
        regulatory_findings = self._check_regulatory_updates(text, file_name)
        findings.extend(regulatory_findings)
        
        return {
            "success": True,
            "findings": findings,
            "method": "Rule-Based",
        }
    
    def _check_discipline(self, text: str, file_name: str, 
                         discipline: str, building_type: str) -> List[Dict]:
        """Checks discipline-specific requirements"""
        
        findings = []
        text_upper = text.upper()
        
        if discipline == "Architecture":
            findings.extend(self._check_architecture(text_upper, file_name))
        elif discipline == "Structural":
            findings.extend(self._check_structural(text_upper, file_name))
        elif discipline == "Electrical":
            findings.extend(self._check_electrical(text_upper, file_name))
        elif discipline == "Mechanical":
            findings.extend(self._check_mechanical(text_upper, file_name))
        elif discipline == "Plumbing":
            findings.extend(self._check_plumbing(text_upper, file_name))
        elif discipline == "Fire Protection":
            findings.extend(self._check_fire_protection(text_upper, file_name))
        
        return findings
    
    def _check_architecture(self, text: str, file_name: str) -> List[Dict]:
        """Architecture-specific compliance checks"""
        
        findings = []
        required = DisciplineRequirements.ARCHITECTURE["required_elements"]
        
        # Check for missing critical elements
        missing_items = []
        for item in required:
            if item.upper() not in text:
                missing_items.append(item)
        
        if missing_items and len(missing_items) > 3:
            findings.append({
                "title": "Missing Architectural Elements",
                "severity": "High",
                "probability": 85,
                "code": "ARC-001",
                "discipline": "Architecture",
                "description": f"Missing {len(missing_items)} required architectural elements: {', '.join(missing_items[:5])}",
                "how_to_fix": "Add all required elements per IBC and ADA standards",
                "impact": "Plan rejection, construction delays",
                "estimated_fix_time": 8
            })
        
        # Check for accessibility
        if "ADA" not in text and "ACCESSIBILITY" not in text:
            findings.append({
                "title": "Missing Accessibility Compliance Notes",
                "severity": "High",
                "probability": 90,
                "code": "ARC-002",
                "discipline": "Architecture",
                "description": "No ADA/accessibility compliance documentation found",
                "how_to_fix": "Add accessibility compliance notes and calculations",
                "impact": "Plan rejection, ADA violation",
                "estimated_fix_time": 4
            })
        
        # Check for professional seal
        if "PROFESSIONAL SEAL" not in text and "PE" not in text and "AIA" not in text:
            findings.append({
                "title": "Missing Professional Seal or Signature",
                "severity": "Critical",
                "probability": 95,
                "code": "ARC-003",
                "discipline": "Architecture",
                "description": "No professional architect seal or signature found",
                "how_to_fix": "Have licensed architect seal and sign all plan sheets",
                "impact": "Plan rejection, non-permittable",
                "estimated_fix_time": 1
            })
        
        # Check for egress
        if "EGRESS" not in text and "EXIT" not in text:
            findings.append({
                "title": "Missing Egress Analysis",
                "severity": "Critical",
                "probability": 80,
                "code": "ARC-004",
                "discipline": "Architecture",
                "description": "No egress path analysis or exit requirements documented",
                "how_to_fix": "Add egress calculations per IBC occupant load requirements",
                "impact": "Life safety violation, plan rejection",
                "estimated_fix_time": 6
            })
        
        return findings
    
    def _check_structural(self, text: str, file_name: str) -> List[Dict]:
        """Structural-specific compliance checks"""
        
        findings = []
        
        # Check for wind load calculations
        if "WIND" not in text and "LOAD" not in text:
            findings.append({
                "title": "Missing Wind Load Calculations",
                "severity": "Critical",
                "probability": 88,
                "code": "STR-001",
                "discipline": "Structural",
                "description": "No wind load calculations or design criteria found",
                "how_to_fix": "Provide wind load calculations per ASCE 7 and FBC 2024",
                "impact": "Structural inadequacy, hurricane vulnerability",
                "estimated_fix_time": 12
            })
        
        # Check for foundation design
        if "FOUNDATION" not in text or "FOOTING" not in text:
            findings.append({
                "title": "Foundation Design Documentation Missing",
                "severity": "High",
                "probability": 85,
                "code": "STR-002",
                "discipline": "Structural",
                "description": "Foundation design, footings, or bearing pressure not documented",
                "how_to_fix": "Provide foundation plans with bearing capacity calculations",
                "impact": "Structural failure risk, settlement issues",
                "estimated_fix_time": 10
            })
        
        # Check for connection details
        if "CONNECTION" not in text and "DETAIL" not in text:
            findings.append({
                "title": "Missing Structural Connection Details",
                "severity": "High",
                "probability": 82,
                "code": "STR-003",
                "discipline": "Structural",
                "description": "No structural connection details or bolt specifications",
                "how_to_fix": "Add detailed connection drawings with bolt size and spacing",
                "impact": "Structural integrity compromise, construction issues",
                "estimated_fix_time": 8
            })
        
        # Check for lateral bracing
        if "BRACE" not in text and "SHEAR" not in text:
            findings.append({
                "title": "Lateral Bracing System Not Documented",
                "severity": "High",
                "probability": 80,
                "code": "STR-004",
                "discipline": "Structural",
                "description": "No lateral bracing or shear wall system shown",
                "how_to_fix": "Add lateral bracing design per seismic/wind requirements",
                "impact": "Inadequate lateral support, wind vulnerability",
                "estimated_fix_time": 10
            })
        
        # Check for PE seal
        if "PROFESSIONAL ENGINEER" not in text and "PE SEAL" not in text:
            findings.append({
                "title": "Missing Structural Engineer Professional Seal",
                "severity": "Critical",
                "probability": 95,
                "code": "STR-005",
                "discipline": "Structural",
                "description": "No PE seal or structural engineer signature found",
                "how_to_fix": "Have licensed PE seal and sign all structural plans",
                "impact": "Plan rejection, non-permittable",
                "estimated_fix_time": 1
            })
        
        return findings
    
    def _check_electrical(self, text: str, file_name: str) -> List[Dict]:
        """Electrical-specific compliance checks"""
        
        findings = []
        
        # Check for panel schedule
        if "PANEL" not in text or "BREAKER" not in text:
            findings.append({
                "title": "Missing Electrical Panel Schedule",
                "severity": "High",
                "probability": 85,
                "code": "ELE-001",
                "discipline": "Electrical",
                "description": "No electrical panel schedule or breaker ratings documented",
                "how_to_fix": "Provide complete panel schedule with all breaker sizes",
                "impact": "Overloaded circuits, fire hazard",
                "estimated_fix_time": 6
            })
        
        # Check for load calculations
        if "LOAD" not in text or "CAPACITY" not in text:
            findings.append({
                "title": "Missing Load Calculations",
                "severity": "High",
                "probability": 82,
                "code": "ELE-002",
                "discipline": "Electrical",
                "description": "No electrical load calculations per NEC Article 220",
                "how_to_fix": "Perform and document electrical load calculations",
                "impact": "Undersized service, inadequate power",
                "estimated_fix_time": 8
            })
        
        # Check for GFCI/AFCI protection
        if "GFCI" not in text and "AFCI" not in text:
            findings.append({
                "title": "GFCI/AFCI Protection Not Specified",
                "severity": "High",
                "probability": 88,
                "code": "ELE-003",
                "discipline": "Electrical",
                "description": "Ground Fault and Arc Fault protection requirements not specified",
                "how_to_fix": "Add GFCI/AFCI requirements per NEC 2023",
                "impact": "Shock/fire hazard, code violation",
                "estimated_fix_time": 4
            })
        
        # Check for emergency systems
        if "EMERGENCY" not in text and "GENERATOR" not in text:
            findings.append({
                "title": "Emergency Power System Not Documented",
                "severity": "Medium",
                "probability": 70,
                "code": "ELE-004",
                "discipline": "Electrical",
                "description": "Emergency lighting and backup power requirements not shown",
                "how_to_fix": "Add emergency system design and calculations",
                "impact": "Life safety concern, code violation",
                "estimated_fix_time": 6
            })
        
        return findings
    
    def _check_mechanical(self, text: str, file_name: str) -> List[Dict]:
        """Mechanical-specific compliance checks"""
        
        findings = []
        
        # Check for HVAC design
        if "HVAC" not in text and "DUCTWORK" not in text:
            findings.append({
                "title": "HVAC System Design Not Documented",
                "severity": "High",
                "probability": 85,
                "code": "MEC-001",
                "discipline": "Mechanical",
                "description": "No HVAC ductwork layout or equipment specifications",
                "how_to_fix": "Provide complete HVAC design per ASHRAE 62.1/90.1",
                "impact": "Poor indoor air quality, code violation",
                "estimated_fix_time": 10
            })
        
        # Check for load calculations
        if "LOAD" not in text or "COOLING" not in text:
            findings.append({
                "title": "Missing HVAC Load Calculations",
                "severity": "High",
                "probability": 82,
                "code": "MEC-002",
                "discipline": "Mechanical",
                "description": "No heating/cooling load calculations provided",
                "how_to_fix": "Perform HVAC Manual J load calculations",
                "impact": "Undersized/oversized equipment, inefficiency",
                "estimated_fix_time": 8
            })
        
        # Check for outdoor air
        if "OUTDOOR AIR" not in text and "VENTILATION" not in text:
            findings.append({
                "title": "Outdoor Air Requirements Not Specified",
                "severity": "High",
                "probability": 80,
                "code": "MEC-003",
                "discipline": "Mechanical",
                "description": "Outdoor air intake and ventilation rates not documented",
                "how_to_fix": "Add ventilation calculations per ASHRAE 62.1",
                "impact": "Poor indoor air quality, health hazard",
                "estimated_fix_time": 5
            })
        
        return findings
    
    def _check_plumbing(self, text: str, file_name: str) -> List[Dict]:
        """Plumbing-specific compliance checks"""
        
        findings = []
        
        # Check for fixture schedule
        if "FIXTURE" not in text or "TOILET" not in text:
            findings.append({
                "title": "Plumbing Fixture Schedule Missing",
                "severity": "High",
                "probability": 85,
                "code": "PLU-001",
                "discipline": "Plumbing",
                "description": "No fixture schedule with types and quantities",
                "how_to_fix": "Provide complete fixture schedule per IPC",
                "impact": "Inadequate sanitary facilities, code violation",
                "estimated_fix_time": 4
            })
        
        # Check for riser diagrams
        if "RISER" not in text or "DIAGRAM" not in text:
            findings.append({
                "title": "Plumbing Riser Diagrams Not Provided",
                "severity": "High",
                "probability": 82,
                "code": "PLU-002",
                "discipline": "Plumbing",
                "description": "No plumbing riser diagrams for water, waste, and vent",
                "how_to_fix": "Add riser diagrams per IPC requirements",
                "impact": "Construction confusion, code violation",
                "estimated_fix_time": 6
            })
        
        # Check for water heater
        if "WATER HEATER" not in text and "HOT WATER" not in text:
            findings.append({
                "title": "Hot Water System Not Specified",
                "severity": "Medium",
                "probability": 75,
                "code": "PLU-003",
                "discipline": "Plumbing",
                "description": "Water heater type and sizing not documented",
                "how_to_fix": "Add water heater specifications and sizing calculations",
                "impact": "Inadequate hot water service",
                "estimated_fix_time": 3
            })
        
        return findings
    
    def _check_fire_protection(self, text: str, file_name: str) -> List[Dict]:
        """Fire Protection-specific compliance checks"""
        
        findings = []
        
        # Check for fire alarm
        if "FIRE ALARM" not in text and "DETECTOR" not in text:
            findings.append({
                "title": "Fire Alarm System Not Documented",
                "severity": "High",
                "probability": 85,
                "code": "FIR-001",
                "discipline": "Fire Protection",
                "description": "No fire alarm system design or device locations",
                "how_to_fix": "Provide fire alarm plan per NFPA 72",
                "impact": "Life safety violation, code rejection",
                "estimated_fix_time": 8
            })
        
        # Check for sprinkler system
        if "SPRINKLER" not in text and "SUPPRESSION" not in text:
            findings.append({
                "title": "Fire Suppression System Missing",
                "severity": "High",
                "probability": 80,
                "code": "FIR-002",
                "discipline": "Fire Protection",
                "description": "No fire sprinkler or suppression system design",
                "how_to_fix": "Add sprinkler design per NFPA 13",
                "impact": "Life safety risk, code violation",
                "estimated_fix_time": 10
            })
        
        return findings
    
    def _check_hurricane_compliance(self, text: str, file_name: str) -> List[Dict]:
        """Florida hurricane compliance checks"""
        
        findings = []
        compliance_items = FloridaHurricaneCompliance.HURRICANE_COMPLIANCE_ITEMS
        
        text_upper = text.upper()
        
        # Check for wind zone specification
        wind_zones = ["ZONE I", "ZONE II", "ZONE III", "ZONE IV", "WIND ZONE"]
        if not any(zone in text_upper for zone in wind_zones):
            findings.append({
                "title": "Hurricane Wind Zone Not Specified",
                "severity": "Critical",
                "probability": 90,
                "code": "HUR-001",
                "discipline": "Structural",
                "description": "No wind zone designation (I, II, III, or IV) for hurricane compliance",
                "how_to_fix": "Specify applicable wind zone and design per FBC 2024",
                "impact": "Inadequate hurricane protection, insurance issues",
                "estimated_fix_time": 2
            })
        
        # Check for roof-to-wall connections
        if "ROOF-TO-WALL" not in text_upper and "ROOF TIE" not in text_upper:
            findings.append({
                "title": "Roof-to-Wall Connections Not Documented",
                "severity": "Critical",
                "probability": 95,
                "code": "HUR-002",
                "discipline": "Structural",
                "description": "No roof-to-wall connection details or tie-down specifications",
                "how_to_fix": "Add roof tie-down details per FBC 2024 (minimum 16\" O.C.)",
                "impact": "Roof failure in hurricanes, major structural damage",
                "estimated_fix_time": 6
            })
        
        # Check for impact-resistant windows
        if "IMPACT RESISTANT" not in text_upper and "HVHZ" not in text_upper:
            findings.append({
                "title": "Impact-Resistant Windows Not Specified",
                "severity": "High",
                "probability": 85,
                "code": "HUR-003",
                "discipline": "Architecture",
                "description": "No impact-resistant window specifications for HVHZ areas",
                "how_to_fix": "Specify impact-resistant (hurricane) windows per FBC",
                "impact": "Window failure, water intrusion, interior damage",
                "estimated_fix_time": 4
            })
        
        # Check for hurricane shutters
        if "SHUTTER" not in text_upper and "ACCORDION" not in text_upper:
            findings.append({
                "title": "Hurricane Shutter System Not Shown",
                "severity": "High",
                "probability": 75,
                "code": "HUR-004",
                "discipline": "Architecture",
                "description": "No hurricane shutter or protection system design",
                "how_to_fix": "Add shutter details (roll-down, accordion, etc.)",
                "impact": "Window vulnerability, insurance concerns",
                "estimated_fix_time": 3
            })
        
        # Check for garage door rating
        if "GARAGE DOOR" not in text_upper or "WIND RATING" not in text_upper:
            findings.append({
                "title": "Garage Door Wind Rating Not Specified",
                "severity": "High",
                "probability": 80,
                "code": "HUR-005",
                "discipline": "Architecture",
                "description": "Garage door wind resistance rating not documented",
                "how_to_fix": "Specify impact-rated garage door for wind zone",
                "impact": "Garage door failure, property damage, liability",
                "estimated_fix_time": 2
            })
        
        # Check for foundation tie-down
        if "TIE-DOWN" not in text_upper and "ANCHOR" not in text_upper:
            findings.append({
                "title": "Foundation Tie-Down Not Documented",
                "severity": "Critical",
                "probability": 88,
                "code": "HUR-006",
                "discipline": "Structural",
                "description": "No foundation tie-down or anchorage details for uplift resistance",
                "how_to_fix": "Add foundation anchors per FBC wind uplift calculations",
                "impact": "Building uplift in extreme winds, catastrophic failure",
                "estimated_fix_time": 8
            })
        
        # Check for soffit protection
        if "SOFFIT" not in text_upper or "FASCIA" not in text_upper:
            findings.append({
                "title": "Soffit and Fascia Wind Protection Missing",
                "severity": "High",
                "probability": 82,
                "code": "HUR-007",
                "discipline": "Architecture",
                "description": "No wind-resistant soffit/fascia or enclosure details",
                "how_to_fix": "Specify wind-resistant soffit design or full enclosure",
                "impact": "Soffit peeling, water intrusion, attic exposure",
                "estimated_fix_time": 4
            })
        
        return findings
    
    def _check_regulatory_updates(self, text: str, file_name: str) -> List[Dict]:
        """Checks for compliance with recent regulatory updates"""
        
        findings = []
        text_upper = text.upper()
        
        # Check for 2024 FBC compliance
        if "FBC 2024" not in text_upper and "2024" not in text_upper:
            findings.append({
                "title": "2024 FBC Compliance Not Referenced",
                "severity": "Medium",
                "probability": 70,
                "code": "REG-001",
                "discipline": "General",
                "description": "Plans may not comply with 2024 FBC requirements (effective Jan 1, 2024)",
                "how_to_fix": "Update plans to comply with FBC 2024 standards",
                "impact": "Plan rejection, requires resubmission",
                "estimated_fix_time": 12
            })
        
        # Check for Miami-Dade wind speeds (140+ mph)
        if "140" not in text and "MIAMI-DADE" in text_upper:
            findings.append({
                "title": "Miami-Dade Wind Speed (140+ mph) Not Documented",
                "severity": "High",
                "probability": 85,
                "code": "REG-002",
                "discipline": "Structural",
                "description": "Miami-Dade projects must use 140+ mph design wind speed (2024 update)",
                "how_to_fix": "Update wind load calculations for 140 mph minimum",
                "impact": "Structural inadequacy, increased insurance risk",
                "estimated_fix_time": 10
            })
        
        return findings
    
    def _normalize_finding(self, item: Dict) -> Dict:
        """Normalizes finding data structure"""
        
        return {
            "title": item.get("title", "Untitled Finding"),
            "severity": item.get("severity", "Medium"),
            "probability": int(item.get("probability", 50)),
            "code": item.get("code", "GEN-000"),
            "discipline": item.get("discipline", "General"),
            "description": item.get("description", "No description provided"),
            "how_to_fix": item.get("how_to_fix", "Consult with professional"),
            "impact": item.get("impact", "Unknown impact"),
            "estimated_fix_time": int(item.get("estimated_fix_time", 0)),
            "source_file": item.get("source_file", "Unknown"),
            "page": item.get("page", 0),
        }

# ============================================================================
# ANALYSIS ORCHESTRATOR
# ============================================================================

class AnalysisOrchestrator:
    """Orchestrates complete file-by-file analysis"""
    
    def __init__(self, ai_key: str = None):
        """Initialize orchestrator with optional AI"""
        self.analyzer = AIAnalyzer(ai_key)
        self.analysis_history = {}
    
    def analyze_files(self, files_data: List[Tuple[str, str, str, List[str]]]) -> Dict:
        """
        Analyze multiple files with unique results per file
        
        Args:
            files_data: List of (file_name, extracted_text, building_type, disciplines)
        
        Returns:
            Dictionary with analysis for each file
        """
        
        results = {
            "total_files": len(files_data),
            "timestamp": datetime.now().isoformat(),
            "analyses": {}
        }
        
        for file_name, text, building_type, disciplines in files_data:
            analysis = self.analyzer.analyze_extraction(
                text, file_name, building_type, disciplines
            )
            
            results["analyses"][file_name] = {
                "findings_count": len(analysis.get("findings", [])),
                "findings": analysis.get("findings", []),
                "method": analysis.get("method", "Unknown"),
                "timestamp": datetime.now().isoformat(),
            }
            
            # Store in history
            self.analysis_history[file_name] = analysis
        
        return results
    
    def get_file_analysis(self, file_name: str) -> Optional[Dict]:
        """Retrieve analysis for specific file"""
        return self.analysis_history.get(file_name)

