import React, { useState } from 'react'
import "../index.css";
import { Input, Button, List, Select } from 'antd';
import { VictoryPie, VictoryLabel } from 'victory';
import { brokenRecord, note, brush, unconnected } from "../assets";
import { examplePlaylist } from "../constants";

const PlaylistForm = () => {

    const emotionColors = {
        angry: "#F43535",
        happy: "#FCBD00",
        relaxed: "#FF77AC",
        sad: "#3C92F8",
    };

    const [inputURL, setInputURL] = useState('https://open.spotify.com/playlist/0Nn0WvcRs07ES1Ha0JO1iM?si=09506cc2096d4aac'); // Playlist textbox
    const [inputStyle, setInputStyle] = useState(''); // Style textbox
    const [playlistScanAPIState, setPSAPIState] = useState('done');
    const [playlistInfo, setPlaylistInfo] = useState(examplePlaylist);

    const handleURLChange = (e) => { // Playlist textbox
        setInputURL(e.target.value);
    };
    const handleStyleChange = (e) => { // Playlist textbox
        setInputStyle(e.target.value);
    };

    const [selectedMotifs, setSelectedMotifs] = useState([]); // multiselect
    const handleSelectChange = (selectedValues) => {
        setSelectedMotifs(selectedValues);
    };

    const handlePlaylistSubmit = () => {

        setPSAPIState('loading');
        const regex = /playlist\/([a-zA-Z0-9]+)/; // URI is always between 'playlist/' and '?'
        const match = inputURL.match(regex);
        const URI = match ? match[1] : null;

        const requestBody = {
            playlistURI: URI,
            spotifyClientId: process.env.REACT_APP_SPOTIFY_CLIENT_ID,
            spotifyClientSecret: process.env.REACT_APP_SPOTIFY_CLIENT_SECRET,
            geniusAPIToken: process.env.REACT_APP_GENIUS_API_TOKEN
        };

        fetch(`${process.env.REACT_APP_BACKEND_ROOT}/analyze-playlist`, { // Send a POST request to the backend endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        })
            .then(response => {
                if (response.ok) {
                    return response.json()
                        .then(data => {
                            setPlaylistInfo(data);
                            setPSAPIState('done');
                        })
                } else {
                    setPSAPIState('default');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                setPSAPIState('default');
            });
    };

    const [imgGenAPIState, setIGAPIState] = useState('default');
    const [imgGenURL, setImgGenURL] = useState(null);

    const handleImgGenSubmit = () => {

        setIGAPIState('loading');

        const requestBody = {
            playlistName: playlistInfo.playlistName,
            percentAngry: playlistInfo.percentAngry,
            percentHappy: playlistInfo.percentHappy,
            percentRelaxed: playlistInfo.percentRelaxed,
            percentSad: playlistInfo.percentSad,
            motifs: selectedMotifs,
            style: inputStyle
        };

        fetch(`${process.env.REACT_APP_BACKEND_ROOT}/generate-image`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        })
            .then(response => {
                if (response.ok) {
                    return response.json()
                        .then(data => {
                            setImgGenURL(data.image_url);
                            setIGAPIState('done');
                        })
                } else {
                    setPSAPIState('default');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                setPSAPIState('default');
            });
    };

    return (
        <>
            <div className='flex flex-row items-center mt-36 mx-36 my-5' style={{ borderLeft: '10px solid red', backgroundColor: '#fff6f6', borderRadius: '3px', boxShadow: '4px 4px 8px rgba(0, 0, 0, 0.08)' }}>
                <img className='mx-10 align-center' style={{ width: 'auto', height: '60px' }}
                    src={unconnected}
                    alt="error"
                />
                <div className='py-5' >
                    <h2 className='text-start' style={{ fontSize: "30px", fontWeight: 'bold' }}>
                        Hang in there!
                    </h2>
                    <h2 className='mt-2' style={{ fontSize: "20px", color: "grey" }}>
                        Synesthesiac's backend deployment is currently being migrated. Check back soon for updates!
                    </h2>
                    <h2 className='text-start' style={{ fontSize: "20px", color: "grey" }}>
                        <span style={{ color: 'grey' }}>
                            For now, click here for a{' '}
                            <a
                                href="https://drive.google.com/file/d/1sY26UKxp4Yw-U3GwCOltl-g05kp3fSw_/view?usp=sharing"
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{ textDecoration: 'underline' }}
                            >
                                video demo
                            </a> {' '}
                            of playlist analysis and cover generation functions.
                        </span>
                    </h2>
                </div>
            </div>

            <div className="mx-36 mt-28 mb-20">
                <Input
                    id='playlistURL'
                    placeholder="Paste link of a public Spotify playlist"
                    value={inputURL}
                    onChange={handleURLChange}
                    style={{ width: '75%', borderWidth: '2px' }}
                />
                <Button
                    key='submitPlaylist'
                    onClick={handlePlaylistSubmit}
                    style={{ marginLeft: "5%", backgroundColor: "#FCBD00", borderColor: "#FCBD00", color: 'white', width: "20%", borderRadius: '6px', boxShadow: '4px 4px 8px rgba(0, 0, 0, 0.1)', transition: 'background-color 0.3s ease' }}
                    onMouseEnter={(e) => { e.target.style.backgroundColor = '#FCA600' }}
                    onMouseLeave={(e) => { e.target.style.backgroundColor = '#FCBD00' }}
                >
                    Search Playlist
                </Button>

                <div className='mt-8 min-h-96 rounded-md border-2 border-neutral-300'>
                    {playlistScanAPIState === 'default' && (
                        <div className="mt-36 flex flex-col items-center">
                            <img className="mb-4" src={brokenRecord} style={{ width: 'auto', height: '100px' }} />
                            <p style={{ color: "#FCBD00" }}> No Playlist Found </p>
                        </div>
                    )}

                    {playlistScanAPIState === 'loading' && (
                        <div className="mt-40 flex flex-col items-center">
                            <img className="mb-10 loadingNote" src={note} style={{ width: 'auto', height: '70px' }} />
                            <p style={{ color: "#FCBD00" }}> Processing Playlist: This process takes approx. 1.9 seconds per song </p>
                        </div>
                    )}

                    {playlistScanAPIState === 'done' && (
                        <div>
                            <div className=' p-8 flex flex-row justify-between'>
                                <List
                                    className='left-side'
                                    style={{
                                        maxHeight: '300px', // fix this height
                                        width: '48%', overflow: 'auto', overflowY: 'scroll', border: '2px solid #d9d9d9', borderRadius: '6px'
                                    }}
                                    dataSource={playlistInfo.storedSongs}
                                    renderItem={song => (
                                        <List.Item className='mx-4'>
                                            {song.song_name} - {song.artist_name} &nbsp;
                                            <span style={{ color: emotionColors[song.emotion] || 'black' }}>
                                                ({song.emotion})
                                            </span>
                                        </List.Item>
                                    )}
                                />
                                <div style={{ width: '48%' }}>
                                    <div className="font-bold text-4xl text-center" style={{ marginBottom: '-25px', height: 'auto' }}> {playlistInfo.playlistName} </div>
                                    <VictoryPie
                                        height={230}
                                        data={[
                                            playlistInfo.percentAngry !== 0 ? { x: "Angry", y: playlistInfo.percentAngry } : { x: " ", y: 0 },
                                            playlistInfo.percentHappy !== 0 ? { x: "Happy", y: playlistInfo.percentHappy } : { x: " ", y: 0 },
                                            playlistInfo.percentRelaxed !== 0 ? { x: "Relaxed", y: playlistInfo.percentRelaxed } : { x: " ", y: 0 },
                                            playlistInfo.percentSad !== 0 ? { x: "Sad", y: playlistInfo.percentSad } : { x: " ", y: 0 },
                                        ]}
                                        colorScale={["#F43535", "#FCBD00", "#FF77AC", "#3C92F8"]}
                                        labelComponent={
                                            <VictoryLabel
                                                text={({ datum }) => {
                                                    if (datum.y === 0) return " ";
                                                    const roundedPercent = Math.round(datum.y * 1000) / 10;
                                                    return `${datum.x}: ${roundedPercent}%`;
                                                }}
                                                style={{ fontSize: 14, fill: "black" }}
                                            />
                                        }
                                    />
                                </div>
                            </div>
                            <div className='mb-8 px-8 flex flex-row justify-between'>
                                <Select
                                    className='rounded-md border border-neutral-300 bg-neutral-300' // add "other" option
                                    mode="tags"
                                    style={{ width: '48%' }}
                                    placeholder="Select detected motifs, or type your own motifs to include"
                                    value={selectedMotifs}
                                    onChange={handleSelectChange}
                                    allowClear
                                >
                                    {playlistInfo.motifs.map((motif) => (
                                        <Select.Option key={motif} value={motif}>
                                            {motif}
                                        </Select.Option>
                                    ))}
                                </Select>
                                <Input
                                    id='style'
                                    placeholder="Input a cover artstyle"
                                    value={inputStyle}
                                    onChange={handleStyleChange}
                                    style={{ width: '48%', borderWidth: '2px' }}
                                />
                            </div>
                        </div>
                    )}
                </div>
                <div className='mt-8 flex justify-center'>
                    <Button
                        key='submitPlaylist'
                        onClick={handleImgGenSubmit}
                        style={{ backgroundColor: "#FCBD00", borderColor: "#FCBD00", color: 'white', height: "60px", width: "24%", borderRadius: '6px', boxShadow: '4px 4px 8px rgba(0, 0, 0, 0.1)', transition: 'background-color 0.3s ease' }}
                        onMouseEnter={(e) => { e.target.style.backgroundColor = '#FCA600' }}
                        onMouseLeave={(e) => { e.target.style.backgroundColor = '#FCBD00' }}
                    >
                        Generate Playlist Cover
                    </Button>
                </div>
                <div className='mt-8 min-h-96 rounded-md border-2 border-neutral-300'>
                    {imgGenAPIState === 'default' && (
                        <div className="mt-36 flex flex-col items-center">
                            <img className="mb-4" src={brokenRecord} style={{ width: 'auto', height: '100px' }} />
                            <p style={{ color: "#FCBD00" }}> No Playlist Data Found </p>
                        </div>
                    )}

                    {imgGenAPIState === 'loading' && (
                        <div className="mt-20 flex flex-col items-center">
                            <img className="mb-4" src={brush} style={{ width: 'auto', height: '200px' }} />
                            <p className="mb-16" style={{ color: "#FCBD00" }}> Generating Playlist Cover </p>
                        </div>
                    )}

                    {imgGenAPIState === 'done' && (
                        <div className="mt-14 flex flex-col items-center">
                            <div className="mb-14 px-12 pt-12 pb-3 flex flex-col items-center rounded-md" style={{ backgroundColor: "#FCBD00" }}>
                                <img className="mb-2" src={imgGenURL} alt="Generated Image" style={{ width: 'auto', height: '500px' }} />
                                <p className="text-white text-xl font-bold"> {playlistInfo.playlistName} </p>
                            </div>
                        </div>
                    )}
                </div>
            </div>

        </>
    );
};

export default PlaylistForm;