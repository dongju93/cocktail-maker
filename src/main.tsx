import React from 'react'
import ReactDOM from 'react-dom/client'
import SuperTokens, { SuperTokensWrapper } from 'supertokens-auth-react'
import EmailPassword from 'supertokens-auth-react/recipe/emailpassword'
import Session from 'supertokens-auth-react/recipe/session'
import App from './App'
import './index.css'

// SuperTokens 초기화
SuperTokens.init({
  appInfo: {
    appName: 'cocktail-maker',
    apiDomain: 'http://127.0.0.1:8000',
    websiteDomain: 'http://localhost:3000',
    apiBasePath: '/auth',
    websiteBasePath: '/auth',
  },
  recipeList: [EmailPassword.init(), Session.init()],
})

const rootElement = document.getElementById('root')
if (!rootElement) {
  throw new Error('Root element not found')
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <SuperTokensWrapper>
      <App />
    </SuperTokensWrapper>
  </React.StrictMode>,
)
