const Header = () => {
  return (
    <header className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 text-white shadow-lg border-b border-blue-800/50">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight drop-shadow-sm">
              Weather Radar
            </h1>
            <p className="text-blue-100 text-sm mt-1 font-light">
              Real-time MRMS Reflectivity at Lowest Altitude
            </p>
          </div>
          <div className="hidden md:flex items-center space-x-3 bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 border border-white/20">
            <div className="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse shadow-lg shadow-green-400/50"></div>
            <span className="text-sm font-medium">Live Data</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

