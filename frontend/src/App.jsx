import { useState } from 'react'
import './App.css'

import { Lava, Body } from "./components";

const App = () => {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="" style={{ height:'100vh'}}>
        <Lava/>
      </div>
      <Body/>
      <div>
        hi
      </div>
    </>
  )
}

export default App
