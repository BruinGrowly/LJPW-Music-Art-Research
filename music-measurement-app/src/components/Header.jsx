import './Header.css'

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">
          <span className="logo-text">LJPW</span>
          <span className="logo-subtitle">Music Measurement</span>
        </h1>
        <div className="header-dimensions">
          <span className="dim dim-l" title="Love">L</span>
          <span className="dim dim-j" title="Justice">J</span>
          <span className="dim dim-p" title="Power">P</span>
          <span className="dim dim-w" title="Wisdom">W</span>
        </div>
      </div>
    </header>
  )
}

export default Header
