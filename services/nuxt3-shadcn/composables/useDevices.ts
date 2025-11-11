/**
 * Device management composable
 * Handles external brewing device configurations (iSpindel, Tilt, etc.)
 */

export interface Device {
  id: number
  name: string
  device_type: string // ispindel, tilt, etc.
  description?: string
  api_endpoint?: string
  api_token?: string
  calibration_data?: {
    polynomial?: number[]
    temp_correction?: boolean
    [key: string]: any
  }
  configuration?: {
    update_interval?: number
    battery_warning_threshold?: number
    cloud_url?: string
    hydrometer_id?: string
    [key: string]: any
  }
  alert_config?: {
    enable_alerts?: boolean
    temperature_min?: number
    temperature_max?: number
    [key: string]: any
  }
  is_active: boolean
  batch_id?: number
  last_reading_at?: string
  created_at: string
  updated_at?: string
}

export interface DeviceCreate {
  name: string
  device_type: string
  description?: string
  api_endpoint?: string
  api_token?: string
  calibration_data?: Record<string, any>
  configuration?: Record<string, any>
  alert_config?: Record<string, any>
  is_active?: boolean
  batch_id?: number
}

export interface DeviceUpdate {
  name?: string
  device_type?: string
  description?: string
  api_endpoint?: string
  api_token?: string
  calibration_data?: Record<string, any>
  configuration?: Record<string, any>
  alert_config?: Record<string, any>
  is_active?: boolean
  batch_id?: number
}

export const useDevices = () => {
  const api = useApi()

  /**
   * Fetch all devices
   */
  const getAllDevices = async () => {
    return await api.get<Device[]>('/devices')
  }

  /**
   * Fetch a specific device by ID
   */
  const getDevice = async (deviceId: number) => {
    return await api.get<Device>(`/devices/${deviceId}`)
  }

  /**
   * Create a new device
   */
  const createDevice = async (device: DeviceCreate) => {
    return await api.post<Device, DeviceCreate>('/devices', device)
  }

  /**
   * Update an existing device
   */
  const updateDevice = async (deviceId: number, device: DeviceUpdate) => {
    return await api.put<Device, DeviceUpdate>(`/devices/${deviceId}`, device)
  }

  /**
   * Delete a device
   */
  const deleteDevice = async (deviceId: number) => {
    return await api.delete<Device>(`/devices/${deviceId}`)
  }

  /**
   * Toggle device active status
   */
  const toggleDeviceStatus = async (deviceId: number, isActive: boolean) => {
    return await updateDevice(deviceId, { is_active: isActive })
  }

  /**
   * Associate device with batch for automatic data collection
   */
  const associateDeviceWithBatch = async (deviceId: number, batchId: number) => {
    return await api.post(`/devices/${deviceId}/batch/${batchId}/associate`, {})
  }

  /**
   * Dissociate device from batch (manual override)
   */
  const dissociateDeviceFromBatch = async (deviceId: number) => {
    return await api.delete(`/devices/${deviceId}/batch`)
  }

  /**
   * Get devices associated with a specific batch
   */
  const getDevicesByBatch = async (batchId: number) => {
    const devices = await getAllDevices()
    return devices.filter((device: Device) => device.batch_id === batchId)
  }

  return {
    getAllDevices,
    getDevice,
    createDevice,
    updateDevice,
    deleteDevice,
    toggleDeviceStatus,
    associateDeviceWithBatch,
    dissociateDeviceFromBatch,
    getDevicesByBatch,
  }
}
