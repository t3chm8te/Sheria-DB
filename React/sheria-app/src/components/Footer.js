import { Link } from "react-router-dom"
import '../styles/Footer.css'

export default function Footer () {
    return(
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-section">
                    <h3>Sheria DB</h3>
                    <p>Legal information powered by artificial intelligence.</p>
                </div>
                <div className="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><Link to="/">Home</Link></li>
                        <li><Link to="/about">About</Link></li>
                        <li><Link to="/caselaws">Case Laws</Link></li>
                        <li><Link to="/courts">Courts</Link></li>
                        <li><Link to="/gazzettes">Gazettes</Link></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h3>Contact Us</h3>
                    <p>Email: hello@krltech.com</p>
                    <p>Phone: +254 700 000 000</p>
                </div>

                <div className="footer-section">
                    <h3>Connect with us</h3>
                </div>
            </div>
            <div className="footer-bottom">
                <p>&copy; 2025 Sheria. All rights reserved.</p>
            </div>
        </footer>
    )
}