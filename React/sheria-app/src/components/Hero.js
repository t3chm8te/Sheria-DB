import '../styles/Hero.css'

function Hero() {
    return(
        <div className="hero-container">
            <h1>Access up to date Legal Information</h1>
            <p> Comprehensive database of laws, cases, and legal documents at your fingertips </p>
            <button className="my-button" href="/archives"> View archives </button>
            <button className="my-button" href="/latest"> Browse Latest </button>
        </div>
    )
}

export default Hero