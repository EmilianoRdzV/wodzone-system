export interface CheckInResponse {
  success: boolean
  message: string
  name: string
  streakCurrent: number
  streakName: string
  expiryDate: string
  error?: string
}

export interface MemberInfo {
  name: string
  streakCurrent: number
  streakName: string
  expiryDate: string
  hasStreak: boolean
}
