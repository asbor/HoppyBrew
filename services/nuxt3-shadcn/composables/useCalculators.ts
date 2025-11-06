/**
 * Brewing calculation composable
 * Centralizes all brewing formulas for reuse across the application
 */

export interface ABVResult {
  abv: number
  formatted: string
}

export interface IBUResult {
  ibu: number
  formatted: string
}

export interface SRMResult {
  srm: number
  ebc: number
  color: string
  formatted: string
}

export interface PrimingSugarResult {
  grams: number
  oz: number
  formatted: string
}

export const useCalculators = () => {
  /**
   * Calculate ABV (Alcohol by Volume) using the standard formula
   * @param og Original Gravity
   * @param fg Final Gravity
   * @returns ABV percentage
   */
  function calculateABV(og: number, fg: number): ABVResult {
    if (og <= fg || og <= 0 || fg <= 0) {
      return { abv: 0, formatted: '0.00%' }
    }
    
    const abv = (og - fg) * 131.25
    return {
      abv,
      formatted: `${abv.toFixed(2)}%`
    }
  }

  /**
   * Calculate IBU (International Bitterness Units) using Tinseth formula
   * @param alphaAcid Alpha acid percentage of hops
   * @param hopWeight Weight of hops in grams
   * @param boilTime Boil time in minutes
   * @param batchSize Batch size in liters
   * @param boilGravity Gravity of wort during boil
   * @returns IBU value
   */
  function calculateIBU(
    alphaAcid: number,
    hopWeight: number,
    boilTime: number,
    batchSize: number,
    boilGravity: number
  ): IBUResult {
    if (alphaAcid === 0 || hopWeight === 0 || boilTime === 0 || batchSize === 0) {
      return { ibu: 0, formatted: '0 IBU' }
    }
    
    // Tinseth formula
    const gravityFactor = 1.65 * Math.pow(0.000125, boilGravity - 1.0)
    const timeFactor = (1 - Math.exp(-0.04 * boilTime)) / 4.15
    const utilization = gravityFactor * timeFactor
    const alphaFraction = alphaAcid / 100.0
    
    // IBU = (alpha acid % × weight in grams × 1000 × utilization) / volume in liters
    const ibu = (alphaFraction * hopWeight * 1000 * utilization) / batchSize
    
    return {
      ibu: Math.max(ibu, 0),
      formatted: `${Math.max(ibu, 0).toFixed(1)} IBU`
    }
  }

  /**
   * Calculate SRM (Standard Reference Method) color using Morey equation
   * @param grainColor Grain color in Lovibond
   * @param grainWeight Grain weight in kg
   * @param batchSize Batch size in liters
   * @returns SRM and EBC values with color hex
   */
  function calculateSRM(
    grainColor: number,
    grainWeight: number,
    batchSize: number
  ): SRMResult {
    if (grainColor === 0 || grainWeight === 0 || batchSize === 0) {
      return { srm: 0, ebc: 0, color: '#FFE699', formatted: '0 SRM / 0 EBC' }
    }
    
    // MCU (Malt Color Units) = (grain color × grain weight in lbs) / volume in gallons
    const weightLbs = grainWeight * 2.20462
    const volumeGal = batchSize * 0.264172
    const mcu = (grainColor * weightLbs) / volumeGal
    
    // Morey equation: SRM = 1.4922 × MCU^0.6859
    const srm = 1.4922 * Math.pow(mcu, 0.6859)
    const ebc = srm * 1.97 // Convert SRM to EBC
    
    // Get color hex based on SRM
    const color = getSRMColor(srm)
    
    return {
      srm,
      ebc,
      color,
      formatted: `${srm.toFixed(1)} SRM / ${ebc.toFixed(1)} EBC`
    }
  }

  /**
   * Get hex color for a given SRM value
   */
  function getSRMColor(srmValue: number): string {
    if (srmValue < 2) return '#FFE699'
    if (srmValue < 4) return '#FFD878'
    if (srmValue < 6) return '#FFCA5A'
    if (srmValue < 8) return '#FFBF42'
    if (srmValue < 10) return '#FBB123'
    if (srmValue < 13) return '#F8A600'
    if (srmValue < 17) return '#F39C00'
    if (srmValue < 20) return '#EA8F00'
    if (srmValue < 24) return '#E58500'
    if (srmValue < 30) return '#DE7C00'
    if (srmValue < 40) return '#D77200'
    return '#8D4C1A'
  }

  /**
   * Calculate priming sugar needed for carbonation
   * @param batchVolume Volume in liters
   * @param desiredCO2 Desired CO2 volumes
   * @param temperature Beer temperature in Celsius
   * @param sugarType Type of sugar (table, corn, dme, honey)
   * @returns Sugar needed in grams and oz
   */
  function calculatePrimingSugar(
    batchVolume: number,
    desiredCO2: number,
    temperature: number,
    sugarType: 'table' | 'corn' | 'dme' | 'honey' = 'table'
  ): PrimingSugarResult {
    // Calculate dissolved CO2 at temperature
    const dissolvedCO2 = 3.0378 - (0.050062 * temperature) + (0.00026555 * Math.pow(temperature, 2))
    
    // CO2 needed
    const co2Needed = desiredCO2 - dissolvedCO2
    
    if (co2Needed <= 0) {
      return { grams: 0, oz: 0, formatted: '0g / 0oz' }
    }
    
    // Sugar conversion factors (grams per liter for 1 volume CO2)
    const sugarFactors = {
      table: 4.0,   // Table sugar (sucrose)
      corn: 4.5,    // Corn sugar (dextrose)
      dme: 5.3,     // Dry malt extract
      honey: 3.8    // Honey
    }
    
    const factor = sugarFactors[sugarType]
    const totalGrams = co2Needed * factor * batchVolume
    const totalOz = totalGrams / 28.35
    
    return {
      grams: totalGrams,
      oz: totalOz,
      formatted: `${totalGrams.toFixed(0)}g / ${totalOz.toFixed(1)}oz`
    }
  }

  /**
   * Calculate strike water temperature and volume for mashing
   * @param grainTemp Grain temperature in Celsius
   * @param targetTemp Target mash temperature in Celsius
   * @param grainWeight Grain weight in kg
   * @param waterToGrainRatio Water to grain ratio in L/kg
   * @returns Strike water volume and temperature
   */
  function calculateStrikeWater(
    grainTemp: number,
    targetTemp: number,
    grainWeight: number,
    waterToGrainRatio: number = 3.0
  ) {
    const waterVolume = grainWeight * waterToGrainRatio
    const tempDiff = targetTemp - grainTemp
    const strikeTemp = targetTemp + (0.41 / waterToGrainRatio) * tempDiff
    
    return {
      volume: waterVolume,
      temperature: strikeTemp,
      formatted: `${waterVolume.toFixed(1)}L @ ${strikeTemp.toFixed(1)}°C`
    }
  }

  /**
   * Calculate water needed to dilute wort to target gravity
   * @param currentGravity Current gravity
   * @param currentVolume Current volume in liters
   * @param targetGravity Target gravity
   * @returns Water to add and final volume
   */
  function calculateDilution(
    currentGravity: number,
    currentVolume: number,
    targetGravity: number
  ) {
    if (currentGravity <= targetGravity) {
      return {
        volume: 0,
        finalVolume: currentVolume,
        formatted: 'No dilution needed'
      }
    }
    
    const gravityPoints = (currentGravity - 1) * 1000
    const targetPoints = (targetGravity - 1) * 1000
    
    const finalVolume = (gravityPoints * currentVolume) / targetPoints
    const waterToAdd = finalVolume - currentVolume
    
    return {
      volume: waterToAdd,
      finalVolume: finalVolume,
      formatted: `Add ${waterToAdd.toFixed(1)}L to reach ${finalVolume.toFixed(1)}L total`
    }
  }

  /**
   * Calculate yeast pitch rate
   * @param targetGravity Target gravity
   * @param batchVolume Batch volume in liters
   * @param yeastType Type of beer (ale, lager, high-gravity)
   * @returns Required yeast cells in billions and number of packages
   */
  function calculateYeastPitchRate(
    targetGravity: number,
    batchVolume: number,
    yeastType: 'ale' | 'lager' | 'high-gravity' = 'ale'
  ) {
    const gravityPoints = (targetGravity - 1) * 1000
    
    // Pitch rate: million cells per mL per degree Plato
    const pitchRates = {
      ale: 0.75,
      lager: 1.5,
      'high-gravity': 1.5
    }
    
    const rate = pitchRates[yeastType]
    const plato = gravityPoints / 4 // Rough conversion
    const totalCells = rate * (batchVolume * 1000) * plato // in millions
    const billion = totalCells / 1000
    const packages = Math.ceil(billion / 100) // Assuming 100B cells per package
    
    return {
      billion,
      packages,
      formatted: `${billion.toFixed(0)} billion cells (${packages} packages)`
    }
  }

  /**
   * Calculate mash efficiency
   * @param og Original Gravity achieved
   * @param grainWeight Total grain weight in kg
   * @param batchSize Batch size in liters
   * @param potentialOG Theoretical max OG based on grain bill
   * @returns Efficiency percentage
   */
  function calculateMashEfficiency(
    og: number,
    grainWeight: number,
    batchSize: number,
    potentialOG: number
  ) {
    if (potentialOG <= 1.0 || og <= 1.0) {
      return { efficiency: 0, formatted: '0%' }
    }
    
    const actualPoints = (og - 1) * 1000
    const potentialPoints = (potentialOG - 1) * 1000
    const efficiency = (actualPoints / potentialPoints) * 100
    
    return {
      efficiency,
      formatted: `${efficiency.toFixed(1)}%`
    }
  }

  /**
   * Calculate attenuation percentage
   * @param og Original Gravity
   * @param fg Final Gravity
   * @returns Attenuation percentage
   */
  function calculateAttenuation(og: number, fg: number) {
    if (og <= 1.0 || fg <= 0) {
      return { attenuation: 0, formatted: '0%' }
    }
    
    const attenuation = ((og - fg) / (og - 1)) * 100
    
    return {
      attenuation,
      formatted: `${attenuation.toFixed(1)}%`
    }
  }

  /**
   * Convert gravity to Plato
   * Using the standard brewing formula
   * @param gravity Specific gravity
   * @returns Degrees Plato
   */
  function gravityToPlato(gravity: number): number {
    // Standard brewing conversion constants
    const PLATO_CONSTANT_A = -463.37
    const PLATO_CONSTANT_B = 668.72
    const PLATO_CONSTANT_C = 205.35
    
    return PLATO_CONSTANT_A + (PLATO_CONSTANT_B * gravity) - (PLATO_CONSTANT_C * gravity * gravity)
  }

  /**
   * Convert Plato to gravity
   * Using the standard brewing formula
   * @param plato Degrees Plato
   * @returns Specific gravity
   */
  function platoToGravity(plato: number): number {
    // Standard brewing conversion constants
    const GRAVITY_CONSTANT_A = 258.6
    const GRAVITY_CONSTANT_B = 258.2
    const GRAVITY_CONSTANT_C = 227.1
    
    return 1 + (plato / (GRAVITY_CONSTANT_A - ((plato / GRAVITY_CONSTANT_B) * GRAVITY_CONSTANT_C)))
  }

  return {
    calculateABV,
    calculateIBU,
    calculateSRM,
    getSRMColor,
    calculatePrimingSugar,
    calculateStrikeWater,
    calculateDilution,
    calculateYeastPitchRate,
    calculateMashEfficiency,
    calculateAttenuation,
    gravityToPlato,
    platoToGravity,
  }
}
