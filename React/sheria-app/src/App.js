import Header from './components/Header'
import Footer from './components/Footer'
import About from './pages/About'
import Courts from './pages/Courts'
import CaseLaws from './pages/CaseLaws'
import Gazzettes from './pages/Gazzettes'
import Home from './pages/Home'
import Search from './pages/Search'
import {Route , Routes} from 'react-router-dom'

function App(){

  return (
  <>
    <Header/>
    <div className="container">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About/>} />
        <Route path="/caselaws" element={<CaseLaws/>} />
        <Route path="/courts" element={<Courts/>} />
        <Route path="/gazzettes" element={<Gazzettes/>} />
        <Route path="/search" element={<Search/>} />
      </Routes>
    </div>
    <Footer/>
  </>
  )
}

export default App