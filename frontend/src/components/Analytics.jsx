import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'
import { 
  BarChart, Bar, 
  LineChart, Line, 
  AreaChart, Area, 
  PieChart, Pie, Cell, 
  XAxis, YAxis, Tooltip, Legend, ResponsiveContainer 
} from 'recharts'
import { 
  MdAssessment, 
  MdTrendingUp, 
  MdPieChart, 
  MdShowChart, 
  MdFilterAlt,
  MdRefresh
} from 'react-icons/md'

const COLORS = ['#6366f1', '#14b8a6', '#f59e0b', '#a855f7'];

function Analytics() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    daily_trends: [],
    vehicle_distribution: [],
    confidence_history: [],
    source_breakdown: []
  });

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/analytics');
      setData(response.data);
    } catch (e) {
      console.error("Failed to load analytics details:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12 select-none">
      
      {/* Page header controller */}
      <div className="glass-card p-5 flex justify-between items-center">
        <div>
          <h4 className="font-extrabold text-base text-white tracking-tight">AI Analytical Engine</h4>
          <p className="text-xs text-slate-400 mt-0.5">Aggregated visual analytics compiled from model pipeline runs</p>
        </div>
        <button 
          onClick={fetchAnalytics}
          disabled={loading}
          className="p-3 bg-white/5 hover:bg-white/10 text-slate-300 rounded-xl hover:text-indigo-400 border border-white/5 transition-all flex items-center justify-center"
        >
          <MdRefresh className={loading ? "animate-spin" : ""} size={18} />
        </button>
      </div>

      {/* Grid: Trends over time */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Daily Accident Trends (Line Chart) */}
        <div className="glass-card p-6 min-h-[380px] flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <MdTrendingUp size={14} className="text-indigo-400" /> System Incidents
            </span>
            <h4 className="font-extrabold text-base text-white mt-1.5 tracking-tight">Daily Accident Trend</h4>
          </div>

          <div className="h-64 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.daily_trends} margin={{ top: 10, right: 5, left: -25, bottom: 0 }}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', color: '#f8fafc' }} />
                <Legend verticalAlign="top" height={36} iconType="circle" />
                <Line type="monotone" dataKey="accidents" name="Accident Collision Events" stroke="#f43f5e" strokeWidth={3} activeDot={{ r: 8 }} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Vehicle Classification Distribution (Bar Chart) */}
        <div className="glass-card p-6 min-h-[380px] flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <MdAssessment size={14} className="text-teal-400" /> Objects Count
            </span>
            <h4 className="font-extrabold text-base text-white mt-1.5 tracking-tight">Vehicle Distribution</h4>
          </div>

          <div className="h-64 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.vehicle_distribution} margin={{ top: 10, right: 5, left: -25, bottom: 0 }}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', color: '#f8fafc' }} />
                <Bar dataKey="value" name="Detected Count" fill="#6366f1" radius={[8, 8, 0, 0]}>
                  {data.vehicle_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Average Confidence Over Recent Events (Area Chart) */}
        <div className="glass-card p-6 min-h-[380px] flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <MdShowChart size={14} className="text-purple-400" /> Model Accuracy
            </span>
            <h4 className="font-extrabold text-base text-white mt-1.5 tracking-tight">Average Confidence Curve</h4>
          </div>

          <div className="h-64 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.confidence_history} margin={{ top: 10, right: 5, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorConf" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#a855f7" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#a855f7" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="event" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} domain={[0.0, 1.0]} />
                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', color: '#f8fafc' }} />
                <Area type="monotone" dataKey="confidence" name="Avg Confidence Score" stroke="#a855f7" fillOpacity={1} fill="url(#colorConf)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Source breakdown (Pie Chart) */}
        <div className="glass-card p-6 min-h-[380px] flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <MdPieChart size={14} className="text-amber-400" /> Stream Sources
            </span>
            <h4 className="font-extrabold text-base text-white mt-1.5 tracking-tight">Detection Source Distribution</h4>
          </div>

          <div className="h-64 mt-4 flex items-center justify-center">
            {data.source_breakdown.length > 0 && data.source_breakdown.some(s => s.value > 0) ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data.source_breakdown.filter(s => s.value > 0)}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {data.source_breakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', color: '#f8fafc' }} />
                  <Legend verticalAlign="bottom" height={36} iconType="circle" />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-xs font-semibold text-slate-500">No logs on record to display breakdown.</div>
            )}
          </div>
        </div>

      </div>

    </div>
  )
}

export default Analytics
