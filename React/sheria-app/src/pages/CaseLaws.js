import { useEffect, useState } from 'react';
import '../styles/CaseLaws.css'

export default function CaseLaws() {
    
    const [pdfs, setPdfs] = useState([]);

    useEffect(() => {
        const fetchPdfs = async () => {
            const response = await fetch('http://localhost:8000/documents/');
            const data = await response.json();
            setPdfs(data); 
        };
        fetchPdfs();
    }, []);

    return (
        <div className="case-laws-container">
            <h1 className="case-laws-title">Case Laws</h1>
            <ul className="pdf-list">
                {pdfs.map((pdf, index) => (
                    <li key={index} className="pdf-item">
                        <a href={`/documents/${pdf}`} target="_blank" rel="noopener noreferrer" className="pdf-link">
                            {pdf}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
}