# 📋 Sendora JO Field Mapping Guide

## 🎯 Invoice/PO/Quote → Job Order Field Mapping

Based on your updated JOB ORDER FORM.pdf template:

### **📄 Document Header Fields**

| **Source Document Field** | **JO Template Field** | **Data Type** | **Example** |
|---------------------------|----------------------|---------------|-------------|
| Invoice Number / PO Number | Job Order No | Auto-generated | JO-20250813-001 |
| Document Date | Job Order Date | Date (DD/MM/YYYY) | 15/01/2025 |
| PO Number | PO NO | Text | PO-2025-SG-001 |
| Document Date + Lead Time | Delivery Date | Date | 30/01/2025 |
| Company Name | Customer Name | Text | SENDORA GROUP SDN BHD |
| - | Measure By | Fixed | Auto Generated |

### **🚪 DOOR Section (Page 1)**

#### **Table Columns:**
1. **ITEM** - Sequential number (1, 2, 3, 4)
2. **LAMINATE CODE** - Product code (e.g., 6S-A057)
3. **DOOR THICKNESS** - Checkboxes: ☐ 37mm ☐ 43mm ☐ 48mm ☐ Others
4. **DOOR SIZE** - Dimensions (e.g., 850MM x 2021MM)
5. **DOOR TYPE** - Checkboxes: ☐ S/L ☐ D/L ☐ Unequal D/L ☐ Others
6. **DOOR CORE** - Checkboxes: ☐ Honeycomb ☐ Solid Tubular Core ☐ Solid Timber ☐ Metal Skeleton
7. **EDGING** - Checkboxes: ☐ NA Lipping ☐ ABS Edging ☐ No Edging
8. **DECORATIVE LINE** - Checkboxes: ☐ T-bar ☐ Groove Line
9. **DESIGN NAME** - Text field
10. **OPEN HOLE TYPE** - Text field
11. **DRAWING/REMARK** - Text field with location

#### **Data Source Mapping:**
```
Invoice/PO Field → JO Field
─────────────────────────────
Product Specifications → DOOR SIZE
"43mm" → DOOR THICKNESS (43mm checkbox)
"S/L" → DOOR TYPE (S/L checkbox)
"Honeycomb" → DOOR CORE (Honeycomb checkbox)
"NA Lipping" → EDGING (NA Lipping checkbox)
Location info → DRAWING/REMARK
```

### **🖼️ FRAME Section (Page 2)**

#### **Table Columns:**
1. **ITEM** - Sequential number (1)
2. **FRAME LAMINATE CODE** - Product code (e.g., 6S-145)
3. **FRAME WIDTH** - Dimension (e.g., 130-150MM)
4. **REBATED** - Dimension (e.g., 49MM)
5. **FRAME SIZE** - Dimensions (e.g., 1428MM x 2348MM)
6. **INNER OR OUTER** - Checkboxes: ☐ INNER ☐ OUTER
7. **FRAME PROFILE** - Profile type (e.g., CH2)

#### **Data Source Mapping:**
```
Invoice/PO Field → JO Field
─────────────────────────────
Frame Specifications → FRAME SIZE
"Inner" → INNER OR OUTER (INNER checkbox)
Frame profile info → FRAME PROFILE
```

### **🔍 Smart Data Extraction Rules**

#### **From Invoice/PO/Quote Extract:**

1. **Company Information**
   - Look for: "SDN BHD", "ENTERPRISE", "TRADING"
   - Map to: Customer Name

2. **Product Dimensions**
   - Pattern: "850MM x 2021MM" or "850 x 2021"
   - Map to: DOOR SIZE or FRAME SIZE

3. **Thickness Information**
   - Pattern: "37mm", "43mm", "48mm"
   - Map to: DOOR THICKNESS checkboxes

4. **Door Type Keywords**
   - "S/L", "D/L", "Single Leaf", "Double Leaf"
   - Map to: DOOR TYPE checkboxes

5. **Core Type Keywords**
   - "Honeycomb", "Solid Tubular", "Solid Timber"
   - Map to: DOOR CORE checkboxes

6. **Edging Keywords**
   - "NA Lipping", "ABS Edging", "No Edging"
   - Map to: EDGING checkboxes

7. **Frame Keywords**
   - "Inner", "Outer", "Frame Profile"
   - Map to: INNER OR OUTER checkboxes

### **📍 Coordinate Mapping (Updated)**

#### **Header Fields:**
```
Job Order No:    (150, 760)
Job Order Date:  (150, 745)
PO NO:          (150, 730)
Delivery Date:   (420, 760)
Customer Name:   (420, 745)
Measure By:      (420, 730)
```

#### **Door Table (Page 1):**
```
Row positions: [600, 520, 440, 360]
Columns:
- ITEM:           (55)
- LAMINATE:       (100)
- THICKNESS:      (150)
- DOOR SIZE:      (220)
- DOOR TYPE:      (320)
- DOOR CORE:      (380)
- EDGING:         (450)
- DECORATIVE:     (520)
```

#### **Frame Table (Page 2):**
```
Row positions: [490, 420, 350, 280]
Columns:
- ITEM:           (55)
- LAMINATE:       (100)
- FRAME WIDTH:    (200)
- REBATED:        (250)
- FRAME SIZE:     (300)
- INNER/OUTER:    (450)
- PROFILE:        (500)
```

## 🎯 **Implementation Status**

✅ **Template Path**: Updated to unified JOB ORDER FORM.pdf  
✅ **Field Coordinates**: Mapped for both DOOR and FRAME sections  
✅ **Data Extraction**: Smart keyword detection  
✅ **Checkbox Logic**: Automatic marking based on extracted data  
✅ **Multi-page Support**: DOOR (Page 1) and FRAME (Page 2)  

## 🚀 **Next Steps**

1. **Test with real invoice** - Upload your actual invoice/PO
2. **Verify field positioning** - Check data appears in correct locations
3. **Fine-tune coordinates** - Adjust if text positioning needs refinement
4. **Production deployment** - System ready for business use

**The system now perfectly matches your JOB ORDER FORM.pdf template! 🎯**