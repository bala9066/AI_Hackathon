import json
import os

# Paths
WORKFLOW_DIR = r'c:\Users\HP\OneDrive\Desktop\AI\AG\workflows'
INPUT_FILE = os.path.join(WORKFLOW_DIR, 'Phase1_Interactive_V5_Persistent.json')
OUTPUT_FILE = os.path.join(WORKFLOW_DIR, 'Phase1.5_ProductionGrade.json')
NODE_UPDATES_FILE = os.path.join(WORKFLOW_DIR, 'phase1.5_node_updates.js')

# content for updates
NEW_AI_SYSTEM_PROMPT = """You are an expert hardware design AI. Create detailed block diagrams with pin-level connections.

Analyze the user's request and produce a response in STRICT JSON format.
Follow this JSON structure (the values shown below are EXAMPLES ONLY - you must generate values relevant to the user's specific request):

{
  "parsed_requirements": {
    "system_type": "RF|FPGA|IoT|Mixed-Signal|Power (choose one)",
    "project_name": "Project Name",
    "specifications": {
      "param_1": "value_1",
      "param_2": "value_2"
    }
  },
  "block_diagram": {
    "title": "System Block Diagram",
    "components": [
      {
        "id": "U1",
        "type": "Component Type",
        "name": "Component Name",
        "part_suggestion": "Manufacturer Part Number",
        "pins": {
          "PIN_NAME": "PIN_NUMBER"
        },
        "power": {
          "VCC_RAIL": "Voltage @ Current"
        }
      }
    ],
    "connections": [
      {
        "from": "U1",
        "from_pin": "PIN_A",
        "to": "U2",
        "to_pin": "PIN_B",
        "signal_name": "SIGNAL_NAME",
        "signal_type": "Standard/Voltage"
      }
    ],
    "power_rails": [
      {
        "name": "VCC_RAIL_NAME",
        "voltage": "X.XV",
        "current_budget": "X.XA",
        "components": ["U1_CORE"]
      }
    ]
  },
  "mermaid_diagram": "graph TB\\n  subgraph...",
  "component_categories": [
    {
      "category": "Category Name",
      "search_keywords": ["Keyword1", "Keyword2"],
      "quantity": 1,
      "priority": "critical",
      "specifications": "Key specs for search"
    }
  ]
}"""

NEW_FORMAT_OPTIONS_CODE = """const items = $input.all();
const allComponents = [];

items.forEach(item => {
  const data = item.json;
  
  // DigiKey
  if (data.Products) {
    data.Products.slice(0, 3).forEach(p => {
      allComponents.push({
        supplier: 'DigiKey',
        part_number: p.DigiKeyPartNumber,
        manufacturer: p.Manufacturer?.Name || 'Unknown',
        manufacturer_pn: p.ManufacturerPartNumber,
        description: (p.ProductDescription || '').substring(0, 100),
        unit_price: parseFloat(p.UnitPrice) || 0,
        stock: p.QuantityAvailable || 0,
        datasheet: p.PrimaryDatasheet || '',
        category: item.json.category || 'Unknown'
      });
    });
  }
  
  // Mouser
  if (data.SearchResults?.Parts) {
    data.SearchResults.Parts.slice(0, 3).forEach(p => {
      allComponents.push({
        supplier: 'Mouser',
        part_number: p.MouserPartNumber,
        manufacturer: p.Manufacturer || 'Unknown',
        manufacturer_pn: p.ManufacturerPartNumber,
        description: (p.Description || '').substring(0, 100),
        unit_price: parseFloat((p.PriceBreaks?.[0]?.Price || '0').replace(/[^0-9.]/g, '')) || 0,
        stock: parseInt(p.AvailabilityInStock) || 0,
        datasheet: p.DataSheetUrl || '',
        category: item.json.category || 'Unknown'
      });
    });
  }
});

return { json: { component_options: allComponents, original_data: items[0]?.json?.original_data } };"""

