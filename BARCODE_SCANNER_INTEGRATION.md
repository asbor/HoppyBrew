# Barcode/QR Scanner Integration

This document describes the barcode and QR code scanner integration implemented for HoppyBrew Issue #22.

## Overview

The barcode/QR scanner integration enables users to scan ingredients and bottles using their device camera or by manually entering barcode values. The system supports all common barcode formats including UPC, EAN, Code 128, and QR codes.

## Features

- **Camera-based scanning** - Use device camera to scan barcodes in real-time
- **Manual entry** - Option to manually type barcode values
- **Multi-format support** - Supports UPC, EAN, Code 128, QR codes, and more
- **Unique barcode validation** - Ensures barcodes are unique across all inventory types
- **Lookup by barcode** - Quickly find inventory items by scanning their barcode
- **Recent scans history** - Track recently scanned items
- **Responsive design** - Works on desktop and mobile devices

## Backend Implementation

### Database Changes

Added `barcode` field to all inventory tables with unique index:
- `inventory_hops.barcode`
- `inventory_fermentables.barcode`
- `inventory_yeasts.barcode`
- `inventory_miscs.barcode`

**Migration:** `0008_add_barcode_fields.py`

### API Endpoints

#### GET `/inventory/barcode/{barcode}`
Look up an inventory item by its barcode.

**Response:**
```json
{
  "type": "hop",
  "item": {
    "id": 1,
    "name": "Cascade",
    "barcode": "HOP-CASCADE-001",
    "alpha": 5.5,
    ...
  }
}
```

**Response Codes:**
- `200` - Item found
- `404` - No item found with this barcode

#### PUT `/inventory/{item_type}/{item_id}/barcode`
Update or set the barcode for an inventory item.

**Parameters:**
- `item_type`: One of 'hop', 'fermentable', 'yeast', or 'misc'
- `item_id`: ID of the inventory item
- `barcode`: Barcode value (query parameter, or null to remove)

**Response:**
```json
{
  "id": 1,
  "name": "Cascade",
  "barcode": "HOP-CASCADE-001",
  ...
}
```

**Response Codes:**
- `200` - Barcode updated successfully
- `400` - Barcode already in use or invalid item type
- `404` - Item not found

### Database Models

All inventory models now include:
```python
barcode = Column(String, nullable=True, unique=True, index=True)
```

### Schemas

All inventory schemas now include:
```python
barcode: Optional[str] = None
```

## Frontend Implementation

### Components

#### BarcodeScanner.vue

Reusable camera-based barcode scanner component.

**Usage:**
```vue
<BarcodeScanner
  button-text="Scan Barcode"
  @scan-success="handleScan"
  @scan-error="handleError"
/>
```

**Props:**
- `buttonText` (string) - Text to display on scan button
- `supportedFormats` (array) - Array of barcode format codes to support

**Events:**
- `scan-success` - Emitted when barcode is successfully scanned
  ```js
  { code: string, format: string }
  ```
- `scan-error` - Emitted when scanning fails

**Features:**
- Auto-stops after successful scan
- Shows last scanned code
- Error handling with user feedback
- Cancel button to stop scanning
- Uses rear camera on mobile devices

#### BarcodeField.vue

Form field component with integrated scanner.

**Usage:**
```vue
<BarcodeField
  v-model="barcodeValue"
  hint="Optional: Assign a unique barcode"
/>
```

**Props:**
- `modelValue` (string) - Barcode value (v-model)
- `hint` (string) - Help text to display

**Features:**
- Manual text input option
- Inline scanner toggle
- Two-way data binding
- Error display

### Composables

Extended `useInventory` composable with:

```typescript
// Look up item by barcode
const { data, error } = await lookupByBarcode(barcode)

// Update item barcode
const { data, error } = await updateBarcode(itemType, itemId, barcode)
```

### Demo Page

Access at `/barcode-demo` to test the scanner functionality.

**Features:**
- Live barcode scanning
- Item lookup display
- Recent scans history
- Usage instructions
- Error handling

## Usage Examples

### Scanning an Item

