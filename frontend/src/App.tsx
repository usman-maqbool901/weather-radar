import { useRadarData } from './hooks/useRadarData';
import Header from './components/Header';
import RadarMap from './components/RadarMap';
import Legend from './components/Legend';
import LastUpdated from './components/LastUpdated';
import { Badge } from './components/ui/badge';

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || '';

function App() {
  const { data, loading, error, refetch } = useRadarData(false);

  if (!MAPBOX_TOKEN) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-slate-800 mb-2">
            Mapbox Token Required
          </h1>
          <p className="text-slate-600">
            Please set VITE_MAPBOX_TOKEN in your environment variables
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Header />
      <main className="flex-1 relative">
        <div className="absolute top-4 right-20 z-10">
          <LastUpdated
            lastUpdated={data?.lastUpdated || null}
            dataTimestamp={data?.dataTimestamp || null}
            loading={loading}
          />
        </div>
        <div className="h-[calc(100vh-120px)]">
          {error ? (
            <div className="h-full flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
              <div className="text-center space-y-4 bg-white rounded-xl shadow-xl p-8 border border-slate-200">
                <Badge variant="error" className="text-lg px-4 py-2">
                  {error.error}
                </Badge>
                <p className="text-slate-600 max-w-md">{error.message}</p>
                <button
                  onClick={refetch}
                  className="mt-4 px-6 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all shadow-md hover:shadow-lg font-medium"
                >
                  Retry
                </button>
              </div>
            </div>
          ) : (
            <RadarMap data={data?.data || null} mapboxToken={MAPBOX_TOKEN} />
          )}
        </div>
        {!error && <Legend />}
      </main>
    </div>
  );
}

export default App;
