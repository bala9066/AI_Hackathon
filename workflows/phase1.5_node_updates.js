/**
 * Phase 1.5 Node Updates - Enhanced Code for "Generate Final (FS)" Node
 * 
 * This file contains the production-grade JavaScript code for the final
 * BOM, Power Budget, and RF Analysis generation in the Phase 1.5 workflow.
 * 
 * Usage: Copy this code into the "Generate Final (FS)" node in n8n workflow editor
 */

// ========================================================================
// GENERATE FINAL (FS) NODE - Production-Grade Code
// ========================================================================

const data = $input.first().json.sessionData || $input.first().json.previous_data;
const fs = require('fs');

// Validate input data
if (!data || !data.component_options || data.component_options.length === 0) {
  return {
    json: {
      error: 'No component data found',
      output: 'Error: No components selected. Please run workflow again.'
    }
  };
}

const components = data.component_options;
const systemType = data.parsed_requirements?.system_type || 'Unknown';
const powerRails = data.block_diagram?.power_rails || [];

// ========================================================================
// 1. GENERATE BOM (Bill of Materials)
// ========================================================================

let bomCsv = 'Reference,Part Number,Manufacturer,Manufacturer PN,Description,Qty,Unit Price,Total Price,Supplier,Stock,Datasheet\n';
let totalCost = 0;

components.forEach((component, index) => {
  const qty = component.quantity || 1;
  const unitPrice = parseFloat(component.unit_price) || 0;
  const totalPrice = unitPrice * qty;
  totalCost += totalPrice;

  bomCsv += `${component.reference || 'U' + (index + 1)},`;
  bomCsv += `"${component.part_number || 'N/A'}",`;
  bomCsv += `"${component.manufacturer || 'N/A'}",`;
  bomCsv += `"${component.manufacturer_pn || 'N/A'}",`;
  bomCsv += `"${(component.description || 'N/A').replace(/"/g, '""')}",`;
  bomCsv += `${qty},`;
  bomCsv += `$${unitPrice.toFixed(2)},`;
  bomCsv += `$${totalPrice.toFixed(2)},`;
  bomCsv += `${component.supplier || 'N/A'},`;
  bomCsv += `${component.stock || 0},`;
  bomCsv += `"${component.datasheet || 'N/A'}"\n`;
});

// Add summary row
bomCsv += `\nTOTAL,,,,,${components.length},,,$${totalCost.toFixed(2)},,,\n`;

fs.writeFileSync('/home/node/.n8n/BOM.csv', bomCsv);

// ========================================================================
// 2. GENERATE POWER BUDGET
// ========================================================================

let powerCsv = 'Power Rail,Voltage (V),Current Budget (A),Power (W),Efficiency (%),Input Power (W),Components,Notes\n';
let totalPower = 0;

// Parse power requirements from components and block diagram
const powerCalculations = [];

if (powerRails && powerRails.length > 0) {
  // Use power rails from block diagram
  powerRails.forEach(rail => {
    const voltage = parseFloat(rail.voltage) || 0;
    const current = parseFloat(rail.current_budget) || 0;
    const power = voltage * current;
    const efficiency = 0.85; // Assume 85% efficiency for DC-DC converters
    const inputPower = power / efficiency;

    totalPower += power;

    powerCsv += `${rail.name},`;
    powerCsv += `${voltage.toFixed(2)},`;
    powerCsv += `${current.toFixed(3)},`;
    powerCsv += `${power.toFixed(3)},`;
    powerCsv += `${(efficiency * 100).toFixed(1)},`;
    powerCsv += `${inputPower.toFixed(3)},`;
    powerCsv += `"${(rail.components || []).join(', ')}",`;
    powerCsv += `${rail.notes || ''}\n`;
  });
} else {
  // Default power rails for common system types
  const defaultRails = [
    { name: 'VCC_CORE', voltage: 1.0, current: 2.5, components: ['FPGA Core'] },
    { name: 'VCC_IO', voltage: 1.8, current: 0.8, components: ['FPGA I/O'] },
    { name: 'VCC_3V3', voltage: 3.3, current: 1.0, components: ['Peripherals'] },
    { name: 'VCC_5V0', voltage: 5.0, current: 0.5, components: ['Analog Circuits'] }
  ];

  if (systemType === 'RF') {
    defaultRails.push({ name: 'VCC_PA', voltage: 28.0, current: 1.5, components: ['Power Amplifier'] });
  }

  defaultRails.forEach(rail => {
    const power = rail.voltage * rail.current;
    const efficiency = 0.85;
    const inputPower = power / efficiency;
    totalPower += power;

    powerCsv += `${rail.name},`;
    powerCsv += `${rail.voltage.toFixed(2)},`;
    powerCsv += `${rail.current.toFixed(3)},`;
    powerCsv += `${power.toFixed(3)},`;
    powerCsv += `${(efficiency * 100).toFixed(1)},`;
    powerCsv += `${inputPower.toFixed(3)},`;
    powerCsv += `"${rail.components.join(', ')}",`;
    powerCsv += `Estimated\n`;
  });
}

