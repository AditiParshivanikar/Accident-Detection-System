import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Slider, Switch, Select, Input, Button, message, Tooltip } from 'antd'
import { 
  MdSettings, 
  MdSave, 
  MdSms, 
  MdVolumeUp, 
  MdTune,
  MdLayers,
  MdShield
} from 'react-icons/md'

const { Option } = Select;

function SettingsPage({ settings, onSettingsSaved }) {
  const [loading, setLoading] = useState(false);
  const [testingSms, setTestingSms] = useState(false);
  const [form, setForm] = useState({
    confidence_threshold: 0.5,
    nms_threshold: 0.4,
    alert_sound: true,
    dark_mode: true,
    model_name: 'yolov4-tiny',
    twilio_sid: '',
    twilio_token: '',
    twilio_from: '',
    twilio_to: '',
    twilio_enabled: false
  });

  useEffect(() => {
    if (settings) {
      setForm(settings);
    }
  }, [settings]);

  const handleChange = (key, value) => {
    setForm(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      const response = await axios.put('/api/settings', form);
      message.success("System configurations saved successfully!");
      if (onSettingsSaved) onSettingsSaved();
    } catch (e) {
      console.error("Failed to save settings:", e);
      message.error("Failed to save configuration settings.");
    } finally {
      setLoading(false);
    }
  };

  const handleTestSms = async () => {
    setTestingSms(true);
    try {
      const response = await axios.post('/api/settings/test-sms');
      message.success(response.data.message || "Test SMS sent successfully!");
    } catch (e) {
      console.error("SMS test failed:", e);
      message.error(e.response?.data?.detail || "SMS test failed. Verify Twilio SID & Token.");
    } finally {
      setTestingSms(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12 select-none">
      
      {/* Configuration Cards */}
      <div className="glass-card p-6 space-y-6">
        <div className="flex items-center gap-2 pb-4 border-b border-white/5 text-indigo-400">
          <MdTune size={22} />
          <h4 className="font-extrabold text-base text-white tracking-tight">Detection Pipeline Parameters</h4>
        </div>

        {/* Model Selection */}
        <div className="flex flex-col gap-2">
          <label className="text-xs font-bold text-slate-300">Active AI Neural Network</label>
          <Select 
            value={form.model_name}
            onChange={(val) => handleChange('model_name', val)}
            className="w-full"
            dropdownClassName="bg-slate-900 border border-white/10"
          >
            <Option value="yolov4-tiny">YOLOv4-Tiny (Low Latency / CPU Optimal)</Option>
            <Option value="yolov8">YOLOv8 Medium / best(3).pt (Custom Detection Model)</Option>
          </Select>
          <p className="text-[10px] text-slate-500 font-semibold leading-relaxed">
            Note: YOLOv4-Tiny uses OpenCV's C++ DNN wrapper. YOLOv8 requires Python PyTorch dependencies to run locally.
          </p>
        </div>

        {/* Confidence Threshold */}
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center text-xs font-bold text-slate-300">
            <span>Confidence Threshold</span>
            <span className="text-indigo-400">{(form.confidence_threshold * 100).toFixed(0)}%</span>
          </div>
          <Slider 
            min={0.1} 
            max={1.0} 
            step={0.05} 
            value={form.confidence_threshold} 
            onChange={(val) => handleChange('confidence_threshold', val)}
            tooltip={{ formatter: (v) => `${(v * 100).toFixed(0)}%` }}
            className="mt-1"
          />
        </div>

        {/* NMS Threshold */}
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center text-xs font-bold text-slate-300">
            <span>Non-Maximum Suppression (NMS) Overlap</span>
            <span className="text-indigo-400">{(form.nms_threshold * 100).toFixed(0)}%</span>
          </div>
          <Slider 
            min={0.1} 
            max={1.0} 
            step={0.05} 
            value={form.nms_threshold} 
            onChange={(val) => handleChange('nms_threshold', val)}
            tooltip={{ formatter: (v) => `${(v * 100).toFixed(0)}%` }}
            className="mt-1"
          />
        </div>
      </div>

      {/* Notifications and audio alarm sound settings */}
      <div className="glass-card p-6 space-y-6">
        <div className="flex items-center gap-2 pb-4 border-b border-white/5 text-indigo-400">
          <MdVolumeUp size={22} />
          <h4 className="font-extrabold text-base text-white tracking-tight">Audio & Visual Warnings</h4>
        </div>

        <div className="flex items-center justify-between py-1">
          <div>
            <div className="text-xs font-bold text-white">Emergency Warning Siren Sound</div>
            <div className="text-[10px] text-slate-400 font-semibold mt-0.5">Play browser alarm buzzer when accidents are logged</div>
          </div>
          <Switch 
            checked={form.alert_sound} 
            onChange={(checked) => handleChange('alert_sound', checked)}
            className="bg-slate-700"
          />
        </div>
      </div>

      {/* Twilio SMS settings card */}
      <div className="glass-card p-6 space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-white/5">
          <div className="flex items-center gap-2 text-indigo-400">
            <MdSms size={22} />
            <h4 className="font-extrabold text-base text-white tracking-tight">Twilio SMS Alert Integration</h4>
          </div>
          <Switch 
            checked={form.twilio_enabled} 
            onChange={(checked) => handleChange('twilio_enabled', checked)}
            className="bg-slate-700"
          />
        </div>

        {form.twilio_enabled && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Account SID</label>
              <Input 
                value={form.twilio_sid} 
                onChange={(e) => handleChange('twilio_sid', e.target.value)}
                placeholder="AC..."
                className="bg-black/20 text-white border-white/10 rounded-xl"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Auth Token</label>
              <Input.Password 
                value={form.twilio_token} 
                onChange={(e) => handleChange('twilio_token', e.target.value)}
                placeholder="Token String"
                className="bg-black/20 text-white border-white/10 rounded-xl"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">From Twilio Number</label>
              <Input 
                value={form.twilio_from} 
                onChange={(e) => handleChange('twilio_from', e.target.value)}
                placeholder="+1..."
                className="bg-black/20 text-white border-white/10 rounded-xl"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Recipient Number</label>
              <Input 
                value={form.twilio_to} 
                onChange={(e) => handleChange('twilio_to', e.target.value)}
                placeholder="+91..."
                className="bg-black/20 text-white border-white/10 rounded-xl"
              />
            </div>

            <div className="md:col-span-2 pt-2 border-t border-white/5 mt-2 flex justify-end">
              <Button 
                onClick={handleTestSms}
                loading={testingSms}
                disabled={!form.twilio_sid || !form.twilio_token || !form.twilio_from || !form.twilio_to}
                className="bg-white/5 hover:bg-white/10 text-slate-300 font-bold border border-white/10 rounded-xl hover:text-white"
              >
                Send Test SMS Alert
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Primary Action Row */}
      <div className="flex justify-end gap-3 pt-2">
        <Button 
          type="primary"
          onClick={handleSave}
          loading={loading}
          icon={<MdSave size={18} className="inline mr-1" />}
          className="bg-indigo-600 hover:bg-indigo-500 border-none text-xs font-bold rounded-xl py-5 px-6 flex items-center shadow-lg hover:shadow-indigo-500/20"
        >
          Save System Configurations
        </Button>
      </div>

    </div>
  )
}

export default SettingsPage