def load_file_content(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print(f"Loading workflow from {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find input file: {INPUT_FILE}")
        return

    # Load Generate Final code
    print(f"Loading Generate Final code from {NODE_UPDATES_FILE}...")
    try:
        generate_final_code = load_file_content(NODE_UPDATES_FILE)
    except FileNotFoundError:
        print(f"Error: Could not find node updates file: {NODE_UPDATES_FILE}")
        return

    nodes_updated = 0
    
    for node in workflow['nodes']:
        # Update AI - Parse Requirements
        if node['name'] == 'AI - Parse Requirements':
            print("Updating 'AI - Parse Requirements' node...")
            # Navigate to the prompt field (this structure varies by n8n version/node version, assuming OpenAI node structure based on name)
            # The structure for the OpenAI Chat Model node typically has 'parameters' -> 'messages' -> 'values' -> 'content' or similar
            # Or if it's a basic LLM Chain, it might differ.
            # Based on the guide, it says "Edit the AI - Parse Requirements node system message".
            
            # Let's inspect the node parameters to find where the system message is.
            # Assuming standard OpenAI Chat node or similar
            if 'parameters' in node:
                # Check for 'options' -> 'systemMessage' (older nodes) or 'messages' (newer)
                 if 'options' in node['parameters'] and 'systemMessage' in node['parameters']['options']:
                     node['parameters']['options']['systemMessage'] = NEW_AI_SYSTEM_PROMPT
                     nodes_updated += 1
                 elif 'systemMessage' in node['parameters']:
                     node['parameters']['systemMessage'] = NEW_AI_SYSTEM_PROMPT
                     nodes_updated += 1
                 elif 'messages' in node['parameters']:
                     # New conversational agent structure?
                     # Sometimes the system message is a separate parameter or part of the messages list
                     pass 
                 
                 # NOTE: Since the JSON structure can vary, we will try to set it if we find a likely candidate, 
                 # but for robustness we might need to be careful.
                 # Given the previous context, let's assume it's a "OpenAI Chat Model" or "Chain"
                 # If it's the "AI - Parse Requirements" connected to "OpenAI Chat Model", the prompt might be in the Chat Model?
                 # Wait, the screenshot shows "AI - Parse Requirements" as a separate node, and "OpenAI Chat Model" connected to it.
                 # Actually, usually "AI - Parse Requirements" IS the LLM Chain or Agent.
                 # But looking at the screenshot, "AI - Parse Requirements" has an OpenAI logo.
                 # Let's try to set the parameter `text` if it's a weak prompt node, or `messages` if it's chat.
                 
                 # Let's look for "systemMessage" or "prompt" keys recursively or just set it if we find the text from the OLD prompt.
                 # But without seeing the JSON, I'll assume a standard structure or just overwrite 'options.systemMessage' if it exists.
                 # Actually, let's try to catch a common case:
                 if 'options' not in node['parameters']:
                     node['parameters']['options'] = {}
                 
                 # Force update system message if meaningful
                 node['parameters']['options']['systemMessage'] = NEW_AI_SYSTEM_PROMPT
                 nodes_updated += 1

        # Update Format Options
        if node['name'] == 'Format Options':
            print("Updating 'Format Options' node...")
            if 'parameters' in node:
                 if 'jsCode' in node['parameters']:
                     node['parameters']['jsCode'] = NEW_FORMAT_OPTIONS_CODE
                     nodes_updated += 1
                 elif 'code' in node['parameters']: # Code node
                     node['parameters']['code']['js'] = NEW_FORMAT_OPTIONS_CODE
                     nodes_updated += 1

        # Update Generate Final (FS)
        if node['name'] == 'Generate Final (FS)':
            print("Updating 'Generate Final (FS)' node...")
            if 'parameters' in node:
                 if 'jsCode' in node['parameters']:
                     node['parameters']['jsCode'] = generate_final_code
                     nodes_updated += 1
                 elif 'code' in node['parameters']: # Code node
                     node['parameters']['code']['js'] = generate_final_code
                     nodes_updated += 1

    print(f"Updated {nodes_updated} nodes.")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"Saved updated workflow to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
