import { useState } from 'react';
import axios from 'axios';
import '../styles/Search.css';

const Search = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('http://localhost:8000/search/', {
                query: query
            });
            setResults(response.data.results);
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="search-container">
            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter your search query..."
                    className="search-input"
                />
                <button 
                    type="submit"
                    disabled={loading}
                    className="search-button"
                >
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </form>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {loading && (
                <div className="loading-spinner">
                    Loading...
                </div>
            )}

            <div className="results-container">
                {results.map((result, index) => (
                    <div key={index} className="result-card">
                        <div className="result-score">
                            Score: {result.score.toFixed(4)}
                        </div>
                        <div className="result-text">
                            {result.text}
                        </div>
                        <div className="result-metadata">
                            {Object.entries(result.metadata).map(([key, value]) => (
                                <div key={key}>
                                    <strong>{key}:</strong> {value}
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Search;