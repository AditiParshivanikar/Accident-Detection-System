import React from 'react'
import { motion } from 'framer-motion'
import { 
  MdSecurity, 
  MdLayers, 
  MdPeople, 
  MdFolderZip,
  MdCode,
  MdPlayArrow,
  MdTerminal
} from 'react-icons/md'

function About() {
  const techStack = [
    { name: "FastAPI", desc: "Python high-performance REST & WebSocket backend routing framework", icon: "🐍" },
    { name: "React.js", desc: "Component architecture client interface library", icon: "⚛️" },
    { name: "OpenCV", desc: "Open-source computer vision library for image manipulation and DNN execution", icon: "📷" },
    { name: "YOLO Architecture", desc: "YOLOv4-Tiny (OpenCV DNN weights) and YOLOv8 PyTorch integration", icon: "🎯" },
    { name: "Tailwind CSS", desc: "Utility-first responsive styles and glassmorphism styling layers", icon: "🎨" },
    { name: "Ant Design (AntD)", desc: "Enterprise component systems for tables, forms, and layout controls", icon: "🧱" },
    { name: "SQLite & SQLAlchemy", desc: "Relational persistence storage and query logging", icon: "💾" }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12 select-none">
      
      {/* Introduction Card */}
      <div className="glass-card p-6 relative overflow-hidden">
        <div className="absolute -top-12 -right-12 w-48 h-48 bg-gradient-to-tr from-indigo-600 to-purple-600 opacity-10 rounded-full blur-2xl"></div>
        
        <div className="flex items-center gap-4 text-indigo-400 pb-4 border-b border-white/5">
          <MdSecurity size={24} />
          <h3 className="font-extrabold text-base text-white tracking-tight">System Specification Profile</h3>
        </div>

        <div className="mt-4 space-y-4">
          <h2 className="text-xl font-black text-white bg-gradient-to-r from-indigo-200 to-slate-200 bg-clip-text text-transparent tracking-tight">
            AI Accident Detection & Alert System (v1.0.0)
          </h2>
          <p className="text-xs text-slate-300 leading-relaxed font-semibold">
            This application is designed to enhance roadway safety operations using computer vision pipelines. 
            By processing video files or live camera streams, it isolates traffic targets (cars, trucks, buses, motorcycles) using lightweight convolutional networks. 
            If overlap collisions are flagged based on bounding box geometry calculations, it instantly triggers browser audio sirens, UI overlays, and SMS warnings.
          </p>
        </div>
      </div>

      {/* Tech stack card details */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-4 text-indigo-400 pb-4 border-b border-white/5 mb-5">
          <MdLayers size={22} />
          <h4 className="font-extrabold text-base text-white tracking-tight">Technology Stack Integration</h4>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {techStack.map((tech, idx) => (
            <div key={idx} className="bg-black/20 p-4 border border-white/5 rounded-2xl flex items-start gap-3">
              <span className="text-2xl mt-0.5">{tech.icon}</span>
              <div>
                <h5 className="text-xs font-bold text-white tracking-wide">{tech.name}</h5>
                <p className="text-[10px] text-slate-400 font-semibold mt-1 leading-relaxed">{tech.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Developers card credits */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Developers metadata */}
        <div className="glass-card p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-4 text-indigo-400 pb-4 border-b border-white/5 mb-4">
              <MdPeople size={22} />
              <h4 className="font-extrabold text-base text-white tracking-tight">Developer Information</h4>
            </div>
            
            <div className="text-xs text-slate-300 font-semibold space-y-2">
              <div className="flex justify-between py-1 border-b border-white/5">
                <span className="text-slate-400">Team Profile</span>
                <span className="text-white">AI Vision Security Team</span>
              </div>
              <div className="flex justify-between py-1 border-b border-white/5">
                <span className="text-slate-400">Project Branch</span>
                <span className="text-white">Main Release</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-400">License Profile</span>
                <span className="text-white">MIT Enterprise License</span>
              </div>
            </div>
          </div>
        </div>

        {/* Repository details */}
        <div className="glass-card p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-4 text-indigo-400 pb-4 border-b border-white/5 mb-4">
              <MdCode size={22} />
              <h4 className="font-extrabold text-base text-white tracking-tight">Code Repository & Deployments</h4>
            </div>
            
            <p className="text-[10px] text-slate-400 font-semibold leading-relaxed">
              This structure is pre-configured with complete configuration manifests including Docker, Vercel router configs, Render settings, and CORS dependencies for automated cloud CI/CD pipelines.
            </p>
          </div>

          <a 
            href="https://github.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="w-full mt-4 py-3 bg-white/5 hover:bg-white/10 border border-white/5 text-slate-300 font-bold rounded-xl text-xs tracking-wide flex items-center justify-center gap-1.5 transition-colors"
          >
            <MdTerminal size={18} /> View GitHub Source Repository
          </a>
        </div>
      </div>

    </div>
  )
}

export default About
