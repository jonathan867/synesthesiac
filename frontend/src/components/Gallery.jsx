import React from 'react';
import '../index.css';
import { motion } from 'framer-motion';
import { VictoryPie, VictoryLabel } from 'victory';

const Gallery = ({ examples, direction }) => {
    const duplicatedExamples = [...examples, ...examples];

    return (
        <div className={`mt-4 conveyor-belt-${direction}`} style={{ display: 'flex', gap: '16px' }}>
            {duplicatedExamples.map((example, index) => (

                <div key={index} style={{ position: 'relative', flexShrink: 0 }}>
                    <img src={example.image} alt={`Image ${index}`} style={{ width: '300px', height: '300px' }} />
                    <motion.div
                        className="example-hover py-4 px-3 text-white"
                        transition={{ duration: 0.3 }}
                        whileHover={{ opacity: 1 }}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 0 }}
                    >
                        <div>
                            <p className='mb-4' style={{ textAlign: 'center', fontSize: '18px' }}> <a href={example.link} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'underline', color: 'white' }} >{example.playlistName}</a></p>

                            <div style={{ justifyContent: 'center', textAlign: 'center' }}>
                                <VictoryPie
                                    height={230}
                                    data={[
                                        example.percentAngry !== 0 ? { x: "Angry", y: example.percentAngry } : { x: " ", y: 0 },
                                        example.percentHappy !== 0 ? { x: "Happy", y: example.percentHappy } : { x: " ", y: 0 },
                                        example.percentRelaxed !== 0 ? { x: "Relaxed", y: example.percentRelaxed } : { x: " ", y: 0 },
                                        example.percentSad !== 0 ? { x: "Sad", y: example.percentSad } : { x: " ", y: 0 },

                                    ]}
                                    colorScale={["#F43535", "#FCBD00", "#FF77AC", "#3C92F8"]}
                                    labelComponent={
                                        <VictoryLabel
                                            text={({ datum }) => {
                                                if (datum.y === 0) return " ";
                                                const roundedPercent = Math.round(datum.y * 1000) / 10;
                                                return `${datum.x}: ${roundedPercent}%`;
                                            }}
                                            style={{ fontSize: 19, fill: "#D9D9D9" }}
                                        />
                                    }
                                />
                            </div>
                            <p className='mt-3 mx-4'> Motifs: {example.motifs.join(', ')} </p>
                            <p className='mx-4'> Style: {example.style} </p>
                        </div>
                    </motion.div>
                </div>
            ))}
        </div>
    );
};

export default Gallery;
