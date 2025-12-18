import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { DBZ_RANGES } from '../utils/constants';

const Legend = () => {
  return (
    <Card className="absolute bottom-4 left-4 z-10 bg-white/95 backdrop-blur-sm shadow-2xl border border-slate-200/50 max-w-xs">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold text-slate-800">
          Reflectivity (dBZ)
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {DBZ_RANGES.map((range, index) => (
            <div key={index} className="flex items-center space-x-3 group hover:bg-slate-50 rounded px-1 py-0.5 transition-colors">
              <div
                className="w-8 h-4 rounded border border-slate-300 shadow-sm"
                style={{ backgroundColor: range.color }}
              />
              <span className="text-sm text-slate-700 font-medium">
                {range.label}
              </span>
            </div>
          ))}
        </div>
        <div className="mt-4 pt-4 border-t border-slate-200">
          <p className="text-xs text-slate-500 italic">
            Higher values indicate stronger precipitation
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default Legend;

