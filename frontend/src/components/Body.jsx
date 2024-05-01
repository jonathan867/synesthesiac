import React from 'react'
import "../index.css";
import { examples } from "../constants";
import Gallery from './Gallery';


const Body = () => {
    const half1 = examples.slice(0, 7);
    const half2 = examples.slice(7);
    return (
        <div>
            <div className="mt-60 mx-48 text-black font-bold text-4xl text-center">
                Say goodbye to Spotify's <span style={{ color: "#FCBD00" }}> ugly </span> default covers for your personal playlists.
            </div>
            <div className='mt-20' style={{ overflow: 'hidden' }} >
                <Gallery examples={half1} direction="right" />
                <Gallery examples={half2} direction="left" />
            </div>
            <div className="mt-28 mx-48 text-black font-bold text-4xl text-center">
                Analyze playlists for motifs and emotional composition with <br />
                <span style={{ color: "#FCBD00" }}>
                    {'\u{2728}'}&nbsp;&nbsp;Song Classification&nbsp;
                    <a
                        href="https://colab.research.google.com/drive/1P7xr095bJbNavheDrmumXypSykjib2CA?usp=sharing"
                        style={{ textDecoration: 'underline' }}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        ML Model
                    </a>
                    &nbsp;&nbsp;{'\u{2728}'}
                </span>
            </div>
            <div className="mt-24 mx-48 text-black font-bold text-4xl text-center">
                Create cover artwork to match the vibe. <br /> <span style={{ color: "#FCBD00" }}> Instantly. </span>
            </div>
        </div>
    );
};

export default Body;