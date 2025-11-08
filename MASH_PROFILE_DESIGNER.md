# Mash Profile Designer Documentation

## Overview

The Mash Profile Designer is a comprehensive visual tool for creating and managing mash schedules in HoppyBrew. It provides step-by-step mash design, temperature/time validation, brew day timer integration, and common profile templates.

## Features

### 1. Visual Mash Step Designer

The designer allows you to create, edit, and manage mash steps with a visual interface.

#### Key Capabilities:
- **Add Steps**: Create new mash steps with detailed parameters
- **Edit Steps**: Modify existing steps inline
- **Reorder Steps**: Use up/down arrows to rearrange step sequence
- **Delete Steps**: Remove unwanted steps
- **Validation**: Real-time validation of temperatures and times

#### Step Parameters:
- **Name**: Descriptive name (e.g., "Saccharification Rest")
- **Type**: Infusion, Temperature, or Decoction
- **Temperature**: Target temperature (0-100°C)
- **Duration**: Step time (0-300 minutes)
- **Ramp Time**: Time to reach temperature (0-60 minutes)
- **Description**: Optional notes about the step
- **Decoction Amount**: For decoction steps (e.g., "30%")

### 2. Mash Profile Templates

Pre-configured templates for common brewing styles:

#### Available Templates:

**1. Single Infusion - Medium Body**
- 2 steps
- Best for: Most ales
- Characteristics: Simple, reliable, medium body
- Steps:
  - Saccharification Rest: 66°C for 60 minutes
  - Mash Out: 76°C for 10 minutes

**2. Step Mash - Full Body**
- 3 steps
- Best for: Stouts, porters, full-bodied beers
- Characteristics: Enhanced body and head retention
- Steps:
  - Protein Rest: 55°C for 15 minutes
  - Saccharification Rest: 68°C for 60 minutes
  - Mash Out: 76°C for 10 minutes

**3. Hochkurz - Dry/Crisp**
- 3 steps
- Best for: German lagers, pilsners
- Characteristics: Highly fermentable, dry finish
- Steps:
  - Beta Glucan Rest: 45°C for 20 minutes
  - High Temperature Rest: 72°C for 30 minutes
  - Mash Out: 76°C for 10 minutes

**4. Traditional Decoction**
- 5 steps
- Best for: Authentic German lagers
- Characteristics: Complex malt character
- Steps:
  - Acid Rest: 40°C for 20 minutes
  - Protein Rest: 55°C for 30 minutes (with decoction)
  - Saccharification Rest 1: 63°C for 30 minutes (with decoction)
  - Saccharification Rest 2: 72°C for 20 minutes (with decoction)
  - Mash Out: 76°C for 10 minutes

**5. Light Lager - Highly Attenuative**
- 3 steps
- Best for: Light lagers, highly attenuated beers
- Characteristics: Maximum fermentability
- Steps:
  - Beta Amylase Rest: 63°C for 45 minutes
  - Alpha Amylase Rest: 70°C for 30 minutes
  - Mash Out: 76°C for 10 minutes

### 3. Brew Day Timer

Interactive timer for executing your mash schedule on brew day.

#### Timer Features:
- **Real-time Countdown**: See remaining time for current step
- **Progress Bars**: Visual progress for current step and overall mash
- **Step Navigation**: View all steps with current step highlighted
- **Controls**:
  - Start: Begin the timer
  - Pause: Temporarily stop the timer
  - Resume: Continue from pause
  - Stop: End the session (with confirmation)
  - Skip Step: Move to next step early
- **Notifications**:
  - Browser notifications when steps complete
  - Optional audio alerts
- **Step Details**: Current temperature, duration, and ramp time displayed

## Usage Guide

### Creating a New Mash Profile

#### Option 1: Using a Template

1. Navigate to **Profiles > Mash Profiles**
2. Click **Create New Profile**
3. Template selector automatically opens
4. Browse available templates
5. Select a template
6. Optionally customize the profile name
7. Click **Use Template**
8. Profile is created and you're redirected to edit page

#### Option 2: From Scratch

1. Navigate to **Profiles > Mash Profiles**
2. Click **Create New Profile**
3. In template selector, click **Start from Scratch**
4. Fill in **Basic Info** tab:
   - Profile Name (required)
   - Grain Temperature
   - Tun Temperature
   - Sparge Temperature
   - Target pH
   - Tun Weight
   - Tun Specific Heat
   - Notes
5. Switch to **Mash Steps** tab
6. Click **Add Step**
7. Configure step parameters
8. Click **Save Step**
9. Repeat for additional steps
10. Click **Save Profile**

### Editing an Existing Profile

