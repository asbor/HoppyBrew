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
    [key: string]: any
  }
  is_active: boolean
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
  is_active?: boolean
}

export interface DeviceUpdate {
  name?: string
  device_type?: string
  description?: string
  api_endpoint?: string
  api_token?: string
  calibration_data?: Record<string, any>
  configuration?: Record<string, any>
  is_active?: boolean
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

  return {
    getAllDevices,
    getDevice,
    createDevice,
    updateDevice,
    deleteDevice,
    toggleDeviceStatus,
  }
}