1. Navigate to `/barcode-demo`
2. Click "Scan Barcode/QR Code"
3. Allow camera permissions if prompted
4. Point camera at barcode
5. Scanner automatically detects and looks up the item
6. View item details or scan another

### Adding Barcode to Inventory Item

**Backend (Python):**
```python
# Update hop barcode
response = requests.put(
    f"{API_URL}/inventory/hop/1/barcode",
    params={"barcode": "HOP-CASCADE-001"}
)
```

**Frontend (Vue):**
```vue
<template>
  <BarcodeField v-model="hopData.barcode" />
</template>

<script setup>
const hopData = ref({
  name: 'Cascade',
  barcode: 'HOP-CASCADE-001'
})
</script>
```

### Looking Up by Barcode

**Backend (Python):**
```python
response = requests.get(f"{API_URL}/inventory/barcode/HOP-CASCADE-001")
data = response.json()
# { "type": "hop", "item": { ... } }
```

**Frontend (Vue):**
```javascript
const { lookupByBarcode } = useInventory()
const result = await lookupByBarcode('HOP-CASCADE-001')
if (!result.error.value) {
  console.log('Found:', result.data.value)
}
```

## Supported Barcode Formats

The scanner supports all formats provided by html5-qrcode:
- QR Code
- UPC-A
- UPC-E
- EAN-8
- EAN-13
- Code 128
- Code 39
- Code 93
- Codabar
- ITF (Interleaved 2 of 5)
- RSS-14
- Data Matrix
- PDF417

## Browser Compatibility

The scanner requires:
- Modern browser with camera API support
- HTTPS connection (camera access requirement)
- User permission to access camera

Supported browsers:
- Chrome/Edge 53+
- Firefox 63+
- Safari 11+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Security Considerations

- Barcode uniqueness is enforced at database level with unique indexes
- Cross-inventory validation prevents duplicate barcodes
- Camera access requires user permission
- No barcode data is stored in browser localStorage
- All API endpoints use standard authentication

## Testing

### Backend Tests

Run barcode endpoint tests:
```bash
cd services/backend
python -m pytest tests/test_endpoints/test_barcode.py -v
```

Tests cover:
- ✅ Barcode lookup for all inventory types
- ✅ Item not found scenarios
- ✅ Barcode update operations
- ✅ Barcode removal
- ✅ Duplicate barcode prevention
- ✅ Invalid item type handling

### Frontend Testing

Manual testing recommended:
1. Test camera access on different devices
2. Verify barcode scanning accuracy
3. Test manual entry fallback
4. Verify error handling
5. Test on different browsers

## Future Enhancements

Potential improvements for future iterations:

1. **Bulk Barcode Assignment** - Assign barcodes to multiple items at once
2. **Barcode Generation** - Generate unique barcodes for items
3. **Barcode Printing** - Print barcode labels
4. **Offline Support** - Cache barcode lookups for offline use
5. **Batch Management** - Scan barcodes during batch creation
6. **Ingredient Consumption** - Scan to record ingredient usage
7. **Bottle Tracking** - Track individual bottles with barcodes
8. **Analytics** - Track scan frequency and popular items
9. **Mobile App** - Native mobile app for better scanning
10. **External Scanner Support** - Support USB barcode scanners

## Troubleshooting

### Camera Not Working
- Ensure HTTPS connection (required for camera access)
- Check browser permissions
- Verify camera is not in use by another application
- Try a different browser

### Barcode Not Scanning
- Ensure good lighting
- Hold camera steady
- Try different angles
- Clean camera lens
- Verify barcode format is supported

### Item Not Found
- Verify barcode is assigned to an inventory item
- Check for typos in manual entry
- Ensure barcode uniqueness hasn't been violated

## Related Issues

- Implements: #22 - Barcode/QR Scanner Integration
- Related to: #3 - Inventory Management Integration

## Dependencies

**Backend:**
- SQLAlchemy 2.0.30
- FastAPI 0.111.0
- Pydantic 2.7.3

**Frontend:**
- html5-qrcode 2.3.8
- Nuxt 3.11.2
- Vue 3.5.24

## License

This feature is part of HoppyBrew and is distributed under the MIT License.
