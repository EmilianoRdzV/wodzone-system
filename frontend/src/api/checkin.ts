import axios from 'axios'
import type { CheckInResponse } from '../types'

const API_BASE = '/api'

export async function getMemberInfo(qr: string): Promise<CheckInResponse> {
  const response = await axios.get<CheckInResponse>(`${API_BASE}/member/${qr}/`)
  return response.data
}

export async function postCheckin(qr: string): Promise<CheckInResponse> {
  const response = await axios.post<CheckInResponse>(`${API_BASE}/checkin/`, { qr_code: qr })
  return response.data
}
