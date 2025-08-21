import { useQuery, useQueryClient } from '@tanstack/react-query'

// API base URL
const API_BASE_URL = '/api/v1'

// Custom hook for API calls with React Query
export const useApi = () => {
  const queryClient = useQueryClient()

  // Generic GET request
  const get = async <T>(endpoint: string): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`)
    }

    return response.json()
  }

  // Generic POST request
  const post = async <T>(endpoint: string, data?: unknown): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: data ? JSON.stringify(data) : undefined,
    })

    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`)
    }

    return response.json()
  }

  // Generic PUT request
  const put = async <T>(endpoint: string, data?: unknown): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: data ? JSON.stringify(data) : undefined,
    })

    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`)
    }

    return response.json()
  }

  // Generic DELETE request
  const del = async <T>(endpoint: string): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`${response.status}: ${response.statusText}`)
    }

    return response.json()
  }

  return {
    get,
    post,
    put,
    del,
    queryClient,
  }
}

// Hook for health check
export const useHealthCheck = () => {
  const { get } = useApi()

  return useQuery({
    queryKey: ['health'],
    queryFn: () => get('/health'),
    refetchInterval: 30000, // Refetch every 30 seconds
  })
}

// Hook for spirits data
export const useSpirits = (search?: string) => {
  const { get } = useApi()

  return useQuery({
    queryKey: ['spirits', search],
    queryFn: () => get(`/spirits${search ? `?q=${encodeURIComponent(search)}` : ''}`),
    enabled: true,
  })
}

// Hook for single spirit
export const useSpirit = (name: string) => {
  const { get } = useApi()

  return useQuery({
    queryKey: ['spirit', name],
    queryFn: () => get(`/spirits/${encodeURIComponent(name)}`),
    enabled: !!name,
  })
}

// Hook for metadata
export const useMetadata = (kind: string, category: string) => {
  const { get } = useApi()

  return useQuery({
    queryKey: ['metadata', kind, category],
    queryFn: () => get(`/metadata/${kind}/${category}`),
    enabled: !!kind && !!category,
  })
}
