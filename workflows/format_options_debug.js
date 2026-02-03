const items = $input.all();
const originalData = items[0]?.json?.original_data || {};
const allComponents = [];

items.forEach(item => {
    const data = item.json;
    // DigiKey logic...
    if (data.Products) {
        data.Products.slice(0, 3).forEach(p => allComponents.push({ supplier: 'DigiKey', part: p.DigiKeyPartNumber, price: p.UnitPrice || 0 }));
    }
    // Mouser logic...
    if (data.SearchResults?.Parts) {
        data.SearchResults.Parts.slice(0, 3).forEach(p => allComponents.push({ supplier: 'Mouser', part: p.MouserPartNumber, price: p.PriceBreaks?.[0]?.Price || 0 }));
    }
});

return { json: { execution_id: originalData.execution_id, component_options: allComponents, original_data: originalData, waiting_for: 'component_approval' } };
