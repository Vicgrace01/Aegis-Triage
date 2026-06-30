import math
import subprocess
import json
import sys

# --- OFFLINE SPATIAL DATABASE (ENUGU REGION PROTOTYPE) ---
CLINIC_LAT, CLINIC_LON = 6.856, 7.393 # Default: Rural Clinic near Nsukka

HOSPITALS = [
    {"name": "UNTH Ituku-Ozalla", "lat": 6.244, "lon": 7.422, "tier": "Tertiary (Surgery/Trauma)"},
    {"name": "Enugu State University Teaching Hospital", "lat": 6.433, "lon": 7.510, "tier": "Secondary"},
    {"name": "Nsukka District Hospital", "lat": 6.856, "lon": 7.393, "tier": "Secondary"},
    {"name": "Bishop Shanahan Hospital", "lat": 6.867, "lon": 7.412, "tier": "Secondary"}
]

def find_nearest_hospital():
    """Calculates the closest escalation facility using offline Haversine math."""
    nearest = None
    min_dist = float('inf')
    
    for h in HOSPITALS:
        # Haversine distance calculation
        R = 6371 # Earth radius in km
        dlat = math.radians(h['lat'] - CLINIC_LAT)
        dlon = math.radians(h['lon'] - CLINIC_LON)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(CLINIC_LAT)) * math.cos(math.radians(h['lat'])) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        if distance > 0 and distance < min_dist: # Exclude self if clinic shares coordinates
            min_dist = distance
            nearest = h
            
    if nearest:
        print("\n[ESCALATION ROUTING] -> OFFLINE SPATIAL DB")
        print(f" -> Nearest Facility: {nearest['name']}")
        print(f" -> Facility Tier: {nearest['tier']}")
        print(f" -> Distance: {min_dist:.1f} km away. Prepare for transport.")
def extract_symptoms(user_input):
    """Silently runs llama.cpp and forces the JSON output."""
    print(">> AI Layer: Parsing natural language into machine logic...")
    
    # THE FEW-SHOT FIX: We give the tiny model a vocabulary cheat sheet
    system_prompt = f"Analyze the emergency and output strict JSON. Rules: If text says 'awake' or 'fine', unconscious is false. If text says 'no blood', severe_bleeding is false. Map 'gasping' to breathing_difficulty: true. Emergency: {user_input}"
    
    command = [
        "llama-cli.exe",
        "-m", "qwen2.5-3b-instruct-q4_k_m.gguf",
        "-n", "128",
        "--grammar-file", "triage.gbnf",
        "--log-disable", 
        "-p", system_prompt
    ]
    
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', input="/exit\n")
    output = result.stdout

    try:
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        json_str = output[json_start:json_end]
        return json.loads(json_str)
    except Exception as e:
        print("[!] Error parsing LLM output.")
        return None

def who_protocol(symptoms):
    """The Deterministic Safety Engine."""
    print("\n==================================================")
    print(" AEGIS DETERMINISTIC PROTOCOL (WHO RURAL FIRST-AID)")
    print("==================================================")
    
    if symptoms.get('severe_bleeding'):
        print("[CRITICAL] SEVERE BLEEDING DETECTED")
        print(" -> 1. Apply direct, firm pressure to the wound with a clean cloth.")
        print(" -> 2. If on a limb and bleeding does not stop, apply a tourniquet 2-3 inches above.")
        print(" -> 3. Keep the patient warm to prevent shock.\n")
        
    if symptoms.get('breathing_difficulty'):
        print("[CRITICAL] BREATHING DIFFICULTY DETECTED")
        print(" -> 1. Sit the patient upright to ease breathing.")
        print(" -> 2. Loosen any tight clothing around the neck and chest.\n")
        
    if symptoms.get('unconscious'):
        print("[CRITICAL] UNCONSCIOUSNESS DETECTED")
        print(" -> 1. Ensure the airway is clear.")
        print(" -> 2. If breathing normally, place in the recovery position (on their side).")
        print(" -> 3. Do NOT give them anything by mouth.\n")
        
    if not any(symptoms.values()):
        print("[INFO] No critical trauma indicators detected based on input.")
        print(" -> Monitor the patient closely and seek standard medical advice when possible.\n")

    print("==================================================\n")

if __name__ == "__main__":
    print("\n--- AEGIS OFFLINE TRIAGE SYSTEM BOOTED ---")
    print("Memory Footprint: < 2.5GB | Hardware: CPU Only\n")
    
    user_text = input("Enter the emergency situation: ")
    print("\n")
    
    symptoms = extract_symptoms(user_text)
    
    if symptoms is not None:
        print(f">> Parsed Variables: {json.dumps(symptoms)}")
        who_protocol(symptoms)
        
        # Only trigger routing if there is a critical trauma flag
        if any(symptoms.values()):
            find_nearest_hospital()
            print("==================================================\n")
    else:
        print("System safely aborted due to unreadable AI output.")