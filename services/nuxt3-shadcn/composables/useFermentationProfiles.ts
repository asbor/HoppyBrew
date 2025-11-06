/**
 * Composable for fermentation profile management
 * Provides CRUD operations for fermentation profiles and steps
 */

import { useApi } from './useApi'

export interface FermentationStep {
  id?: number
  fermentation_profile_id?: number
  step_order: number
  name?: string
  step_type: string
  temperature?: number
  duration_days?: number
  ramp_days?: number
  pressure_psi?: number
  notes?: string
  created_at?: string
}

export interface FermentationProfile {
  id?: number
  name: string
  description?: string
  is_pressurized: boolean
  is_template: boolean
  created_at?: string
  updated_at?: string
  steps?: FermentationStep[]
}

export const useFermentationProfiles = () => {
  const api = useApi()

  /**
   * Get all fermentation profiles
   */
  const getAllProfiles = async () => {
    return await api.get<FermentationProfile[]>('/fermentation-profiles')
  }

  /**
   * Get a specific fermentation profile by ID
   */
  const getProfile = async (id: number) => {
    return await api.get<FermentationProfile>(`/fermentation-profiles/${id}`)
  }

  /**
   * Create a new fermentation profile
   */
  const createProfile = async (profile: FermentationProfile) => {
    return await api.post<FermentationProfile>('/fermentation-profiles', profile)
  }

  /**
   * Update a fermentation profile
   */
  const updateProfile = async (id: number, profile: Partial<FermentationProfile>) => {
    return await api.put<FermentationProfile>(`/fermentation-profiles/${id}`, profile)
  }

  /**
   * Delete a fermentation profile
   */
  const deleteProfile = async (id: number) => {
    return await api.delete(`/fermentation-profiles/${id}`)
  }

  /**
   * Get steps for a profile
   */
  const getSteps = async (profileId: number) => {
    return await api.get<FermentationStep[]>(`/fermentation-profiles/${profileId}/steps`)
  }

  /**
   * Add a step to a profile
   */
  const addStep = async (profileId: number, step: FermentationStep) => {
    return await api.post<FermentationStep>(`/fermentation-profiles/${profileId}/steps`, step)
  }

  /**
   * Update a step
   */
  const updateStep = async (stepId: number, step: Partial<FermentationStep>) => {
    return await api.put<FermentationStep>(`/fermentation-steps/${stepId}`, step)
  }

  /**
   * Delete a step
   */
  const deleteStep = async (stepId: number) => {
    return await api.delete(`/fermentation-steps/${stepId}`)
  }

  return {
    getAllProfiles,
    getProfile,
    createProfile,
    updateProfile,
    deleteProfile,
    getSteps,
    addStep,
    updateStep,
    deleteStep,
  }
}

/**
 * Predefined fermentation profile templates
 */
export const FERMENTATION_TEMPLATES = {
  ale: {
    name: 'Standard Ale',
    description: 'Basic ale fermentation profile with primary and conditioning phases',
    is_pressurized: false,
    is_template: true,
    steps: [
      {
        step_order: 1,
        name: 'Primary Fermentation',
        step_type: 'primary',
        temperature: 20,
        duration_days: 7,
        ramp_days: 0,
        notes: 'Primary fermentation at 20°C',
      },
      {
        step_order: 2,
        name: 'Conditioning',
        step_type: 'conditioning',
        temperature: 18,
        duration_days: 7,
        ramp_days: 1,
        notes: 'Conditioning phase with gradual temperature ramp',
      },
    ],
  },
  lager: {
    name: 'Lager',
    description: 'Traditional lager fermentation profile with lagering phase',
    is_pressurized: false,
    is_template: true,
    steps: [
      {
        step_order: 1,
        name: 'Primary Fermentation',
        step_type: 'primary',
        temperature: 10,
        duration_days: 14,
        ramp_days: 0,
      },
      {
        step_order: 2,
        name: 'Diacetyl Rest',
        step_type: 'diacetyl_rest',
        temperature: 18,
        duration_days: 2,
        ramp_days: 1,
      },
      {
        step_order: 3,
        name: 'Lagering',
        step_type: 'lagering',
        temperature: 2,
        duration_days: 28,
        ramp_days: 2,
      },
    ],
  },
  neipa: {
    name: 'NEIPA',
    description: 'New England IPA fermentation profile with cold crash',
    is_pressurized: false,
    is_template: true,
    steps: [
      {
        step_order: 1,
        name: 'Primary Fermentation',
        step_type: 'primary',
        temperature: 19,
        duration_days: 4,
        ramp_days: 0,
      },
      {
        step_order: 2,
        name: 'Dry Hop Conditioning',
        step_type: 'conditioning',
        temperature: 21,
        duration_days: 3,
        ramp_days: 0,
      },
      {
        step_order: 3,
        name: 'Cold Crash',
        step_type: 'cold_crash',
        temperature: 4,
        duration_days: 2,
        ramp_days: 1,
      },
    ],
  },
}

/**
 * Step type options
 */
export const STEP_TYPES = [
  { value: 'primary', label: 'Primary Fermentation' },
  { value: 'secondary', label: 'Secondary Fermentation' },
  { value: 'conditioning', label: 'Conditioning' },
  { value: 'cold_crash', label: 'Cold Crash' },
  { value: 'diacetyl_rest', label: 'Diacetyl Rest' },
  { value: 'lagering', label: 'Lagering' },
]
