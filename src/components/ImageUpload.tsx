import React, { useCallback, useState } from 'react'

interface ImageUploadProps {
  id: string
  name: string
  label: string
  required?: boolean
  accept?: string
  maxSize?: number // in MB
  value: File | null
  onChange: (file: File | null) => void
  onBlur?: () => void
  error?: string
  className?: string
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  id,
  name,
  label,
  required = false,
  accept = 'image/jpeg,image/png,image/jpg,image/webp,image/bmp,image/gif,image/tiff',
  maxSize = 2,
  value,
  onChange,
  onBlur,
  error,
  className = '',
}) => {
  const [isDragOver, setIsDragOver] = useState(false)
  const [preview, setPreview] = useState<string | null>(null)

  // Generate preview URL when file changes
  React.useEffect(() => {
    if (value) {
      const url = URL.createObjectURL(value)
      setPreview(url)
      return () => URL.revokeObjectURL(url)
    }
    setPreview(null)
  }, [value])

  const validateFile = useCallback(
    (file: File): string | null => {
      if (file.size > maxSize * 1024 * 1024) {
        return `파일 크기가 ${maxSize}MB를 초과합니다.`
      }

      const acceptedTypes = accept.split(',').map((type) => type.trim())
      if (!acceptedTypes.includes(file.type)) {
        return '지원하지 않는 파일 형식입니다.'
      }

      return null
    },
    [accept, maxSize],
  )

  const handleFileChange = useCallback(
    (file: File | null) => {
      if (!file) {
        onChange(null)
        return
      }

      const validationError = validateFile(file)
      if (validationError) {
        alert(validationError)
        return
      }

      onChange(file)
    },
    [onChange, validateFile],
  )

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0] || null
      handleFileChange(file)
    },
    [handleFileChange],
  )

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragOver(false)

      const files = e.dataTransfer.files
      if (files.length > 0) {
        handleFileChange(files[0])
      }
    },
    [handleFileChange],
  )

  const handleRemove = useCallback(() => {
    onChange(null)
  }, [onChange])

  const supportedFormats = accept
    .split(',')
    .map((type) => {
      const extension = type.split('/')[1]?.toUpperCase()
      return extension
    })
    .join(', ')

  return (
    <div className={className}>
      <label className="mb-2 block font-medium text-gray-700 text-sm" htmlFor={id}>
        {label} {required && '*'}
      </label>

      <button
        className={`relative w-full rounded-lg border-2 border-dashed transition-colors ${
          isDragOver
            ? 'border-blue-400 bg-blue-50'
            : value
              ? 'border-green-300 bg-green-50'
              : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        type="button"
      >
        {preview ? (
          <div className="relative p-4">
            <img
              alt="Preview"
              className="mx-auto max-h-48 max-w-full rounded-md shadow-sm"
              src={preview}
            />
            <div className="mt-3 flex items-center justify-between">
              <span className="mr-2 flex-1 truncate text-gray-600 text-sm">{value?.name}</span>
              <button
                className="font-medium text-red-600 text-sm hover:text-red-800"
                onClick={handleRemove}
                type="button"
              >
                제거
              </button>
            </div>
          </div>
        ) : (
          <div className="p-8 text-center">
            <svg
              aria-label="Upload image"
              className="mx-auto mb-4 h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 48 48"
            >
              <title>Upload image</title>
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
              />
            </svg>

            <div className="space-y-2">
              <p className="text-gray-600">
                <span className="font-medium">이미지를 드래그하여 업로드하거나</span>
              </p>
              <label
                className="inline-flex cursor-pointer items-center rounded-md border border-transparent bg-blue-600 px-4 py-2 font-medium text-sm text-white transition-colors hover:bg-blue-700"
                htmlFor={id}
              >
                파일 선택
              </label>
            </div>

            <input
              accept={accept}
              className="sr-only"
              id={id}
              name={name}
              onBlur={onBlur}
              onChange={handleInputChange}
              type="file"
            />
          </div>
        )}
      </button>

      <p className="mt-2 text-gray-500 text-xs">
        최대 {maxSize}MB, {supportedFormats} 형식 지원
      </p>

      {error && <p className="mt-1 text-red-600 text-sm">{error}</p>}
    </div>
  )
}
