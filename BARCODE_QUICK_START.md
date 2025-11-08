# Quick Start: Barcode Scanner

## What is it?

Scan barcodes and QR codes to quickly identify and manage your brewing ingredients.

## How to Use

### 1. Try the Demo

Visit **http://localhost:3000/barcode-demo** to test the scanner.

### 2. Assign Barcodes to Items

You can assign barcodes in two ways:

**Option A: Manual Entry**
1. Edit any inventory item (hop, fermentable, yeast, or misc)
2. Enter the barcode value in the "Barcode" field
3. Save the item

**Option B: Scan to Assign**
1. Use the BarcodeField component in edit forms
2. Click "Scan" button
3. Scan the product barcode
4. Barcode is automatically assigned

### 3. Look Up Items by Scanning

1. Go to `/barcode-demo`
2. Click "Scan Barcode/QR Code"
3. Allow camera access when prompted
4. Point camera at barcode
5. Item details appear automatically

## Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- HTTPS connection (for camera access)
- Device with camera (or USB barcode scanner)

## Supported Formats

- QR Code
- UPC (Universal Product Code)
- EAN (European Article Number)
- Code 128
- Code 39
- And many more...

## Tips

- **Good Lighting** - Ensure the barcode is well-lit
- **Hold Steady** - Keep camera still for best results
- **Distance** - Keep barcode 6-12 inches from camera
- **Manual Entry** - You can always type barcodes manually

## Troubleshooting

**Camera won't start:**
- Make sure you're using HTTPS
- Check browser permissions
- Try a different browser

**Barcode won't scan:**
- Improve lighting
- Try different angles
- Clean the camera lens
- Use manual entry as fallback

**Item not found:**
- Make sure barcode is assigned to an item first
- Check for typos if entering manually

## Demo Workflow

1. **Setup** - Add a test hop with barcode "TEST-001"
2. **Scan** - Go to demo page and scan "TEST-001"
3. **Result** - See the hop details appear
4. **History** - View in recent scans section

## Need Help?

See full documentation in `BARCODE_SCANNER_INTEGRATION.md`
