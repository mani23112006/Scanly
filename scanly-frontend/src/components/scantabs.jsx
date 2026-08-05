// ScanTabs.jsx

// Import React hook for state management
import { useState } from 'react'

// Import the three scanning components
import ScanForm from './ScanForm'
import URLInput from './URLInput'
import ImageUpload from './ImageUpload'

// Array containing information about each tab
const TABS = [
  {
    id: 'text',
    label: '📝 Text',
    desc: 'SMS / WhatsApp / Email',
  },
  {
    id: 'url',
    label: '🔗 URL',
    desc: 'Suspicious links',
  },
  {
    id: 'image',
    label: '🖼️ Image',
    desc: 'Screenshot scan',
  },
]

// Main component
export default function ScanTabs() {

  // Stores the currently selected tab
  // Initially "text" tab is selected
  const [active, setActive] = useState('text')

  return (

    // Main container
    <div className="w-full max-w-2xl">

      {/* ================= TAB BAR ================= */}

      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-1.5 mb-4 flex gap-1">

        {/* Loop through every tab */}
        {TABS.map((tab) => (

          <button
            key={tab.id}

            // Change active tab when clicked
            onClick={() => setActive(tab.id)}

            className={`

              flex-1
              py-2.5
              px-3
              rounded-xl
              text-sm
              font-medium
              transition-all
              duration-150

              ${
                active === tab.id
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/30'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }

            `}
          >

            {/* Tab title */}
            <span className="block">
              {tab.label}
            </span>

            {/* Tab description */}
            <span className="block text-xs opacity-60 mt-0.5 font-normal hidden sm:block">
              {tab.desc}
            </span>

          </button>

        ))}

      </div>

      {/* ================= TAB CONTENT ================= */}

      {/* Show ScanForm only if Text tab is active */}
      {active === 'text' && <ScanForm />}

      {/* Show URLInput only if URL tab is active */}
      {active === 'url' && <URLInput />}

      {/* Show ImageUpload only if Image tab is active */}
      {active === 'image' && <ImageUpload />}

    </div>
  )
}