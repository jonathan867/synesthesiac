import React from 'react'
import './App.css'

import { Lava, Body, PlaylistForm, Footer } from "./components";

const App = () => {

  return (
    <>
      <div className="" style={{ height:'100vh'}}>
        <Lava/>
      </div>
      <Body/>
      <PlaylistForm/>
      <Footer/>
    </>
  ) 
}

export default App
