import React from 'react'
import "../index.css";
import { examples } from "../constants";
import Gallery from './Gallery';


const Body = () => {
    const half1 = examples.slice(0, 6);
    const half2 = examples.slice(6);
    return (
        <div>
            <div className="mt-60 mx-48 text-black font-bold text-4xl text-center">
                Say goodbye to Spotify's <span style={{color: "#FCBD00"}}> ugly </span> default covers for your personal playlists. 
            </div>
            <div className = 'mt-20' style={{overflow: 'hidden'}} >
                {/* <h1>Conveyor Belt Example</h1> */}
                <Gallery examples={half1} direction="right"/>
                <Gallery examples={half2} direction="left"/>
            </div>

            <div className="mt-28 mx-48 text-black font-bold text-4xl text-center">
                Capture playlist motifs and emotional composition with <br/> <span style={{color: "#FCBD00"}}> {'\u{2728}'}machine learning{'\u{2728}'} </span>
            </div>
            <div className="mt-24 mx-48 text-black font-bold text-4xl text-center">
                Create artwork to match the vibe. <span style={{color: "#FCBD00"}}> Instantly. </span>
            </div>

            <div className="mt-60 text-black text-4xl text-center">
                "Exquisite playlists require exquisite cover art"
            </div>
            <div className="mt-8 mb-40 text-black italic text-xl text-center">
                - Unknown, 02/31/1898
            </div>
        </div>
    );
};

export default Body;