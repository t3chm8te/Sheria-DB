import '../styles/Header.css'
import { Link, useMatch, useResolvedPath } from 'react-router-dom'

export default function Header(){
    return (
        <nav className="nav">
            <Link to="/" className="site-title">
                Sheria
            </Link>
            <ul>
                <CustomLink to="/">Home</CustomLink>
                <CustomLink to="/about">About</CustomLink>
                <CustomLink to="/caselaws">Case Laws</CustomLink>
                <CustomLink to="/courts">Courts</CustomLink>
                <CustomLink to="/gazzettes">Gazettes</CustomLink>
                <CustomLink to="/search">Search</CustomLink>
            </ul>

            <button className="sign-in-button" href="/login">Sign In</button>
        </nav>
    )
}

function CustomLink( {to, children, ...props} ){
    const resolvedPath = useResolvedPath(to)
    const isActive = useMatch({ path: resolvedPath.pathname, end: true })

    return (
        <li className={isActive ? "active": ""}>
            <Link to={to} {...props}>
                {children}
            </Link>
        </li>
    )
}