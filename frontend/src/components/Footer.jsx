import React from 'react'
import "../index.css";

const Footer = () => {
    return (
        <>
            <div className="mt-48 text-black text-4xl text-center">
                "Exquisite playlists require exquisite cover art"
            </div>
            <div className="mt-8 mb-40 text-black italic text-xl text-center">
                - Unknown, 02/31/1898
            </div>
            <div className="mt-8 pt-7 text-white text-center" style={{height: "80px", backgroundColor: "#FCBD00"}}>
                Jonathan Feng - 2024
            </div>
        </>
    );
};

export default Footer;