// Add summary
powerCsv += `\nTOTAL SYSTEM POWER,,,${totalPower.toFixed(3)},,,Total DC Power,\n`;
powerCsv += `Input Power Required (12V),,,${(totalPower / 0.85).toFixed(3)},85.0,${(totalPower / 0.85 / 12).toFixed(3)} A @ 12V,,Including converter losses\n`;

fs.writeFileSync('/home/node/.n8n/Power_Budget.csv', powerCsv);

// ========================================================================
// 3. GENERATE RF ANALYSIS (if applicable)
// ========================================================================

let rfCsv = '';

if (systemType === 'RF' || systemType === 'Mixed-Signal') {
  rfCsv = 'Parameter,Value,Unit,Notes\n';

  // Extract RF specs from parsed requirements
  const specs = data.parsed_requirements?.specifications || {};
  const freqRange = specs.frequency_range || '5-18 GHz';
  const outputPower = specs.output_power || '40 dBm';
  const outputPowerDbm = parseFloat(outputPower);

  // RF System Calculations
  rfCsv += 'Frequency Range,' + freqRange + ',,From requirements\n';
  rfCsv += 'Output Power,' + outputPower + ',dBm,Target specification\n';
  rfCsv += 'Output Power,' + (Math.pow(10, outputPowerDbm / 10)).toFixed(2) + ',mW,Converted from dBm\n';
  rfCsv += 'Output Power,' + (Math.pow(10, outputPowerDbm / 10) / 1000).toFixed(2) + ',W,Converted from dBm\n';

  // Link Budget Analysis
  rfCsv += '\nLink Budget Analysis,,,\n';
  rfCsv += 'PA Output Power,' + outputPower + ',dBm,Power Amplifier Output\n';
  rfCsv += 'Insertion Loss (Filters/Matching),-1.5,dB,Estimated\n';
  rfCsv += 'Cable/Connector Loss,-0.5,dB,Estimated\n';
  rfCsv += 'Antenna Gain,+10,dBi,Typical high-gain antenna\n';
  rfCsv += 'EIRP,' + (outputPowerDbm - 1.5 - 0.5 + 10).toFixed(1) + ',dBm,Effective Radiated Power\n';

  // PA Requirements
  const paEfficiency = 0.30; // 30% typical for GaN PA
  const outputPowerWatts = Math.pow(10, outputPowerDbm / 10) / 1000;
  const dcPowerRequired = outputPowerWatts / paEfficiency;

  rfCsv += '\nPA Specifications,,,\n';
  rfCsv += 'Output Power (Linear),' + outputPowerWatts.toFixed(2) + ',W,\n';
  rfCsv += 'PA Efficiency,' + (paEfficiency * 100).toFixed(0) + ',%,Typical for GaN\n';
  rfCsv += 'DC Power Required,' + dcPowerRequired.toFixed(2) + ',W,PA Supply Power\n';
  rfCsv += 'Supply Voltage,28,V,Typical for high-power PA\n';
  rfCsv += 'Supply Current,' + (dcPowerRequired / 28).toFixed(2) + ',A,Calculated\n';

  // Thermal Calculations
  const dissipatedPower = dcPowerRequired - outputPowerWatts;
  rfCsv += '\nThermal Analysis,,,\n';
  rfCsv += 'Dissipated Power,' + dissipatedPower.toFixed(2) + ',W,Heat to be removed\n';
  rfCsv += 'Thermal Resistance Required,' + (100 / dissipatedPower).toFixed(2) + ',°C/W,For 100°C rise\n';
  rfCsv += 'Heatsink Required,Yes,,For ' + dissipatedPower.toFixed(0) + 'W dissipation\n';

  // Signal Chain
  rfCsv += '\nSignal Chain,,,\n';
  rfCsv += 'DAC Output Level,-5,dBm,Typical FPGA DAC\n';
  rfCsv += 'Driver Amplifier Gain,+20,dB,Pre-driver stage\n';
  rfCsv += 'PA Gain,+15,dB,Final stage\n';
  rfCsv += 'Total Gain,' + (20 + 15).toFixed(0) + ',dB,DAC to output\n';
  rfCsv += 'Required DAC Level,' + (outputPowerDbm - 20 - 15).toFixed(1) + ',dBm,Back-calculated\n';

} else {
  rfCsv = 'Parameter,Value,Unit,Notes\n';
  rfCsv += 'RF Analysis,Not Applicable,,System type: ' + systemType + '\n';
  rfCsv += 'Note,RF analysis only generated for RF or Mixed-Signal systems,,\n';
}

