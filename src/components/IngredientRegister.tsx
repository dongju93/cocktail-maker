import { useForm } from '@tanstack/react-form'
import type React from 'react'
import type { IngredientFormData } from '../types/forms'
import { ImageUpload } from './ImageUpload'

export const IngredientRegister: React.FC = () => {
  const form = useForm<
    IngredientFormData,
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
      brand: [],
      kind: '',
      originNation: '',
      description: '',
      mainImage: null,
    },
    onSubmit: async ({ value }: { value: IngredientFormData }) => {
      try {
        const formData = new FormData()

        // Add all text fields
        formData.append('name', value.name)
        if (value.brand && value.brand.length > 0) {
          formData.append('brand', JSON.stringify(value.brand))
        }
        formData.append('kind', value.kind)
        formData.append('description', value.description)

        // Add image file
        if (value.mainImage) {
          formData.append('mainImage', value.mainImage)
        }

        const response = await fetch('/api/v1/ingredient', {
          method: 'POST',
          body: formData,
        })

        if (response.ok) {
          const result = await response.json()
          console.log('Ingredient registered successfully:', result)
          alert('재료가 성공적으로 등록되었습니다!')
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

  const handleBrandFieldChange = (value: string) => {
    const values = value
      .split(',')
      .map((v) => v.trim())
      .filter((v) => v.length > 0)
    form.setFieldValue('brand', values.length > 0 ? values : [])
  }

  return (
    <div className="mx-auto max-w-4xl rounded-lg bg-white p-6 shadow-lg">
      <h1 className="mb-8 font-bold text-3xl text-gray-800">기타 재료 등록</h1>

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
                  placeholder="재료 이름을 입력하세요"
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
                  placeholder="예: 시럽, 과일, 향신료, 가니쉬 등"
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

        {/* Brand (Optional) */}
        <form.Field
          name="brand"
          validators={{
            onChange: ({ value }: { value: string[] }) =>
              value && Array.isArray(value) && value.length > 10
                ? '브랜드는 최대 10개까지 입력할 수 있습니다'
                : undefined,
          }}
        >
          {(field) => (
            <div>
              <label className="mb-2 block font-medium text-gray-700 text-sm" htmlFor={field.name}>
                브랜드 (선택사항)
              </label>
              <input
                className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                id={field.name}
                name={field.name}
                onBlur={field.handleBlur}
                onChange={(e) => handleBrandFieldChange(e.target.value)}
                placeholder="쉼표로 구분하여 입력 (예: 몬닌, 토라니, 앙고스투라)"
                type="text"
                value={
                  field.state.value && Array.isArray(field.state.value)
                    ? field.state.value.join(', ')
                    : ''
                }
              />
              <p className="mt-1 text-gray-500 text-xs">
                여러 브랜드가 있는 경우 쉼표로 구분해서 입력하세요 (최대 10개)
              </p>
              {field.state.meta.errors.length > 0 && (
                <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
              )}
            </div>
          )}
        </form.Field>

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
                placeholder="재료에 대한 자세한 설명을 입력하세요 (사용법, 특징, 맛 등)"
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

        {/* Additional Information */}
        <div className="rounded-md bg-blue-50 p-4">
          <h3 className="mb-2 font-medium text-blue-900 text-lg">등록 안내</h3>
          <ul className="space-y-1 text-blue-800 text-sm">
            <li>• 모든 필수 항목(*)은 반드시 입력해야 합니다.</li>
            <li>
              • 브랜드는 선택사항이지만, 여러 브랜드가 있는 경우 쉼표로 구분해서 입력해주세요.
            </li>
            <li>
              • 이미지는 드래그앤드롭 또는 파일 선택으로 업로드 가능하며, 최대 2MB까지 지원합니다.
            </li>
            <li>• 설명란에는 재료의 특징, 사용법, 맛 등을 자세히 입력해주세요.</li>
          </ul>
        </div>

        {/* Form Status Display */}
        <form.Subscribe
          selector={(state) => ({ canSubmit: state.canSubmit, isSubmitting: state.isSubmitting })}
        >
          {({ canSubmit, isSubmitting }) => (
            <div className="space-y-2">
              {canSubmit && !isSubmitting && (
                <div className="rounded-md border border-green-200 bg-green-50 p-3">
                  <p className="text-green-800 text-sm">
                    모든 필수 항목이 입력되었습니다. 등록할 준비가 되었습니다!
                  </p>
                </div>
              )}
            </div>
          )}
        </form.Subscribe>

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
