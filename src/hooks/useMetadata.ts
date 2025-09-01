import { useState, useEffect } from 'react'

interface MetadataItem {
  id: number
  name: string
}

interface MetadataResponse {
  status: string
  code: number
  data: MetadataItem[]
  message: string
}

type MetadataKind = 'spirits' | 'liqueur' | 'ingredient'
type MetadataCategory = 'aroma' | 'taste' | 'finish'

export const useMetadata = (kind: MetadataKind, category: MetadataCategory) => {
  const [data, setData] = useState<MetadataItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(`/api/v1/metadata/${kind}/${category}`)

        if (!response.ok) {
          throw new Error(`Failed to fetch metadata: ${response.status}`)
        }

        const result: MetadataResponse = await response.json()

        if (result.status === 'success') {
          setData(result.data)
        } else {
          throw new Error(result.message || 'Failed to fetch metadata')
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error occurred')
        setData([])
      } finally {
        setLoading(false)
      }
    }

    void fetchMetadata()
  }, [kind, category])

  return { data, loading, error }
}
