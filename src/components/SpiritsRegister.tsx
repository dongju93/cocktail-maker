import { useForm } from '@tanstack/react-form'
import type React from 'react'
import { useMetadata } from '../hooks/useMetadata'
import type { SpiritsFormData } from '../types/forms'
import { ImageUpload } from './ImageUpload'

export const SpiritsRegister: React.FC = () => {
  // Fetch metadata for taste profiles
  const { data: aromaOptions, loading: aromaLoading } = useMetadata('spirits', 'aroma')
  const { data: tasteOptions, loading: tasteLoading } = useMetadata('spirits', 'taste')
  const { data: finishOptions, loading: finishLoading } = useMetadata('spirits', 'finish')

  const form = useForm<
    SpiritsFormData,
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
      aroma: [],
      taste: [],
      finish: [],
      kind: '',
      subKind: '',
      amount: 0,
      alcohol: 0,
      originNation: '',
      originLocation: '',
      description: '',
      mainImage: null,
      subImage1: null,
      subImage2: null,
      subImage3: null,
      subImage4: null,
    },
    onSubmit: async ({ value }: { value: SpiritsFormData }) => {
      try {
        const formData = new FormData()

        // Add all text fields
        formData.append('name', value.name)
        formData.append('aroma', JSON.stringify(value.aroma))
        formData.append('taste', JSON.stringify(value.taste))
        formData.append('finish', JSON.stringify(value.finish))
        formData.append('kind', value.kind)
        formData.append('subKind', value.subKind)
        formData.append('amount', value.amount.toString())
        formData.append('alcohol', value.alcohol.toString())
        formData.append('originNation', value.originNation)
        formData.append('originLocation', value.originLocation)
        formData.append('description', value.description)

        // Add image files
        if (value.mainImage) {
          formData.append('mainImage', value.mainImage)
        }
        if (value.subImage1) {
          formData.append('subImage1', value.subImage1)
        }
        if (value.subImage2) {
          formData.append('subImage2', value.subImage2)
        }
        if (value.subImage3) {
          formData.append('subImage3', value.subImage3)
        }
        if (value.subImage4) {
          formData.append('subImage4', value.subImage4)
        }

        const response = await fetch('/api/v1/spirits', {
          method: 'POST',
          body: formData,
        })

        if (response.ok) {
          const result = await response.json()
          console.log('Spirits registered successfully:', result)
          alert('주류가 성공적으로 등록되었습니다!')
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

  // Removed unused function

  const handleCheckboxChange = (
    fieldName: 'aroma' | 'taste' | 'finish',
    itemId: number,
    isChecked: boolean,
  ) => {
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
      <h1 className="mb-8 font-bold text-3xl text-gray-800">주류 등록</h1>

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
                  placeholder="주류 이름을 입력하세요"
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
                !value ? '종류는 필수 입력 사항입니다' : undefined,
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
                  placeholder="예: 위스키, 진, 럼 등"
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
                !value ? '세부 종류는 필수 입력 사항입니다' : undefined,
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
                  placeholder="예: 싱글몰트, 스카치, 아이리시 등"
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
            name="amount"
            validators={{
              onChange: ({ value }: { value: number }) =>
                value <= 0 ? '용량은 0보다 커야 합니다' : undefined,
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
                  placeholder="예: 750"
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
            name="alcohol"
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
                  placeholder="예: 40"
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
                !value ? '원산지 국가는 필수 입력 사항입니다' : undefined,
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
                  placeholder="예: 스코틀랜드, 일본, 미국 등"
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
            name="originLocation"
            validators={{
              onChange: ({ value }: { value: string }) =>
                !value ? '원산지 지역은 필수 입력 사항입니다' : undefined,
            }}
          >
            {(field) => (
              <div>
                <label
                  className="mb-2 block font-medium text-gray-700 text-sm"
                  htmlFor={field.name}
                >
                  원산지 지역 *
                </label>
                <input
                  className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                  id={field.name}
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="예: 이슬레이, 하이랜드, 켄터키 등"
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

        {/* Taste Profile */}
        <div className="space-y-4">
          <h2 className="font-semibold text-gray-800 text-xl">맛 프로필</h2>

          <form.Field
            name="aroma"
            validators={{
              onChange: ({ value }: { value: string[] }) =>
                !value || (Array.isArray(value) && value.length === 0)
                  ? '향은 필수 입력 사항입니다'
                  : undefined,
            }}
          >
            {(field) => (
              <div>
                <h3 className="mb-2 block font-medium text-gray-700 text-sm">향 (Aroma) *</h3>
                {aromaLoading ? (
                  <div className="text-gray-500 text-sm">로딩 중...</div>
                ) : (
                  <div className="grid max-h-40 grid-cols-2 gap-2 overflow-y-auto rounded-md border border-gray-300 p-3 md:grid-cols-3">
                    {(aromaOptions ?? [])
                      .filter((option) => option && option.id != null && option.name != null)
                      .map((option) => {
                        const idStr = String(option.id)
                        return (
                          <label
                            className="flex cursor-pointer items-center space-x-2 rounded p-1 hover:bg-gray-50"
                            key={`${idStr}-${option.name}`}
                          >
                            <input
                              checked={
                                Array.isArray(field.state.value) &&
                                field.state.value.includes(idStr)
                              }
                              className="text-blue-600 focus:ring-blue-500"
                              onChange={(e) =>
                                handleCheckboxChange('aroma', option.id, e.target.checked)
                              }
                              type="checkbox"
                            />
                            <span className="text-gray-700 text-sm">{option.name}</span>
                          </label>
                        )
                      })}
                  </div>
                )}
                <p className="mt-1 text-gray-500 text-xs">원하는 향을 선택해주세요</p>
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>

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
                    {(tasteOptions ?? [])
                      .filter((option) => option && option.id != null && option.name != null)
                      .map((option) => {
                        const idStr = String(option.id)
                        return (
                          <label
                            className="flex cursor-pointer items-center space-x-2 rounded p-1 hover:bg-gray-50"
                            key={`${idStr}-${option.name}`}
                          >
                            <input
                              checked={
                                Array.isArray(field.state.value) &&
                                field.state.value.includes(idStr)
                              }
                              className="text-blue-600 focus:ring-blue-500"
                              onChange={(e) =>
                                handleCheckboxChange('taste', option.id, e.target.checked)
                              }
                              type="checkbox"
                            />
                            <span className="text-gray-700 text-sm">{option.name}</span>
                          </label>
                        )
                      })}
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
            name="finish"
            validators={{
              onChange: ({ value }: { value: string[] }) =>
                !value || (Array.isArray(value) && value.length === 0)
                  ? '끝맛은 필수 입력 사항입니다'
                  : undefined,
            }}
          >
            {(field) => (
              <div>
                <h3 className="mb-2 block font-medium text-gray-700 text-sm">끝맛 (Finish) *</h3>
                {finishLoading ? (
                  <div className="text-gray-500 text-sm">로딩 중...</div>
                ) : (
                  <div className="grid max-h-40 grid-cols-2 gap-2 overflow-y-auto rounded-md border border-gray-300 p-3 md:grid-cols-3">
                    {(finishOptions ?? [])
                      .filter((option) => option && option.id != null && option.name != null)
                      .map((option) => {
                        const idStr = String(option.id)
                        return (
                          <label
                            className="flex cursor-pointer items-center space-x-2 rounded p-1 hover:bg-gray-50"
                            key={`${idStr}-${option.name}`}
                          >
                            <input
                              checked={
                                Array.isArray(field.state.value) &&
                                field.state.value.includes(idStr)
                              }
                              className="text-blue-600 focus:ring-blue-500"
                              onChange={(e) =>
                                handleCheckboxChange('finish', option.id, e.target.checked)
                              }
                              type="checkbox"
                            />
                            <span className="text-gray-700 text-sm">{option.name}</span>
                          </label>
                        )
                      })}
                  </div>
                )}
                <p className="mt-1 text-gray-500 text-xs">원하는 끝맛을 선택해주세요</p>
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
              !value ? '설명은 필수 입력 사항입니다' : undefined,
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
                placeholder="주류에 대한 자세한 설명을 입력하세요"
                rows={4}
                value={field.state.value}
              />
              {field.state.meta.errors.length > 0 && (
                <p className="mt-1 text-red-600 text-sm">{field.state.meta.errors[0]}</p>
              )}
            </div>
          )}
        </form.Field>

        {/* Image Uploads */}
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
                error={field.state.meta.errors[0]}
                id={field.name}
                label="대표 이미지"
                name={field.name}
                onBlur={field.handleBlur}
                onChange={(file) => field.handleChange(file)}
                required
                value={field.state.value}
              />
            )}
          </form.Field>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <form.Field name="subImage1">
              {(field) => (
                <ImageUpload
                  className="h-full"
                  id={field.name}
                  label="보조 이미지 1"
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(file) => field.handleChange(file)}
                  value={field.state.value as File | null}
                />
              )}
            </form.Field>
            <form.Field name="subImage2">
              {(field) => (
                <ImageUpload
                  className="h-full"
                  id={field.name}
                  label="보조 이미지 2"
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(file) => field.handleChange(file)}
                  value={field.state.value as File | null}
                />
              )}
            </form.Field>
            <form.Field name="subImage3">
              {(field) => (
                <ImageUpload
                  className="h-full"
                  id={field.name}
                  label="보조 이미지 3"
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(file) => field.handleChange(file)}
                  value={field.state.value as File | null}
                />
              )}
            </form.Field>
            <form.Field name="subImage4">
              {(field) => (
                <ImageUpload
                  className="h-full"
                  id={field.name}
                  label="보조 이미지 4"
                  name={field.name}
                  onBlur={field.handleBlur}
                  onChange={(file) => field.handleChange(file)}
                  value={field.state.value as File | null}
                />
              )}
            </form.Field>
          </div>
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
