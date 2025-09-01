// Form data type definitions for cocktail maker components

export interface SpiritsFormData {
  name: string
  aroma: string[]
  taste: string[]
  finish: string[]
  kind: string
  subKind: string
  amount: number
  alcohol: number
  originNation: string
  originLocation: string
  description: string
  mainImage: File | null
  subImage1: File | null
  subImage2: File | null
  subImage3: File | null
  subImage4: File | null
}

export interface LiqueurFormData {
  name: string
  brand: string
  taste: string[]
  kind: string
  subKind: string
  mainIngredients: string[]
  volume: number
  abv: number
  originNation: string
  description: string
  mainImage: File | null
}

export interface IngredientFormData {
  name: string
  brand: string[]
  kind: string
  originNation: string
  description: string
  mainImage: File | null
}

// Form field props types
export interface FormFieldState<T = unknown> {
  value: T
  meta: {
    isValid: boolean
    errors: string[]
    isTouched: boolean
    isDirty: boolean
  }
}

export interface FormFieldAPI<T = unknown> {
  state: FormFieldState<T>
  name: string
  handleChange: (value: T) => void
  handleBlur: () => void
}

export interface FormState {
  canSubmit: boolean
  isSubmitting: boolean
  values: Record<string, unknown>
  errors: Record<string, string>
}

export interface FormSubscribeState {
  canSubmit: boolean
  isSubmitting: boolean
}