fs.writeFileSync('/home/node/.n8n/RF_Analysis.csv', rfCsv);

// ========================================================================
// 4. GENERATE RESPONSE MESSAGE
// ========================================================================

let response = `## Phase 1 Complete: Requirements & Component Selection\n\n`;
response += `**System Type:** ${systemType}\n\n`;

// BOM Summary
response += `### Bill of Materials\n`;
response += `- **Total Components:** ${components.length}\n`;
response += `- **Estimated Cost:** $${totalCost.toFixed(2)} USD\n`;
response += `- **File:** \`BOM.csv\`\n\n`;

// Power Budget Summary
response += `### Power Budget\n`;
response += `- **Total Power:** ${totalPower.toFixed(2)}W\n`;
response += `- **Input Power Required:** ${(totalPower / 0.85).toFixed(2)}W @ 85% efficiency\n`;
response += `- **File:** \`Power_Budget.csv\`\n\n`;

// RF Analysis Summary
if (systemType === 'RF' || systemType === 'Mixed-Signal') {
  const specs = data.parsed_requirements?.specifications || {};
  response += `### RF Analysis\n`;
  response += `- **Frequency Range:** ${specs.frequency_range || 'N/A'}\n`;
  response += `- **Output Power:** ${specs.output_power || 'N/A'}\n`;
  response += `- **File:** \`RF_Analysis.csv\`\n\n`;
}

response += `### Generated Files\n`;
response += `All files saved to \`/home/node/.n8n/\`\n\n`;
response += `To extract files:\n`;
response += `\`\`\`bash\n`;
response += `docker cp n8n:/home/node/.n8n/BOM.csv ./output/\n`;
response += `docker cp n8n:/home/node/.n8n/Power_Budget.csv ./output/\n`;
response += `docker cp n8n:/home/node/.n8n/RF_Analysis.csv ./output/\n`;
response += `\`\`\`\n\n`;
response += `**Phase 1.5 complete! Ready for Phase 2: HRS Document Generation**`;

// ========================================================================
// 5. RETURN RESULT
// ========================================================================

return {
  json: {
    output: response,
    phase1_complete: true,
    total_cost: totalCost,
    total_power: totalPower,
    component_count: components.length,
    files_generated: [
      '/home/node/.n8n/BOM.csv',
      '/home/node/.n8n/Power_Budget.csv',
      '/home/node/.n8n/RF_Analysis.csv'
    ]
  }
};
