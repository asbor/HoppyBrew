# Batch Workflow System - HoppyBrew

This document describes the comprehensive batch workflow system inspired by Brewfather's interface, providing a systematic approach to managing the brewing process from planning to completion.

## 🔄 Batch Phases

The system tracks batches through seven distinct phases:

### 1. **Planning** 📋
- Recipe overview with stats (ABV, IBU, OG, FG, Color)
- Equipment profile and water calculations  
- Ingredient checklist and inventory status
- Pre-brew preparation and scheduling
- Printable brew sheet generation

### 2. **Brew Day** 🔥
- Interactive brewing interface with timers
- Measured values tracking (pH, gravity, volumes)
- Mash profile with temperature monitoring
- Hop schedule with addition timeline
- Real-time brew log and notes
- Step-by-step brewing checklist

### 3. **Primary Fermentation** 🧪
- Gravity and temperature tracking
- Fermentation progress charts
- Sensor integration (Tilt, iSpindel support)
- Fermentation profile management
- Daily readings and logs

### 4. **Secondary Fermentation** 🌡️
- Extended fermentation monitoring
- Clarity and flavor development tracking
- Transfer to secondary vessel
- Continued gravity monitoring

### 5. **Conditioning** ❄️
- Cold conditioning phase
- Clarity improvement tracking
- Final gravity stabilization
- Preparation for packaging

### 6. **Packaged** 🍾
- Bottling or kegging tracking
- Carbonation monitoring
- Packaging date and method
- Conditioning timeline

### 7. **Completed** ✅
- Final beer evaluation
- Tasting notes and ratings
- Batch archival
- Recipe feedback and improvements

## 🖥️ User Interface

### Batch Detail Page (`/batches/[id]`)

The main batch detail page provides:

- **Phase Navigation**: Visual timeline showing current phase and progress
- **Phase-Specific Content**: Dynamic interface based on current batch status
- **Quick Actions**: Add readings, notes, generate brew sheets
- **Real-time Updates**: Live data from connected sensors

### Phase Components

Each phase has its own specialized component:

- `BatchPlanningPhase.vue` - Recipe overview and preparation
- `BatchBrewingPhase.vue` - Interactive brew day interface  
- `BatchFermentationPhase.vue` - Fermentation tracking and charts
- `BatchConditioningPhase.vue` - Conditioning monitoring
- `BatchPackagedPhase.vue` - Packaging and carbonation
- `BatchCompletedPhase.vue` - Final evaluation and archival

## 📊 Data Tracking

### Measurements
- **Gravity readings** (SG/°P)
- **Temperature** (mash, fermentation, conditioning)
- **pH levels** (mash, wort, beer)
- **Volume measurements** (pre-boil, post-boil, fermenter)

### Calculated Values
- **ABV percentage** (from OG/FG)
- **Attenuation percentage**
- **Brewhouse efficiency**
- **Color (SRM/EBC)**
- **Bitterness (IBU)**

### Logs and Notes
- **Timestamped brew log** entries
- **Process notes** and observations
- **Recipe modifications** and adjustments
- **Tasting notes** and evaluations

## 🔌 Sensor Integration

The system supports various brewing sensors:

### Supported Devices
- **Tilt Hydrometer** - Gravity and temperature
- **iSpindel** - DIY gravity sensor
- **Brewbot sensors** - Multiple parameter monitoring
- **Manual entry** - For any measurement

### Real-time Monitoring
- Automatic data collection from connected devices
- Live charts and trend analysis
- Alerts for out-of-range conditions
- Historical data export

## 🎯 Sample Data

The system includes comprehensive sample data demonstrating all phases:

### Sample Batches
1. **Batch #33** - Planning phase (Black Citrus IPA)
2. **Batch #1** - Brew day phase (5 Yeast Experimental NEIPA)  
3. **Batch #47** - Primary fermentation (American Pale Ale)
4. **Batch #45** - Conditioning (Sample Blonde Ale)
5. **Batch #44** - Packaged (Belgian Tripel)
6. **Batch #43** - Completed (Imperial Stout)

### Loading Sample Data

```bash
# Generate sample data
cd scripts
python3 generate_sample_data.py

# Load into backend (requires running backend)
python3 load_sample_data.py
```

## 🚀 Getting Started

### Prerequisites
- HoppyBrew backend running on `http://localhost:8000`
- HoppyBrew frontend running on `http://localhost:3000`

### Demo Workflow

1. **Start with Planning**: Visit Batch #33 to see recipe planning
2. **Active Brewing**: Check Batch #1 for brew day interface
3. **Monitor Fermentation**: View Batch #47 for active fermentation
4. **Track Progress**: See how batches progress through phases

### Key Features to Test

- **Phase Navigation**: Click through different phases
- **Add Readings**: Record gravity and temperature
- **Brew Day Timer**: Use the boil timer and hop schedule
- **Charts**: View fermentation progress graphs
- **Notes**: Add brewing observations and notes

## 🔧 Technical Implementation

### Frontend Components
```
components/batch/
├── BatchPhaseNavigation.vue    # Phase timeline and navigation
├── BatchPlanningPhase.vue      # Planning interface
├── BatchBrewingPhase.vue       # Brew day interface
├── BatchFermentationPhase.vue  # Fermentation tracking
├── BatchConditioningPhase.vue  # Conditioning phase
├── BatchPackagedPhase.vue      # Packaging tracking
├── BatchCompletedPhase.vue     # Completion interface
├── BatchEditDialog.vue         # Batch editing
├── BatchReadingDialog.vue      # Reading entry
└── BatchNoteDialog.vue         # Note addition
```

### Backend Integration
- RESTful API endpoints for batch CRUD operations
- Batch status transitions and workflow management
- Reading storage and retrieval
- Sensor data integration endpoints

### Data Models
```typescript
interface Batch {
  id: string
  recipe_id: string
  batch_name: string
  batch_number: number
  batch_size: number
  status: BatchStatus
  brew_date?: string
  fermentation_start_date?: string
  packaging_date?: string
  completion_date?: string
  og?: number
  fg?: number
  abv?: number
  notes?: string
}

type BatchStatus = 
  | 'planning'
  | 'brew_day' 
  | 'primary_fermentation'
  | 'secondary_fermentation'
  | 'conditioning'
  | 'packaged'
  | 'completed'
  | 'archived'
```

## 📱 Mobile Responsive

The interface is fully responsive and optimized for:
- **Desktop**: Full feature access with multiple columns
- **Tablet**: Optimized layout for brew day use
- **Mobile**: Essential features for monitoring on-the-go

## 🎨 Design Inspiration

This implementation closely follows Brewfather's proven interface design:
- Clean, professional layout
- Clear phase progression
- Intuitive navigation
- Data-rich dashboards
- Mobile-first responsive design

The goal is to provide brewers with a familiar, professional-grade brewing management experience that scales from homebrew to commercial operations.