import axios from 'axios'

const http = axios.create({ baseURL: '/api' })

export interface TestRecord {
  id: number
  sample_id: string
  test_name: string
  operator?: string
  equipment?: string
  result_value?: number
  unit?: string
  status?: string
  note?: string
  created_at: string
}

export const listRecords = (params: any) =>
  http.get<TestRecord[]>('/records', { params }).then((r) => r.data)

export const countRecords = (params: any) =>
  http.get<{ total: number }>('/records/count', { params }).then((r) => r.data)

export const createRecord = (data: any) =>
  http.post<TestRecord>('/records', data).then((r) => r.data)

export const updateRecord = (id: number, data: any) =>
  http.put<TestRecord>(`/records/${id}`, data).then((r) => r.data)

export const deleteRecord = (id: number) =>
  http.delete(`/records/${id}`).then((r) => r.data)

export const seedRecords = (n: number) =>
  http.post<{ inserted: number }>('/seed', null, { params: { n } }).then((r) => r.data)