1. Navigate to **Profiles > Mash Profiles**
2. Click **Edit** on the desired profile
3. Use tabs to navigate:
   - **Basic Info**: Modify profile settings
   - **Mash Steps**: Edit step sequence
   - **Brew Day Timer**: Use timer (if steps exist)
4. Make desired changes
5. Click **Update Profile**

### Using the Brew Day Timer

1. Open a mash profile with defined steps
2. Navigate to **Brew Day Timer** tab
3. Review the step sequence
4. Click **Start** to begin
5. Follow on-screen instructions for each step
6. Timer automatically advances to next step
7. Can pause/resume as needed
8. Click **Stop** to end session

## API Endpoints

### Get Templates
```
GET /mash/templates/list
```
Returns all available mash profile templates.

**Response:**
```json
[
  {
    "id": "single_infusion",
    "name": "Single Infusion - Medium Body",
    "description": "Standard single infusion mash...",
    "grain_temp": 20,
    "tun_temp": 20,
    "sparge_temp": 76,
    "ph": 5.4,
    "notes": "Most common mash profile...",
    "steps": [...]
  }
]
```

### Create from Template
```
POST /mash/from-template/{template_id}?custom_name={name}
```
Creates a new mash profile from a template.

**Parameters:**
- `template_id`: ID of the template (e.g., "single_infusion")
- `custom_name`: Optional custom name for the profile

**Response:**
```json
{
  "id": "123",
  "name": "My Single Infusion",
  "template_used": "Single Infusion - Medium Body",
  "steps_created": 2,
  "message": "Mash profile created successfully..."
}
```

## Validation Rules

### Temperature Validation
- **Range**: 0-100°C
- **Purpose**: Ensure realistic brewing temperatures
- **Common ranges**:
  - Protein rest: 45-55°C
  - Beta amylase: 60-65°C
  - Alpha amylase: 66-72°C
  - Mash out: 75-78°C

### Time Validation
- **Step Duration**: 0-300 minutes (5 hours max)
- **Ramp Time**: 0-60 minutes (1 hour max)
- **Purpose**: Prevent unrealistic mash schedules

### Required Fields
- Profile name
- Step name
- Step type
- Step temperature
- Step duration

## Best Practices

### Designing Mash Profiles

1. **Start with a Template**: Use templates as a starting point and modify
2. **Consider Your Goals**:
   - Full body: Higher temps (68-70°C), shorter times
   - Dry finish: Lower temps (63-65°C), longer times
3. **Include Mash Out**: Always end with mash out step (76°C) for better lautering
4. **Ramp Times**: Account for heating time between steps
5. **Total Time**: Keep total mash time under 2 hours for most beers

### Using the Timer

1. **Prepare Before Starting**: Have all equipment ready
2. **Enable Notifications**: Allow browser notifications for step alerts
3. **Monitor Temperature**: Timer is for time tracking only
4. **Document Deviations**: Use notes to record actual temps/times
5. **Practice Runs**: Test timer with a new profile before brew day

### Template Selection

- **First-time brewers**: Start with "Single Infusion"
- **German lagers**: Use "Hochkurz" or "Traditional Decoction"
- **Stouts/Porters**: Use "Step Mash - Full Body"
- **Light lagers**: Use "Light Lager - Highly Attenuative"
- **Advanced techniques**: Use "Traditional Decoction"

## Troubleshooting

### Timer Issues

**Timer not advancing:**
- Check browser isn't in power-saving mode
- Keep browser tab active
- Disable sleep mode during brew day

**Notifications not working:**
- Check browser notification permissions
- Ensure notifications enabled in browser settings
- Some browsers block notifications by default

**Audio not playing:**
- Check browser audio permissions
- Ensure device volume is on
- Audio file may be missing (optional feature)

### Profile Creation Issues

**Template won't load:**
- Check backend server is running
- Verify API endpoint is accessible
- Check browser console for errors

**Steps won't save:**
- Verify all required fields are filled
- Check validation errors
- Ensure temperatures are in valid range

**Can't reorder steps:**
- Save current edits first
- Refresh page and try again
- Check for JavaScript errors

## Tips and Tricks

1. **Duplicate Profiles**: Create a base profile and copy for variations
2. **Document Changes**: Use notes field to track modifications
3. **Version Control**: Increment version number for profile iterations
4. **Batch Testing**: Try profile on small batch before production
5. **Share Knowledge**: Export successful profiles to share with others
6. **Seasonal Adjustment**: Adjust grain/tun temps based on ambient conditions
7. **Equipment Notes**: Record equipment-specific settings in notes

## Future Enhancements

Planned features for future releases:
- Export/import profiles as JSON
- Share profiles with community
- Strike water calculator integration
- Temperature control device integration
- Mash efficiency tracking
- Recipe-specific profile recommendations
- Multi-stage decoction calculator
- Automated step timing based on grain bill
