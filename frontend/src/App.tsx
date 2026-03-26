import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import MemberPage from './pages/MemberPage'
import './index.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/member/:qr" element={<MemberPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
