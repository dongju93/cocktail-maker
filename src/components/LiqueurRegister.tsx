import { useForm } from '@tanstack/react-form'
import type React from 'react'
import { useMetadata } from '../hooks/useMetadata'
import type { LiqueurFormData } from '../types/forms'
import { ImageUpload } from './ImageUpload'

export const LiqueurRegister: React.FC = () => {
  // Fetch metadata for taste profiles
  const { data: tasteOptions, loading: tasteLoading } = useMetadata('liqueur', 'taste')

  const form = useForm<
    LiqueurFormData,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined
  >({
    defaultValues: {
      name: '',
      brand: '',
      taste: [],
      kind: '',
      subKind: '',
      mainIngredients: [],
      volume: 0,
      abv: 0,
      originNation: '',
      description: '',
      mainImage: null,
    },
    onSubmit: async ({ value }: { value: LiqueurFormData }) => {
      try {
        const formData = new FormData()

        // Add all text fields
        formData.append('name', value.name)
        formData.append('brand', value.brand)
        formData.append('taste', JSON.stringify(value.taste))
        formData.append('kind', value.kind)
        formData.append('subKind', value.subKind)
        formData.append('mainIngredients', JSON.stringify(value.mainIngredients))
        formData.append('volume', value.volume.toString())
        formData.append('abv', value.abv.toString())
        formData.append('originNation', value.originNation)
        formData.append('description', value.description)

        // Add image file
        if (value.mainImage) {
          formData.append('mainImage', value.mainImage)
        }

        const response = await fetch('/api/v1/liqueur', {
          method: 'POST',
          body: formData,
        })

        if (response.ok) {
          const result = await response.json()
          console.log('Liqueur registered successfully:', result)
          alert('리큐르가 성공적으로 등록되었습니다!')
          form.reset()
        } else {
          const error = await response.json()
          console.error('Registration failed:', error)
          alert(`등록 실패: ${error.message || '알 수 없는 오류가 발생했습니다'}`)
        }
      } catch (error) {
        console.error('Network error:', error)
        alert('네트워크 오류가 발생했습니다. 다시 시도해주세요.')
      }
    },
  })

  const handleArrayFieldChange = (fieldName: 'mainIngredients', value: string) => {
    const values = value
      .split(',')
      .map((v) => v.trim())
      .filter((v) => v.length > 0)
    form.setFieldValue(fieldName, values)
  }

  const handleCheckboxChange = (fieldName: 'taste', itemId: number, isChecked: boolean) => {
    const currentValue = form.getFieldValue(fieldName) || []
    let newValue: string[]

    if (isChecked) {
      newValue = Array.isArray(currentValue)
        ? [...currentValue, itemId.toString()]
        : [itemId.toString()]
    } else {
      newValue = Array.isArray(currentValue)
        ? currentValue.filter((id) => id !== itemId.toString())
        : []
    }

    form.setFieldValue(fieldName, newValue)
  }

  return (
    <div className="mx-auto max-w-4xl rounded-lg bg-white p-6 shadow-lg">
      <h1 className="mb-8 font-bold text-3xl text-gray-800">리큐르 등록</h1>

      <form
        className="space-y-6"
        onSubmit={(e) => {
          e.preventDefault()
          e.stopPropagation()
          form.handleSubmit()
        }}
      >
        {/* Basic Information */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <form.Field
            name="name"
            validators={{
              onChange: ({ value }: { value: string }) =>
                !value
                  ? '이름은 필수 입력 사항입니다'
                  : value.length < 1
                    ? '이름은 최소 1자 이상이어야 합니다'
                    : value.length > 100
                      ? '이름은 100자를 초과할 수 없습니다'
                      : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  이름 *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="리큐르 이름을 입력하세요"
                  type="text"
                  value={field.state.value}
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>

          <form.Field
            name="brand"
            validators={{
              onChange: ({ value }: { value: string }) =>
                !value
                  ? '브랜드는 필수 입력 사항입니다'
                  : value.length > 100
                    ? '브랜드는 100자를 초과할 수 없습니다'
                    : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  브랜드 *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="브랜드명을 입력하세요"
                  type="text"
                  value={field.state.value}
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>

          <form.Field
            name="kind"
            validators={{
              onChange: ({ value }: { value: string }) =>
                !value
                  ? '종류는 필수 입력 사항입니다'
                  : value.length > 50
                    ? '종류는 50자를 초과할 수 없습니다'
                    : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  종류 *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="예: 과일 리큐르, 허브 리큐르, 크림 리큐르 등"
                  type="text"
                  value={field.state.value}
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>

          <form.Field
            name="subKind"
            validators={{
              onChange: ({ value }: { value: string }) =>
                !value
                  ? '세부 종류는 필수 입력 사항입니다'
                  : value.length > 50
                    ? '세부 종류는 50자를 초과할 수 없습니다'
                    : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  세부 종류 *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="예: 오렌지 리큐르, 커피 리큐르 등"
                  type="text"
                  value={field.state.value}
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>

          <form.Field
            name="volume"
            validators={{
              onChange: ({ value }: { value: number }) =>
                value <= 0
                  ? '용량은 0보다 커야 합니다'
                  : value > 1000
                    ? '용량은 1000mL를 초과할 수 없습니다'
                    : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  용량 (mL) *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(Number.parseFloat(e.target.value) || 0)}
                  placeholder="예: 500"
                  step="0.01"
                  type="number"
                  value={field.state.value}
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>

          <form.Field
            name="abv"
            validators={{
              onChange: ({ value }: { value: number }) =>
                value <= 0
                  ? '도수는 0보다 커야 합니다'
                  : value > 100
                    ? '도수는 100%를 초과할 수 없습니다'
                    : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  알코올 도수 (%) *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(Number.parseFloat(e.target.value) || 0)}
                  placeholder="예: 20"
                  step="0.1"
                  type="number"
                  value={field.state.value}
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>

          <form.Field
            name="originNation"
            validators={{
              onChange: ({ value }: { value: string }) =>
                !value
                  ? '원산지 국가는 필수 입력 사항입니다'
                  : value.length > 50
                    ? '원산지 국가는 50자를 초과할 수 없습니다'
                    : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  원산지 국가 *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="예: 프랑스, 이탈리아, 아일랜드 등"
                  type="text"
                  value={field.state.value}
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>
        </div>

        {/* Taste and Ingredients */}
        <div className="space-y-4">
          <h2 className="font-semibold text-gray-800 text-xl">맛과 재료</h2>

          <form.Field
            name="taste"
            validators={{
              onChange: ({ value }: { value: string[] }) =>
                !value || (Array.isArray(value) && value.length === 0)
                  ? '맛은 필수 입력 사항입니다'
                  : undefined,
            }}
          >
            {(field) => (
              <div>
                <h3 className="mb-2 block font-medium text-gray-700 text-sm">맛 (Taste) *</h3>
                {tasteLoading ? (
                  <div className="text-gray-500 text-sm">로딩 중...</div>
                ) : (
                  <div className="grid max-h-40 grid-cols-2 gap-2 overflow-y-auto rounded-md border border-gray-300 p-3 md:grid-cols-3">
                    {tasteOptions.map((option) => (
                      <label
                        className="flex cursor-pointer items-center space-x-2 rounded p-1 hover:bg-gray-50"
                        key={option.id}
                      >
                        <input
                          checked={
                            Array.isArray(field.state.value) &&
                            field.state.value.includes(option.id.toString())
                          }
                          className="text-blue-600 focus:ring-blue-500"
                          onChange={(e) =>
                            handleCheckboxChange('taste', option.id, e.target.checked)
                          }
                          type="checkbox"
                        />
                        <span className="text-gray-700 text-sm">{option.name}</span>
                      </label>
                    ))}
                  </div>
                )}
                <p className="mt-1 text-gray-500 text-xs">원하는 맛을 선택해주세요</p>
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>

          <form.Field
            name="mainIngredients"
            validators={{
              onChange: ({ value }: { value: string[] }) =>
                !value || (Array.isArray(value) && value.length === 0)
                  ? '주재료는 필수 입력 사항입니다'
                  : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  주재료 *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => handleArrayFieldChange('mainIngredients', e.target.value)}
                  placeholder="쉼표로 구분하여 입력 (예: 오렌지 껍질, 설탕, 브랜디)"
                  type="text"
                  value={
                    field.state.value && Array.isArray(field.state.value)
                      ? field.state.value.join(', ')
                      : ''
                  }
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>
        </div>

        {/* Description */}
        <form.Field
          name="description"
          validators={{
            onChange: ({ value }: { value: string }) =>
              !value
                ? '설명은 필수 입력 사항입니다'
                : value.length > 1000
                  ? '설명은 1000자를 초과할 수 없습니다'
                  : undefined,
          }}
        >
          {(field) => (
            <div>
              <label className="mb-2 block font-medium text-gray-700 text-sm" htmlFor={field.name}>
                설명 *
              </label>
              <textarea
                className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                id={field.name}
                name={field.name}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
                placeholder="리큐르에 대한 자세한 설명을 입력하세요"
                rows={4}
                value={field.state.value}
              />
              {field.state.meta.errors.length > 0 && (
                <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
              )}
            </div>
          )}
        </form.Field>

        {/* Image Upload */}
        <div className="space-y-4">
          <h2 className="font-semibold text-gray-800 text-xl">이미지 업로드</h2>

          <form.Field
            name="mainImage"
            validators={{
              onChange: ({ value }: { value: File | null }) =>
                !value ? '대표 이미지는 필수입니다' : undefined,
            }}
          >
            {(field) => (
              <ImageUpload
                accept="image/jpeg,image/png,image/jpg,image/webp,image/bmp,image/gif,image/tiff"
                error={field.state.meta.errors[0]}
                id={field.name}
                label="대표 이미지"
                maxSize={2}
                name={field.name}
                onBlur={field.handleBlur}
                onChange={(file) => field.handleChange(file)}
                required
                value={field.state.value}
              />
            )}
          </form.Field>
        </div>

        {/* Submit Button */}
        <form.Subscribe
          selector={(state) => ({ canSubmit: state.canSubmit, isSubmitting: state.isSubmitting })}
        >
          {({ canSubmit, isSubmitting }) => (
            <div className="flex justify-end space-x-4">
              <button
                className="rounded-md border border-gray-300 px-6 py-2 text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
                onClick={() => form.reset()}
                type="button"
              >
                초기화
              </button>
              <button
                className="rounded-md bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-400"
                disabled={!canSubmit || isSubmitting}
                type="submit"
              >
                {isSubmitting ? '등록 중...' : '등록'}
              </button>
            </div>
          )}
        </form.Subscribe>
      </form>
    </div>
  )
}
