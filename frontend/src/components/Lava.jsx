import React, { useRef } from 'react'
import "../styles.css";

const Lava = () => { // source code: https://codesandbox.io/p/sandbox/lava-lamp-rsd5m?file=%2Fsrc%2Findex.js
  return (
    <>
      <div className="lamp">
        <div className="lava">
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob"></div>
          <div className="blob top"></div>
          <div className="blob bottom"></div>
        </div>
        <div className='m-24 mt-96 text-white italic text-9xl font-serif absolute top-0 left-0' >
          Synesthesiac
        </div>
      </div>
      
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <defs>
          <filter id="goo">
            <feGaussianBlur
              in="SourceGraphic"
              stdDeviation="10"
              result="blur"
            />
            <feColorMatrix
              in="blur"
              mode="matrix"
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7"
              result="goo"
            />
            <feBlend in="SourceGraphic" in2="goo" />
          </filter>
        </defs>
      </svg>
      
    </>
  );
};

export default Lava;